
// IIFE - izolace promennych GlobeScope pouze v teto noname funkci
(function () {
    console.log("emp_login.js");
    //
    const timeText = document.getElementById("timeText");
    const inputStatus = document.getElementById("statusVal");
    const subBtns = document.querySelectorAll(".L-choose__item")

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

    subBtns.forEach(function (element) {
        element.addEventListener("click", function (e) {
            inputStatus.value = element.dataset.value.trim()
        })
    })
})();
