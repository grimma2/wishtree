async function searchLetter (text) {
  try {
    let response = await fetch(`usertools/search/letter/${text}`)
    let data = (await response).json()
    if (!data?.data) {
      return
    }
    document.getElementById('searchDropout').insertAdjacentElement(
      'afterbegin',
      ``
    )
  } catch (e) {
    console.log(e)
  }
}