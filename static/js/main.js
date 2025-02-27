// IIFE - izolace promennych GlobeScope pouze v teto noname funkci
(() => {
    console.log('welcome');
    console.log('main.js');
    //
    let timeText = document.getElementById('timeText');
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

    updateTime();

})();
