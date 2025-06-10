// [= TORCH main javascript file =]

// [= Main functions =]

// Global variables
let language_obj = {}; // Language strings container

function enable_disable_operations_in_progress(){ // Function to show or hide operations in progress div
    if($("#div-operations-in-progress").css("display") == "none"){
        $("#div-operations-in-progress").css("display", "block");
    }else{
        $("#div-operations-in-progress").css("display", "none");
    }
}

function restore_commas(str){ // Function to restore commas in a string
                            // Directly connected to replace_commas function in modules/main_module.py
    let new_str = str.replaceAll("@single_quote@", "'").replaceAll("@double_quote@", '"');
    return new_str;
}

function show_hidden_element(e, hidden_element, position="none", padding_from_right=0){ // Function to show hidden elements
    let pos_val = {};
    $(hidden_element).css("display", "block");
    if(position == "none"){ // If position is not specified calculate position dinamically
        if((e.pageX + $(hidden_element)[0].scrollWidth) >= $(window).width() && (e.pageY + $(hidden_element)[0].scrollHeight) >= $(window).height()){
            pos_val["top"] = (e.pageY - $(hidden_element)[0].scrollHeight) + "px";
            pos_val["left"] = (e.pageX - $(hidden_element)[0].scrollWidth) + "px";
        }else if((e.pageX + $(hidden_element)[0].scrollWidth) >= $(window).width() && (e.pageY + $(hidden_element)[0].scrollHeight) < $(window).height()){
            pos_val["top"] = e.pageY + "px";
            pos_val["left"] = (e.pageX - $(hidden_element)[0].scrollWidth) + "px";
        }else if((e.pageX + $(hidden_element)[0].scrollWidth) < $(window).width() && (e.pageY + $(hidden_element)[0].scrollHeight) > $(window).height()){
            pos_val["top"] = (e.pageY - $(hidden_element)[0].scrollHeight) + "px";
            pos_val["left"] = e.pageX + "px";
        }else{
            pos_val["top"] = e.pageY + "px";
            pos_val["left"] = e.pageX + "px";
        }
    }
    if(position == "bottom"){ // Set hidden element at the bottom of the selected element
        $element = $(e);
        let element_right = parseInt($element.offset().left) + $element.width(); // Calculate right position of the clicked element
        pos_val["top"] = ($element.offset().top + $element.outerHeight(true)) + "px";
        if((parseInt($element.offset().left) + parseInt($(hidden_element).width())) >= $(window).width()){ // If hidden element goes out of window to right
            pos_val["left"] = (element_right - parseInt($(hidden_element).width()) - padding_from_right) + "px";
        }else{ // If hidden element not goes out of window to right
            pos_val["left"] = $element.offset().left + "px";
        }
    }
    $(hidden_element).css({ // Set position
        "top": pos_val["top"],
        "left": pos_val["left"]
    });
}

// Quick alert
let quick_alert_timeout;

function close_quick_alert(){
    $("#div-quick-alert").css("display", "none");
}
function quick_alert(text="", time=5){
    let timeout = time * 1000; // Set timeout in milliseconds
    $("#div-quick-alert").html(`<p class='main-text-white'>${text}</p>`); // Set quick alert text
    clearTimeout(quick_alert_timeout); // Stop quick alert timeout if it's in execution
    quick_alert_timeout = setTimeout(close_quick_alert, timeout); // Start quick alert timeout
    $("#div-quick-alert").css("display", "block"); // Display div
}

// Alert
let alert_parameters = {};

function create_alert({title, text, enable_ok_button = false, enable_input = false, input_placeholder = "", parameters = {}}){
    // Cleaning
    $("#alert-input").val("").attr("placeholder", input_placeholder);

    $("#alert-title").text(title);
    $("#alert-text").text(text);
    alert_parameters = parameters;
    if(enable_ok_button == false){
        $("#alert-ok-button").css("display", "none");
    }else{
        $("#alert-ok-button").css("display", "block");
    }
    if(enable_input == false){
        $("#alert-input").css("display", "none");
    }else{
        $("#alert-input").css("display", "block");
        $("#alert-input").focus();
    }

    $("#div-alert").css("display", "block");
}

function set_language(language){ // Function to set user language
    enable_disable_operations_in_progress();
    $.ajax({
        async: false,
        type:"GET",
        url:"/setlanguage",
        headers:{
            "Content-type":"application/json", 
            "Accept":"application/json"
        },
        data:{
            p_language: language
        },
        success:function(response){
            enable_disable_operations_in_progress();
            if(response["response"] == "ok"){
                location.reload();
            }else if(response["response"] == "error"){
                location.replace("/error");
            }
        },
        error:function(xhr, status, error){
            console.error(xhr);
        }
    });
}

// [= Window loading funtions =]

window.onload = function(){
    $.ajax({
        async: false,
        type:"GET",
        url:"/getlanguage",
        headers:{
            "Content-type":"application/json", 
            "Accept":"application/json"
        },
        success:function(response){
            language_obj = JSON.parse(response["language"]);
        },
        error:function(xhr, status, error){
            console.error(xhr);
        }
    });
};

// [= Starting document =]

$(document).ready(function(){
    // Click on close alert button
    $(document).on("click", "#alert-close", function(){
        $("#div-alert").css("display", "none");
    });

    // Logout
    $(document).on("click", "#logout-button", function(){
        $.ajax({
            type: "POST",
            url: "logout",
            headers: {
                "Content-type": "application/json",
                "Accept": "application/json"
            },
            success: function(response){
                if(response["response"] == "ok"){
                    location.replace("/");
                }else if(response["response"] == "error"){
                    location.replace("/error");
                }
            },
            error: function(xhr, status, error){
                console.error(xhr);
            }
        });
    });

    // Language buttons
    $(document).on("click", "#it_language_button", function(){
        set_language("IT");
    });
    $(document).on("click", "#en_language_button", function(){
        set_language("EN");
    });
});