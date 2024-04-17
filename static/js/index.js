
sendStartCommand = async () => {
  await fetch('/start', {method: 'post'});
}

handleStartButton = async (event) => {
  event.preventDefault(); 
  await sendStartCommand()
  window.location.href = event.target.parentNode.href;
}

const startButton = document.getElementById('startButton');
startButton.parentNode.addEventListener('click', handleStartButton);


