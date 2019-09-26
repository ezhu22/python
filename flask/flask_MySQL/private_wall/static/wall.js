$(document).ready(function(){
    $('#email').keyup(function(){
        var data = $("#email").serialize()   // capture all the data in the form in the variable data
        $.ajax({
            method: "POST",   // we are using a post request here, but this could also be done with a get
            url: "/email",
            data: data
        })
        .done(function(res){
             $('#email_msg').html(res)  // manipulate the dom when the response comes back
        })
    })
})

$(document).ready(function(){
    $('#btn_search_friend').click(function(){
        $.ajax({
            method: "POST",   // we are using a post request here, but this could also be done with a get
            url: "/usersearch",
            data: $('#search_email').serialize()
        })
        .done(function(res){
            console.log(res);
             $('#search_friend_msg').html(res);  // manipulate the dom when the response comes back
        })
    return false;
    })
})