const registerServiceWorker = async () =>{
    if ("serviceWorker" in navigator){
        window.addEventListener('load', ()=> {
            try {
                const registration = navigator.serviceWorker.register("sw.js", {
                    scope: "/",
                });
                if (registration.installing){
                    console.log("SW esta instalado")
                } else if (registration.waiting){
                    console.log("SW esta sendo instalado")
                } else if (registration.active){
                    console.log("SW esta ativo")
                }
            } catch (error){
                console.error(`Registro falhou com ${error}`);
            };
        });
        
    }
};

registerServiceWorker();