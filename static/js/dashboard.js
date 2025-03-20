
// IIFE - izolace promennych GlobeScope pouze v teto noname funkci
$(function () {
    console.log('dashboard.js');
    const filterJQ = $(".c-filter");
    const cardList = document.querySelectorAll(".L-departments__list");




    filterJQ.children(".c-filter__container").hide(1)

    filterJQ.children(".c-filter__banner").on("click", function (e) {
        $($(this).next(".c-filter__container")).stop(true, true).slideToggle();
    });

    // zmena datasetu na barvy v c-count cards v L-department layoutu
    cardList.forEach(function (element) {
        let num = 1
        let cards = element.querySelectorAll(".c-count__card__content")

        cards.forEach(function (card) {
            card.dataset.color = `clr_${num}`
            num += 1
            if (num > 10) {
                num = 1
            }
        })
    })

});
