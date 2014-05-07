'use strict';


// Declare app level module which depends on filters, and services
angular.module('sweepApp', [
  'ngRoute',
  'sweepApp.directives',
  'sweepApp.services',
  'sweepApp.controllers'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/', {
    templateUrl: 'static/partials/index.html', 
    controller: 'IndexCtrl'});
  $routeProvider.when('/s/:fieldId', {
    templateUrl: 'static/partials/game.html', 
    controller: 'GameCtrl'});
  $routeProvider.when('/records', {
    templateUrl: 'static/partials/records.html', 
    controller: 'RecordsCtrl'});
  $routeProvider.otherwise({redirectTo: '/'});
          
  TogetherJS();
}]);
