let height = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight
let burgerBlock = document.getElementById('burger-block')
let burgerMenu = document.getElementById('burger-menu')


document.addEventListener('click', (event) => {
  if (height > 1300) {
    if (!burgerBlock.contains(event.target)) {
      burgerMenu.style.display = 'none'
    } else {
      burgerMenu.style.display = 'flex'
      burgerMenu.style.marginTop = `${document.querySelector('header').offsetHeight}px`
    }
  }

  if (!searchBlock.contains(event.target) && !(changeButton[0].contains(event.target) || changeButton[1].contains(event.target))) {
    searchBlock.style.display = 'none'
  }

  let helper = document.querySelector('div.helper')
  if (!helper) return
  if (!helper.contains(event.target)) {
    helper.classList.add('helper-limited')
    for (let content of helper.querySelectorAll('div.helper-content')) {
      content.style.display = 'none'
    }
  }
})