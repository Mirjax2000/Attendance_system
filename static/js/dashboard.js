
// IIFE - izolace promennych GlobeScope pouze v teto noname funkci
$(function () {
    console.log('dashboard.js');
    let filterContainerJQ = $(".c-filter");
    filterContainerJQ.children(".c-filter__container").hide(1)

    filterContainerJQ.on("click", function (e) {
        $($(this).children(".c-filter__container")).stop(true, true).slideToggle();
    });


});
