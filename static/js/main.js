function complete_message() {
    $.ajax({
        url: 'http://127.0.0.1:5000/api/ai/chatgpt-3.5',
        type: 'POST',
        contentType: "application/json",
        data: JSON.stringify({text: document.getElementById('message-input').value }),
        success: function(response) {
            document.getElementById('message-input').value = response['text'];
        }
    });
}

function get_messages() {
    $.ajax({
        url: 'http://127.0.0.1:5000/api/channels/global/messages',
        type: 'GET',
        contentType: "application/json",
        success: function(response) {
            document.getElementById('messages').innerHTML = '';
            let oldAuthor = '';
            for (let index = 0; index < response.length; index++) {
                const element = response[index];
                console.log(oldAuthor)
                if (oldAuthor == element['author']) {
                    document.getElementById('messages').innerHTML += `<p>${element['message']}</p>`;
                    oldAuthor = element['author'];
                }
                else {
                    document.getElementById('messages').innerHTML += `<h2>${element['author']}</h2><p>${element['message']}</p>`;
                    oldAuthor = element['author'];
                }
            }
        }
    });
}

function send_message() {
    $.ajax({
        url: 'http://127.0.0.1:5000/api/channels/global/messages',
        type: 'POST',
        contentType: "application/json",
        data: JSON.stringify({text: document.getElementById('message-input').value }),
        success: function(response) {
            document.getElementById('messages').innerHTML = '';
            let oldAuthor = '';
            for (let index = 0; index < response.length; index++) {
                const element = response[index];
                console.log(oldAuthor)
                if (oldAuthor == element['author']) {
                    document.getElementById('messages').innerHTML += `<p>${element['message']}</p>`;
                    oldAuthor = element['author'];
                }
                else {
                    document.getElementById('messages').innerHTML += `<h2>${element['author']}</h2><p>${element['message']}</p>`;
                    oldAuthor = element['author'];
                }
            }
        }
    });
}
// $.ajax({
//     url: 'http://127.0.0.1:5000/',
//     type: 'GET',
//     contentType: "application/json",
//     success: function(response) {
//         //
//     }
// });