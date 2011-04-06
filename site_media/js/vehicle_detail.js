$(function() {
        $("#edit-vehicle-details a").click(function(e) {
                e.preventDefault();
                $("form").slideToggle('fast');
            });
    });