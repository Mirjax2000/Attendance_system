
$(function () {

    const employeeLink = $("#employee");
    const employeeSublist = $("#employeeSublist");
    const content = $("#content");
    const navMenu = $(".l-nav");
    const navlinks = navMenu.find(".ajax-link");


    employeeLink.on("click", function (e) {
        e.preventDefault();
        this.dataset.pointer = this.dataset.pointer === "left" ? "down" : "left";

        if (this.dataset.pointer === "down") {
            employeeSublist.stop().slideDown(500);
        } else {
            employeeSublist.stop().slideUp(500);
        }
    });

    navlinks.on('click', function (e) {
        e.preventDefault();

        const url = $(this).data('url');

        $.ajax({
            url: url,
            method: 'GET',
            success: function (html) {
                content.html(html);
            },
            error: function (xhr, status, error) {
                console.error('Chyba:', error);
            }
        });
    });
})

