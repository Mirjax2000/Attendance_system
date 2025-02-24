(() => {
    const employeesBtn = document.getElementById("employeesBtn");
    const employeesSublist = document.getElementById("employeesSublist");
    // const employeeSublistJQ = $("#employeeSublist");
    // const SublistLinks = navMenu.querySelectorAll(".sublink");

    const content = document.getElementById("content");
    const navMenu = document.getElementById("navigationPanel");
    const fetchLinks = navMenu.querySelectorAll(".fetch-url");
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

    // employeesBtn.addEventListener("click", function (e) {
    //     e.preventDefault()
    // })

    // employeeLink.on("click", function (e) {
    //     e.preventDefault();
    //     let $this = $(this);
    //     // Toggler datasetu
    //     if ($this.attr("data-pointer") === "down") {
    //         $this.attr("data-pointer", "left");
    //         Sublist.stop(true, true).slideUp(200)
    //     } else {
    //         $this.attr("data-pointer", "down");
    //         Sublist.stop(true, true).slideDown(200)
    //     }
    // });

    // navLinks.on("click", function (e) {
    //     e.preventDefault();
    //     let $this = $(this);

    //     navLinks.removeClass("active_link");
    //     $this.addClass("active_link");

    //     if (!$this.is(employeeLink) && !$this.is(SublistLinks)) {
    //         Sublist.stop(true, true).slideUp(animationTime);
    //         employeeLink.data("pointer", "left").attr("data-pointer", "left");
    //     }

    //     loadContent(this.dataset.url);
    // });
})();
