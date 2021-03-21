// pages/mine/mine.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    poem: [],
    isModifying: false,
    poemIndex: -1,
    isChangingContent: false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // 以下为测试代码
    wx.setStorageSync("poem", [
        "窗前明月光，疑似地上霜，举头望明月，低头思故乡。",
        "两个黄鹂鸣翠柳，一行白鹭上青天。窗含西岭千秋雪，门泊东吴万里船。"
      ])
    // 获取本地存储诗词，加载到this.data中
    const poem = wx.getStorageSync('poem')
    console.log(poem)
    this.setData({poem})
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  ontap(e) {
    const index = e.currentTarget.dataset.index  //获取诗歌的下标
    console.log(index)
    this.setData({isModifying: true, poemIndex: index})
  },
  closeModify() {
    this.setData({isModifying: false, poemIndex: -1})
  },
  deletePoem() {
    console.log("delete " + this.data.poemIndex)
    this.data.poem.splice(this.data.poemIndex, 1)
    this.setData({poem: this.data.poem})
    this.closeModify()
  },
  changeContent() {
    this.setData({isChangingContent: true})
  },
  formSubmit(e) {
    console.log(e)
  },
})