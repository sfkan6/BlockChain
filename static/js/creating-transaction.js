
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

getIndexOfNewBlock = async () => {
  const response = await fetch('/chainlength', {method: 'get'})
  const jsonResponse = await response.json();
  return jsonResponse.chain_length;
}

getDataString = ({block_index, timestamp, sender, recipient, amount, message}) => {
  return block_index + timestamp + sender + recipient + amount + message;
}

getFormData = () => {
  const sender = document.getElementsByName('sender')[0].value;
  const recipient = document.getElementsByName('recipient')[0].value;
  const amount = document.getElementsByName('amount')[0].value;
  const message = document.getElementsByName('message')[0].value;
  const privateKey = document.getElementsByName('privateKey')[0].value;
  return {sender, recipient, amount, message, privateKey};
}

getTransactionByData = async (transactionData) => {
  const privateKey = transactionData.privateKey;
  delete transactionData.privateKey;
  const dataString = getDataString(transactionData);
  const signature = await getDERSignature(privateKey, dataString);
  return {...transactionData, signature};
}

getTransaction = async () => {
  transactionData = getFormData();
  transactionData.block_index = await getIndexOfNewBlock();
  transactionData.timestamp = getCurrentDate();
  return await getTransactionByData(transactionData);
}

createTransaction = async (transaction) => {
  const data = {method: 'post', body: JSON.stringify(transaction)}
  await fetch('/transaction/create', data)
    .then(response => {
      if (response.redirected) {
        window.location.href = response.url;
      }
      return response.json();
    })
    .then(response => {
      alert(response.detail);
    })
}

handleTransactionForm = async (event) => {
  event.preventDefault(); 
  const transaction = await getTransaction();
  await createTransaction(transaction);
}

const transactionForm = document.getElementById("transactionForm");
transactionForm.addEventListener("submit", handleTransactionForm);

