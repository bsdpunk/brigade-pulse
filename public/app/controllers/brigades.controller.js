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
    var projectsData = [
      [Date.UTC(2015, 0, 0), 10],
      [Date.UTC(2015, 1, 0), 20],
      [Date.UTC(2015, 2, 0), 22],
      [Date.UTC(2015, 3, 0), 23],
      [Date.UTC(2015, 4, 0), 24],
      [Date.UTC(2015, 5, 0), 24],
      [Date.UTC(2015, 6, 0), 24],
      [Date.UTC(2015, 7, 0), 24],
      [Date.UTC(2015, 8, 0), 25]
    ];
    var membershipData = [
      [Date.UTC(2015, 0, 0), 15],
      [Date.UTC(2015, 1, 0), 30],
      [Date.UTC(2015, 2, 0), 31],
      [Date.UTC(2015, 3, 0), 25],
      [Date.UTC(2015, 4, 0), 35],
      [Date.UTC(2015, 5, 0), 40],
      [Date.UTC(2015, 6, 0), 50],
      [Date.UTC(2015, 7, 0), 70],
      [Date.UTC(2015, 8, 0), 80]
    ];
    var eventAttendanceData = [
      {
        name: 'Hack Night',
        x: Date.UTC(2015, 0, 0),
        y: 15
      },{
        name: 'Hack Night',
        x: Date.UTC(2015, 1, 0),
        y: 32
      },{
        name: 'Hack Night',
        x: Date.UTC(2015, 2, 0),
        y: 26
      },{
        name: 'Hack Night',
        x: Date.UTC(2015, 3, 0),
        y: 33
      },{
        name: 'Charity Dinner',
        x: Date.UTC(2015, 3, 15),
        y: 125
      }, {
        name: 'Hack Night',
        x: Date.UTC(2015, 4, 0),
        y: 54
      },{
        name: 'Hack Night',
        x: Date.UTC(2015, 5, 0),
        y: 60
      },{
        name: 'Hack Night',
        x: Date.UTC(2015, 6, 0),
        y: 21
      }, {
        name: 'Hack Night',
        x: Date.UTC(2015, 7, 0),
        y: 49
      },{
        name: 'Hack Night',
        x: Date.UTC(2015, 8, 0),
        y: 65
      },
    ];
    $("#projects-graph").highcharts({
      chart: {
        type: 'line'
      },
      title: {
        text: 'Public Github Repos'
      },
      xAxis: {
        type: 'datetime'
      },
      yAxis: {
        title: {
          text: 'Public Github Repos'
        }
      },
      series: [{
        name: '# Repos',
        data: projectsData
      }],
      legend: {
        enabled: false
      }
    });

    $("#membership-graph").highcharts({
      chart: {
        type: 'line'
      },
      title: {
        text: 'Meetup Membership'
      },
      xAxis: {
        type: 'datetime'
      },
      yAxis: {
        title: '# Members'
      },
      series: [{
        name: 'Meetup Membership',
        data: membershipData
      }],
      legend: {
        enabled: false
      }
    });

    $("#events-graph").highcharts({
      chart: {
        type: 'line'
      },
      title: {
        text: 'Event Attendance'
      },
      xAxis: {
        type: 'datetime'
      },
      yAxis: {
        title: {
          text: 'Event Attendance'
        }
      },
      series: [{
        name: '# Attendees',
        data: eventAttendanceData
      }],
      legend: {
        enabled: false
      }
    });

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
