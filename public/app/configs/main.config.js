angular
  .module('project-x')
  .config(ProjectXConfig);

function ProjectXConfig($routeProvider) {
  'use strict';
  $routeProvider
    .when('/', {
      templateUrl: './app/views/home.html',
      controller: 'MainController',
      controllerAs: 'main',
      private: false
    })
    .when('/brigades', {
      templateUrl: './app/views/brigades.html',
      controller: 'brigadesController',
      controllerAs: 'brigades',
      private: false
    })
    .when('/brigades/:brigadeName', {
      templateUrl: './app/views/profile.html',
      controller: 'profileController',
      controllerAs: 'brigade',
      private: false
    })
    .otherwise({
      redirectTo: '/'
    });
}
