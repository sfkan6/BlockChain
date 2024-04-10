

const header = document.getElementById('header');
const transactions = document.getElementById('transactions');

ChangeTab = (e) => {
  const activeButton = document.getElementsByClassName('activeMode')[0];
  if (e.target.innerText != activeButton.innerHTML) {
    activeButton.classList.remove('activeMode');
    e.target.classList.add('activeMode');

    if (e.target.innerHTML == 'Info') {
      header.classList.remove('hidden');
      transactions.classList.add('hidden');
    } else {
      transactions.classList.remove('hidden');
      header.classList.add('hidden');
    }
  }
}

const TransactionsButton = document.getElementById('TransactionsButton');
const InfoButton = document.getElementById('InfoButton');

InfoButton.addEventListener('click', ChangeTab);
TransactionsButton.addEventListener('click', ChangeTab);


