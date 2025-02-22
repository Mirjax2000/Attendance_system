
$(function () {

    const employeeLink = $("#employee");
    const employeeSublist = $("#employeeSublist");

    employeeLink.on("click", function (event) {
        event.preventDefault();
        this.dataset.pointer = this.dataset.pointer === "left" ? "down" : "left";
        this.dataset.show = this.dataset.pointer === "down" ? "true" : "false";

        employeeSublist.slideToggle(500);
    });
})

