/*
maintenance.js
*/

$(document).ready(function(){
    $("#btnOutputCsv").click(function(){
        do_output_csv();
    });
});

function do_output_csv(){
    $("#frmOutputCsv").submit();
}
