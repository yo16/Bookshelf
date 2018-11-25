/* enter_new_book.js

This source is used in "enter_new_book.html".

2018/11/11 y.ikeda
*/
var GOOGLE_API_BOOK = "https://www.googleapis.com/books/v1/volumes?q=";

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
        setPublisherCode();
    });

    $("#btnAddAuthors").click(function(){
        addAuthor();
    });

    $("#btnRegist").click(function(){
        registBook();
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
        if (js_data["image_url"].length>0){
            $("#img_thumbnail").attr("src", js_data["image_url"]);
            $("#image_url").val(js_data["image_url"]);
        }
        $("#comment").val(js_data["comment"]);
        $("#tags").val(js_data["tags"]);
    })
    .fail((data)=>{
        console.log("Could not found book info by isbn["+isbn+"].");
        console.log(data);
    })
    .always((data)=>{

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
    $("#img_thumbnail").attr("src","");
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
