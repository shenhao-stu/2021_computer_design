### 作品名称：《诗情画意》

AI自动识别上传的图片并生成诗歌，进行配图

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
- pattern_id
	- 00 七绝一
	- 01 七绝二
	- 02 七绝三
	- 03 七绝四
	- 04 五绝一
	- 05 五绝二
	- 06 五绝三
	- 07 五绝四
- rhyme : 1-30 的韵脚

![image-20210204204603197](./诗歌生成图例.png)

#### 诗歌+图片——前端正在做

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
  - cartoon：卡通画风格
  - pencil：铅笔风格
  - color_pencil：彩色铅笔画风格
  - warm：彩色糖块油画风格
  - wave：神奈川冲浪里油画风格
  - lavender：薰衣草油画风格
  - mononoke：奇异油画风格
  - scream：呐喊油画风格
  - gothic：哥特油画风格

##### step 4 : Response
- msg : success
- state : success
- res : 图片Base64编码
![](./Style_trans/res_img.jpg)

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
![](./Filter/res_img.jpg)

