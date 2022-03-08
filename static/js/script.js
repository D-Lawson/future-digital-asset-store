$(document).ready(function(){
    $(".dropdown").hover(function(){
        var dropdownMenu = $(this).children(".dropdown-menu");
        var hover_css = $(this);
        if(dropdownMenu.is(":visible")){
            hover_css.style.color = "blue";
            dropdownMenu.parent().toggleClass("open");
        }
    });
}); 