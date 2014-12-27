'use strict';

var TicketModule = angular.module('TicketApp', ["ngRoute"]);


TicketModule.config(function ($routeProvider) {
    $routeProvider
        .when("/", {
            templateUrl: "static/js/app/views/index.html",
            controller: "AppController"
//            resolve: {
//                posts: function (PostService) {
//                    return PostService.list();
//                }
//            }
        })
//        .when("/post/:id", {
//            templateUrl: "static/js/app/views/view.html",
//            controller: "PostController",
//            resolve: {
//                post: function ($route, PostService) {
//                    var postId = $route.current.params.id
//                    return PostService.get(postId);
//                }
//            }
//        })
        .otherwise({
            redirectTo: '/'
        })
})