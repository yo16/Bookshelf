/* enter_new_book.js

This source is used in "enter_new_book.html".

2018/11/11 y.ikeda
*/
var GOOGLE_API_BOOK = "https://www.googleapis.com/books/v1/volumes?q=";

$(document).ready(function(){
    $("#btnSearchByISBN").click(function(){
        search_book_by_isbn($("#isbn").val());
    });

    $("#btnAddAuthors").click(function(){
        addAuthor();
    });

    $("#btnRegist").click(function(){
        registBook();
    });

    initialize();
    $("#isbn").val("9784873117584");
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
        $("#publisher").val(js_data["publisher"]);
        $("#isbn").val(js_data["isbn"]);
        $("#img_thumbnail").attr("src", js_data["thumbnail"])
        $("#img_url").val(js_data["image_url"])
    })
    .fail((data)=>{
        console.log("Could not found book info by isbn["+isbn+"].");
        console.log(data);
    })
    .always((data)=>{

    })

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