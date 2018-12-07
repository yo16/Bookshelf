/*
maintenance.js
*/

$(document).ready(function(){
    $("#btnOutputCsv").click(function(){
        doOutputCsv();
    });

    $("#btnInputCsv").click(function(){
        doInputCsv();
    });
});

function doOutputCsv(){
    $("#frmOutputCsv").submit();
}

function doInputCsv(){
    var filePath = $("#fileCsv").val();
    if (filePath.length==0){
        alert('ファイルを選択してください。')
        return;
    }
    var dotPos = filePath.lastIndexOf(".");
    if (dotPos<0){
        alert('CSVファイルを選択してください。')
        $("#fileCsv").val("");
        return;
    }
    var ext = filePath.substr(dotPos);
    if (ext != '.csv'){
        alert('CSVファイルを選択してください。')
        $("#fileCsv").val("");
        return;
    }
    // submit
    $("#frmInputCsv").submit();
}
