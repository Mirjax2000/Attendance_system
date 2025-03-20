
// IIFE - izolace promennych GlobeScope pouze v teto noname funkci
(function () {
    console.log("check_pin.js");
    //
    const timeText = document.getElementById("timeText");
    const pinInput = document.getElementById("pinInput");
    const pinDisplay = document.getElementById("pinDisplay");
    const numpad = document.getElementById("numpad");
    const numpadKeys = numpad.querySelectorAll(".btn");
    const delPin = document.getElementById("delPin");
    const enterPin = document.getElementById("enterPin");


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

    // tlacitka na numpadu
    numpadKeys.forEach(function (element) {

        element.addEventListener("click", function (e) {
            // cte text v HTML elementu, tlacitko
            let numVal = this.querySelector(".num").textContent

            // pokud nemam 4 znaky v Pinu
            if (pinInput.value.length <= 3) {
                pinInput.value += numVal.trim()
                pinDisplay.append("*")
                enterPin.dataset.show = "hide"
                if (pinInput.value.length === 4) {
                    enterPin.dataset.show = "show"
                    numpadKeys.forEach(function (item) {
                        item.dataset.show = "hide"
                    })
                }
            }
        })
    });

    delPin.addEventListener("click", function () {
        pinDisplay.textContent = pinDisplay.textContent.slice(0, -1);
        pinInput.value = pinInput.value.slice(0, -1);
        enterPin.dataset.show = "hide"
        numpadKeys.forEach(function (item) {
            item.dataset.show = "show"
        })
    });



})();
