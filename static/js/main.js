// IIFE - izolace promennych GlobeScope pouze v teto noname funkci
(() => {
    console.log('main.js');
    //
    let timeText = document.getElementById('timeText');
    let captureBtn = document.getElementById('captureBtn');
    // casova funkce
    function updateTime() {
        const now = new Date();
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const seconds = String(now.getSeconds()).padStart(2, '0');
        const timeString = `${hours}:${minutes}:${seconds}`;

        timeText.textContent = timeString;
    }
    //spusteni hodin - refresh 1s
    setInterval(updateTime, 1000);
    // spusteni casove funkce
    updateTime();
    // funkce na prepnuti flagu na True u capture img
    async function captureImage() {
        try {
            const response = await fetch("/app_main/capture", {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                }
            });
            const data = await response.json();
            console.log(data.message);
            return data;
        } catch (error) {
            console.error("Chyba při zachycení snímku:", error);
            throw error;
        }
    }
    // get result
    let delay = 1000; // Počáteční delay
    let captureResultTimeoutId = null; // Proměnná pro uložení ID timeoutu
    async function captureResult() {
        try {
            const response = await fetch("/app_main/result", {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                }
            });

            const data = await response.json();
            console.log(data.message, data.name);

            if (data.message === "fail") {
                if (delay >= 5000) {
                    console.log("Stopuji další pokusy, maximální delay dosažen.");
                    delay = 1000;
                    captureResultTimeoutId = null; // Reset timeout ID
                    return;
                }
                console.log(`Opakuji request za ${delay / 1000} sekund...`);
                captureResultTimeoutId = setTimeout(captureResult, delay); // Uložíme ID timeoutu
                delay = Math.min(delay * 2, 5000); // Zastaví se na max. 5000 ms
            } else {
                captureResultTimeoutId = null; // Reset timeout ID, pokud je úspěch
            }

            return data;
        } catch (error) {
            console.error("Žádný result:", error);
            captureResultTimeoutId = null; // Reset timeout ID v případě chyby
        }
    }




    // Funkce na ziskani hodnoty cookie z prohlizece
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (const cookie of cookies) {
                const trimmedCookie = cookie.trim();

                if (trimmedCookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(trimmedCookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    // 
    // CSRF fetch na aktivaci snimku
    // endpoint zapina FLAG na TRUE a tim zapne funkci na Capture img
    // zaroven ceka na vysledek porovnani obliceje

    captureBtn.addEventListener("click", function (e) {
        e.preventDefault();

        // Zrušíme timeout, pokud existuje
        if (captureResultTimeoutId !== null) {
            clearTimeout(captureResultTimeoutId);
            console.log("captureResult zastaveno.");
            captureResultTimeoutId = null; // Reset timeout ID
            delay = 1000; // Reset delay
        }

        captureImage()
            .then(function (data) {
                if (data.message === "success") {
                    captureResult();
                }
            })
            .catch(function (error) {
                console.error("Chyba při zachytávání obrázku:", error);
            });
    });
})();
