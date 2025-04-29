const map = L.map('map').setView([-15, -55], 4);
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
      maxZoom: 19,
      attribution: 'Tiles © Esri — Source: Esri, Maxar, Earthstar Geographics'
    }).addTo(map);
  
    let georasterLayer, georaster, bounds;
  
    fetch('geotiff/img/teste.tif')
      .then(response => response.arrayBuffer())
      .then(arrayBuffer => parseGeoraster(arrayBuffer))
      .then(parsed => {
        georaster = parsed;
  
        georasterLayer = new GeoRasterLayer({
          georaster: georaster,
          opacity: 0.9,
          pixelValuesToColorFn: values => {
            const ndvi = values[0]; // Single-band NDVI raster
            if (ndvi === null || ndvi === undefined) return null;
            const green = Math.round(255 * Math.max(0, Math.min(1, ndvi)));
            return `rgb(0, ${green}, 0)`;
          },
          resolution: 64
        });
        bounds = [[georasterLayer.getBounds()._southWest.lat, georasterLayer.getBounds()._southWest.lng], [georasterLayer.getBounds()._northEast.lat, georasterLayer.getBounds()._northEast.lng]]
        //georasterLayer.addTo(map);
        fetch('geotiff/img/teste.png')
          .then(response => response.blob())
          .then(blob => {
            const imageUrl = URL.createObjectURL(blob);
            L.imageOverlay(imageUrl, bounds).addTo(map);
          });
      });



    function focusOnImage() {
      if (georasterLayer) {
        map.fitBounds(georasterLayer.getBounds());
      }
    }

    // Variable to store the current marker
    let currentMarker = null;

    // On click event on map
    map.on("click", function (event) {
      var lat = event.latlng.lat;
      var lng = event.latlng.lng;
      var value = geoblaze.identify(georaster, [lng, lat]);

      // If there's already a marker, remove it
      if (currentMarker) {
        map.removeLayer(currentMarker);
      }

      // Create new marker
      currentMarker = L.marker([lat, lng])
        .addTo(map)
        .bindPopup("Raster Value: " + value)
        .openPopup();
    });