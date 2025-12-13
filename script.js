const response = await fetch(url + '/api/map');
data = await response.json();

const overlay = L.imageOverlay(url + data.map_url, mapBounds).addTo(map);
