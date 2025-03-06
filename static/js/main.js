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

    captureBtn.addEventListener("click", function (e) {
        e.preventDefault();
        get_result();
    });

    async function get_result() {
        const csrftoken = getCookie("csrftoken");

        // Nastavení timeoutu na 5 sekund
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000); // 5000 ms = 5 sekund

        try {
            const response = await fetch("app_main/get_result", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken,
                },
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
            clearTimeout(timeoutId); // Uvolnění timeoutu, když požadavek skončí
        }
    }

})();
