$(document).ready(function(){
    console.log("Hello WOrld");

    $("#filter-button").click(function(e){
      e.preventDefault();
      console.log("FIlter click syoyfo");
      $("#hidden-detail").toggleClass("hidden");
      var currentHTML = e.target.innerHTML;
      if (currentHTML == "Advanced"){
        e.target.innerHTML = "Hide";
      } else {
        e.target.innerHTML = "Advanced";
      }
    });

    $("#submit-button").click(function(e){
      console.log("Submit click syoyfo");
    });
});
