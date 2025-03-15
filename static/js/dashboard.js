
// IIFE - izolace promennych GlobeScope pouze v teto noname funkci
$(function () {
    console.log('dashboard.js');
    let filterJQ = $(".c-filter");

    filterJQ.children(".c-filter__container").hide(1)

    filterJQ.children(".c-filter__banner").on("click", function (e) {
        $($(this).next(".c-filter__container")).stop(true, true).slideToggle();
    });


    document.getElementById("myForm").addEventListener("submit", async function (e) {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        try {
            const response = await fetch("/dashboard/save_vector_to_db", {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken,  // Ochrana proti CSRF
                },
                body: formData,  
            });

            if (!response.ok) {
                throw new Error("Chyba při odesílání dat");
            }

            const data = await response.json();

        } catch (error) {
            console.error("Error:", error);
        }
    });


});
