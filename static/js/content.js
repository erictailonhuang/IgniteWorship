var app = angular.module('app', []);

app.controller('HomeCtrl', ['$scope', '$http', '$sce', function($scope, $http, $sce) {
    var scope = $scope;
    var sce = $sce;

    // view data
    $scope.userFirstName = null;
    $scope.userFullName = null;
    $scope.googleID = null;
    $scope.email = null;
    $scope.surveyURL = null;
    $scope.profileImage = null;
    $scope.isAdmin = false;
    $scope.isLeader = false;
    $scope.surveyCompleted = false;




    $scope.loggedIn = false;
    $scope.badLogin = false;
    $scope.welcomeView = false;
    $scope.surveyView = false;
    $scope.scheduleView = false;
    $scope.swapView = false;
    $scope.requestsView = false;
    $scope.requestsCount = 0;

    $scope.iframeLoaded = false;

    function onSignIn(googleUser) {
        var profile = googleUser.getBasicProfile();
        console.log('attempted ID: ' + profile.getId());
        console.log('attemped Name: ' + profile.getName());
        console.log('attemped email: ' + profile.getEmail());

        scope.googleID = profile.getId();
        scope.userFullName = profile.getName();
        scope.userFirstName = profile.getName().split(" ")[0];
        scope.email = profile.getEmail();
        scope.profileImage = profile.getImageUrl();
        scope.googleID = profile.getId();
        
        scope.loginWithGoogle();
    };

    window.onSignIn = onSignIn;

    $scope.loginWithGoogle = function(){
        //reset just in case
        $scope.loggedIn = false;
        $scope.badLogin = false;
        $scope.welcomeView = false;
        $scope.surveyView = false;
        $scope.scheduleView = false;
        $scope.swapView = false;
        $scope.requestsView = false;
        $scope.requestsCount = 0;
        $scope.currentProfile = null;
        $scope.currentProfileImage = null;
        $scope.iframeLoaded = false;
        $scope.iframeToggleCount = 0;
        $scope.surveyCompleted = false;

        $http({
            method: 'POST',
            url: '/login',
            data: {"email": $scope.email, "googleID": $scope.googleID}
        }).then(function(response) {
            console.log(response.data);
            if (response.data.status=="OK") {
                $scope.loggedIn = true;
                $scope.welcomeView = true;
                $scope.surveyURL = sce.trustAsResourceUrl("https://docs.google.com/forms/d/e/1FAIpQLSe4y1FjLSUt-d4GNWooavs2rsfGHnMEgUDzqHpdniMuqakYhA/viewform?usp=pp_url&entry.1856311932=".concat($scope.googleID));
                $scope.profileImage = sce.trustAsResourceUrl($scope.profileImage);

                //SET USER PROFILE
                $scope.getUserProfile();
            }
            else {
                $scope.badLogin = true;
            }
        }, function(error) {
            console.log(error);
        });
    };


    $scope.getUserProfile = function(){
        $http({
            method: 'POST',
            url: '/getUserProfile',
            data: {'googleID': $scope.googleID}
        }).then(function(response) {
            console.log(response);
            $scope.isAdmin = response.data.isAdmin;
            $scope.isLeader = response.data.leader;
            $scope.surveyCompleted = response.data.completedSurveys;

        }, function(error) {
            console.log(error);
        });
    };

// toggling
    $scope.toggleSurvey = function(){
        console.log("TOGGLING SURVEY");
        $scope.welcomeView = false;
        $scope.surveyView = true;
        $scope.scheduleView = false;
        $scope.swapView = false;
        $scope.requestsView = false;
        if ($scope.iframeLoaded == false) {
            $scope.iframeLoaded = true;
        }
    };
    $scope.toggleSchedule = function(){
        console.log("TOGGLING SCHEDULE");
        $scope.welcomeView = false;
        $scope.surveyView = false;
        $scope.scheduleView = true;
        $scope.swapView = false;
        $scope.requestsView = false;
    };
    $scope.toggleSwap = function(){
        console.log("TOGGLING SWAP");
        $scope.welcomeView = false;
        $scope.surveyView = false;
        $scope.scheduleView = false;
        $scope.swapView = true;
        $scope.requestsView = false;
    };
    $scope.toggleRequests = function(){
        console.log("TOGGLING REQUESTS");
        $scope.welcomeView = false;
        $scope.surveyView = false;
        $scope.scheduleView = false;
        $scope.swapView = false;
        $scope.requestsView = true;
    };

    $scope.logout = function(){
        $scope.loggedIn = false;
        $scope.badLogin = false;
        $scope.welcomeView = false;
        $scope.surveyView = false;
        $scope.scheduleView = false;
        $scope.swapView = false;
        $scope.requestsView = false;
        $scope.requestsCount = 0;
        $scope.currentProfileImage = null;

        $scope.userFirstName = null;
        $scope.userFullName = null;
        $scope.googleID = null;
        $scope.email = null;
        $scope.surveyURL = null;
        $scope.isAdmin = false;
        $scope.isLeader = false;
        $scope.surveyCompleted = false;

        $scope.iframeLoaded = false;
        $scope.iframeToggleCount = 0;
    };


    $scope.markSurveyCompleted = function(){
        $http({
            method: 'POST',
            url: '/setSurveyCompleted',
            data: {"googleID": $scope.googleID}
        }).then(function(response) {
            console.log("survey marked complete");
        }, function(error) {
            console.log(error);
        });
    };


    $scope.iframeLoadedCallBack = function(){
        if (!$scope.surveyCompleted) {
            $scope.iframeToggleCount += 1;
        }

        if ($scope.iframeToggleCount == 2) {
            //update DB
            $scope.markSurveyCompleted();

            //update view control var
            $scope.surveyCompleted = true;
            console.log("form submitted");
        } 
    }

    $scope.clearSurvey = function(){
        $scope.iframeToggleCount = 0;
        $scope.surveyCompleted = false;
        $scope.iframeLoaded = true;
    }

}]);

app.config(function($sceProvider) {
    $sceProvider.enabled(false);
 });



app.directive('iframeOnload', [function(){
return {
    scope: {
        callBack: '&iframeOnload'
    },
    link: function(scope, element, attrs){
        element.on('load', function(){
            return scope.callBack();
        })
    }
}}])
