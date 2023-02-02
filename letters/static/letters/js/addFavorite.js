async function setPopupMessage (event) {
  let el = event.target
  while (!el.dataset.href) {
    el = el.parentElement
  }

  let response = await fetch(url + el.dataset.href)
  if (response.redirected) {
    window.location.href = response.url
    return
  }

  let messageText
  if (response.ok) {
    messageText = 'Письмо было успешно добавленно'
  } else if (response.status === 403) {
    messageText = 'Вы больше не можете добавлять письма в избранные'
  }

  let popupMessage = document.querySelector('p.popup-message')
  popupMessage.style.display = 'flex'
  let height = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight
  popupMessage.style.marginTop = `${height + window.scrollY - 80}px`
  popupMessage.textContent = messageText
  setTimeout(() => {
    popupMessage.style.display = 'none'
  }, 3000)
}
