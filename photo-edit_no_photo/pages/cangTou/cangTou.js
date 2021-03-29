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
    keywords: '',  //藏的头
    poem: [], //请求到的藏头诗结果
  },

  formSubmit(e) {
    const self = this, keywords = e.detail.value.input
    self.setData({keywords})
    if (keywords.length !== 4) {
      wx.showToast({
        title: '必须为4个字！',
        icon: "none",
        duration: 2000,
      })
      return 
    }
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
  },

  anotherPoem(ev) {
    const self = this
    wx.showLoading({
      title: '努力写诗中',
    })
    wx.request({
      url: 'https://ai-poetry.top:5000/poetry',
      data: {
        acrostic: true,
        keywords: self.data.keywords,
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
  savePoem() {
    const poems = wx.getStorageSync('poem') || []
    poems.push(this.data.poem.join("。"))
    console.log(poems)
    wx.setStorageSync('poem', poems)
    wx.showToast({
      title: '保存成功',
      icon: 'success',
      duration: 2000,
    })
  }
})
