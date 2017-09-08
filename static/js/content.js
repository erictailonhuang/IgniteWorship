angular.module('myApp', [])
    .filter('orderObjectBy', function() {
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
    // .controller('HomeCtrl', ['$scope', '$http', '$timeout', '$window', '$routeParams', function($scope, $http, $timeout, $window, $routeParams) {
    .controller('HomeCtrl', ['$scope', '$http', '$timeout', '$window', function($scope, $http, $timeout, $window, $routeProvider) {
        var scope = $scope;
        // var routeParams = $routeParams;
        
        $scope.info = {}; //for requests, outgoing

        $scope.editMode = false;
        $scope.chordEditMode = false;
        $scope.lyricsOnlyMode = false;

        $scope.showAutosaveMessage = false;
        
        // $scope.currentSong = $routeParams.param1; //for display, store incoming

        $scope.idSelected = null;

        $scope.searchFocus = false;

        /////////////////// modals
        $scope.showDeleteModal = false;
        $scope.showAddChord = false;
        $scope.showAddSong = false;

        //////////////////// for key selection
        $scope.keys = ["Ab", "A", "A#", "Bb", "B", "C", "C#", "Db", "D", "D#", "Eb", "E", "F", "F#", "Gb", "G", "G#"]
        $scope.keysInput = ["NNS", "Ab", "A", "A#", "Bb", "B", "C", "C#", "Db", "D", "D#", "Eb", "E", "F", "F#", "Gb", "G", "G#"]
        $scope.selectedKey;
        $scope.keySelected_DD = function(key) {
            $scope.selectedKey = key;

            if (!$scope.editMode) {
                console.log("changing display key for song: " + $scope.currentSong.id);
                $scope.chordEditMode = false;
                

                $http({
                    method: 'POST',
                    url: '/getSong',
                    data: {id:$scope.currentSong.id, selectedKey:key}
                }).then(function(response) {
                    console.log("display dis song", response);
                    $scope.currentSong = response.data;
                    $scope.selectedKey = response.data.displayedKey;
                }, function(error) {
                    console.log(error);
                });

                $scope.showMainSongDiv = true;      
            }
            else { 
                $scope.currentSong.key = key;
                $scope.updateSongWithNewEdits();
                console.log("updating key for song: " + $scope.currentSong.id);
            }


        };
        ////////////////////////

        $scope.closeDeleteModal = function () {
            $scope.showDeleteModal = false;
            $('#deleteConfirm').modal('hide');
        };
        $scope.closeAddSongModal = function () {
            $scope.showAddSong = false;
            $('#addPopUp').modal('hide')
        };
        $scope.closeAddChordModal = function () {
            $scope.showAddChord = false;
            $('#addChordPopUp').modal('hide')
        };

        $scope.setSelected = function (idSelected) {
            $scope.dontMessStuffUpOnTheWayOut();
            $scope.idSelected = idSelected;
        };  

        $scope.pullSongListUpdate = function(){
            $http({
                method: 'POST',
                url: '/getSongList',

            }).then(function(response) {
                $scope.Songs = response.data;
                console.log('list o dem songs',$scope.Songs);
            }, function(error) {
                console.log(error);
            });
        };


        $scope.refreshSongDisplay = function(){
            //refresh
            $scope.info.id = $scope.idSelected;

            $http({
                method: 'POST',
                url: '/getSong',
                data: {id:$scope.info.id, padded:true}
            }).then(function(response) {
                console.log("display dis song", response);
                $scope.currentSong = response.data;
            }, function(error) {
                console.log(error);
            });
        };

        $scope.addSong = function(){
            $http({
                method: 'POST',
                url: '/addSong',
                data: {info:$scope.info}
            }).then(function(response) {
                $scope.pullSongListUpdate();
                $('#addPopUp').modal('hide')
                showAddSong = false;
                $scope.info = {};
                console.log("display newly added song", response);
                $scope.currentSong = response.data;
                $scope.setSelected($scope.currentSong.id);
                $scope.selectedKey = $scope.currentSong.key;
                $scope.showMainSongDiv = true;
                $scope.editModeOn();
            }, function(error) {
                console.log(error);
            });
        };

        $scope.toggleLyricsOnlyMode = function() {
            if ($scope.lyricsOnlyMode) {
                $scope.lyricsOnlyMode = false;
            }
            else {
                $scope.lyricsOnlyMode = true;
            }
        }
        
        $scope.searchFocusOn = function() {
            $scope.searchFocus = true;
        }

        $scope.searchFocusOff = function() {
            $scope.searchFocus = false;
        }

        $scope.toggleEditMode = function() {
            if ($scope.editMode) {
                $scope.editModeOff();
            }
            else {
                $scope.editModeOn();
            }
        }

        $scope.editModeOn = function() {
            $scope.editMode = true;
            $scope.lyricsOnlyMode = false;
        };

        $scope.editModeOff = function() {
            if ($scope.currentSong.songName.trim() != "") { //must have title before saving
                $scope.chordEditMode = false;
                $scope.dontMessStuffUpOnTheWayOut();
                $scope.showSong($scope.currentSong.id);
            }
            
        };

        $scope.chordEditModeOn = function() {
            $scope.updateSongWithNewEdits();
            //retrieve original key
            $scope.keySelected_DD($scope.currentSong.key);
            $scope.lyricsOnlyMode = false;
            $scope.chordEditMode = true;
            $(".character_split").lettering();
        };

        $scope.chordEditModeOff = function() {
            $scope.updateSongWithNewEdits();
            $scope.chordEditMode = false;
            $scope.showAddChord = false;
        };

        $scope.getClickedLetter = function() {
            $scope.chordToAdd_spanNo = event.target.className;
            $scope.chordToAdd_songid = $scope.idSelected;
            $scope.chordToAdd_key = $scope.currentSong.key;

            // make sure class selection span is valid
            // console.log(/^char\\d*$/.test($scope.chordToAdd_spanNo));
            if(/^char\d*$/.test($scope.chordToAdd_spanNo) == false) {
                console.log("selection for chord input not valid");
                return
            }

            //check if a chord already exists at this location then show option to delete
            var position = (Number($scope.chordToAdd_spanNo.replace("char","")) -1).toString();

            $scope.checkAndRemoveOrAddChord($scope.chordToAdd_spanNo);
        };

        scope.showAddChordPopUp = function(){
            $('#addChordPopUp').modal('show')
            $scope.showAddChord = true;
        };

        scope.removeChord = function() {
            var removeChordRequest = 
            {
                'position': $scope.chordToAdd_spanNo,
                'songID': $scope.chordToAdd_songid
            }

            $http({
                method: 'POST',
                url: '/removeChord',
                data: {info:removeChordRequest}
            }).then(function(response) {
                console.log(response.data);
            }, function(error) {
                console.log(error);
            });

            $scope.refreshChords();
        };

        $scope.addChord = function() {
            if ($scope.chordToAdd_chord.trim() == "" || $scope.chordToAdd_chord == null) {
                return;
            }

            var chordRequest = 
            {
                'position': $scope.chordToAdd_spanNo,
                'songID': $scope.chordToAdd_songid,
                'chord': $scope.chordToAdd_chord
            }


            // chord insert
            $http({
                method: 'POST',
                url: '/insertChord',
                data: {info:chordRequest}
            }).then(function(response) {
                console.log(response.data);
                $('#addChordPopUp').modal('hide')
            }, function(error) {
                console.log(error);
                
            });
            $scope.chordToAdd_chord = "";
            $scope.showAddChord = false;
            
            $scope.refreshChords();

        };     

        $scope.refreshChords = function() {
            $http({
                method: 'POST',
                url: '/getChords',
                data: {'songID': $scope.chordToAdd_songid}
            }).then(function(response) {
                console.log("display dis song", response);
                $scope.currentSong.chords = response.data.chords;
            }, function(error) {
                console.log(error);
            });
        };

        $scope.checkAndRemoveOrAddChord = function(position) {
            $http({
                method: 'POST',
                url: '/checkChordExistsHere',
                data: { info:{
                        'position': $scope.chordToAdd_spanNo,
                        'songID': $scope.chordToAdd_songid
                        }}

            }).then(function(response) {
                if (response.data.status) {
                    scope.removeChord();
                    console.log("Remove chord at index: " + position);
                }
                else if (!response.data.status){
                    scope.showAddChordPopUp();
                    console.log("Add chord at index: " + position);
                }
                else{
                    console.log("Error - cannot check " + position);
                }
            }, function(error) {
                console.log(error);
            });

            setTimeout(function(){
                $scope.refreshChords();
            }, 500);
        };

        $scope.updateSongWithNewEdits = function(){
            $http({
                method: 'POST',
                url: '/updateSong',
                data: {info:$scope.currentSong}
            }).then(function(response) {
                console.log(response.data);
                $scope.pullSongListUpdate();
            }, function(error) {
                console.log(error);
            });
        };

        $scope.showAddPopUp = function(){
            $scope.dontMessStuffUpOnTheWayOut();
            $scope.info = {};
            $scope.showAddSong = true;
            $('#addPopUp').modal('show')
        };

        $scope.clearSongDisplay = function(){
            $scope.dontMessStuffUpOnTheWayOut();
            $scope.showMainSongDiv = false;
        };
        
        $scope.showSong = function(id){
            $scope.info.id = id;
            console.log("selected song: " + id);
            $scope.chordEditMode = false;
            $scope.showMainSongDiv = true;

            $http({
                method: 'POST',
                url: '/getSong',
                data: {id:$scope.info.id}
            }).then(function(response) {
                console.log("display dis song", response);
                $scope.currentSong = response.data;
                $scope.selectedKey = $scope.currentSong.key;
            }, function(error) {
                console.log(error);
            });
        };

        $scope.dontMessStuffUpOnTheWayOut = function(){
            if ($scope.editMode == true){
                $scope.updateSongWithNewEdits();
            }
            $scope.editMode = false;
            $scope.chordEditMode = false;
            $scope.showAutosaveMessage = false;

        };
        
        $scope.confirmDelete = function(id){
            $scope.dontMessStuffUpOnTheWayOut();
            $scope.deleteSongId = id;
            $('#deleteConfirm').modal('show');
            $scope.showDeleteModal = true;
        };
        
        $scope.deleteSong = function(){
            $http({
                method: 'POST',
                url: '/deleteSong',
                data: {id:$scope.deleteSongId}
            }).then(function(response) {
                console.log(response.data);
                $scope.deleteSongId = '';
                $scope.pullSongListUpdate();
                $scope.clearSongDisplay();
                $('#deleteConfirm').modal('hide')
            }, function(error) {
                console.log(error);
            });
            $scope.showDeleteModal = false;
        };


        $scope.openModals = function(){
            // console.log("deleteModal: " + $scope.showDeleteModal)
            // console.log("addChordModal: " + $scope.showAddChord)
            // console.log("addSongModal: " + $scope.showAddSong)
                
            if ($scope.showDeleteModal || $scope.showAddChord || $scope.showAddSong){
                return(true);
            }
            return(false);
        };

        $scope.pullSongListUpdate();

// keyboard shortcuts
        $scope.vKey = 86;
        $scope.cKey = 67;
        $scope.sKey = 83;
        $scope.eKey = 69;
        $scope.cKey = 67;
        $scope.qKey = 81;

        $scope.period = 190;
        $scope.comma = 188;        
        $scope.enter = 13;
        $scope.space = 32;
        $scope.escape = 27;
        $scope.ctrlKeys = [224, 17, 93, 91];
// Firefox: 224
// Opera: 17
// WebKit (Safari/Chrome): 91 (Left Apple) or 93 (Right Apple)

        angular.element($window).bind("keydown", function($event) {
            if ($scope.searchFocus) {
                return
            } 

            // autosave
            if (($event.keyCode == $scope.enter || $event.keyCode == $scope.comma || $event.keyCode == $scope.period) && $scope.editMode && !$scope.chordEditMode){
                $scope.showAutosaveMessage = true;
                $scope.updateSongWithNewEdits();
                $scope.$apply();
                console.log('keyboard shortcut: autosaving');
            }
            // enable editmode
            else if (($event.keyCode == $scope.eKey) && !$scope.editMode && $scope.showMainSongDiv && !$scope.openModals()){
                $scope.editModeOn();
                $scope.$apply();
                console.log('keyboard shortcut: edit mode enable');
            }
            // if escape key, clear $scope.showDeleteModal and...
            else if ($event.keyCode == $scope.escape){
                // clear main display
                if ($scope.openModals()){
                    $scope.closeDeleteModal();
                    $scope.closeAddSongModal();
                    $scope.closeAddChordModal();
                }
                else if (!$scope.editMode && !$scope.openModals()){
                    $scope.clearSongDisplay();
                    console.log('keyboard shortcut: clear main display');
                }
                // exit edit mode
                else if (($scope.editMode && !$scope.chordEditMode) && !$scope.openModals()){
                    $scope.editModeOff();
                    console.log('keyboard shortcut: exiting edit mode');
                }
                // exit chord edit mode
                else if ($scope.chordEditMode && !$scope.openModals()){
                    $scope.editModeOff();
                    $scope.chordEditModeOff();
                    console.log('keyboard shortcut: exiting chord edit mode');
                }
                $scope.showDeleteModal = false;
                $scope.$apply();
            }
            else if(($event.keyCode == $scope.qKey) && !$scope.editMode && !$scope.chordEditMode && !$scope.openModals()) {
                $scope.editModeOn();
                $scope.chordEditModeOn();
                $scope.$apply();
                console.log('keyboard shortcut: chord edit mode enable');
            }
            else if(($event.keyCode == $scope.enter) && $scope.showAddChord) {
                $scope.addChord();
                $scope.$apply();
                console.log('keyboard shortcut: submit chord');
            }

        });

        // autosave
        window.setInterval(function(){
            if ($scope.editMode && !$scope.chordEditMode && $scope.currentSong.songName.trim() != ""){
                $scope.showAutosaveMessage = true;
                $scope.updateSongWithNewEdits();
                $timeout(function () {
                    $scope.showAutosaveMessage = false;
                }, 700);
            }
        }, 7000); //save every 7 seconds, flash notification for .7 second
    }]);




