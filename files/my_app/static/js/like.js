function isEmpty( el ){
  return !$.trim(el.html())
}

$(document).ready(function(){
    $(".heart").click(function(){
        let nb_like = $(this).prev('span')
        let result
        if ($(this).attr("src") === "../static/img/heart.png"){
            $(this).attr("src","../static/img/heart-red.png")
            result = "increment"
        } else {
            $(this).attr("src","../static/img/heart.png")
            result = "decrement"
        }

        let id = $(this).attr("id").split("heart")[1];
        let url = "like/" + id
        $.ajax({
            type: "POST",
            url: url,
            data: JSON.stringify({"nb_like": nb_like.text(), "result": result}),
            contentType: 'application/json;charset=UTF-8',
            success: function (){
               if (result === "increment"){
                    if(isEmpty(nb_like)){
                        nb_like.html(parseInt(1, 10))
                    } else {
                        nb_like.html(parseInt(nb_like.html(), 10)+1)
                    }
                } else if (result === "decrement") {
                   if(parseInt(nb_like.html(), 10)-1 === 0){
                       nb_like.html(" ")
                   } else {
                       nb_like.html(parseInt(nb_like.html(), 10)-1)
                   }
                }
            }
        })
    })
})