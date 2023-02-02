setInterval(() => {
  if (Math.floor(Math.random() * 3) === 1) {
    let santa = document.getElementById('santa')

    if (!santa) return

    santa.classList.add('santa-event')
    setTimeout(() => {
      santa.classList.remove('santa-event')
    }, 5000)
  }
}, 30000)


const url = `${location.protocol}//${location.host}`

let changeButton = document.querySelectorAll('.search-button')
let searchBlock = document.querySelector('div.search-container')
let hideSearch = document.querySelector('div.search-container > div.back-arrow')

for (let button of changeButton) {
  button.addEventListener('click', () => {
    if (height >= 1500) {
      searchBlock.style.display = 'grid'
    } else {
      searchBlock.style.display = 'block'
    }
  })
}

searchBlock.querySelector('input').addEventListener('input', (event) => {
  let url = ''
  if (document.querySelector('header').id === 'user_header') {
    fetchSearchUser(event.target.value)
  } else {
    fetchSearchAdmin(event.target.value)
  }
})

hideSearch.addEventListener('click', () => {
  searchBlock.style.display = 'none'
})

let initialWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth
// change viewport onresize event, because device height change when keyboard appear on android device
window.onresize = () => {
  const metaViewport = document.querySelector('meta[name=viewport]')
  if (metaViewport.content) {
    return
  }

  let heightIsReduce = height > window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight
  let widthNotChange = initialWidth === (window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth)
  if (heightIsReduce && widthNotChange) {
    metaViewport.setAttribute('content', 'height=' + height)
  } else {
    metaViewport.setAttribute('content', '')
  }
}

function getAdaptValue (forSmall, forMedium, forLarge) {
  let height = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight
  let result = forSmall
  if ((height < 1500) && (height > 850)) {
    result = forMedium
  } else if (height < 850) {
    result = forLarge
  }

  return result
}

document.addEventListener('DOMContentLoaded', () => {
  for (let letter of document.querySelectorAll('img.letter-img')) {
    letter.addEventListener('click', (event) => {
      window.location.href = event.target.src
    })
  }
})
