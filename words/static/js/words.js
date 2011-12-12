(function($) {

    init = function() {
//        $(".facet").chosen({allow_single_deselect:true});
        $(".category select").chosen({allow_single_deselect:true});

        $("form#search input").keydown(function (e) {
            if (e.keyCode == 13) {
                $("form#search").submit();
                return true;
            }
        });

        $(".reset-facets").click(function(e) {
            $(".facet").prop('checked', false);
//            $(".facet-block").hide();
//            $(".category").val("");
        });
    }

    $(document).ready(init);
})((typeof django !== "undefined" && django.jQuery) || (typeof django === "undefined" && jQuery));


