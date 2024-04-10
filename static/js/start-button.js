
sendStartCommand = () => {
  const xhr = new XMLHttpRequest();
  xhr.open('GET', '/start');
  xhr.send();
  xhr.onreadystatechange = (e) => {
    console.log(Http.responseText);
  }
  location.reload();
}


const startButton = document.getElementById('startButton');
startButton.addEventListener('click', sendStartCommand);


