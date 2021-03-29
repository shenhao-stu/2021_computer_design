//app.js
// App({
//   onLaunch: function () {
//     // 展示本地存储能力
//     var logs = wx.getStorageSync('logs') || []
//     logs.unshift(Date.now())
//     wx.setStorageSync('logs', logs)

//     this.globalData.myDevice = wx.getSystemInfoSync()

//     for (var i = 0; i < 156; i++) {
//       this.globalData.imgUrl[i] = 'https://qcloudtest-1256525699.cos.ap-guangzhou.myqcloud.com/emotion/' + (i + 1) + '.png'
//     }
//     // 登录
//     wx.login({
//       success: res => {
//         // 发送 res.code 到后台换取 openId, sessionKey, unionId
//       }
//     })
//     // 获取用户信息
//     wx.getSetting({
//       success: res => {
//         if (res.authSetting['scope.userInfo']) {
//           // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
//           wx.getUserInfo({
//             success: res => {
//               // 可以将 res 发送给后台解码出 unionId
//               this.globalData.userInfo = res.userInfo

//               // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
//               // 所以此处加入 callback 以防止这种情况
//               if (this.userInfoReadyCallback) {
//                 this.userInfoReadyCallback(res)
//               }
//             }
//           })
//         }
//       }
//     })
//   },
//   globalData: {
//     userInfo: null,
//     myDevice:null,
//     imgUrl:[],
//   }
// })

//app.js

const AV = require('./libs/av-weapp-min');

AV.init({
  appId: '5QYsrni4fqM7383D0jPb1isT-gzGzoHsz',
  appKey: 'LHOhQmG8nzXRGUVBpS9IxIK0',
});

const Q = new AV.Query('poetry')

Q._limit = 500

App({
  onLaunch: function () {
    this.globalData.myDevice = wx.getSystemInfoSync()

    for (var i = 0; i < 156; i++) {
      this.globalData.imgUrl[i] = 'https://qcloudtest-1256525699.cos.ap-guangzhou.myqcloud.com/emotion/' + (i + 1) + '.png'
    }
    // 展示本地存储能力
    var vm = this;
    Q.find().then(function (results) {
      var poetrys = {}

      for (var i in results) {
        var item = results[i]
        var poetry = {}
        poetry['author'] = item.attributes.author
        poetry['title']= item.attributes.title
        poetry['paragraphs'] = item.attributes.paragraphs
        poetry['cover'] = item.attributes.cover
        poetry['id'] = item.id
        poetrys[item.id] = poetry
      }

      wx.setStorageSync('poetrys', poetrys)

      vm.globalData.poetrys = poetrys;

      if (vm.poetrysCallback) {
        vm.poetrysCallback(poetrys);
      }
    })
  },
  globalData: {
    userInfo: null,
    current: null,
    poetrys: {},
    myDevice:null,
    imgUrl:[],
  }
})