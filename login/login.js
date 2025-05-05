let client;

window.onload = function(){
    client = google.accounts.oauth2.initCodeClient({
        client_id: '',
        scope: 'openid email profile',
        callback: (tokenResponse) => {
            const jwt = tokenResponse.acess_token;
            console.log("Token de acesso:", jwt)

            fetch('https://www.googleapis.com/oauth2/v3/userinfo',{
                headers: {
                    Authorization:  `Bearer ${jwt}`
                }
            })
            .then(res => res.json())
            .then(user => {
                console.log("User:", user);
                alert(`Bem-vindo, ${user.name}`);
            });
        }

    });

    document.getElementById('google-login-btn').addEventListener('click', () => {
        client.requestAccessToken();
    });
};