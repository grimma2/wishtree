function showInfoMessage(message) {
  message.style.display = 'block'
  document.querySelector('div.helper').classList.remove('helper-limited')
}

function setVisitedMessage (cookieName, messageText) {
  if (!document.cookie.includes(cookieName)) {
    document.cookie = `${cookieName}=1; expires=Fri, 31 Dec 9999 23:59:59 GMT; path=/`
    let message = document.querySelector('div.info-message')
    showInfoMessage(message)
    message.querySelector('span.message-text').textContent = messageText
  }
}

document.querySelector('div.info-message > img').addEventListener('click', () => {
  document.querySelector('div.helper').classList.add('helper-limited')
  document.querySelector('div.info-message').style.display = 'none'
})


const hints = {
  'Что мне делать, после того, как я выбиру письмо?':
  'Подсказка к тексту: Что мне делать, после того, как я выбиру письмо?',

  'Подсказка 2': 'Текст к подсказке 2',

  'Что мне делать, после того, как я выбиру письмо? 2':
  'Подсказка к тексту: Что мне делать, после того, как я выбиру письмо? 2',

  'Что мне делать, после того, как я выбиру письмо? 3':
  'Подсказка к тексту: Что мне делать, после того, как я выбиру письмо? 3'
}

for (let hintKey of Object.keys(hints)) {
  document.querySelector('div.hints-swiper > div.swiper-wrapper').insertAdjacentHTML(
    'afterbegin',
    `<div class="swiper-slide hint-key"><span class="hint-text">${hintKey}</span></div>`
  )
}

for (let hintKeyElement of document.querySelectorAll('div.hint-key')) {
  hintKeyElement.addEventListener('click', (event) => {
    document.querySelector('div.hints-swiper').style.display = 'none'
    let message = document.querySelector('div.info-message')
    showInfoMessage(message)
    message.querySelector('span.message-text').textContent = hints[event.target.textContent]
  })
}

document.querySelector('div.helper-img-container').addEventListener('click', () => {
  document.querySelector('div.helper').classList.remove('helper-limited')
  document.querySelector('div.hints-swiper').style.display = 'block'
  document.querySelector('div.info-message').style.display = 'none'
})


new Swiper('.hints-swiper', {
  spaceBetween: 10,
  freeMode: true,
  mousewheel: {
    invent: true
  },
  slidesPerView: getAdaptValue(1.2, 1.8, 2.5)
})