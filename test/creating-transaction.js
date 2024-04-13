
getChainLength = async () => {
  var xhr = new XMLHttpRequest();
  url = 'http://127.0.0.1:8000/chainlength';
  xhr.open('GET', url);
  // xhr.setRequestHeader("Access-Control-Allow-Origin", 'http://127.0.0.1:8000');
  // xhr.setRequestHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  // xhr.setRequestHeader('Access-Control-Allow-Headers', 'Content-Type');
  xhr.onreadystatechange = function() {
      if (xhr.readyState == XMLHttpRequest.DONE) {
        console.log(xhr);
        console.log(xhr.response);
        console.log(xhr.status);
      }
  }
  xhr.send();
}

getChainLength();


getSHA256Hash = async (string) => {
  const utf8 = new TextEncoder().encode(string);
  return crypto.subtle.digest('SHA-256', utf8).then((hashBuffer) => {
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray
      .map((bytes) => bytes.toString(16).padStart(2, '0'))
      .join('');
    return hashHex;
  });
}


getDERSignature = async (privateKey, text) => {
  let EC = elliptic.ec;
  let ec = new EC('secp256k1');
  let key = ec.keyFromPrivate(privateKey);
  const textHash = await getSHA256Hash(text);
  return key.sign(textHash).toDER('hex');
}


handleButton = async () => {
  const message = document.getElementById('message').value;
  const privateKey = document.getElementById('privateKey').value;
  const signature = await getDERSignature(privateKey, message);
  console.log(signature);
} 


