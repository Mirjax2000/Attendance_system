
// IIFE - izolace promennych GlobeScope pouze v teto noname funkci
(function () {
    console.log("check_pin.js");
    //
    let timeText = document.getElementById("timeText");
    let pinInput = document.getElementById("pinInput")
    let pinDisplay = document.getElementById("pinDisplay")
    let numpad = document.getElementById("numpad");
    let numpadKeys = numpad.querySelectorAll(".btn")
    let delButton = numpad.querySelector('.c-numpad__text.del');


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


    numpadKeys.forEach(function (element) {


        element.addEventListener("click", function (e) {
            let numVal = this.querySelector(".num").innerText
            pinInput.value += numVal
            pinDisplay.append("*")
            console.log(pinInput.value);
        })

    });

    delButton.addEventListener("click", function () {
        pinDisplay.innerText = pinDisplay.innerText.slice(0, -1);
        pinInput.value = pinInput.value.slice(0, -1);
    });



})();
