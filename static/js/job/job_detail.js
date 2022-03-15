document.addEventListener('keydown', function (event) {
    if (event.keyCode === 13 && event.srcElement.type != 'textarea') {
        event.preventDefault();
        if (document.getElementById('smilesResult'))
            drawMolecularStructureBySmileExpression();
    };
},true);

$(document).ready(function (){
    var module_api = $('#api_select').val();
    $('#api_select').val(module_api.split('/')[2]);

    var module_id = $("select[name='module']").val();
    var module_api = $("select[name='moduleApi']");

    $.ajax({
        url : 'module_id',
        data: {
            'module_id' : module_id
        },
        type: 'get',
        dataType: 'json',
        success : function (result){
            if(result.length > 0){
                var str = '';
                for(var i = 0; i < result.length; i++){
                    str += '<option i="' + result[i].module_api_name + '" value="' + result[i].id + '">' + result[i].module_api_name.split('/')[2] + '</option>';
                }
                module_api.html(str);
            }else{
                var result = '<option>해당 모듈에는 존재하는 API가 없습니다.</option>';
                module_api.html(result);
            }
        }
    });
})

function api_select_change(){
    var module_api_name = $("select[name='moduleApi'] option:selected").attr('i');
    $('#api_select').val(module_api_name.split('/')[2]);
    var module_id = $("select[name='moduleApi'] option:selected").attr('value');
    $('#api_select').attr('i', module_id);
}

function module_api_change(){
    var module_id = $("select[name='module']").val();
    var module_api = $("select[name='moduleApi']");

    $.ajax({
        url : 'module_id',
        data: {'module_id' : module_id},
        type: 'get',
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        success : function (result){
            if(result.length > 0){
                var str = '';
                for(var i = 0; i < result.length; i++){
                    str += '<option r="' + i + '" class="api_results" i="' + result[i].module_api_name + '" value="' + result[i].id + '">' + result[i].module_api_name.split('/')[2] + '</option>';
                }
                module_api.html(str);

                $('.api_results').first().attr('selected', true);

                var module_api_name = $("select[name='moduleApi'] option:selected").attr('i');
                $('#api_select').val(module_api_name.split('/')[2]);
            }else{
                var result = '<option>해당 모듈에는 존재하는 API가 없습니다.</option>';
                module_api.html(result);
            }
        }
    });
}

function CancelBtn(){
    if(confirm('JOB 수정을 취소 하시겠습니까?') == true){
        history.go(-1);
    }else{
        return false;
    }
}

function job_Modify_submit() {
    var module_api = $("select[id='moduleApi']");
    var module_api_id = $("input[id='module_api_id_check']");

    if(module_api.val() == null){
        module_api_id.attr('name', 'moduleApi');
    }else{
        module_api.attr('name', 'moduleApi');
    }

    if(confirm('해당 내용으로 JOB을 수정 하시겠습니까?') == true){
        var start_date = $('#sch_date').val();
        var start_time = $('#sch_time').val();

        $('#job_start_dt').attr('value', start_date + " " + start_time);
        $("form[name='job_Modify_form']").submit();
    }else{
        return false;
    }

}

function job_Delete_submit() {
    var job_name = $("input[name='job_name']").val();

    if(confirm(job_name + ' JOB을 삭제 하시겠습니까? \n삭제 시 복구가 불가능 합니다.') == true){
        var form = $("form[name='job_Modify_form']");

        form.attr('action','delete');
        form.submit();
    }else{
        return false;
    }

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

    var smilesInput = document.getElementById('smilesResult').value;

    jsmeApplet.readGenericMolecularInput(smilesInput);

}

function drawMolecularStructureBySmileExpression() {
        var smilesInput = document.getElementById('smilesResult');

        if (smilesInput !== null)
            jsmeApplet.readGenericMolecularInput(smilesInput.value);

}