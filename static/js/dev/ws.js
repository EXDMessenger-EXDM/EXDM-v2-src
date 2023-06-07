/*
WebSocket dev

Используется для проверки WebSocket сервера
*/

function add_ws_message(message) {
    document.getElementById('ws-messages').innerHTML = document.getElementById('ws-messages').innerHTML + `<p>[${new Date().toLocaleString()}] ${message}</p>`;
    console.log(`[${new Date().toLocaleString()} WebSocket] ${message}`);
}

add_ws_message('connecting');
const myWs = new WebSocket('ws://localhost:9000');
myWs.onopen = function () {
    add_ws_message('connected');
};
myWs.onclose = function (event) {
    add_ws_message(`closed: ${event}`);
};
myWs.onerror = function (event) {
    add_ws_message(`error: ${event}`);
};
myWs.onmessage = function (message) {
    add_ws_message(message.data);
};