// pages/cangTou/cangTou.js
Page({
  onShareAppMessage() {
    return {
      title: 'form',
      path: 'page/component/pages/form/form',
    }
  },

  data: {
    chosen: '',
    //请求到的藏头诗结果
    poem: []
  },

  formSubmit(e) {
    const self = this, keywords = e.detail.value.input
    if (keywords.length !== 4) {
      wx.showToast({
        title: '必须为4个字！',
        icon: "none",
        duration: 2000,
      })
      return 
    }
    console.log('form发生了submit事件，携带数据为：', e.detail.value)
    wx.showLoading({
      title: '努力写诗中',
    })
    wx.request({
      url: 'https://ai-poetry.top:5000/poetry',
      data: {
        acrostic: true,
        keywords,
      },
      success(res) {
        console.log(res.data.result.res)
        const poem = res.data.result.res.split("。")
        poem.pop()
        self.setData({poem})
        console.log(self.data.poem)
      },
      fail() {
        console.log("藏头诗请求失败")
      },
      complete() {
        wx.hideLoading()
      }
    })
  },

  formReset(e) {
    console.log('form发生了reset事件，携带数据为：', e.detail.value)
    this.setData({
      chosen: '',
      poem: []
    })
  }
})
