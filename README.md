<p align="center">
  <a href="https://github.com/shenhao-stu/2021_computer_design">
      <img src="https://gitee.com/shenhao-stu/picgo/raw/master/Other/logo_3.png" alt="chinese-poetry" height=40% width=40% />
  </a>
</p>
<p align="center">Python | shenhao0223@163.sufe.edu.cn | 上海财经大学 </p>

<h2 align="center">AI-chinese-poetry: 《诗情画意》</h2>

<p align="center">
  <a href="https://github.com/shenhao-stu/2021_computer_design" rel="nofollow">
    <img height="28px" alt="Build Status" src="https://img.shields.io/badge/build-passing-green.svg?style=for-the-badge" style="max-width:100%;">
  </a>
  <a href="https://github.com/shenhao-stu/2021_computer_design/LICENSE">
    <img height="28px" alt="License" src="http://img.shields.io/badge/license-mit-blue.svg?style=for-the-badge" style="max-width:100%;">
  </a>
  <a href="https://github.com/shenhao-stu/2021_computer_design" rel="nofollow">
    <img alt="HitCount" height="28px" src="http://hits.dwyl.com/shenhao-stu/2021_computer_design.svg" style="max-width:100%;">
  </a>
</p>
特色：AI自动识别上传的图片并生成诗歌，进行配图 + 全唐诗、全宋词的数据库模糊匹配

#### 使用步骤：

- **扫描二维码图片**

<img src="https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210327000009820.png" height=40% width=40% />

<u>由于小程序正在进行审核，可以使用下面第二种方式</u>

- **打开微信开发者工具，导入photo-edit项目**

![Snipaste_2021-03-27_00-05-42](https://gitee.com/shenhao-stu/picgo/raw/master/Other/Snipaste_2021-03-27_00-05-42.png)

---


#### MongoDB + Flask实现诗词模糊查询

##### step 1 : 诗词的爬取
```
cd database_api/craw_poetry
python3 crawl_poetry
python3 db.py
```
##### step 2 : MongoDB数据库的存储

> db = poetry collection = ccpc

![image-20210314215946890](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210314215946890.png)

##### step 3 : API+response
![response](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210314215257981.png)

---

#### 图片的识别——功能已经实现


##### step 1 : 配置access_token


```
cd General_object_recognition/
python3 access_token.py
```
##### step 2 : 测试图片预测结果
```
python3 res_sample.py
```

![](./诗歌的识别.png)

---

#### 关键字生成诗歌——功能正在调试


##### step 1 : 安装依赖


```
pip install requirements.txt
```
##### step 2 : 开启服务并测试
```
cd Poem_generator/codes/
python3 server.py
```

##### step 3 : 让服务保持运行状态
```
nohup python3 server.py > response.log 2>&1 &
```
##### step 4 : 接口API参数
- keys : 关键词不超过4个

- pattern: 五言、七言


![image-20210204204603197](./诗歌生成图例.png)

---

#### 诗歌+图片——前端

![image-20210314220233037](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210314220233037.png)

---

#### 诗歌匹配滤镜——风格迁移
##### step 1 : 配置access_token


```
cd Style_trans/
python3 access_token.py
```
##### step 2 : 测试图片预测结果
```
python3 sample_serve.py
```

##### step 3 : 接口API
- file : 图片的二进制

- opt

  | 序号 | opt          | 中文名称             |
  | ---- | ------------ | -------------------- |
  | 1    | cartoon      | 卡通画风格           |
  | 2    | pencil       | 铅笔风格             |
  | 3    | color_pencil | 彩色铅笔画风格       |
  | 4    | warm         | 彩色糖块油画风格     |
  | 5    | wave         | 神奈川冲浪里油画风格 |
  | 6    | lavender     | 薰衣草油画风格       |
  | 7    | mononoke     | 奇异油画风格         |
  | 8    | scream       | 呐喊油画风格         |

##### step 4 : Response
- msg : success
- state : success
- res : 图片Base64编码
![](./Style_trans/res_img.jpg)

---

#### 诗歌的美颜滤镜
##### step 1 : 接口API
- file : 图片的二进制

- opt ：

  | 序号 | opt          | 中文名称 |
  | ---- | ------------ | -------- |
  | 1    | black_white  | 黑白     |
  | 2    | calm         | 平静     |
  | 3    | sunny        | 晴天     |
  | 4    | trip         | 旅程     |
  | 5    | beautify     | 美肤     |
  | 6    | wangjiawei   | 王家卫   |
  | 7    | cutie        | 唯美     |
  | 8    | macaron      | 可人儿   |
  | 9    | new_york     | 纽约     |
  | 10   | sakura       | 樱花     |
  | 11   | 17_years_old | 十七岁   |
  | 12   | clight       | 柔光灯   |
  | 13   | tea_time     | 下午茶   |
  | 14   | whiten       | 亮肤     |
  | 15   | chaplin      | 卓别林   |
  | 16   | flowers      | 花香     |
  | 17   | memory       | 回忆     |
  | 18   | ice_lady     | 冰美人   |
  | 19   | paris        | 巴黎     |
  | 20   | times        | 时光     |
  | 21   | lomo         | LOMO     |
  | 22   | old_times    | 旧时光   |
  | 23   | spring       | 早春     |
  | 24   | story        | 故事     |
  | 25   | abao         | 阿宝色   |
  | 26   | wlight       | 补光灯   |
  | 27   | warm         | 暖暖     |
  | 28   | glitter      | 绚烂     |
  | 29   | lavender     | 薰衣草   |
  | 30   | chanel       | 香奈儿   |
  | 31   | prague       | 布拉格   |
  | 32   | old_dream    | 旧梦     |
  | 33   | blossom      | 桃花     |
  | 34   | pink         | 粉黛     |
  | 35   | jiang_nan    | 江南     |

##### step 4 : Response
- msg : success
- state : success
- res : 图片Base64编码

![image-20210327000838518](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210327000838518.png)