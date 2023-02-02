function setConfirmMessage (hrefTags, messageCustomClass) {
  let message = document.querySelector(`div.${messageCustomClass}`)
  for (let hrefTag of hrefTags) {
    hrefTag.addEventListener('click', () => {
      message.style.display = 'flex'
      document.body.style.overflow = 'hidden'
      message.setAttribute('data-href', hrefTag.dataset.href)
    })
  }
  message.querySelector('button.confirm-button').addEventListener('click', () => {
    window.location.href = url + message.dataset.href
  })
  message.querySelector('button.decline-button').addEventListener('click', () => {
    document.body.style.overflow = 'auto'
    message.style.display = 'none'
  })
}