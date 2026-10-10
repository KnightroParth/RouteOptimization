import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap } from 'react-leaflet';
import { useEffect } from 'react';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix Leaflet default marker icons
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

// Numbered marker
function createNumberedIcon(number, color = '#18181b') {
  return L.divIcon({
    className: 'custom-marker',
    html: `<div style="
      background:${color};color:white;width:28px;height:28px;
      border-radius:50%;display:flex;align-items:center;justify-content:center;
      font-size:12px;font-weight:600;font-family:Inter,sans-serif;
      border:2px solid white;box-shadow:0 1px 4px rgba(0,0,0,0.3);
    ">${number}</div>`,
    iconSize: [28, 28],
    iconAnchor: [14, 14],
  });
}

// Depot marker (start/end)
function createDepotIcon() {
  return L.divIcon({
    className: 'custom-marker',
    html: `<div style="
      background:#22c55e;color:white;width:32px;height:32px;
      border-radius:50%;display:flex;align-items:center;justify-content:center;
      font-size:14px;font-weight:700;font-family:Inter,sans-serif;
      border:2px solid white;box-shadow:0 1px 4px rgba(0,0,0,0.3);
    ">⌂</div>`,
    iconSize: [32, 32],
    iconAnchor: [16, 16],
  });
}

// Auto-fit bounds
function FitBounds({ positions }) {
  const map = useMap();
  useEffect(() => {
    if (positions?.length > 1) {
      const bounds = L.latLngBounds(positions);
      map.fitBounds(bounds, { padding: [40, 40] });
    }
  }, [positions, map]);
  return null;
}

export default function RouteMap({ route, visits = [], center = [18.5204, 73.8567] }) {
  const hasRoute = route?.route_polyline?.length > 0;
  const hasVisits = visits.length > 0;

  // Collect all marker positions for bounds
  const allPositions = [];

  if (hasRoute) {
    route.route_polyline.forEach((p) => allPositions.push(p));
  } else if (hasVisits) {
    visits.forEach((v) => {
      if (v.doctor_latitude && v.doctor_longitude) {
        allPositions.push([v.doctor_latitude, v.doctor_longitude]);
      }
    });
  }

  return (
    <div className="map-container">
      <MapContainer center={center} zoom={13} style={{ width: '100%', height: '100%' }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {allPositions.length > 1 && <FitBounds positions={allPositions} />}

        {/* Route polyline */}
        {hasRoute && (
          <Polyline
            positions={route.route_polyline}
            pathOptions={{ color: '#18181b', weight: 3, opacity: 0.7, dashArray: '8, 4' }}
          />
        )}

        {/* Route stops */}
        {hasRoute && route.stops?.map((stop) => (
          <Marker
            key={stop.sequence_number}
            position={[stop.latitude, stop.longitude]}
            icon={createNumberedIcon(stop.sequence_number)}
          >
            <Popup>
              <div style={{ fontFamily: 'Inter, sans-serif', fontSize: 13 }}>
                <strong>{stop.doctor_name}</strong><br />
                Arrival: {stop.estimated_arrival}<br />
                Duration: {stop.service_duration} min<br />
                {stop.priority_class && <>Priority: {stop.priority_class}</>}
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Depot markers */}
        {hasRoute && route.route_polyline?.length > 0 && (
          <>
            <Marker position={route.route_polyline[0]} icon={createDepotIcon()}>
              <Popup>Start (Depot)</Popup>
            </Marker>
            {route.route_polyline.length > 1 && (
              <Marker
                position={route.route_polyline[route.route_polyline.length - 1]}
                icon={createDepotIcon()}
              >
                <Popup>End (Depot)</Popup>
              </Marker>
            )}
          </>
        )}

        {/* Fallback: show visit markers when no route */}
        {!hasRoute && hasVisits && visits.map((v, i) => {
          if (!v.doctor_latitude || !v.doctor_longitude) return null;
          return (
            <Marker
              key={v.id || i}
              position={[v.doctor_latitude, v.doctor_longitude]}
              icon={createNumberedIcon(i + 1)}
            >
              <Popup>
                <div style={{ fontFamily: 'Inter, sans-serif', fontSize: 13 }}>
                  <strong>{v.doctor_name}</strong><br />
                  {v.doctor_specialization}<br />
                  {v.priority_class && <>Priority: {v.priority_class}</>}
                </div>
              </Popup>
            </Marker>
          );
        })}
      </MapContainer>
    </div>
  );
}
