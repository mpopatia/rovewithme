// $(document).ready(function(){
// });

function saveEmail(){
  var email = $.trim($("input[name=email]").val());
  var space = $(".emailAlert");
  if(email.length == 0){
      space.html("");
      space.append("<div class='alert alert-danger' role='alert'>"+"Please enter a valid email."+"</div>")
      window.setTimeout(function() {
                    space.html("");
                },3000);
      
  }else{
      space.html("");
      $.post('contact/',
        {email:JSON.stringify(email)},
        function(data){
            var result = data[0]["success"];
            if (result == 1){
                console.log("Email: "+email+" saved!");
                space.append("<div class='alert alert-success' role='alert'>"+"Saved "+email+". We'll get in touch soon."+"</div>");
                space.slideDown();
                window.setTimeout(function() {
                    space.html("");
                },3000);
            } else {
                console.log("Failed to save email");
                space.append("<div class='alert alert-danger' role='alert'>"+"Failed to save "+email+". Please try again."+"</div>");
                space.slideDown();
                window.setTimeout(function() {
                    space.html("");
                },3000);
            }
          $("input[name=email]").val("");
        });
  }
}

function saveMessage(){
    var email = $.trim($("input[name=messageEmail]").val());
    var message = $.trim($("input[name=message]").val());
    var space = $(".messageAlert");
    
    if(email.length == 0){
      space.html("");
      space.append("<div class='alert alert-danger' role='alert'>"+"Please enter a valid email."+"</div>")
      window.setTimeout(function() {
                    space.html("");
                },3000);
    }else if(message.length == 0){
        space.html("");
        space.append("<div class='alert alert-danger' role='alert'>"+"Please enter a message."+"</div>")
        window.setTimeout(function() {
                    space.html("");
                },3000);
    }else{
      space.html("");
      $.post('message/',
        {email:JSON.stringify(email), message:JSON.stringify(message)},
        function(data){
            var result = data[0]["success"];
            if (result == 1){
                console.log("Message saved!");
                space.append("<div class='alert alert-success' role='alert'>"+"Message save. Thank you!"+"</div>");
                space.slideDown();
                window.setTimeout(function() {
                    space.html("");
                },3000);
            } else {
                console.log("Failed to save message");
                space.append("<div class='alert alert-danger' role='alert'>"+"Failed to save message. Please try again."+"</div>");
                space.slideDown();
                window.setTimeout(function() {
                    space.html("");
                },3000);
            }
          $("input[name=messageEmail]").val("");
          $("input[name=message]").val("");
        });
  }
}

function showHideBuyers(){
    var features = $("#buyerFeatures");
    var button = $("#buyerButton");
    if (features.is(":hidden")) {
        features.slideDown()
        button.text("Hide what buyers can do");
    }
    else {  
         features.slideUp();
         button.text("Show what buyers can do");
    }
}
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');

ga('create', 'UA-59535337-2', 'auto');
ga('send', 'pageview');