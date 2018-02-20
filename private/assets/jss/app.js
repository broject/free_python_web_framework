jQuery(window).load(function () {
    /*window events*/
    var _oldfbw = 0, _contentWrapperSizer = function () {
        var width = $(window).width();
        var scrollTop = $(window).scrollTop();
        var mh = $(window).height() < $('body').height() ? $('body').height() : $(window).height();
        var footer_height = $('.main-footer').outerHeight() || 0;
        var h_f_height = $('.main-header').outerHeight() + footer_height;
        var window_height = $(window).height();
        var sidebar_height = $(".sidebar").height() || 0;
        var rh = (window_height - h_f_height);
        $(".content-wrapper").css('min-height', window_height);
        $('.main-sidebar .sidebar').slimScroll({
            height: rh + 'px',
            size: '5px',
            position: 'right',
            color: '#999',
            alwaysVisible: false,
            distance: '0px',
            railVisible: true,
            railColor: '#111',
            railOpacity: 0.1,
            wheelStep: 5,
            allowPageScroll: false,
            disableFadeOut: false
        });
    };
    $(this).on('scroll', function () {
        _contentWrapperSizer();
    }).on('resize', function () {
        _contentWrapperSizer();
        /*
         if (_oldfbw !== $('.social-part').width()) {
         _oldfbw = $('.social-part').width();
         var durl = $('.social-part').attr('data-url');
         var load_url = durl + '/' + _oldfbw + '/' + 500;
         $('#facebook-panel').load(load_url, function () {
         FB.XFBML.parse();
         });
         }*/
    }).trigger('resize');
    setTimeout(function () {
        var cnstr = document.body.className;
        var cns = cnstr.split(' ');
        var arr = [];
        for (var ndx in cns) {
            var cn = cns[ndx];
            if (cn.toString().toLowerCase() !== 'preload') {
                arr.push(cn);
            }
        }
        cnstr = arr.join(' ');
        document.body.className = cnstr;
    }, 500);
});
(function ($) {
    $.fn.readMoreNews = function () {
        $(this).click(function () {
            var ul = $('#cat-news-list');
            var p = parseInt(ul.find('li[data-page]').last().attr('data-page')) + 1;
            var u = $(this).attr('data-url');
            $.ajax({
                url: u,
                data: { p: p },
                type: 'POST',
                dataType: 'html',
                success: function (data, textStatus, jqXHR) {
                    var arts = $(data);
                    ul.append(arts);
                    var pp = parseInt(ul.find('li[data-page]').last().attr('data-page')) + 1;
                    if (pp === p) {
                        $('.read-more').remove();
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    alert(errorThrown);
                }
            });
        });
    };
    $.fn.homeTopSlider = function (l) {
        var slide_length = l;
        var slide_content_next = function (curr, toSlid) {
            var cch = $('.carousel-content').height();
            $('.carousel-content .sitem:eq(' + curr + ')')
                .css({ 'opacity': 1, 'z-index': 10000, 'margin-top': '0px' })
                .animate({
                    'opacity': 0, 'z-index': 1000, 'margin-top': '-50px'
                }, 800);
            if (toSlid >= slide_length) {
                toSlid = 0;
            }
            $('.carousel-content .sitem:eq(' + toSlid + ')')
                .css({ 'opacity': 0, 'z-index': 1000, 'margin-top': (cch) + 'px' })
                .animate({
                    'opacity': 1, 'z-index': 10000, 'margin-top': '0px'
                }, 800);
        };
        var slide_content_prev = function (curr, toSlid) {
            var cch = $('.carousel-content').height();
            $('.carousel-content .sitem:eq(' + curr + ')')
                .css({ 'opacity': 1, 'z-index': 10000, 'margin-top': '0px' })
                .animate({
                    'opacity': 0, 'z-index': 1000, 'margin-top': '150px'
                }, 800);
            if (toSlid < 0) {
                toSlid = slide_length - 1;
            }
            $('.carousel-content .sitem:eq(' + toSlid + ')')
                .css({ 'opacity': 0, 'z-index': 1000, 'margin-top': (-1 * cch) + 'px' })
                .animate({
                    'opacity': 1, 'z-index': 10000, 'margin-top': '0px'
                }, 800);
        };
        var carousel_obj = $("#carousel");
        var carousel = carousel_obj.carousel({
            interval: 5000
        });
        carousel.on("slid.bs.carousel", function () {
            var all = carousel.find('.item'),
                active = carousel.find('.active'),
                slidTo = all.index(active);
            $('.slider-dots .dot:eq(' + slidTo + ')').addClass('sel');
            /*console.log("Slid - Slid To: " + slidTo);*/
        });
        carousel.on("slide.bs.carousel", function (e) {
            var all = carousel.find('.item'),
                active = carousel.find('.active'),
                slidFrom = all.index(active);
            $('.slider-dots .dot:eq(' + slidFrom + ')').removeClass('sel');
            /*console.log("Slide - Slid From: " + slidFrom);*/
            var toSlid = carousel_obj.data('selected-ndx');
            carousel_obj.removeData('selected-ndx');

            var command = (toSlid > slidFrom || e.direction === 'left') ? 1 : -1;
            if (command === 1)
                slide_content_next(slidFrom, toSlid !== undefined ? toSlid : slidFrom + 1);
            else
                slide_content_prev(slidFrom, toSlid !== undefined ? toSlid : slidFrom - 1);
        });
        $('.slider-dots').find('.dot').click(function (e) {
            e.preventDefault();
            $(this).addClass('sel');
            var all = carousel.find('.item'),
                active = carousel.find('.active'),
                slidFrom = all.index(active);
            var ndx = parseInt($(this).attr('data-index')) - 1;
            if (slidFrom !== ndx) {
                carousel_obj.data('selected-ndx', ndx);
                carousel.carousel(ndx);
            }
        });
        $('.slider-prev').click(function (e) {
            e.preventDefault();
            carousel.carousel('prev');
        });
        $('.slider-next').click(function (e) {
            e.preventDefault();
            carousel.carousel('next');
        });
    };
    $.fn.popupAboutUsInfo = function () {
        $(this).click(function () {
            var mh = $(window).height() < $('body').height() ? $('body').height() : $(window).height();
            $('#popup-about-us-info').removeClass('hidden').height(mh)
                .find('.about-us-info-box').height(mh - 100)
                .find('.content').height(mh - 500);
        });
        $('#popup-about-us-info').click(function (e) {
            if (e.target === this) {
                $(this).addClass('hidden');
            }
        });
        $('#popup-about-us-info .modal-close').click(function () {
            $('#popup-about-us-info').addClass('hidden');
        });
    };
    $.fn.toscroll = function () {
        var t = $(this).offset().top - 16;
        if (t <= 0) {
            t = 0;
        }
        $('html, body').animate({
            scrollTop: t + 'px'
        }, 'slow');
        return this;/*for chaining...*/
    };
    $(document).ready(function () {
        $('.sidebar-menu > .menuitem').click(function () {
            if (!$('body').hasClass('sidebar-collapse')) {
                var th = $(this);
                var submenu = th.find('.menuitem-submenu');
                submenu_h = submenu.height();
                if (th.hasClass('active')) {
                    submenu.animate({ height: 0 }, 500, function () {
                        th.removeClass('active');
                        submenu.css('height', 'auto');
                    });
                } else {
                    th.addClass('active');
                    submenu.css('height', '0px');
                    submenu.animate({ height: submenu_h }, 500);
                }
            }
        });
        $('#toggler-sidebar').click(function () {
            $('body').toggleClass('sidebar-collapse');
            if ($('body').hasClass('sidebar-collapse')) {
                $('.sidebar-menu > .menuitem').each(function () {
                    $(this).removeClass('active');
                });
            }
        });
        var list_object = $('#std-table');
        if (typeof list_object.DataTable === 'function') {
            var table = list_object.DataTable({
                "classes": { "sFilterInput": 'form-control' },
                "language": { "search": "Шүүлт: _INPUT_" },
                "info": false,
                "paging": false,
                "lengthChange": false,
                "searching": false
            });
            list_object.data('table', table);
        }
        $('#search-q').keydown(function (e) {
            var u = $(this).attr('data-url');
            var q = $(this).val();
            if (e.keyCode === 13) {
                window.location.href = u + '?q=' + q;
            }
        });
    });
})(jQuery);