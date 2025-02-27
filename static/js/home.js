// IIFE - izolace promennych GlobeScope pouze v teto noname funkci
(() => {
    // by ID
    const employeesBtn = document.getElementById("employeesBtn");
    const content = document.getElementById("content");
    const navMenu = document.getElementById("navigationPanel");
    const employeeSublistJQ = $("#employeesSublist"); /* pro JQ slide */

    const loginBtn = document.getElementById("loginBtn");
    // const registrBtn = document.getElementById("registBtn");
    const loginForm = document.getElementById("loginForm");
    const loginClose = document.getElementById("loginClose");
    // Nodelists
    const fetchLinks = navMenu.querySelectorAll(".fetch-url");
    // Arrays
    const sublistLinksArray = Array.from(navMenu.querySelectorAll(".sublink"));
    // settings
    const animationTime = 200;
    // 
    // --- Fetch function ---
    function loadContent(url) {
        fetch(url)
            .then(function (response) {
                if (!response.ok) {
                    throw new Error("Síťová odpověď nebyla OK");
                }
                return response.text();
            })
            .then(function (html) {
                content.innerHTML = html;// html injektaz
            })
            .catch(function (error) {
                console.error("Chyba:", error);
            });
    }
    // prace s fetchlinkama - jako Nodelist
    fetchLinks.forEach(function (element) {
        // hlavni nacitaci stranka
        if (element.classList.contains("active_link")) {
            loadContent(element.dataset.url);
        }

        element.addEventListener('click', function (e) {
            e.preventDefault()
            // remove active_link Class
            fetchLinks.forEach(function (link) {
                link.classList.remove("active_link")
            })
            // pridej classu activ_link na link
            this.classList.add("active_link")
            // spust fetch funkci s dataset url parametrem
            loadContent(this.dataset.url);

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

    // logovani z loging rollety 
    loginBtn.addEventListener("click", function (e) {
        loginForm.dataset.show = "show"
    })

    // registrBtn.addEventListener("click", function (e) {
    //     registrForm.dataset.show = "show"
    // })

    loginClose.addEventListener("click", function (e) {
        loginForm.dataset.show = "hide"
    })
    // 
})();
