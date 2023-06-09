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
            loginState.innerText = `Вы вошли! Вот ваш токен: ${data['token']} (Заходите через другие клиенты, наш не доделан). Не отправляйте его никому! Вы же не хотите, чтобы кто-то от вашего имени что-то сделал?`;
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
            else if (jqXHR.status == 500) {
                loginState.innerText = "Что-то пошло не так на сервере";
            }
            else {
                loginState.innerText = 'Что-то пошло не так...';
                console.error(jqXHR.responseText);
            }
        }
    });
}