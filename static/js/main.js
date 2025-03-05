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

    setInterval(updateTime, 1000);
    // spusteni casove funkce
    updateTime();

    function captureImage() {
        fetch("/app_main/capture", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            }
        })
            .then(response => response.json())
            .then(data => console.log(data.message))
            .catch(error => console.error("Chyba při zachycení snímku:", error));
    }

    // CSRF fetch na aktivaci snimku
    // endpoint zapina FLAG na TRUE a tim zapne funkci na Capture img
    captureBtn.addEventListener("click", function () {
        captureImage(); // Volani funkce captureImage pri kliknuti na tlacitko
        captureFace(); // Volani funkce captureFace pri kliknuti na tlacitko
    });

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

    function captureFace() {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000); // Timeout po 10s

        fetch('app_main/face_recon', {
            method: 'POST',
            signal: controller.signal // Napojení na abort signal
        })
            .then(response => response.json())
            .then(data => {
                clearTimeout(timeoutId); // Pokud odpověď přišla včas, zruší timeout

                if (data.status === 'success') {
                    console.log(`Rozpoznán: ${data.message}`);
                } else {
                    console.log('nerozpoznan');
                }
            })
            .catch(error => {
                if (error.name === 'AbortError') {
                    console.error('Požadavek byl zrušen kvůli timeoutu.');
                } else {
                    console.error('Chyba při komunikaci se serverem:', error);
                }
            });
    }

})();
