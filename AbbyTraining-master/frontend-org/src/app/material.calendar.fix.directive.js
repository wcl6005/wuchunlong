(function() {
    angular
        .module('app')
        .directive('mdDatepicker', DatePickerFixDirective);

    /* @ngInject */
    function DatePickerFixDirective($mdTheming) {
        return {
            link: function(scope, element){
                var calendarPane = angular.element(element[0].querySelector('.md-datepicker-calendar-pane'));
                $mdTheming(calendarPane);
            }
        };
    }
})();
