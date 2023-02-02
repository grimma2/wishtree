let results = document.querySelector('ul.search-results')

async function fetchSearchAdmin(queryText) {
  results.innerHTML = ''
  if (!queryText) {
    return
  }

  let response = await fetch(`${url}/letters/search/admin/${queryText}/`)
  let data = await response.json()

  for (let letter of data.letters_by_user) {
    results.insertAdjacentHTML(
      'afterbegin',
      `
<li class="search-result search-by-user">
    <a href="/letters/letter/admin/${letter.pk}">Пользователь ${letter.picked_by__first_name}</a>
</li>`
    )
  }

  for (let letter of data.letters_by_child) {
    results.insertAdjacentHTML(
      'afterbegin',
      `
<li class="search-result search-by-child">
    <a href="/letters/letter/admin/${letter.pk}">Ребёнок ${letter.child__name}</a>
</li>
`
    )
  }

  for (let letter of data.letters_by_gift) {
    results.insertAdjacentHTML(
      'afterbegin',
      `
<li class="search-result search-by-gift">
    <a href="/letters/letter/admin/${letter.pk}">Подарок ${letter.gift__name}</a>
</li>
`
    )
  }
}


async function fetchSearchUser(queryText) {
  results.innerHTML = ''
  if (!queryText) {
    return
  }

  let response = await fetch(`/letters/search/user/${queryText}/`)
  let data = await response.json()

  for (let letter of data.letters_by_child) {
    results.insertAdjacentHTML(
      'afterbegin',
      `
<li class="search-result search-by-child">
    <a href="/letters/letter/user/${letter.pk}">Ребёнок ${letter.child__name}</a>
</li>
`
    )
  }

  for (let letter of data.letters_by_gift) {
    results.insertAdjacentHTML(
      'afterbegin',
      `
<li class="search-result search-by-gift">
    <a href="/letters/letter/user/${letter.pk}">Подарок ${letter.gift__name}</a>
</li>
`
    )
  }
}
