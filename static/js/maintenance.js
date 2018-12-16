/*
maintenance.js
*/

$(document).ready(function(){
    $("#btnOutputCsv").click(function(){
        doOutputCsv();
    });

    $("#btnInputCsv_book").click(function(){
        doInputCsv('book');
    });

    $("#btnInputCsv_pub").click(function(){
        doInputCsv('pub');
    });
});

function doOutputCsv(){
    $("#frmOutputCsv").submit();
}

function doInputCsv(model_name){
    var filePath = $("#fileCsv_"+model_name).val();
    if (filePath.length==0){
        // 未入力
        alert('ファイルを選択してください。');
        return;
    }
    var dotPos = filePath.lastIndexOf(".");
    if (dotPos<0){
        // .がない
        alert('CSVファイルを選択してください。');
        $("#fileCsv_"+model_name).val("");
        return;
    }
    var ext = filePath.substr(dotPos);
    if (ext != '.csv'){
        // csvではない
        alert('CSVファイルを選択してください。');
        $("#fileCsv_"+model_name).val("");
        return;
    }
    // submit
    $("#frmInputCsv_"+model_name).submit();
}
