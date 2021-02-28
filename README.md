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
cd Peom_generator/codes/
python3 server.py
```

##### step 3 : 让服务保持运行状态
```
nohup python3 server.py > response.log 2>&1 &
```

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
![](./Style_trans/res_img.jpg)

