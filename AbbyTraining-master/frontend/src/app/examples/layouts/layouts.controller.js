(function() {
    'use strict';

    angular
        .module('app.examples.layouts')
        .controller('FullWidthController', FullWidthController);

    /* @ngInject */
    function FullWidthController($http, API_CONFIG) {
        var vm = this;
        vm.data = {
        };
        vm.courses = [];

        clearForm();
        getCourses();

        ////////////////

        function getCourses() {
            return $http.get(API_CONFIG.api + 'courses').
            then(function(response) {
                vm.courses = response.data.courses;
            });
        }

        function clearForm() {
        }

    }
})();