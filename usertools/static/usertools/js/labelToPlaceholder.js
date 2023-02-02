let inputs = document.querySelectorAll('form > p > label')

for (let i of inputs) {
  let inputText = i.textContent.slice(0, i.textContent.length - 1)
  document.getElementById(i.attributes.for.value).placeholder = inputText
}
