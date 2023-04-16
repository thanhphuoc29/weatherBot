const messageInput = document.getElementById('exampleFormControlInput1');
const sendMessage = document.getElementById('sendText');
const boxChat = document.querySelector('.card-body');
var api = "http://127.0.0.1:5000/respone";
// run
sendMessageToBot()

function getTextUser() {
  let text = messageInput.value;
  let imageUrl = "/static/images/user.png";
  let content = `<div class="d-flex flex-row justify-content-end mb-4">
    <div>
      <p class="small p-2 me-3 mb-1 text-white rounded-3 bg-primary">${text}
    </div>
    <img src="${imageUrl}" alt="avatar 1" style="width: 45px; height: 100%;">
  </div>`;

  boxChat.insertAdjacentHTML('beforeend', content);
  boxChat.scrollTop = boxChat.scrollHeight;
  messageInput.value = ''
  var data = {
    text: text
  }
  sendApiRequest(data);

}

function sendApiRequest(data) {
  var xhttp = new XMLHttpRequest();
  xhttp.onload = function () {
    var respone = xhttp.responseText;
    var data = JSON.parse(respone);
    console.log(data)
    BotRespone(data['respone']);
  }
  xhttp.open("POST", api, true);
  xhttp.setRequestHeader("Content-type", "application/json");
  console.log(data)
  xhttp.send(JSON.stringify(data));
}

function BotRespone(respone) {
  let content = ` <div class="d-flex flex-row justify-content-start">
    <img src="/static/images/bot-icon.png" alt="avatar 1"
      style="width: 45px; height: 100%;">
    <div>
      <p class="small p-2 ms-3 mb-1 rounded-3" style="background-color: #f5f6f7;">${respone}</p>
    </div>
  </div>`
  boxChat.insertAdjacentHTML('beforeend', content);
  boxChat.scrollTop = boxChat.scrollHeight;
}
function sendMessageToBot() {
  sendMessage.addEventListener('click', getTextUser)
  messageInput.addEventListener('keydown', function (event) {
    if (event.keyCode === 13) {
      getTextUser(event);
    }
  });

}