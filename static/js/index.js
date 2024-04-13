
sendStartCommand = () => {
  fetch('/start', {method: 'get'});
}

handleStartButton = (event) => {
  event.preventDefault(); 
  sendStartCommand()
  window.location.href = event.target.parentNode.href;
}

const startButton = document.getElementById('startButton');
startButton.parentNode.addEventListener('click', handleStartButton);


