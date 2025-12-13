const url = 'http://10.82.168.73:8000';

document.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch(url + '/api/map');
    data = await response.json();
    var map = L.map('map', {
        center: [992.5, 3402], 
        fadeAnimation: true,
        zoom: -2,
        minZoom: -3, 
        maxZoom: 0,
        maxBoundsViscosity: 1.0,
        inertia: false,
        crs: L.CRS.Simple,
        zoomControl: false,
        attributionControl: false
    });
    map.options.crs.transformation = new L.Transformation(1, 0, -1, 0);
    var mapBounds = [[0, 0], [1985, 6804]]; 
    const overlay = L.imageOverlay(url + data.map_url, mapBounds).addTo(map);
    map.setMaxBounds(mapBounds);
    document.getElementById('map').style.backgroundColor = '#30462D';

    data.points.forEach(point => {
        
        const createIcon = () => {
            const zoom = map.getZoom();
            const size = point.size * 0.3 * zoom;
            return L.divIcon({
                className: 'animal-marker',
                html: `<div class="animal-circle" style="
                            width: ${size}px;
                            height: ${size}px;
                            border-radius: 50%;
                            overflow: hidden;
                        ">
                        <img src="${url + point.avatar_url}" 
                            style="width:100%; height:100%; object-fit: cover;">
                        </div>`,
                iconSize: [size, size],
                iconAnchor: [size / 2, size / 2]
            });
        };
            
        const marker = L.marker([point.y, point.x], {icon: createIcon(), title: point.name}).addTo(map)
            .bindPopup(`
                <div class="mini-page" style="padding: 5px;">
                    <h3>${point.name}</h3>
                    <p>kjsndsndksdnskjdnskjdnsdndkjnsdknsdnsdksdnsdnsk <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br> djdjdkjjfkdfndk</p>
                </div>`, {
                    autoPan: false,
                    closeButton: true,
                    className: 'custom-popup',
                    offset: L.point(0, 0)
                });

        marker.on('click', function() {
                this.openPopup();
        });

        map.on('zoom', function() {
            marker.setIcon(createIcon());
        });
    });

    
});        
