var webscraper = {
    init: function() {
        var $feedback = $(".feedback");
        $(".scrap").submit(function(event){
            var username = $(this).find("input[name=username]").val();

            $.ajax({
                url: "/profile?username="+ username,
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