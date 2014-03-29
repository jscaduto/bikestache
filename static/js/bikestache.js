(function ( bikestache, undefined ) {
    var bikeImage = {
      url: '/static/img/bike.png',
      size: new google.maps.Size(64, 64),
      origin: new google.maps.Point(0, 0),
      anchor: new google.maps.Point(32, 32),
      scaledSize: new google.maps.Size(64, 64)
    };

    var stacheImage = {
      url: '/static/img/stache.png',
      size: new google.maps.Size(64, 64),
      origin: new google.maps.Point(0, 0),
      anchor: new google.maps.Point(32, 32),
      scaledSize: new google.maps.Size(64, 64)
    };

    var pos;

    bikestache.initialize = function () {
      // Try HTML5 geolocation
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(bikestache.postLocation, function() {
          handleNoGeolocation(true);
        });
      } else {
        // Browser doesn't support Geolocation
        handleNoGeolocation(false);
      }
    };
    function handleNoGeolocation(errorFlag) {
      var content;
      if (errorFlag) {
        content = 'Error: The Geolocation service failed.';
      } else {
        content = 'Error: Your browser doesn\'t support geolocation.';
      }

      //default to San Francisco
      var sanfran = new google.maps.LatLng(37.7577, -122.4376);

      var mapOptions = {
        position: sanfran,
        zoom: 13,
      };

      var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

      var infoOptions = {
        map: map,
        position: sanfran,
        content: content,
      };

      var infoWindow = new google.maps.InfoWindow(infoOptions);
      map.setCenter(mapOptions.position);
      // TODO: Add points to map
    }

    bikestache.postLocation = function (position) {
      var lat = position.coords.latitude;
      var lng = position.coords.longitude;

      pos = new google.maps.LatLng(lat, lng);

      $.post(
        '/get_stache', {
          latitude: lat,
          longitude: lng,
        },
        bikestache.getDirections
      );
    };

    bikestache.getDirections = function (data) {
      //create a map centered on user  
      var mapOptions = {
        zoom: 18,
      };
      var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

      var bikeMarker = new google.maps.Marker({
        icon: bikeImage,
        position: pos,
        map: map,
      });

      //if no staches found, show message and center on user
      if (data.stache == null) {
        var infoWindow = new google.maps.InfoWindow({
          map: map,
          position: pos,
          content: data.message,
        });

        map.setCenter(pos);
        return;
      }
      
      var dest = new google.maps.LatLng(data.stache.latitude, data.stache.longitude);

      var stacheMarker = new google.maps.Marker({
        icon: stacheImage,
        position: dest,
        map: map,
      });

      //create directions service
      var directionsService = new google.maps.DirectionsService();

      var request = {
        origin: pos,
        destination: dest,
        travelMode: google.maps.TravelMode.BICYCLING,
      };

      //create directions display
      var rendererOptions = {
        map: map,
        suppressMarkers: true,
      };

      var directionsDisplay = new google.maps.DirectionsRenderer(rendererOptions);

      directionsService.route(request, function(response, status) {
        if (status == google.maps.DirectionsStatus.OK) {
          directionsDisplay.setDirections(response);
        }
      });
    };
})(window.bikestache = window.bikestache || {});

google.maps.event.addDomListener(window, 'load', window.bikestache.initialize);