
$(function () {

    const employeeLink = $("#employee");
    const employeeSublist = $("#employeeSublist");
    const content = $("#content");
    const navMenu = $(".l-nav");
    const navlinks = navMenu.find(".ajax-link");


    employeeLink.on("click", function (e) {
        e.preventDefault();
        const animationTime = 200
        this.dataset.pointer = this.dataset.pointer === "left" ? "down" : "left";

        if (this.dataset.pointer === "down") {
            employeeSublist.stop(true, true).slideDown(animationTime);
        } else {
            employeeSublist.stop(true, true).slideUp(animationTime);
        }
    });

    navlinks.on('click', function (e) {
        e.preventDefault();
        let $this = $(this);

        navlinks.removeClass('active_link');
        $this.addClass('active_link')

        const url = $this.data('url');


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

