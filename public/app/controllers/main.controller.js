angular
  .module('project-x')
  .controller('MainController', MainController);

function MainController($http, $routeParams) {
  var vm = this;
  loadMap();

  function loadMap() {
      var mapOptions = {
        center: {
          lat: 42.879094,
          lng: -97.381205
        },
        zoom: 4,
        styles: [{
          "stylers": [{
            "visibility": "on"
          }, {
            "saturation": -100
          }, {
            "gamma": 0.54
          }]
        }, {
          "featureType": "road",
          "elementType": "labels.icon",
          "stylers": [{
            "visibility": "off"
          }]
        }, {
          "featureType": "water",
          "stylers": [{
            "color": "#4d4946"
          }]
        }, {
          "featureType": "poi",
          "elementType": "labels.icon",
          "stylers": [{
            "visibility": "off"
          }]
        }, {
          "featureType": "poi",
          "elementType": "labels.text",
          "stylers": [{
            "visibility": "simplified"
          }]
        }, {
          "featureType": "road",
          "elementType": "geometry.fill",
          "stylers": [{
            "color": "#ffffff"
          }]
        }, {
          "featureType": "road.local",
          "elementType": "labels.text",
          "stylers": [{
            "visibility": "simplified"
          }]
        }, {
          "featureType": "water",
          "elementType": "labels.text.fill",
          "stylers": [{
            "color": "#ffffff"
          }]
        }, {
          "featureType": "transit.line",
          "elementType": "geometry",
          "stylers": [{
            "gamma": 0.48
          }]
        }, {
          "featureType": "transit.station",
          "elementType": "labels.icon",
          "stylers": [{
            "visibility": "off"
          }]
        }, {
          "featureType": "road",
          "elementType": "geometry.stroke",
          "stylers": [{
            "gamma": 7.18
          }]
        }]
      };
      var map = new google.maps.Map(document.getElementById('map-canvas'),
        mapOptions);

      var heatmapData = [];
      var weightLookUp;
      $.getJSON("./brigade_weights.json", function(data){weightLookUp = data});
      var heatmap;

      var marker;
      var markers = [];
      vm.brigades = [];

      $http.get('/data/home-page-data/').
      success(function(data) {
        $.each(data, function(index, value) {
          marker = new google.maps.Marker({
            position: new google.maps.LatLng(value.latitude, value.longitude),
            title: value.name,
            url: "#/brigades/" + value.name,
            icon: './pin.png'
            });
          markers.push(marker);
          vm.brigades.push([value.name, value.growth_metric || 0, value.city]);

          heatmapData.push({
            location: new google.maps.LatLng(value.latitude, value.longitude), weight: Math.max(0, value.members)
          });

        });

        for (i = 0; i < markers.length; i++) {
          google.maps.event.addListener(markers[i], 'click', function () {
            window.location.href = this.url
          });
          markers[i].setMap(map)
        }

        vm.brigade_rows = [
            [vm.brigades[0],vm.brigades[2],vm.brigades[4],vm.brigades[6],vm.brigades[8]],
            [vm.brigades[1],vm.brigades[3],vm.brigades[5],vm.brigades[7],vm.brigades[9]]
        ];


        var heatmapGradient = [
          'rgba(0, 255, 255, 0)',
          'rgba(0, 255, 255, 1)',
          'rgba(0, 63, 255, 1)',
          'rgba(255, 0, 91, 1)',
          'rgba(255, 0, 63, 1)',
          'rgba(255, 0, 31, 1)',
          'rgba(255, 0, 20, 1)',
          'rgba(255, 0, 10, 1)',
          'rgba(255, 0, 5, 1)',
          'rgba(255, 0, 0, 1)'
        ];

    heatmap = new google.maps.visualization.HeatmapLayer({
      data: heatmapData,
      radius: 30
    });
    heatmap.setMap(map);
  });
 }
}


