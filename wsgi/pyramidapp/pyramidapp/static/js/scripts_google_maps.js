var Demo = {
	//Autocomplete
	/*var input_1 = document.getElementById('from-input');
	var autocomplete_1 = new google.maps.places.Autocomplete(input_1);
	
	var input_2 = document.getElementById('to-input');
	var autocomplete_2 = new google.maps.places.Autocomplete(input_2);*/

  // HTML Nodes
  mapContainer: document.getElementById('map-container'),
  dirContainer: document.getElementById('dir-container'),
  fromInput: document.getElementById('deformField1'),
  toInput: document.getElementById('deformField2'),
  travelModeInput: document.getElementById('travel-mode-input'),
  unitInput: document.getElementById('unit-input'),

  // API Objects
  dirService: new google.maps.DirectionsService(),
  dirRenderer: new google.maps.DirectionsRenderer(),
  map: null,

  showDirections: function(dirResult, dirStatus) {
    if (dirStatus != google.maps.DirectionsStatus.OK) {
      alert('Directions failed: ' + dirStatus);
      return;
    }

    // Show directions
    Demo.dirRenderer.setMap(Demo.map);
    Demo.dirRenderer.setPanel(Demo.dirContainer);
    Demo.dirRenderer.setDirections(dirResult);
  },

  getDirections: function() {
    var fromStr = Demo.fromInput.value;
    var toStr = Demo.toInput.value;
    var dirRequest = {
      origin: fromStr,
      destination: toStr,
      travelMode: google.maps.DirectionsTravelMode.DRIVING,
      unitSystem: google.maps.DirectionsUnitSystem.METRIC,
      provideRouteAlternatives: true
    };
    Demo.dirService.route(dirRequest, Demo.showDirections);
  },

  init: function() {
    var latLng = new google.maps.LatLng(37.77493, -122.419415);
    Demo.map = new google.maps.Map(Demo.mapContainer, {
      zoom: 13,
      center: latLng,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    // Show directions onload
    Demo.getDirections();
  }
};

// Onload handler to fire off the app.
google.maps.event.addDomListener(window, 'load', Demo.init);