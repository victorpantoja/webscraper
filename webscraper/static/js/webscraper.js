var webscraper = {
    init: function() {
        var $feedback = $(".feedback");
        $(".scrap").submit(function(event){
            var fbUsername = $(this).find("input[name=facebook_username]").val();
            var twUsername = $(this).find("input[name=twitter_username]").val();

            $.ajax({
                url: "/profile?facebook_username=" + fbUsername + "&twitter_username=" + twUsername,
                dataType: "json",
                error: function(){
                    console.log("error");
                },
                statusCode: {
                    202: function(data){
                        $feedback.html("<span>"+data.msg+"</span>");
                    },
                    200: function(data){
                        var htmlProfile = '<span>Username: '+data.username+'</span><br />' +
                            '<span>Name: '+data.name+'</span><br />' +
                            '<span>Short Description: '+data.short_description+'</span><br />' +
                            '<span>Profile Image: '+data.image+'</span><br />' +
                            '<span>Popularity: '+data.popularity+'</span><br />' +
                            '<span>Last Updated: '+data.updated+'</span><br />';

                        $feedback.html(htmlProfile);
                    }
                }
            });

            event.preventDefault();
        });
    }
};

$(document).ready(function() {
    "use strict";
    webscraper.init();
});