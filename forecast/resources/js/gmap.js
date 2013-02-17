function getLatLng() {
	var queryStr = location.search;

	if (queryStr != "") {
		var url = "http://localhost:8000/cgi-bin/location.py" + queryStr;
		var decodedName = getParameterByName("location");

		$.get(url, function(data, status) {
			if (data != null && data != "") {
				var index = data.indexOf("|");
				var latitude = null;
				var longitude = null;

				if (index != -1) {
					latitude = data.substring(0, index)
					longitude = data.substring(index + 1)
				}

				var latlng = new google.maps.LatLng(latitude, longitude);
				var mapOptions = {
					center : latlng,
					zoom : 8,
					mapTypeId : google.maps.MapTypeId.ROADMAP
				};

				var map = new google.maps.Map(document
						.getElementById("map_canvas"), mapOptions);

				var marker = new google.maps.Marker({
					position : latlng,
					map : map,
					title : decodedName
				});
				
				var contentString = "<div>Location : " + decodedName + "</div>" 
				                  + "<div>Latitude : " + latitude + "</div>"
				                  + "<div>Longitude : " + longitude + "</div>";
				var infowindow = new google.maps.InfoWindow({
				    content: contentString
				});
				
				google.maps.event.addListener(marker, 'click', function() {
					infowindow.open(map,marker);
				});
			}
		});
	}
}

function getParameterByName(name) {
    var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
    return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
}
