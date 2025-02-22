
$(function () {

    const employeeLink = $("#employee");
    const employeeSublist = $("#employeeSublist");
    const content = $("#content");
    const navMenu = $(".l-nav");
    const navlinks = navMenu.find('a')


    employeeLink.on("click", function (event) {
        event.preventDefault();
        this.dataset.pointer = this.dataset.pointer === "left" ? "down" : "left";
        this.dataset.show = this.dataset.pointer === "down" ? "true" : "false";

        employeeSublist.slideToggle(500);
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

