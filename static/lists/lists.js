jQuery(document).ready(function ($) {
    $('input').on('keypress', function () {
        $('.alert-danger').hide();
    });
});