(() => {
  const container = document.getElementById('base-map');
  if (!container) return;
  const status = container.querySelector('[role="status"]');
  const showFallback = () => {
    status.textContent = 'Картата не се зареди. Отворете точната локация чрез Google Maps.';
    status.hidden = false;
  };
  const initialize = () => {
    const script = document.createElement('script');
    script.src = container.dataset.library;
    script.onerror = showFallback;
    script.onload = () => {
      if (!window.L) { showFallback(); return; }
      const point = [Number(container.dataset.lat), Number(container.dataset.lng)];
      const map = L.map(container, {
        center: point, zoom: 16, minZoom: 10, maxZoom: 21,
        scrollWheelZoom: false,
        dragging: !window.matchMedia('(pointer: coarse)').matches,
        zoomControl: false,
        attributionControl: false
      });
      L.control.zoom({position: 'topright', zoomInTitle: 'Приближи', zoomOutTitle: 'Отдалечи'}).addTo(map);
      const tiles = L.tileLayer('https://{s}.google.com/vt/lyrs=y&hl=bg&x={x}&y={y}&z={z}&scale=2', {
        maxZoom: 21,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
        attribution: '&copy; <a href="https://maps.google.com/">Google Maps</a>'
      });
      let loaded = false;
      tiles.on('tileload', () => { loaded = true; status.hidden = true; });
      tiles.on('tileerror', () => { if (!loaded) showFallback(); });
      tiles.addTo(map);
      const icon = L.divIcon({
        className: 'base-map-pin', iconSize: [40, 40], iconAnchor: [20, 40], tooltipAnchor: [0, -40],
        html: '<svg width="40" height="40" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path fill="#E53935" stroke="#FFFFFF" stroke-width="2" d="M20,1 C11.716,1 5,7.716 5,16 C5,24.284 20,39 20,39 C20,39 35,24.284 35,16 C35,7.716 28.284,1 20,1 Z"/><circle cx="20" cy="16" r="6" fill="white"/></svg>'
      });
      L.marker(point, {icon, title: 'МАГИМИЛ — база Терамис', alt: 'МАГИМИЛ — база Терамис'})
        .addTo(map).bindTooltip('МАГИМИЛ', {direction: 'top'});
    };
    document.head.appendChild(script);
  };
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      if (entries.some(entry => entry.isIntersecting)) {
        observer.disconnect(); initialize();
      }
    }, {rootMargin: '300px'});
    observer.observe(container);
  } else initialize();
})();
