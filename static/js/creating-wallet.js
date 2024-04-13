
copy = (event) => {
  const keyDiv = event.target.parentNode.getElementsByClassName("key")[0];
  navigator.clipboard.writeText(keyDiv.textContent);
}

const copyButtons = document.getElementsByClassName("copyButton");
Array.prototype.forEach.call(copyButtons, (copyButton) => {
    copyButton.addEventListener("click", copy)
});
