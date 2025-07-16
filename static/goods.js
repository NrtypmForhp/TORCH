// [= TORCH goods javascript file =]

// Function to clear item management window
function clear_item_management_window(){
    // Inputs
    $("#item-management-category-input").val("");
    $("#item-management-type-input").val("");

    // Details p
    $("#item-management-details-p").text("");
}

$(document).ready(function(){
    // Click on new item button
    $(document).on("click", "#new-item-button", function(){ // Open new item div
        $("#div-item-management").css("display", "block");
        clear_item_management_window();
    });
    $(document).on("click", "#item-management-close", function(){ // Close new item div
        $("#div-item-management").css("display", "none");
    });
});