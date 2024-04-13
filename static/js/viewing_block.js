

const blockHeader = document.getElementById('blockHeader');
const transactions = document.getElementById('transactions');

changeTab = (e) => {
  const activeButton = document.getElementsByClassName('activeMode')[0];
  if (e.target.innerText != activeButton.innerHTML) {
    activeButton.classList.remove('activeMode');
    e.target.classList.add('activeMode');

    if (e.target.innerHTML == 'Info') {
      blockHeader.classList.remove('hidden');
      transactions.classList.add('hidden');
    } else {
      transactions.classList.remove('hidden');
      blockHeader.classList.add('hidden');
    }
  }
}

const transactionsButton = document.getElementById('transactionsButton');
const blockHeaderButton = document.getElementById('blockHeaderButton');

blockHeaderButton.addEventListener('click', changeTab);
transactionsButton.addEventListener('click', changeTab);
