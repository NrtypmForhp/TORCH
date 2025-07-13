// [= TORCH goods javascript file =]

$(document).ready(function(){
    // Click on new item button
    $(document).on("click", "#new_item_button", function(){ // Open new item div
        $("#div-new-item").css("display", "block");
    });
    $(document).on("click", "#new-item-close", function(){ // Close new item div
        $("#div-new-item").css("display", "none");
    });
});