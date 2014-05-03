'use strict';

/* Controllers */

var sweepControllers = angular.module('sweepApp.controllers', []);
sweepControllers.controller('IndexCtrl', ['$scope', '$location', 'GameService', function($scope, $location, GameService) {
  function newGame(width, height, chance) {
    
    var promise = GameService.newGame(width, height, chance)
    promise.then(function(args) {
        if (args.data.id) {
          $location.path('/s/' + args.data.id);
        } else {
          $scope.error = 'Something went wrong. Please try again later.';
        }
      })
      .catch(function(args) {
        console.error(args.data);
        
        // use message if provided
        if (args.data.error) {
          $scope.error = args.data.error;
        } else {
          $scope.error = 'Something went wrong. Please try again later.';
        }
      });
    
    return promise;
  }
    
  function newCustomGame() {
    newGame(
      $scope.customField.width, 
      $scope.customField.height, 
      $scope.customField.chance
    ).catch(function(args) {
      if (args.data.width) {
        $scope.inputError.width = args.data.width;
      }
      if (args.data.height) {
        $scope.inputError.height = args.data.height;
      }
      if (args.data.chance) {
        $scope.inputError.chance = args.data.chance;
      }
    });
  }
  
  function clearError() {
    $scope.error = null;
    $scope.inputError = {};
  }
  
  $scope.error = null;
  $scope.inputError = {};
  $scope.customField = {
    width: 10,
    height: 10,
    chance: 20
  }
  
  $scope.clearError = clearError;
  $scope.newCustomGame = newCustomGame;
  $scope.newGame = newGame;
}])


sweepControllers.controller('GameCtrl', ['$scope', '$routeParams', 'GameService', function($scope, $routeParams, GameService) {

  function tick(startTime) {
    $scope.timer = Math.floor((new Date().getTime() - startTime) / 1000);
    
    setTimeout(function () {
      tick(startTime);
      $scope.$digest();
    }, 1000);
  }
  
  function initGame() {
    GameService.getGame($routeParams.fieldId)
      .success(function(data, status, headers, config) {
        var x, y;
        if (data.id) {
          $scope.active = data.active;
          $scope.count = data.count;
          
          for (x = 0; x < data.flags.length; x += 1) {
            $scope.rows.push([]);
            for (y = 0; y < data.flags[x].length; y += 1) {
              $scope.rows[x].push({
                flagged: data.flags[x][y].flagged,
                value: data.flags[x][y].value
              });
            }
          }
            
          tick(data.created_date);
        } else {
          $scope.error = 'Something went wrong. Please try again later.';
        }
      })
      .error(function(data, status, headers, config) {
        console.error(data);
        
        // use message if provided
        if (data.error) {
          $scope.error = data.error;
        } else {
          $scope.error = 'Something went wrong. Please try again later.';
        }
      });
  }
  
  function sweep(x, y) {
    if ($scope.active) {
      console.log('Sweeping: ' + x +', ' + y);

      if ($scope.rows[x][y].flagged) {
        $scope.error = 'There\'s a flag there. Right click to remove the flag first.';
      } else {
        GameService.sweep($routeParams.fieldId, x, y)
          .success(function(data, status, headers, config) {
            var i, c;
            if (data.result === 'loss') {
              $scope.rows[x][y].value = -1;
              $scope.active = false;
              $scope.result = 'loss';
            } else if (data.result === 'win') {
              for (i = 0; i < data.coords.length; i += 1) {
                c = data.coords[i];
                $scope.rows[c.x][c.y].value = c.value;
              }
              
              $scope.active = false;
              $scope.result = 'win';
              
              GameService.createRecord($scope.rows[0].length, $scope.rows.length, $scope.count, $scope.timer);
            } else {
              for (i = 0; i < data.coords.length; i += 1) {
                c = data.coords[i];
                $scope.rows[c.x][c.y].value = c.value;
              }
            }
          })
          .error(function(data, status, headers, config) {
            console.error(data);

            // use message if provided
            if (data.error) {
              $scope.error = data.error;
            } else {
              $scope.error = 'Something went wrong. Please try again later.';
            }
          });
      }
    }
  }
  
  function flag(x, y) {
    if ($scope.active) {
      console.log('Flagging: ' + x +', ' + y);
      
      if ($scope.rows[x][y].value !== '?') {
        $scope.error = 'That\'s already cleared. No need for a flag there.';
      } else {
        GameService.flag($routeParams.fieldId, x, y)
          .success(function(data, status, headers, config) {
            if (data.result === 'flagged') {
              $scope.rows[x][y].flagged = true;
            } else if (data.result === 'unflagged') {
              $scope.rows[x][y].flagged = false;
            }
          })
          .error(function(data, status, headers, config) {
            console.error(data);

            // use message if provided
            if (data.error) {
              $scope.error = data.error;
            } else {
              $scope.error = 'Something went wrong. Please try again later.';
            }
          });
      }
    }
  }
  
  function clearError() {
    $scope.error = null;
  }
  
  $scope.active = false;
  $scope.error = null;
  $scope.result = null;
  $scope.rows = [];
  
  $scope.clearError = clearError;
  $scope.flag = flag;
  $scope.sweep = sweep;
  
  //initialize the data
  initGame();
}]);

sweepControllers.controller('RecordsCtrl', ['$scope', 'GameService', function($scope, GameService) {

  function initRecords() {
    var r, records = GameService.getRecords();
    
    for (r in records) {
      $scope.records.push(records[r]);
    }
  }
  
  $scope.records = [];
  
  initRecords();

}]);