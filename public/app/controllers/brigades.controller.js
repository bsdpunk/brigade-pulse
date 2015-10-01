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
        });

    vm.click = function (id) {
        window.document.location = '/#/brigades/' + id;
    }
}

function profileController($http, $routeParams) {
    var vm = this;
    vm.brigadeName = $routeParams.brigadeName;

    $http.get('/data/brigade-profile-data/' + vm.brigadeName)
        .success(function (data) {
            vm.data = data;
            vm.meetup_members_time_series_js = [];
            for (var i = 0; i < data.meetup_members_time_series.length; ++i) {
                var ts = data.meetup_members_time_series[i];
                vm.meetup_members_time_series_js.push([ts.day, parseInt(ts.members)])
            }
            vm.repos_time_series_js = [];
            for (var i = 0; i < data.repos_time_series.length; ++i) {
                var ts = data.repos_time_series[i];
                vm.repos_time_series_js.push([ts.day, ts.repos])
            }
            vm.meetup_events_time_series_js = [];
            for (var i = 0; i < data.meetup_events_time_series.length; ++i) {
                var ts = data.meetup_events_time_series[i];
                vm.meetup_events_time_series_js.push(
                    {
                        name: ts.name,
                        x: ts.day,
                        y: ts.headcount
                    })
            }
            console.log(vm);
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
                    data: vm.repos_time_series_js
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
                    data: vm.meetup_members_time_series_js
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
                    data: vm.meetup_events_time_series_js
                }],
                legend: {
                    enabled: false
                }
            });
        });


}
