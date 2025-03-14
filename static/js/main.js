// IIFE - izolace promennych GlobeScope pouze v teto noname funkci
(function () {
    console.log("main.js");
    //
    let timeText = document.getElementById("timeText");
    let captureBtn = document.getElementById("captureBtn");

    // casova funkce
    function clock() {
        const now = new Date();
        const hours = String(now.getHours()).padStart(2, "0");
        const minutes = String(now.getMinutes()).padStart(2, "0");
        const seconds = String(now.getSeconds()).padStart(2, "0");
        const timeString = `${hours}:${minutes}:${seconds}`;

        timeText.textContent = timeString;
    }
    //spusteni hodin - refresh 1s
    setInterval(clock, 1000);
    // spusteni casove funkce
    clock();

    // Funkce na ziskani hodnoty cookie z prohlizece
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (const cookie of cookies) {
                const trimmedCookie = cookie.trim();

                if (trimmedCookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(
                        trimmedCookie.substring(name.length + 1),
                    );
                    break;
                }
            }
        }
        return cookieValue;
    }
    //

    // spusteni a cekani na vysledek u funkce ve view get_result
    async function get_result() {
        const csrftoken = getCookie("csrftoken");
        captureBtn.disabled = true;


        // Nastavení timeoutu na 5 sekund
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000);
        try {
            const response = await fetch("/app_main/get_result", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken,
                },
                body: JSON.stringify({}),
                signal: controller.signal // Připojení signálu pro zrušení
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();
            console.log("Success:", data);
        } catch (error) {
            if (error.name === 'AbortError') {
                console.error("Request timed out");
            } else {
                console.error("Error:", error);
            }
        } finally {
            clearTimeout(timeoutId);
            captureBtn.disabled = false;

        }
    }
    // click na btn
    captureBtn.addEventListener("click", function (e) {
        e.preventDefault();
        get_result();
    });
})();
