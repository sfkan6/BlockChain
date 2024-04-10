

getTransactionHash = 
  (privateKey, text) => {
  let EC = elliptic.ec;
  let ec = new EC('secp256k1');
  let key = ec.keyFromPrivate(privateKey)
  return key.sign(text).toDER('hex');
}

formatDate = (date) => {
  return (
    [
      date.getFullYear(),
      date.getMonth(),
      date.getDate(),
    ].join('-') +
    ' ' +
    [
      date.getHours(),
      date.getMinutes(),
      date.getSeconds(),
    ].join(':')
  );
}

getCurrentDate = () => {
  return formatDate(new Date());
}

getFormData = (e) => {
  const timestamp = getCurrentDate();
  const sender = document.getElementsByName('sender')[0].value;
  const recipient = document.getElementsByName('recipient')[0].value;
  const amount = document.getElementsByName('amount')[0].value;
  const message = document.getElementsByName('message')[0].value;
  const text = timestamp + sender + recipient + amount + message
  const privateKey = document.getElementsByName('privateKey')[0].value;
  // const transactionHash = getTransactionHash(privateKey, text);
  return {sender, recipient, amount, message, privateKey} ;
}
sendForm = () => {
  const body = getFormData();
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/transaction/create');
  xhr.setRequestHeader('Content-Type', "application/json");
  xhr.send(JSON.stringify(body));
}

let form = document.getElementById("myForm");
function handleForm(event) { 
  event.preventDefault(); 
  sendForm();
} 
// form.addEventListener('submit', handleForm);


