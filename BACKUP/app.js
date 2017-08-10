angular.module('myApp', [])
    .filter('orderSongsByName', function() {
        return function(items, field, reverse) {
            var filtered = [];

            angular.forEach(items, function(item) {
                filtered.push(item);
            });
            filtered.sort(function (a, b) {
                return (a[field] > b[field] ? 1 : -1);
            });
            if(reverse) filtered.reverse();
                return filtered;
        };
    })
    .controller('HomeCtrl', function($scope, $http) {

        $scope.keys = ["A", "A#/Bb", "B", "C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab"];

        $scope.info = {};
        
        $scope.currentSong = {};
        
        $scope.showAdd = true;
    
        $scope.pullSongListUpdate = function(){
            $scope.showMainSongDiv = false;
            $http({
                method: 'POST',
                url: '/getSongList',

            }).then(function(response) {
                $scope.Songs = response.data;
                console.log('list o dem songs',$scope.Songs);
            }, function(error) {
                console.log(error);
            });
        }

        $scope.addSong = function(){
            $http({
                method: 'POST',
                url: '/addSong',
                data: {info:$scope.info}
            }).then(function(response) {
                $scope.pullSongListUpdate();
                $('#addPopUp').modal('hide')
                $scope.info = {}
            }, function(error) {
                console.log(error);
            });
        }
        
        $scope.editSong = function(id){
            $scope.info.id = id;
            $scope.showAdd = false;
            
            $http({
                method: 'POST',
                url: '/getSong',
                data: {id:$scope.info.id}
            }).then(function(response) {
                console.log(response);
                $scope.info = response.data;
                $('#addPopUp').modal('show')
            }, function(error) {
                console.log(error);
            });
        }
        
        $scope.updateSong = function(id){
            $http({
                method: 'POST',
                url: '/updateSong',
                data: {info:$scope.info}
            }).then(function(response) {
                console.log(response.data);
                $scope.pullSongListUpdate();
                $('#addPopUp').modal('hide')
            }, function(error) {
                console.log(error);
            });
        }
        

        $scope.showAddPopUp = function(){
            $scope.showAdd = true;
            $scope.info = {};
            $('#addPopUp').modal('show')
        }

        $scope.clearSongDisplay = function(){
            $scope.showMainSongDiv = false;
        }
        
        $scope.showSong = function(id){
            $scope.info.id = id;
            $scope.showMainSongDiv = true;
            
            $http({
                method: 'POST',
                url: '/getSong',
                data: {id:$scope.info.id}
            }).then(function(response) {
                console.log("display dis song", response);
                $scope.currentSong = response.data;
            }, function(error) {
                console.log(error);
            });
        }
        
        $scope.confirmDelete = function(id){
            $scope.deleteSongId = id;
            $('#deleteConfirm').modal('show');
        }
        
        $scope.deleteSong = function(){
            $http({
                method: 'POST',
                url: '/deleteSong',
                data: {id:$scope.deleteSongId}
            }).then(function(response) {
                console.log(response.data);
                $scope.deleteSongId = '';
                $scope.pullSongListUpdate();
                $('#deleteConfirm').modal('hide')
            }, function(error) {
                console.log(error);
            });
        }
        
        $scope.pullSongListUpdate();
    })






