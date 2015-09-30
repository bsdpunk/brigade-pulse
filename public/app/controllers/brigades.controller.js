angular
    .module('project-x')
    .controller('brigadesController', brigadesController)
    .controller('profileController', profileController);

function brigadesController($http) {
    var vm = this;
    vm.brigades = [];
    $http.get('/data/home-page-data/')
        .success(function (data) {
            vm.brigades = data;
            console.log('yay')
        })

    vm.click = function(id) {
        window.document.location = '/#/brigades/' + id;
    }
}

function profileController($http, $routeParams) {
    var vm = this;
    vm.brigadeName = $routeParams.brigadeName;
    vm.brigadeDetails;
    vm.brigadeProjects;

    getBrigadeData();

    function getBrigadeData() {
        $http.get('http://codeforamerica.org/api/organizations/' + vm.brigadeName)
            .success(function (data) {
                vm.brigadeDetails = data;
            })

        $http.get('http://codeforamerica.org/api/organizations/' + vm.brigadeName + '/projects?per_page=100')
            .success(function (data) {
                vm.brigadeProjects = data.objects;
                vm.brigadeProjectsTotal = data.total;
            })
    }
};
