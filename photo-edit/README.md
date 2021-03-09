# 图片编辑小程序--HiPhoto

   全能、便捷的图片编辑工具。实现了图片裁剪、添加文字、涂鸦、拼长图、拼相框等图片编辑功能，另外还有一个简易的表情包制作功能。

<div align="center">
<img alt="主界面" src="https://github.com/nimoat/photo-edit/raw/master/image/githubImg/mainPage.jpg">
</div>

   扫描下面的微信小程序码，体验该小程序。

<div align="center">
<img alt="HiPhoto小程序码" src="https://github.com/nimoat/photo-edit/raw/master/image/githubImg/QRcode.jpg">
</div>

## 目录

- [使用代码](#使用代码)
- [功能实现](#功能实现)
  - [一、图片裁剪](#一裁剪功能)
  - [二、添加文字](#二添加文字)
  - [三、涂鸦功能](#三涂鸦功能)
  - [四、拼长图](#四拼长图)
  - [五、拼相框](#五拼相框)
  - [六、表情包制作](#六表情包制作)
  - [七、保存图片](#七保存图片)

## 使用代码

  1. 下载并安装[微信开发者工具](https://mp.weixin.qq.com/debug/wxadoc/dev/devtools/download.html)，使用微信号扫码登录开发者工具。

  2. 打开微信开发者工具，点击“小程序项目”按钮，输入小程序 AppID，项目目录选择下载的代码目录，点击确定创建小程序项目。

## 功能实现

### 一、图片裁剪

  1. 裁剪界面由image组件和裁剪框组成。image组件用来显示用户载入的图片；裁剪框在用户点击裁剪框按钮后浮动显示在图片上，裁剪框的遮罩效果通过背景颜色透明以及盒阴影（box-shadow）实现。

  2. 在image组件上检测触摸事件，通过事件对象判断触摸点数，单点触摸时通过获取手指移动距离实现图片的自由拖动，两点触摸时，通过获取两点之间的距离计算图片缩放比例，实现图片自由缩放。

  3. 在裁剪框上检测触摸事件，通过获取手指移动距离实现裁剪框自由拖动；监测裁剪框右下圆点的触摸事件，通过获取手指移动距离计算裁剪框宽、高的增减，实现裁剪框的自由缩放功能。

  4. 用户裁剪完成（点击右上角√按钮后），根据保存的裁剪框宽、高以及图片缩放比例计算图片真实裁剪区域，根据计算好的区域将图片画在隐藏canvas上，得到裁剪后的图片。

<div align="center">
<img alt="裁剪界面" src="https://github.com/nimoat/photo-edit/raw/master/image/githubImg/cropPage.jpg">
</div>

### 二、添加文字

  1. 添加文字界面由image组件、text组件和input组件构成。image组件用来显示用户载入的图片。input组件使用绝对定位隐藏在界面之外（left:-9999px）。text组件用来动态演示用户对文字大小、颜色、样式的调整，当用户点击添加按钮后，text组件弹出。在text组件上监测tap事件，用户点击text组件时，使input组件获得焦点从而调出键盘。在text组件上绑定触摸事件，实现text组件的自由拖动。在input组件上绑定input事件，将text组件的内容与用户输入绑定。

  2. 用户添加文字完成（点击右上角√按钮后），根据保存的text组件定位，文字大小、颜色、样式。将文字写在隐藏canvas上（先画原图片，再写文字），得到添加文字后的图片。

<div align="center">
<img alt="添加文字界面" src="https://github.com/nimoat/photo-edit/raw/master/image/githubImg/textPage.jpg">
</div>

### 三、涂鸦功能

  1. 涂鸦界面由canvas组件和image组件构成。在canvas上监测touchmove事件连续画线（ctx.moveTo，ctx.lineTo）实现涂鸦功能。线宽、颜色可以由用户在下方工具栏设置。

  2. 由于canvas组件在小程序中层级最高，因此采用动态调整canvas高度的方法显示底部工具菜单栏，即调出和隐藏工具栏时，动态改变canvas的高度。

  3. 为了实现橡皮擦和清除功能（不破坏原图），采用将canvas组件覆盖在image组件上，image组件加载涂鸦前的原图，这样使用橡皮檫时擦掉的区域会显示原图。涂鸦完成后（返回主菜单），先保存canvas得到涂鸦图片，然后在隐藏canvas上先绘制涂鸦前的原图，再绘制涂鸦效果图。就能得到完整的涂鸦后的图片了。

<div align="center">
<img alt="涂鸦界面" src="https://github.com/nimoat/photo-edit/raw/master/image/githubImg/doodlePage.jpg">
</div>

### 四、拼长图

  1. 拼长图界面由image组件构成。用户从系统相册选择图片时，将图片的临时路径保存到数组中，而image组件使用列表渲染（wx:for）将数组中的图片全部载入界面，实现拼接的演示效果。在image上绑定longtap事件，长按一张图片后，弹出删除该图片的确认框，确认后在数组中删除该图片的路径，实现删除的演示效果。

  2. 保存时，将数组中的图片依次画在隐藏canvas上，所有图片宽度保持一致，高度按图片比例缩放，每张图片的定位由图片的宽高、缩放比计算得到。这样就实现的拼长图的功能。

### 五、拼相框

  1. 拼相框界面由两个image组件和包裹它们的view组件构成。相框为部分区域透明的图片，加载相框的image组件覆盖在加载照片的组件之上，照片就会透过透明区域显示出来。在view组件上监测触摸事件，实现照片的自由拖动和缩放。相框保存宽度全显，而照片能够动态调整，就能实现拼相框的效果了。

  2. 保存时，根据照片和相框图片的缩放比例和定位关系，在隐藏canvas中先画照片，再画相框，就就能实现拼相框功能。

<div align="center">
<img alt="拼相框界面" src="https://github.com/nimoat/photo-edit/raw/master/image/githubImg/framePage.jpg">
</div>

### 六、表情包制作

  表情包素材保存在腾讯云存储，进入选择界面后根据链接加载显示缩略图，image使用懒加载，加快素材的渲染。用户选择一个表情素材后，使用wx.downloadFile下载该图片并保存为临时路径。之后的处理实现与添加文字功能相似。

### 七、保存图片

  1. 小程序的所有图片保存都使用隐藏的canvas组件（left:-9999px）完成，根据图片的定位、缩放比、裁剪以及添加的文字的效果等数据在隐藏canvas上作图，并导出临时路径以便进一步处理。

  2. 为了保证图片的质量（图片画在canvas上后像素不降低），隐藏canvas的宽高等于图片的实际宽高。即在画布上调用drawImage之前，使用wx.getImageInfo获取需要画的图片的真实宽高，进而调整隐藏canvas的宽高。

  3. 用户点击保存按钮后，进入图片预览界面（wx.previewImage），长按图片可选择保存本地相册或者发送给微信朋友。

