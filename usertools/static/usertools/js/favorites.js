updateLinkState()

function changeMainCheckbox (event) {
  if (event.target.checked) {
    for (let checkbox of document.querySelectorAll('input[type="checkbox"]:not(:checked)')) {
      checkbox.checked = true
    }
  } else {
    for (let checkbox of document.querySelectorAll('input[type="checkbox"]:checked')) {
      checkbox.checked = false
    }
  }
}

function changeRegularCheckboxes () {
  let checkboxes = Array.prototype.slice.call(
    document.querySelectorAll('input[name="letter-checkbox"]')
  )

  if (checkboxes.reduce((a, b) => a && checkboxes.filter(ch => ch.checked === true).includes(b), true)) {
    document.getElementById('select-all-checkbox').checked = true
  } else {
    document.getElementById('select-all-checkbox').checked = false
  }
}

for (let checkbox of document.querySelectorAll('input[type="checkbox"]')) {
  checkbox.addEventListener('click', (event) => {
    if (event.target.id === 'select-all-checkbox') {
      changeMainCheckbox(event)
    } else {
      changeRegularCheckboxes()
    }
    updateLinkState(false)
  })
}


// send request when user click to delete button
document.getElementById('delete-all-button').addEventListener('click', () => {
  let letters = document.querySelectorAll('div.favorite')
  let delete_letters = Array.prototype.slice.call(letters).filter(
    lt => lt.querySelector('input[name="letter-checkbox"]:checked')
  )

  if (!delete_letters.length) return

  let param = elementsIdForRequest(delete_letters, true)
  try {
    fetch(`${url}/usertools/delete/favorites/${param}`)
  } catch (e) {
    console.log(e)
  }

  if (!document.querySelectorAll('div.favorite').length) {
    location.reload()
  }
})

for (let el of document.querySelectorAll('div.favorite')) {
  el.querySelector('div.delete-favorite').addEventListener('click', () => {
    let param = el.dataset.objectid
    el.remove()

    try {
      fetch(`${url}/usertools/delete/favorites/${param}`)
    } catch (e) {
      console.log(e)
    }

    setTimeout(() => {
      if (!document.querySelectorAll('div.favorite').length) {
        location.reload()
      }
    }, 1000)
  })
}


function elementsIdForRequest (elements, removeElements=false) {
  let result = ''
  for (let el of elements) {
    result = result + `${el.dataset.objectid},`
    if (removeElements) el.remove()
  }

  return result.slice(0, result.length - 1)
}


// move letters from user favorites to selected on click on button
function updateLinkState () {
  let letters = document.querySelectorAll('div.favorite')
  let select_favorites = Array.prototype.slice.call(letters).filter(
    lt => lt.querySelector('input[name="letter-checkbox"]:checked')
  )

  let param = elementsIdForRequest(select_favorites)
  document.querySelector('button.select-all-button').setAttribute(
    'data-href',
    `/usertools/favorites_to_selected/${param}`
  )
}
