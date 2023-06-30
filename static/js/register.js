let loginState = document.getElementById('status');

async function register() {
    $.ajax({
        url: '/auth/register',
        method: 'post',
        data: 
        JSON.stringify({
            username: document.getElementById("username").value,
            password: document.getElementById("password").value,
            email: document.getElementById("email").value
        }),
        contentType: "application/json",
        success: function(data){
            console.log(data)
            loginState.innerText = `Вы зарегистрированы! Идёт вход в клиент`;
            localStorage.setItem("token", data['token']);
        },
        error: function (jqXHR, exception) {
            console.log(jqXHR)
            console.log(exception)
            if (jqXHR.status === 0) {
                loginState.innerText = 'Не подключен, проверьте свой интернет и повторите попытку';
            }
            else if (jqXHR.status == 400) {
                loginState.innerText = "Некоторые поля требуются... Перезагрузите страницу, если эта проблема остаётся, обратитесь в поддержку данного сервера";
            }
            else {
                loginState.innerText = 'Что-то пошло не так...';
                console.error(jqXHR.responseText);
            }
        }
    });
}