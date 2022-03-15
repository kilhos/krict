function report_download(click){
    var pk = $(click).siblings('#jobResult_pk').val();
    location.href='/job_result_page/job_result_report/' + pk + '/';
}

$(document).ready(function (){

    let acc = document.getElementsByClassName("accordion");
    let i;
    for(i = 0; i<acc.length; i++){
        acc[i].addEventListener("click", function(){
            this.classList.toggle('active');
            let panel = this.nextElementSibling;
            var icon = $(this).children('i');

            if(panel.style.display == "block"){
                panel.style.display = "none";
                icon.attr('class', 'xi-plus');
            }else{
                panel.style.display = "block";
                icon.attr('class', 'xi-minus');
            }
        })
    }

})