(function ($) {
    $.extend($.expr[':'], {
        'containsi': $.expr.createPseudo(function (arg) {
            return function (elem) {
                return $(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
            };
        })
    });
})(jQuery);