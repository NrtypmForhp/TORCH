// [= Starting document =]

$(document).ready(function(){
    // Login button
    $(document).on("click", "#login-button", function(){
        if($("#div-login").css("display") == "none"){ // If login div isn't visible
            // Clear inputs
            $("#login-username-input").val("");
            $("#login-password-input").val("");
            // Show login div
            show_hidden_element($("#login-button"), $("#div-login"), "bottom", 13);
            $("#login-username-input").focus(); // Focus on username input
        }else{ // If login div is visible
            // Get username and password
            let username = $("#login-username-input").val().trim();
            let password = $("#login-password-input").val().trim();
            if(username != "" && password != ""){ // If password and username is compiled proceed with login
                enable_disable_operations_in_progress();
                $.ajax({
                    type: "POST",
                    url: "/login",
                    headers: {
                        "Content-type": "application/json",
                        "Accept": "application/json"
                    },
                    data: JSON.stringify({
                        p_username: username,
                        p_password: password
                    }),
                    success: function(response){
                        enable_disable_operations_in_progress();
                        if(response["response"] == "ok"){
                            location.reload();
                        }else if(response["response"] == "error"){
                            location.replace("/error");
                        }
                    },
                    error: function(xhr, status, error){
                        console.error(xhr);
                    }
                })
            }
            $("#div-login").css("display", "none");
        }
    });

    // [= Enter key on input handling =]

    $("#login-username-input, #login-password-input").on("keydown", function(e){ // Login button
        if(e.key == "Enter"){
            $("#login-button").click();
        }
    });

    // [= Click on empty page =]

    $(document).bind("mousedown", function(e){
        if(!$(e.target).is("#div-login") && !$(e.target).parents("#div-login").length > 0 && !$(e.target).is("#login-button")){
            if($("#div-login").css("display") != "none"){
                $("#div-login").css("display", "none");
            }
        }
    });
});