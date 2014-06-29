var webscraper = {
    init: function() {
        var $feedback = $(".feedback");
        $(".scrap").submit(function(event){

            //FB.login();

            //if(FB.getAccessToken()){
                var fbUsername = $(this).find("input[name=facebook_username]").val();
                var twUsername = $(this).find("input[name=twitter_username]").val();
                var accessToken = FB.getAccessToken();

                $.ajax({
                    url: "/profile?facebook_username=" + fbUsername + "&twitter_username=" + twUsername + "&fbAccessToken=" + accessToken,
                    dataType: "json",
                    error: function(){
                        console.log("error");
                    },
                    statusCode: {
                        202: function(data){
                            $feedback.html("<span>"+data.msg+"</span>");
                        },
                        200: function(data){
                            var htmlProfile = '<h2>Facebook</h2>' +
                                '<span>Username: '+data.facebook.username+'</span><br />' +
                                '<span>Name: '+data.facebook.name+'</span><br />' +
                                '<span>Short Description: '+data.facebook.short_description+'</span><br />' +
                                '<span>Profile Image: '+data.facebook.image+'</span><br />' +
                                '<span>Popularity: '+data.facebook.popularity+'</span><br />' +
                                '<span>Last Updated: '+data.facebook.updated+'</span><br />';

                            $feedback.html(htmlProfile);

                            /*FIXME!!!*/
                            var htmlProfile = '<h2>Twitter</h2>' +
                                '<span>Username: '+data.twitter.username+'</span><br />' +
                                '<span>Name: '+data.twitter.name+'</span><br />' +
                                '<span>Short Description: '+data.twitter.short_description+'</span><br />' +
                                '<span>Profile Image: '+data.twitter.image+'</span><br />' +
                                '<span>Popularity: '+data.twitter.popularity+'</span><br />' +
                                '<span>Last Updated: '+data.twitter.updated+'</span><br />';

                            $feedback.append(htmlProfile);
                        }
                    }
                });
            //}


            event.preventDefault();
        });
    }
};

$(document).ready(function() {
    "use strict";
    webscraper.init();
});