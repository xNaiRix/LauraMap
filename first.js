const url = 'http://10.82.19.18:8000';

document.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch(url + '/api/map');
    data = await response.json();
    var map = L.map('map', {
        center: [992.5, 3402], 
        fadeAnimation: true,
        zoom: -2,
        minZoom: -3, 
        maxZoom: 0,
        zoomSnap: 0.5,
        zoomDelta: 0.5,
        wheelPxPerZoomLevel: 60,

        maxBoundsViscosity: 1.0,
        inertia: false,
        crs: L.CRS.Simple,
        zoomControl: false,
        attributionControl: false,
    });
    var mapBounds = [[0, 0], [1985, 6804]]; 
    L.imageOverlay(url + data.map_url, mapBounds).addTo(map);
    map.setMaxBounds(mapBounds);
    document.getElementById('map').style.backgroundColor = '#6D8967';

    data.points.forEach(async point => {
        const info = await fetch(url + '/api/map/points/' + point.id +'/preview')
            .then(response => {return response.json()});
        
        const createIcon = () => {
            const zoom = map.getZoom();
            const size = (75 * Math.pow(2, zoom + 3)) * point.size / 255 * window.innerHeight / 1985;
            console.log(size)
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

        map.on('zoom', function() {
            marker.setIcon(createIcon());
        });

        marker.on('click', function() {
            let audio = null;
            if (info.audio_url) {
                audio = new Audio(url + info.audio_url);
            }

            const oldPopup = document.querySelector('.popup');
            if (oldPopup) {
                if (oldPopup._audioInstance) { 
                    oldPopup._audioInstance.pause();
                }
                oldPopup.remove();
            }

            const popup = document.createElement('div');
            popup.className = 'popup';

            popup.innerHTML = `
            <div>
                <div class="rectangle"></div>
                <button class="popup-close"><img src="images/add_green.png" alt="close"></button>
                <img class="photo" src="${url + point.avatar_url}">
                <div class="name">${info.name}</div>
                <button class="audio-btn">
                    <span class="icon"><img class="img" src="images/forward_green.png"></span>
                    <span class="pause-icon" style="display:none;"><img class="img" src="images/pause.png"></span>
                </button>
                <div class="under-road"></div>
                <img class="road" src="images/sound_road_green.png">
                <div class="info">${info.brief_info}</div>
                <button class="learn-more">УЗНАТЬ БОЛЬШЕ</button>
            </div>
            `;
            
            document.body.appendChild(popup);

            popup.querySelector('.popup-close').onclick = function() {
                if (audio) {
                    audio.pause();
                }
                popup.remove();
            };

            popup._audioInstance = audio;

            if (audio) {
                const audioBtn = popup.querySelector('.audio-btn');
                const playIcon = popup.querySelector('.icon');
                const pauseIcon = popup.querySelector('.pause-icon');
                
                audioBtn.onclick = function(e) {
                    e.stopPropagation();
                    if (audio.paused) {
                        audio.play();
                        playIcon.style.display = 'none';
                        pauseIcon.style.display = 'inline';
                    } else {
                        audio.pause();
                        playIcon.style.display = 'inline';
                        pauseIcon.style.display = 'none';
                    }
                };

                audio.addEventListener('ended', function() {
                    playIcon.style.display = 'inline';
                    pauseIcon.style.display = 'none';
                });
            }
        });
    });
});   
