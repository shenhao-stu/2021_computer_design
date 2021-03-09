# 项目蓝图
## 后台接口
1. 传入关键字，返回对应的古诗
2. 传入图片文件，返回识别出若干的关键词
3. 待完成: 滤镜

## 前端界面:
传入图片->识别图片->用户选择关键字->识别古诗->图片上添加文字

## 图片更新原理: 
1. 界面显示原来的tmpImageSrc  ->注意wxml上的image标签
2. 创建temp canvas(看不见的)  ->createCanvasContext
3. 把原来的图像、文字、滤镜等绘制到temp canvas上  ->在ctx上调用各种draw...
4. 更新图片，把temp canvas保存为tmpImageSrc   ->方法:saveImageUseTempCanvas
5. 界面上显示tmpImageSrc  ->注意wxml上的image标签
