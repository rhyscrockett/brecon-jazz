document.addEventListener('alpine:init', () => {
  Alpine.data('venuesMap', () => ({
    map: null,
    markers: {},
    venues: [],
    async init() {
      console.log('Starting venuesMap init');

      try {
        const response = await fetch('/static/data/venues.json');
        this.venues = await response.json();
        console.log('Loaded venues data:', this.venues);
      } catch (e) {
        console.error('Failed to load venues JSON:', e);
        return;
      }

      if (!this.venues.length) {
        console.warn('No venues found in JSON.');
        return;
      }

      // Clear table to avoid duplicate rows
      const tbody = document.querySelector('#venues-table tbody');
      tbody.innerHTML = '';

      // Populate table
      this.venues.forEach(v => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td><div style="width:24px; height:24px; border-radius:50%; background-color: ${v.color};"></div></td>
          <td>${v.name}</td>
          <td>${v.desc}</td>
          <td><a href="${v.map_url}" target="_blank" rel="noopener noreferrer">
          ${v.address}</a></td>
        `;
        row.addEventListener('mouseenter', () => this.highlightMarker(v.id));
        row.addEventListener('mouseleave', () => this.resetMarker(v.id));
        tbody.appendChild(row);
      });
      console.log('Table populated with venue rows');

      // Initialize map and add markers
      this.map = L.map('venues-map').setView([this.venues[0].lat, this.venues[0].lon], 13);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
      }).addTo(this.map);
      console.log('Map initialized');

      // Track marker positions for bounds
      const positions = [];

      this.venues.forEach(v => {
        const position = [v.lat, v.lon];
        positions.push(position);

        const marker = L.circleMarker(position, {
          radius: 8,
          color: v.color,
          fillColor: v.color,
          fillOpacity: 0.6
        }).addTo(this.map);
        this.markers[v.id] = marker;
        marker.bindPopup(`<b>${v.name}</b><br>${v.desc}`);
      });
      console.log('Markers added to map');

      // Zoom map to fit all markers
      if (positions.length > 1) {
        const bounds = L.latLngBounds(positions);
        this.map.fitBounds(bounds);
      }
    },

    highlightMarker(id) {
      const marker = this.markers[id];
      if (marker) {
        marker.setStyle({ fillOpacity: 1, radius: 12 });
        marker.openPopup();
      }
    },

    resetMarker(id) {
      const marker = this.markers[id];
      if (marker) {
        marker.setStyle({ fillOpacity: 0.6, radius: 8 });
        marker.closePopup();
      }
    }
  }));
});

// Start Alpine without manual init call
window.addEventListener('DOMContentLoaded', () => {
  Alpine.start();
});
