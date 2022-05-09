function compare()
{
    // Call Python code in the backend
    $.ajax({
        url: "/compare",
        type: "POST",
        dataType: 'json',
        success: function(response){
            // Sorted list is returned from the Python code
            console.log(response);
            },
            error: function(error) {
                console.log("Error!");
            }
        });
}