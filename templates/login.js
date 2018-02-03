function handlelogin(resultData) {
    console.log("handleStarResult: populating star table from resultData");

    // populate the star table
    var starTableBodyElement = jQuery("#");
    for (var i = 0; i < Math.min(10, resultData.length); i++) {
        var rowHTML = "";
        rowHTML += "<tr>";
        rowHTML += "<th>" + resultData[i]["star_name"] + "</th>";
        rowHTML += "<th>" + resultData[i]["star_dob"] + "</th>";
        rowHTML += "</tr>"
        starTableBodyElement.append(rowHTML);
    }
}

// makes the HTTP GET request and registers on success callback function handleStarResult
jQuery.ajax({
    dataType: "json",
    method: "POST",
    url: "/login",
    success: (resultData) => handlelogin(resultData)
});