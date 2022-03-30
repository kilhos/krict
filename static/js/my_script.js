let jsmeApplet;

$(document).ready(function () {
    // var module_id = $("select[name='module']").val();
    // var module_api = $("select[name='moduleApi']");
    //
    // $.ajax({
    //     url: 'module_id',
    //     data: {
    //         'module_id': module_id
    //     },
    //     type: 'get',
    //     dataType: 'json',
    //     success: function (result) {
    //         if (result.length > 0) {
    //             var str = '';
    //             for (var i = 0; i < result.length; i++) {
    //                 str += '<option r="' + i + '" class="api_results" i="' + result[i].module_api_name + '" value="' + result[i].id + '" selected>' + result[i].module_api_name + '</option>';
    //             }
    //             module_api.html(str);
    //         } else {
    //             var result = '<option>해당 모듈에는 존재하는 API가 없습니다.</option>';
    //             module_api.html(result);
    //         }
    //     }
    // });
    //
    // setTimeout(function () {
    //     $('.api_results').first().attr('selected', true);
    //
    //     var module_api_name = $("select[name='moduleApi'] option:selected").attr('i');
    //     $('#api_select').val(module_api_name);
    // }, 100);
});

function drawMolecularStructureBySmileExpression() {
    const smilesInput = document.getElementById('smilesResult');

    if (smilesInput !== null)
        jsmeApplet.readGenericMolecularInput(smilesInput.value);

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