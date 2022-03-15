$(document).ready(function () {
    var display_content = $('#chk_display_Search').val();
    var SearchType = $('#SearchType').val();

    if (SearchType == 'job_status') {

        if (display_content.length != 2) {

            var dis_cons = display_content.split(',');
            var dis_cons_len = dis_cons.length;

            if (dis_cons_len > 0) {
                for (var i = 0; i < dis_cons_len; i++) {
                    var idx_first = dis_cons[i].indexOf("'");
                    var idx_last = dis_cons[i].lastIndexOf("'");

                    var dis_cons_result = dis_cons[i].substring(idx_first + 1, idx_last);
                    var dis_parent = $("label[class='" + dis_cons_result + "']");
                    var dis_child = dis_parent.children();

                    dis_child.attr('checked', true);
                }
            }
        }

    }

});

function SearchSelect() {
    var SearchType = $('#SearchType').val();
    var SearchContent = $('.SearchContent');
    var Waiting = $('.Waiting');
    var Running = $('.Running');
    var Completed = $('.Completed');
    var Fail = $('.Fail');
    var Stop = $('.Stop');

    if (SearchType == 'job_name') {
        SearchContent.attr('hidden', false);
        Waiting.attr('hidden', true);
        Running.attr('hidden', true);
        Completed.attr('hidden', true);
        Fail.attr('hidden', true);
        Stop.attr('hidden', true);

    } else if (SearchType == 'job_status') {
        SearchContent.attr('hidden', true);
        Waiting.attr('hidden', false);
        Running.attr('hidden', false);
        Completed.attr('hidden', false);
        Fail.attr('hidden', false);
        Stop.attr('hidden', false);
    }

}

function page_move(click) {
    var SearchContent = $('.SearchContent').val();
    var SearchType = $('#SearchType').val();
    var atag = $(click);
    var display_content = $('#chk_display_Search').val();

    if (SearchType == 'job_name') {
        if (SearchContent == '') {
            atag.attr('href', '?page=' + atag.text());
            atag.click();
        } else {
            atag.attr('href', '?page=' + atag.text() + '&SearchType=' + SearchType + '&SearchContent=' + SearchContent);
            atag.click();
        }
    } else {
        var dis_cons = display_content.split(',');
        var dis_cons_len = dis_cons.length;
        var dis_result_con = new Array();

        for (var i = 0; i < dis_cons_len; i++) {
            var idx_first = dis_cons[i].indexOf("'");
            var idx_last = dis_cons[i].lastIndexOf("'");

            var dis_cons_result = dis_cons[i].substring(idx_first + 1, idx_last);
            dis_result_con[i] = dis_cons_result;
        }

        atag.attr('href', '?page=' + atag.text() + '&SearchType=' + SearchType + '&SearchStatus=' + dis_result_con);
        atag.click();
    }

}

function page_previous(click) {
    var SearchContent = $('.SearchContent').val();
    var SearchType = $('#SearchType').val();
    var atag = $(click);
    var atagByPage = atag.attr('i');
    var display_content = $('#chk_display_Search').val();

    if (SearchType == 'job_name') {
        if (SearchContent == '') {
            atag.attr('href', '?page=' + atagByPage);
            atag.click();
        } else {
            atag.attr('href', '?page=' + atagByPage + '&SearchType=' + SearchType + '&SearchContent=' + SearchContent);
            atag.click();
        }
    } else {
        var dis_cons = display_content.split(',');
        var dis_cons_len = dis_cons.length;
        var dis_result_con = new Array();

        for (var i = 0; i < dis_cons_len; i++) {
            var idx_first = dis_cons[i].indexOf("'");
            var idx_last = dis_cons[i].lastIndexOf("'");

            var dis_cons_result = dis_cons[i].substring(idx_first + 1, idx_last);
            dis_result_con[i] = dis_cons_result;
        }

        atag.attr('href', '?page=' + atagByPage + '&SearchType=' + SearchType + '&SearchStatus=' + dis_result_con);
        atag.click();
    }
}

function page_next(click) {
    var SearchContent = $('.SearchContent').val();
    var SearchType = $('#SearchType').val();
    var atag = $(click);
    var atagByPage = atag.attr('i');
    var display_content = $('#chk_display_Search').val();

    if (SearchType == 'job_name') {
        if (SearchContent == '') {
            atag.attr('href', '?page=' + atagByPage);
            atag.click();
        } else {
            atag.attr('href', '?page=' + atagByPage + '&SearchType=' + SearchType + '&SearchContent=' + SearchContent);
            atag.click();
        }
    } else {
        var dis_cons = display_content.split(',');
        var dis_cons_len = dis_cons.length;
        var dis_result_con = new Array();

        for (var i = 0; i < dis_cons_len; i++) {
            var idx_first = dis_cons[i].indexOf("'");
            var idx_last = dis_cons[i].lastIndexOf("'");

            var dis_cons_result = dis_cons[i].substring(idx_first + 1, idx_last);
            dis_result_con[i] = dis_cons_result;
        }

        atag.attr('href', '?page=' + atagByPage + '&SearchType=' + SearchType + '&SearchStatus=' + dis_result_con);
        atag.click();
    }
}

function page_first(click) {
    var SearchContent = $('.SearchContent').val();
    var SearchType = $('#SearchType').val();
    var atag = $(click);
    var atagByPage = atag.attr('i');
    var display_content = $('#chk_display_Search').val();

    if (SearchType == 'job_name') {
        if (SearchContent == '') {
            atag.attr('href', '?page=' + atagByPage);
            atag.click();
        } else {
            atag.attr('href', '?page=' + atagByPage + '&SearchType=' + SearchType + '&SearchContent=' + SearchContent);
            atag.click();
        }
    } else {
        var dis_cons = display_content.split(',');
        var dis_cons_len = dis_cons.length;
        var dis_result_con = new Array();

        for (var i = 0; i < dis_cons_len; i++) {
            var idx_first = dis_cons[i].indexOf("'");
            var idx_last = dis_cons[i].lastIndexOf("'");

            var dis_cons_result = dis_cons[i].substring(idx_first + 1, idx_last);
            dis_result_con[i] = dis_cons_result;
        }

        atag.attr('href', '?page=' + atagByPage + '&SearchType=' + SearchType + '&SearchStatus=' + dis_result_con);
        atag.click();
    }
}

function page_last(click) {
    var SearchContent = $('.SearchContent').val();
    var SearchType = $('#SearchType').val();
    var atag = $(click);
    var atagByPage = atag.attr('i');
    var display_content = $('#chk_display_Search').val();

    if (SearchType == 'job_name') {
        if (SearchContent == '') {
            atag.attr('href', '?page=' + atagByPage);
            atag.click();
        } else {
            atag.attr('href', '?page=' + atagByPage + '&SearchType=' + SearchType + '&SearchContent=' + SearchContent);
            atag.click();
        }
    } else {
        var dis_cons = display_content.split(',');
        var dis_cons_len = dis_cons.length;
        var dis_result_con = new Array();

        for (var i = 0; i < dis_cons_len; i++) {
            var idx_first = dis_cons[i].indexOf("'");
            var idx_last = dis_cons[i].lastIndexOf("'");

            var dis_cons_result = dis_cons[i].substring(idx_first + 1, idx_last);
            dis_result_con[i] = dis_cons_result;
        }

        atag.attr('href', '?page=' + atagByPage + '&SearchType=' + SearchType + '&SearchStatus=' + dis_result_con);
        atag.click();
    }
}