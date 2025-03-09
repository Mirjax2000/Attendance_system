// IIFE - izolace promennych GlobeScope pouze v teto noname funkci
(() => {
    console.log('dashboard.js');
    // by ID
    const employeesBtn = document.getElementById("employeesBtn");
    const navMenu = document.getElementById("navigationPanel");
    const employeeSublistJQ = $("#employeesSublist"); /* pro JQ slide */

    // Nodelists
    const fetchLinks = navMenu.querySelectorAll(".fetch-url");
    // Arrays
    const sublistLinksArray = Array.from(navMenu.querySelectorAll(".sublink"));
    // settings
    const animationTime = 200;

    // prace s fetchlinkama - jako Nodelist
    fetchLinks.forEach(function (element) {
        // hlavni nacitaci stranka

        element.addEventListener('click', function (e) {
            e.preventDefault()
            // remove active_link Class
            fetchLinks.forEach(function (link) {
                link.classList.remove("active_link")
            })
            // pridej classu activ_link na link
            this.classList.add("active_link")

            if (this !== employeesBtn && !sublistLinksArray.includes(this)) {
                employeeSublistJQ.stop(true, true).slideUp(animationTime);
                employeesBtn.dataset.pointer = "left";
            }
        })
    })
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
