for (let selectEl of document.querySelectorAll('select[name="status-select"]')) {
  selectEl.addEventListener('change', (e) => {
    let optionEl = e.target
    changeGift(optionEl.dataset.objectid, optionEl.value)
  })
}

async function changeGift (giftId, status) {
  try {
    await fetch(`/usertools/update/gift/${giftId}/${status}`)
  } catch (e) {
    console.log(e)
  }

  let pageSize = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight
  let successMessage = document.querySelector('p.popup-message')
  successMessage.style.marginTop = `${pageSize + window.scrollY - 80}px`
  successMessage.style.display = 'flex'
  successMessage.textContent = 'Состояние подарка было успешно изменено'
  setTimeout(() => {
    successMessage.style.display = 'none'
  }, 3000)
}
