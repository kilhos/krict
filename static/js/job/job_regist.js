document.addEventListener('keydown', function (event) {
    if (event.keyCode === 13 && event.srcElement.type != 'textarea') {
        event.preventDefault();
        if (document.getElementById('smilesResult'))
            drawMolecularStructureBySmileExpression();
    }
    ;
}, true);

$(document).ready(function () {
    //#$("#module").val("2").prop("selected", true);
   // $("#module").val("2").prop("selected", true);
    var module_id = $("select[name='module']").val();
    var module_api = $("select[name='moduleApi']");

    $.ajax({
        url: 'module_id',
        data: {
            'module_id': module_id
        },
        type: 'get',
        dataType: 'json',
        success: function (result) {
            if (result.length > 0) {
                var str = '';
                for (var i = 0; i < result.length; i++) {
                    str += '<option r="' + i + '" class="api_results" i="' + result[i].module_api_name + '" value="' + result[i].id + '" selected>' + result[i].module_api_name+ '</option>';
                }
                module_api.html(str);
            } else {
                var result = '<option>해당 모듈에는 존재하는 API가 없습니다.</option>';
                module_api.html(result);
            }
        }
    });

    setTimeout(function () {
        $('.api_results').first().attr('selected', true);

        var module_api_name = $("select[name='moduleApi'] option:selected").attr('i');
        $('#api_select').val(module_api_name);
    }, 100);

})

function api_select_change() {
    var module_api_name = $("select[name='moduleApi'] option:selected").attr('i');
    $('#api_select').val(module_api_name);
    var module_id = $("select[name='moduleApi'] option:selected").attr('value');
    $('#api_select').attr('i', module_id);
}

function module_api_change() {

    var module_id = $("select[name='module']").val();
    var module_api = $("select[name='moduleApi']");

    $.ajax({
        url: 'module_id',
        data: {'module_id': module_id},
        type: 'get',
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        success: function (result) {
            if (result.length > 0) {
                var str = '';
                var module_row_num = '';

                for (var i = 0; i < result.length; i++) {
                    str += '<option r="' + i + '" class="api_results"  i="' + result[i].module_api_name + '" value="' + result[i].id + '">' + result[i].module_api_name + '</option>';
                    module_row_num = $('.api_results').attr('r');

                    module_api.html(str);

                    $('.api_results').first().attr('selected', true);

                    var module_api_name = $("select[name='moduleApi'] option:selected").attr('i');
                    $('#api_select').val(module_api_name);
                }

            } else {
                var result = '<option>해당 모듈에는 존재하는 API가 없습니다.</option>';
                module_api.html(result);
            }
        }
    });
}

function noSubmit() {
    if (confirm('Do you want to cancel? \nYour content will not be saved.') == true) {
        history.go(-1);
    } else {
        return false;
    }

}

var start_date;
var start_time;

function job_date() {
    start_date = document.getElementById('sch_date').value;
}

function job_time() {
    start_time = document.getElementById('sch_time').value;
}

function jsmeOnLoad() {

    jsmeApplet = new JSApplet.JSME("appletContainer", "500px", "400px", {
        //optional parameters
        "options": "oldlook,star"
    });

    jsmeApplet.setAfterStructureModifiedCallback(showEvent);

    var patt = /\[([A-Za-z][a-z]?)H?\d*:\d+\]/g; //regexp pattern for numbered atom
    function showEvent(event) {

        var log = document.getElementById("smilesResult");
        log.value = event.src.smiles();
    }

    document.JME = jsmeApplet;

}

function drawMolecularStructureBySmileExpression() {
    var smilesInput = document.getElementById('smilesResult');

    if (smilesInput !== null)
        jsmeApplet.readGenericMolecularInput(smilesInput.value);

}