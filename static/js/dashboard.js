// IIFE - izolace promennych GlobeScope pouze v teto noname funkci
(() => {
    console.log('dashboard.js');
    // by ID
    const employeesBtn = document.getElementById("employeesBtn");
    const employeeSublistJQ = $("#employeesSublist"); /* pro JQ slide */

    const animationTime = 200;


    // rozbaleni sublistu employeesBtn
    employeesBtn.addEventListener("click", function (e) {
        e.preventDefault()
        let datasetValue = this.dataset.pointer
        // dataset toggler
        if (datasetValue === "down") {
            this.dataset.pointer = "left";
            employeeSublistJQ.stop(true, true).slideUp(animationTime);
        } else {
            this.dataset.pointer = "down";
            employeeSublistJQ.stop(true, true).slideDown(animationTime);
        }
    })
})();
