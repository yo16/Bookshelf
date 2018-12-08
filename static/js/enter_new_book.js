/* enter_new_book.js

This source is used in "enter_new_book.html".

2018/11/11 y.ikeda
*/

$(document).ready(function(){
    $("#isbn").keydown(function(e){
        if(e.keyCode==13){
            // enter
            search_book_by_isbn($("#isbn").val());
        }
    });
    $("#btnSearchByISBN").click(function(){
        search_book_by_isbn($("#isbn").val());
    });

    $("#isbn").blur(function(){
        // ハイフンが入っていたら除く
        var str_isbn = $("#isbn").val();
        str_isbn = str_isbn.replace(/\-/g, "");
        //console.log(str_isbn);
        $("#isbn").val(str_isbn);

        setPublisherCode();
    });

    $("#btnAddAuthors").click(function(){
        addAuthor();
    });

    $("#btnRegist").click(function(){
        registBook();
    });
    $("#btnReset").click(function(){
        initialize();
    });
    $("#btnDelete").click(function(){
        removeBook();
    });

    initialize();
    //$("#isbn").val("9784873117584");    // ゼロから作るDeep Learning
    //$("#isbn").val("9784584135570");    // 体幹トレーニング
    //$("#isbn").val("9784788925458");    // 統計検定２級
});

/*
search_book_by_isbn
*/
function search_book_by_isbn(isbn){
    ret = {};
    if (isbn == "") {
        console.log("search_book_by_isbn() needs isbn code.")
        return;
    }

    // ハイフンが入っていたら除く
    isbn = isbn.replace(/\-/g, "");
    $("#isbn").val(isbn);

    // isbnコードをチェックする
    $("#spnSearchISBNMessage").empty();
    if (!validate_isbn_code(isbn)) {
        console.log('illigal ISBN code.');
        $("#spnSearchISBNMessage")
            .append($("<br></br>"))
            .append($("<span></span>")
                .addClass("warning_message")
                .text("ISBNコードが不正です。")
            )
        return;
    }

    dispLoading("処理中...");

    // initialie
    initialize();
    $("#isbn").val(isbn)

    // using Ajax
    $.ajax({
        url: "./get_book_with_isbn",
        type: "POST",
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({
            "isbn": isbn
        })
    })
    .done((data) => {
        js_data = JSON.parse(data.ResultSet);
        console.log(js_data);
        $("#title").val(js_data["title"]);
        for(var i=0; i<js_data["authors"].length; i++ ){
            if(i>0){
                addAuthor(js_data["authors"][i]);
            }else{
                $("#authors"+i).val(js_data["authors"][i]);
            }
        }
        $("#publisher_code").val(js_data["publisher_code"]);
        $("#publisher").val(js_data["publisher"]);
        $("#publisher_key_id").val(js_data["publisher_key_id"]);
        //$("#isbn").val(js_data["isbn"]);
        $("#isbn").val(isbn);
        if (js_data["image_url"].length>0){
            $("#img_thumbnail").attr("src", js_data["image_url"])
            $("#spnImageThumbnail").css("display", "");
            $("#image_url").val(js_data["image_url"]);
        }
        $("#comment").val(js_data["comment"]);
        $("#tags").val(js_data["tags"]);
    })
    .fail((data)=>{
        console.log("Could not found book info by isbn["+isbn+"].");
        console.log(data);

        initialize();
        $("#isbn").val(isbn);
    })
    .always((data)=>{
        removeLoading();
    });

    return ret;
};

/*
initialize
*/
function initialize(){
    $("#isbn").val("");
    $("#title").val("");
    $("#authors0").val("");
    var cur_num = $("#num_of_authors").val();
    for( var i=1; i<cur_num; i++ ){
        delAuthor(1);
    }
    $("#publisher").val("");
    $("#publisher_code").val("");
    $("#publisher_key_id").val("");
    $("#img_thumbnail").attr("src","")
    $("#spnImageThumbnail").css("display", "None");
    $("#image_url").val("");
    $("#comment").val("");
    $("#tags").val("");
};

/*
addAuthor
*/
function addAuthor(author){
    var initial_num = $("#num_of_authors").val() - 0;
    var next_num = initial_num + 1;

    $("#num_of_authors").val(next_num);
    $("#btnAddAuthors").before(
        $("<input></input>")
            .attr("type", "text")
            .attr("id", "author"+(next_num-1))
            .attr("name", "author"+(next_num-1))
            .addClass("authors_n")
            .val(author)
    );
    $("#btnAddAuthors").before(
        $("<input></input>")
            .attr("type", "button")
            .attr("id", "btnDelAuthor"+(next_num-1))
            .val("x")
            .attr("onclick", "delAuthor("+(next_num-1)+");")
    );
    $("#btnAddAuthors").before(
        $("<br></br>")
            .attr("id", "brAuthor"+(next_num-1))
    );
    $("#author"+(next_num-1)).focus();
};

/*
delAuthor
*/
function delAuthor(i){
    var initial_num = $("#num_of_authors").val() - 0;
    var next_num = initial_num - 1;

    $("#num_of_authors").val(initial_num-1);

    // i != initial_num-1 の場合は、一番大きなindexでないので、
    // 指示indexより大きなindexを１つずつ繰り下げてから、最後を削除
    for( var j=i; j<next_num; j++){
        $("#author"+j).val($("#author"+(j+1)).val());
    }
    $("#author" + next_num).remove();
    $("#btnDelAuthor" + next_num).remove();
    $("#brAuthor" + next_num).remove();
};

/*
registBook
*/
function registBook(){
    // 入力チェック
    var str_isbn = $("#isbn").val();
    if ((str_isbn.length!=10) & (str_isbn.length!=13)){
        alert("ISBNコードが不正です。");
        $("#isbn")[0].focus();
        return;
    }
    var str_title = $("#title").val();
    if (str_title.length==0){
        alert('タイトルが入力されていません。');
        $("#title")[0].focus();
        return;
    }

    $("#frmRegist").submit();
}

/*
setPublisherCode();
*/
function setPublisherCode(){
    var str_isbn = $("#isbn").val();

    if (str_isbn.length==13){
        top2 = str_isbn.slice(4,6);
        keta = 2;
        if (top2 < 20){
            keta = 2;
        } else if (top2 < 70){
            keta = 3;
        } else if (top2 < 85){
            keta = 4;
        } else if (top2 < 90){
            keta = 5;
        } else if (top2 < 95){
            keta = 6;
        } else {
            keta = 7;
        }
        $("#publisher_code").val(str_isbn.slice(4,4+keta));
    }
}

/*
validate_isbn_code();

Returns:
    true: OK
    false: NG
 */
function validate_isbn_code(isbn){
    if ((isbn.length != 10) && (isbn.length != 13)){
        return false;
    }

    var ary_char = isbn.split("");

    // ISBN-10
    if (isbn.length==10) {
        var tmp = (ary_char[0]-0)*10 + (ary_char[1]-0)*9 + (ary_char[2]-0)*8
            + (ary_char[3]-0)*7 + (ary_char[4]-0)*6 + (ary_char[5]-0)*5
            + (ary_char[6]-0)*4 + (ary_char[7]-0)*3 + (ary_char[8]-0)*2;
        var check_num = 11 - tmp % 11;
        if (check_num==10){
            check_num = 'X';
        }else if (check_num==11){
            check_num = '0';
        }
        if (ary_char[9]!=check_num){
            console.log('check digit is ' + check_num);
            return false;
        }
    }else 
    // ISBN-13
    if (isbn.length==13) {
        var tmp = (ary_char[0]-0)*1
            + (ary_char[1]-0)*3
            + (ary_char[2]-0)*1
            + (ary_char[3]-0)*3
            + (ary_char[4]-0)*1
            + (ary_char[5]-0)*3
            + (ary_char[6]-0)*1
            + (ary_char[7]-0)*3
            + (ary_char[8]-0)*1
            + (ary_char[9]-0)*3
            + (ary_char[10]-0)*1
            + (ary_char[11]-0)*3;
        var check_num = (10 - tmp % 10) % 10;
        if (ary_char[12] != check_num){
            console.log('check digit is ' + check_num);
            return false;
        }
    }

    return true;
}

/*
 removeThisBook()
 */
function removeBook(){
    // 確認
    var res = confirm("この本の情報を削除してもいいですか？\n["+$("#title").val()+"]");
    if (!res){
        console.log("rejected.")
        return;
    }

    // 削除処理
    $("#hdnDelete").val("1");
    $("#frmRegist").submit();
}

// 参考
// https://webllica.com/jquery-now-loading/
/* ------------------------------
 Loading イメージ表示関数
 引数： msg 画面に表示する文言
 ------------------------------ */
 function dispLoading(msg){
    // 引数なし（メッセージなし）を許容
    if( msg == undefined ){
        msg = "";
    }
    // 画面表示メッセージ
    var dispMsg = "<div class='loadingMsg'>" + msg + "</div>";
    // ローディング画像が表示されていない場合のみ出力
    if($("#loading").length == 0){
        $("body").append("<div id='loading'>" + dispMsg + "</div>");
    }
}
   
/* ------------------------------
Loading イメージ削除関数
------------------------------ */
function removeLoading(){
    $("#loading").remove();
}
