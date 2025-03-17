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

})();
