
(() => {
    const employeesBtn = document.getElementById("employeesBtn");
    const content = document.getElementById("content");
    const navMenu = document.getElementById("navigationPanel");
    const employeeSublistJQ = $("#employeesSublist");
    // arrays
    const fetchLinks = navMenu.querySelectorAll(".fetch-url");
    const SublistLinks = navMenu.querySelectorAll(".sublink");
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

    fetchLinks.forEach(function (element) {
        const url = element.dataset.url;

        if (element.classList.contains("active_link")) {
            loadContent(url);
        }
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

    fetchLinks.forEach(function (element) {
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
        })
    })




    // if (!$this.is(employeeLink) && !$this.is(SublistLinks)) {
    //     Sublist.stop(true, true).slideUp(animationTime);
    //     employeeLink.data("pointer", "left").attr("data-pointer", "left");
    // }

})();
