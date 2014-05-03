'use strict';

/* Services */
var sweepServices = angular.module('sweepApp.services', []);

/**
 * Election resource.
 */
sweepServices.factory('GameService', ['$http', '$q',
  function ($http, $q) {
    'use strict';
    
    function newGame(width, height, chance) {
      // validate parameters
      var data = {};
      
      var intRegEx = /^[1-9]\d*$/;
      if (typeof width === 'undefined' || !intRegEx.test(width)) {
        data.error = 'Invalid input';
        data.width = 'Width is not a valid number.';
      }
      if (typeof height === 'undefined' || !intRegEx.test(height)) {
        data.error = 'Invalid input';
        data.height = 'Height is not a valid number.';
      }
      if (typeof chance === 'undefined' || (chance !== 0 && !intRegEx.test(chance))) {
        data.error = 'Invalid input';
        data.chance = 'Percent coverage is not a valid number.';
      }
      
      if (typeof data.error !== 'undefined') {
        var d = $q.defer();
        
          d.reject({data: data});
        
        return d.promise;
      } else {
        return $http({method: 'GET', url: '/meansweep/new/' + height + '/' + width + '/' + chance});
      }
    }
    
    function getGame(id) {
      //TODO validate id
      
      return $http({method: 'GET', url: '/meansweep/' + id + '/'});
    }
    
    function flag(id, x, y) {
      //TODO validate parameters
      
      return $http({method: 'GET', url: '/meansweep/flag/' + id + '/' + x + '/' + y});
    }
    
    function sweep(id, x, y) {
      //TODO validate parameters
      
      return $http({method: 'GET', url: '/meansweep/sweep/' + id + '/' + x + '/' + y});
    }
    
    function getRecords() {
      var records = localStorage.getItem('records');
      if (typeof records === 'string') {
        records = JSON.parse(records);
      } else {
        records = {};
      }
      
      return records;
    }
  
    function createRecord(x, y, count, time) {
      var key = (x * y) + '/' + count;

      var records = getRecords();

      if (!records[key] || time < records[key].time) {
        records[key] = {
          width: x,
          height: y,
          count: count,
          time: time,
          recordDate: new Date().getTime()
        };
        
        localStorage.setItem('records', JSON.stringify(records));
      }
    }
    
    return {
      createRecord: createRecord,
      flag: flag,
      getGame: getGame,
      getRecords: getRecords,
      newGame: newGame,
      sweep: sweep
    };
    
  }]);
