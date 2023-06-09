let loginState = document.getElementById('status');

async function login() {
    $.ajax({
        url: '/auth/login',
        method: 'post',
        data: 
        JSON.stringify({
            email: document.getElementById("email").value,
            password: document.getElementById("password").value
        }),
        contentType: "application/json",
        success: function(data){
            console.log(data)
            loginState.innerText = `Вы вошли! Идёт вход в клиент`;
            localStorage.setItem("token", data['token']);
        },
        error: function (jqXHR, exception) {
            console.log(jqXHR)
            console.log(exception)
            if (jqXHR.status === 0) {
                loginState.innerText = 'Не подключен, проверьте свой интернет и повторите попытку';
            }
            else if (jqXHR.status == 404) {
                loginState.innerText = "Аккаунт не найден, может быть вы неверно ввели почту или пароль";
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