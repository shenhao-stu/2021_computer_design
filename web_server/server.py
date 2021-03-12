# -*- coding: utf-8 -*-
# @Author: Hao Shen
# @Last Modified by:   Hao Shen
# @Last Modified time: 2021-02-15 15:26:33
import base64
import requests
import argparse
import copy
import json

from flask import Flask, request, Response, jsonify
from flask_cors import CORS

from config import hparams, device
from generator import Generator

app = Flask(__name__)
CORS(app, supports_credentials=True)

filename = 'predict_log.json'
image_filename = 'res_img.jpg'
image_trans_filename = 'res_trans_img.jpg'


def parse_args():
    parser = argparse.ArgumentParser(description="The parametrs for the generator.")
    parser.add_argument("-m", "--mode", type=str, choices=['interact', 'file'], default='interact',
                        help='The mode of generation. interact: generate in a interactive mode.\
        file: take an input file and generate poems for each input in the file.')
    parser.add_argument("-b", "--bsize", type=int, default=20, help="beam size, 20 by default.")
    parser.add_argument("-v", "--verbose", type=int, default=0, choices=[0, 1, 2, 3],
                        help="Show other information during the generation, False by default.")
    parser.add_argument("-d", "--draw", type=int, default=0, choices=[0, 1, 2],
                        help="Show the visualization of memory reading and writing. It only works in the interact mode.\
        0: not work, 1: save the visualization as pictures, 2: show the visualization at each step.")
    parser.add_argument("-s", "--select", type=int, default=0,
                        help="If manually select each generated line from beam candidates? False by default.\
        It works only in the interact mode.")
    parser.add_argument("-i", "--inp", type=str,
                        help="input file path. it works only in the file mode.")
    parser.add_argument("-o", "--out", type=str,
                        help="output file path. it works only in the file mode")
    return parser.parse_args()


class GenerateTool(object):
    """docstring for GenerateTool"""

    def __init__(self):
        super(GenerateTool, self).__init__()
        self.generator = Generator(hparams, device)
        self._load_patterns(hparams.data_dir + "/GenrePatterns.txt")

    def _load_patterns(self, path):
        with open(path, 'r', encoding='utf-8') as fin:
            lines = fin.readlines()

        self._patterns = []
        '''
        each line contains:
            pattern id, pattern name, the number of lines,
            pattern: 0 either, 31 pingze, 32 ze, 33 rhyme position
        '''
        for line in lines:
            line = line.strip()
            para = line.split("#")
            pas = para[3].split("|")
            newpas = []
            for pa in pas:
                pa = pa.split(" ")
                newpas.append([int(p) for p in pa])

            self._patterns.append((para[1], newpas))

        self.p_num = len(self._patterns)
        print("load %d patterns." % (self.p_num))

    def build_pattern(self, pstr):
        pstr_vec = pstr.split("|")
        patterns = []
        for pstr in pstr_vec:
            pas = pstr.split(" ")
            pas = [int(pa) for pa in pas]
            patterns.append(pas)

        return patterns

    def generate_file(self, args):
        beam_size = args.bsize
        verbose = args.verbose
        manu = True if args.select == 1 else False

        assert args.inp is not None
        assert args.out is not None

        with open(args.inp, 'r', encoding='utf-8') as fin:
            inps = fin.readlines()

        fout = open(args.out, 'w')

        poems = []
        N = len(inps)
        log_step = max(int(N / 100), 2)
        for i, inp in enumerate(inps):
            para = inp.strip().split("#")
            keywords = para[0].split(" ")
            pattern = self.build_pattern(para[1])

            lines, info = self.generator.generate_one(keywords, pattern,
                                                      beam_size, verbose, manu=manu)

            if len(lines) != 4:
                ans = info
            else:
                ans = "|".join(lines)

            fout.write(ans + "\n")

            if i % log_step == 0:
                print("generating, %d/%d" % (i, N))
                fout.flush()

        fout.close()

    def _set_rhyme_into_pattern(self, ori_pattern, rhyme):
        pattern = copy.deepcopy(ori_pattern)
        for i in range(0, len(pattern)):
            if pattern[i][-1] == 33:
                pattern[i][-1] = rhyme
        return pattern

    def get_pattern(self, pattern_id, rhyme):
        ori_pattern = self._patterns[pattern_id]
        name = ori_pattern[0]
        pattern = ori_pattern[1]
        pattern = self._set_rhyme_into_pattern(pattern, rhyme)
        return pattern

    def generate_manu(self, args):
        beam_size = args.bsize
        verbose = args.verbose
        manu = True if args.select == 1 else False
        visual_mode = args.draw

        while True:
            keys = input("please input keywords (with whitespace split), 4 at most > ")
            pattern_id = int(input("please select genre pattern 0~{} > ".format(self.p_num - 1)))
            rhyme = int(input("please input rhyme id, 1~30> "))

            ori_pattern = self._patterns[pattern_id]
            name = ori_pattern[0]
            pattern = ori_pattern[1]
            pattern = self._set_rhyme_into_pattern(pattern, rhyme)
            print("select pattern: %s" % name)

            keywords = keys.strip().split(" ")
            lines, info = self.generator.generate_one(keywords, pattern,
                                                      beam_size, verbose, manu=manu, visual=visual_mode)

            if len(lines) != 4:
                print("generation failed!")
                continue
            else:
                print("\n".join(lines))


@app.route('/style_trans', methods=['POST'])
def style_trans():
    request_url = "https://aip.baidubce.com/rest/2.0/image-process/v1/style_trans"
    if 'file' not in request.files:
        return jsonify({'msg': 'No file part', 'state': 'failure'})
    f = request.files['file']
    img = base64.b64encode(bytearray(f.read()))
    opt = request.form['opt']
    # params = {"image": img, "option": "mononoke"}
    params = {"image": img, "option": opt}
    access_token = "24.d902461769c78e1991937d51541e4c7a.2592000.1617097889.282335-23720533"
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        res = response.json()['image']
        res_img = base64.b64decode(res)
        with open(image_trans_filename, 'wb') as img_obj:
            img_obj.write(res_img)
        response = Response(json.dumps({'msg': 'success', 'state': 'success', 'result': res},
                                       ensure_ascii=False).encode('utf-8'), mimetype="application/json")
        return response


@app.route('/filter', methods=['POST'])
def filter_image():
    request_url = "https://api-cn.faceplusplus.com/facepp/v2/beautify"
    if 'file' not in request.files:
        return jsonify({'msg': 'No file part', 'state': 'failure'})
    f = request.files['file']
    img = base64.b64encode(bytearray(f.read()))
    opt = request.form['opt']
    api_key = "lYPi9IZBXFLi9A7AXtVEQDwMcdkX2YJl"
    api_secret = "vuanKsuMYkxmbofYqSIWt6S5cnsg-2Xq"
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    params = {"api_key": api_key, "api_secret": api_secret, "image_base64": img, "filter_type": opt}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        res = response.json()['result']
        res_img = base64.b64decode(res)
        with open(image_filename, 'wb') as img_obj:
            img_obj.write(res_img)
        response = Response(json.dumps({'msg': 'success', 'state': 'success', 'result': res},
                                       ensure_ascii=False).encode('utf-8'), mimetype="application/json")
        return response


@app.route('/predict', methods=['POST'])
def predict():
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general"
    if 'file' not in request.files:
        return jsonify({'msg': 'No file part', 'state': 'failure'})
    f = request.files['file']
    img = base64.b64encode(bytearray(f.read()))
    params = {"image": img}
    access_token = '24.07a828ab4b1a1ec5772198f5150d2ebd.2592000.1615628511.282335-23658546'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        with open(filename, 'a', encoding='utf-8') as file_obj:
            json.dump(response.json(), file_obj, ensure_ascii=False, indent=4)
            file_obj.write('\n')
        reslines = response.json()['result']
        res = ' '.join(lines['keyword'] for lines in reslines)
        response = Response(json.dumps({'msg': 'success', 'state': 'success', 'result': res},
                                       ensure_ascii=False).encode('utf-8'), mimetype="application/json")
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


@app.route('/GenPoem', methods=['POST'])
def peom_generator():
    generate_tool = GenerateTool()
    keys = request.form['keys']
    pattern_id = int(request.form['pattern_id'])
    rhyme = int(request.form['rhyme'])
    keywords = keys.strip().split(" ")
    pattern = generate_tool.get_pattern(pattern_id, rhyme)
    lines, info = generate_tool.generator.generate_one(keywords, pattern, beam_size=20, verbose=1, manu=False, visual=0)
    if len(lines) != 4:
        return jsonify({'msg': 'No file part', 'state': 'failure'})
    else:
        res = ",".join(lines)
        response = Response(json.dumps({'msg': 'success', 'state': 'success', 'result': res},
                                       ensure_ascii=False).encode('utf-8'), mimetype="application/json")
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

@app.route('/', methods=['GET'])
def index_page():
    return("欢迎来到诗情画意微信小程序的API")

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', debug=True)
