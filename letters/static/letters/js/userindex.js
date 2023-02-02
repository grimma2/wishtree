let pageSize = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight


new Swiper('.swiper', {
  direction: 'vertical',
  freeMode: true,
  mousewheel: {
    invent: true
  },
  grid: {
    rows: getAdaptValue(1, 2, 4)
  },
})

