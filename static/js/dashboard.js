
// IIFE - izolace promennych GlobeScope pouze v teto noname funkci
$(function () {
    console.log('dashboard.js');
    let filterJQ = $(".c-filter");

    filterJQ.children(".c-filter__container").hide(1)

    filterJQ.children(".c-filter__banner").on("click", function (e) {
        $($(this).next(".c-filter__container")).stop(true, true).slideToggle();
    });



});
