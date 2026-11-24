// Optional interface help only. No JavaScript stack or click handlers.
if (window.jQuery) {
    jQuery(function ($) {
        $('#st_data').trigger('focus');

        const $top = $('#stack .stack-item.peek');
        if ($top.length) {
            $top.stop(true, true).css('opacity', 0.35).animate({ opacity: 1 }, 350);
        }
    });
}
