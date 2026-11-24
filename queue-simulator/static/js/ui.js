// Optional interface help only. Queue operations are handled by Flask.
if (window.jQuery) {
    jQuery(function ($) {
        $('#queue_value').trigger('focus');

        const $front = $('#queue .queue-item.peek');
        if ($front.length) {
            $front.stop(true, true).css('opacity', 0.35).animate({ opacity: 1 }, 350);
        }
    });
}
