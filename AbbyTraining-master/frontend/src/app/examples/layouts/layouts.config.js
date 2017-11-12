(function() {
    'use strict';

    angular
        .module('app.examples.layouts')
        // http://www.oschina.net/question/1053626_240336
        // .config(function($provide){
        //     $provide.decorator('$log', function($delegate){
        //         return $delegate;
        //     });
        // })
        .config(function ($provide) {
            // http://zhidao.baidu.com/link?url=JNSJuhxNtMn3HJg6q5rETD848Fk7TAAnY0G-5MI9fiW9ShRiW0Tl8_V9MO-X66VO5LCW43vj0zDl-jLA8qJvggjkfDaRGS5jasf_LJ3404G
            // $provide.service('deco', function ($http, $log) {
            //     this.$http = $http;
            //     this.$log = $log;
            // });
            $provide.factory('deco', function ($http, $log) {
                this.$http = $http;
                this.$log = $log;
                return this;
            });
        })
        .config(moduleConfig);

    /* @ngInject */
    function moduleConfig($stateProvider, triMenuProvider, decoProvider) {
    // function moduleConfig($stateProvider, triMenuProvider, $logProvider, decoProvider) {
        // var $log = $logProvider.$get();
        var testService = decoProvider.$get();
        testService.$log.log(testService);

        $stateProvider
        .state('triangular.layouts-example-full-width', {
            url: '/layouts/full-width',
            templateUrl: 'app/examples/layouts/full-width-page.tmpl.html',
            controller: 'FullWidthController',
            controllerAs: 'vm',
            data: {
                layout: {
                    sideMenuSize: 'hidden'
                },
                permissions: {
                    only: ['viewLayouts']
                }
            }
        });

        var children = [
            {
                name: 'Python',
                type: 'link',
                state: 'triangular.layouts-example-full-width'
            },
            {
                name: 'OpenStack',
                type: 'link',
                state: 'triangular.layouts-example-full-width'
            },
            {
                name: 'Docker',
                type: 'link',
                state: 'triangular.layouts-example-full-width'
            }
        ];

        testService.$http.get('http://abbydemo.cloudapp.net/api/categories').
            then(function(response) {
                testService.$log.log(response.data);
                children[0]['name'] = response.data.categories[0]['name'];
            });
        
        triMenuProvider.addMenu({
            name: 'Category',
            icon: 'zmdi zmdi-view-module',
            type: 'dropdown',
            priority: 2.4,
            permission: 'viewLayouts',
            children: children
        });

    }
})();
