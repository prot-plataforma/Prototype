function handleCredentialResponse(response) {
    console.log("Encoded JWT ID token: " + response.credential);
    var tokens = response.credential.split(".");
    var payload = JSON.parse(atob(tokens[1]));  
    console.log(`user id ${payload.sub}`)
    console.log(`user name ${payload.name}`)
    console.log(`user picture ${payload.picture}`)

    
    window.location.href = "http://localhost:5500/home.html"
}