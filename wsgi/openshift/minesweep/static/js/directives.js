'use strict';

/* Directives */


var directives = angular.module('sweepApp.directives', []);

//Source: http://stackoverflow.com/questions/15731634/how-do-i-handle-right-click-events-in-angular-js
directives.directive('ngRightClick', function($parse) {
    return function(scope, element, attrs) {
        var fn = $parse(attrs.ngRightClick);
        element.bind('contextmenu', function(event) {
            scope.$apply(function() {
                event.preventDefault();
                fn(scope, {$event:event});
            });
        });
    };
});;
