TicketModule.factory('MovieService', function ($http, $q) {
//    var api_url = "http://in.bookmyshow.com/getJSData/?file=/data/js/GetEvents_MT.js&cmd=GETEVENTSWEB&et=MT&rc=BANG&_=1419399279396&_=1419399279395";
//    var api_url = "http://www.imdb.com/title/tt2189461/";
//    var api_url = "http://in.bookmyshow.com";
    var api_url = "http://in.bookmyshow.com/getJSData/?cmd=GETEVENTLIST&f=json&et=CT&rc=BANG&t=67x1xa33b4x422b361ba&pt=WEB&sr=&lt=&lg=";
    var api_suffixe = "/posts/";
    return {
        get: function(){
//            var url = api_url;
//            var defer = $q.defer();
//            $http({method: 'GET', url: url}).
//                success(function(data, status, headers, config) {
//                    console.log(data);
//                    defer.resolve(data);
//                }).
//                error(function(data, status, headers, config) {
//                    defer.reject(status);
//                });
//            return defer.promise;
            var deferred = $q.defer();
//            console.log('fetching url: ', q_url);

            deferred.resolve(
                $.ajax({
                    url: api_url,
                    type: 'GET',
                    success: function(res) {
//                        console.log('returning response for url: '+ q_url);
                        return res;
                    }
                })
            );
            // $timeout(function(){
            //     deferred.resolve('This is the text');
            // }, 2000)

            return deferred.promise;
        }
    }

//    var getResponseText = function(){
//        var deferred = $q.defer();
////            console.log('fetching url: ', q_url);
//
//        deferred.resolve(
//            $.ajax({
//                url: api_url,
//                type: 'GET',
//                success: function(res) {
////                        console.log('returning response for url: '+ q_url);
//                    return res;
//                }
//            })
//        );
//        // $timeout(function(){
//        //     deferred.resolve('This is the text');
//        // }, 2000)
//
//        return deferred.promise;
//    };

});