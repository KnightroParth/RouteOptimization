import { useState, useEffect, useCallback, useMemo } from 'react';
import { GoogleMap, useJsApiLoader, MarkerF, PolylineF, InfoWindowF, DirectionsRenderer } from '@react-google-maps/api';

const containerStyle = {
  width: '100%',
  height: '100%'
};

export default function RouteMap({ route, visits = [], center = { lat: 18.5204, lng: 73.8567 } }) {
  const { isLoaded } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY || 'AIzaSyDuPXC5543bzlypo_9p-scoIRxSasKCOjM',
  });

  const [map, setMap] = useState(null);
  const [activeMarker, setActiveMarker] = useState(null);

  const hasRoute = route?.route_polyline?.length > 0 || route?.stops?.length > 0;
  const hasVisits = visits.length > 0;

  const [directions, setDirections] = useState(null);

  useEffect(() => {
    if (!isLoaded || !hasRoute || !route.stops || route.stops.length < 2 || !window.google?.maps?.DirectionsService) return;
    
    const directionsService = new window.google.maps.DirectionsService();
    const origin = { lat: Number(route.stops[0].latitude), lng: Number(route.stops[0].longitude) };
    const destination = { lat: Number(route.stops[route.stops.length - 1].latitude), lng: Number(route.stops[route.stops.length - 1].longitude) };
    
    const waypoints = route.stops.slice(1, -1).map(stop => ({
      location: { lat: Number(stop.latitude), lng: Number(stop.longitude) },
      stopover: true
    }));

    directionsService.route(
      {
        origin: origin,
        destination: destination,
        waypoints: waypoints,
        travelMode: window.google.maps.TravelMode.DRIVING
      },
      (result, status) => {
        if (status === window.google.maps.DirectionsStatus.OK) {
          setDirections(result);
        }
      }
    );
  }, [route, hasRoute, isLoaded]);

  const allPositions = useMemo(() => {
    const positions = [];
    if (hasRoute) {
      route.route_polyline.forEach(p => positions.push({ lat: p[0], lng: p[1] }));
    } else if (hasVisits) {
      visits.forEach(v => {
        if (v.doctor_latitude && v.doctor_longitude) {
          positions.push({ lat: v.doctor_latitude, lng: v.doctor_longitude });
        }
      });
    }
    return positions;
  }, [route, visits, hasRoute, hasVisits]);

  const onLoad = useCallback(function callback(map) {
    if (allPositions.length > 1) {
      const bounds = new window.google.maps.LatLngBounds();
      allPositions.forEach(p => bounds.extend(p));
      map.fitBounds(bounds);
    }
    setMap(map);
  }, [allPositions]);

  const onUnmount = useCallback(function callback(map) {
    setMap(null);
  }, []);

  useEffect(() => {
    if (map && allPositions.length > 1) {
      const bounds = new window.google.maps.LatLngBounds();
      allPositions.forEach(p => bounds.extend(p));
      map.fitBounds(bounds);
    }
  }, [allPositions, map]);

  if (!isLoaded) return <div className="page-loader">Loading Maps...</div>;

  return (
    <div className="map-container">
      <GoogleMap
        mapContainerStyle={containerStyle}
        center={center}
        zoom={13}
        onLoad={onLoad}
        onUnmount={onUnmount}
        options={{ disableDefaultUI: true, zoomControl: true }}
      >
        {/* Beautiful Road-Snapped Polyline */}
        {hasRoute && route.route_polyline?.length > 0 && (
          <PolylineF
            path={allPositions}
            options={{ strokeColor: '#2563eb', strokeWeight: 5, strokeOpacity: 0.8 }}
          />
        )}

        {/* Route stops */}
        {hasRoute && route.stops?.map((stop, i) => {
          // Check if the visit is completed. Since stops don't have status, we find the matching visit!
          const matchingVisit = visits.find(v => v.doctor_name === stop.doctor_name);
          const isCompleted = matchingVisit?.status === 'completed';
          
          return (
            <MarkerF
              key={`stop-${stop.sequence_number}`}
              position={{ lat: Number(stop.latitude), lng: Number(stop.longitude) }}
              icon={isCompleted ? 'http://maps.google.com/mapfiles/ms/icons/green-dot.png' : 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'}
              label={{ text: String(stop.sequence_number), color: 'white', fontWeight: 'bold' }}
              onClick={() => setActiveMarker(stop.sequence_number)}
            >
              {activeMarker === stop.sequence_number && (
                <InfoWindowF onCloseClick={() => setActiveMarker(null)}>
                  <div style={{ fontFamily: 'Inter, sans-serif', fontSize: 13, color: '#000' }}>
                    <strong>{stop.doctor_name}</strong><br />
                    Arrival: {stop.estimated_arrival}<br />
                    Duration: {stop.service_duration} min<br />
                    {stop.priority_class && <>Priority: {stop.priority_class}</>}
                  </div>
                </InfoWindowF>
              )}
            </MarkerF>
          );
        })}

        {/* Fallback visits */}
        {!hasRoute && hasVisits && visits.map((v, i) => {
          if (!v.doctor_latitude || !v.doctor_longitude) return null;
          return (
            <MarkerF
              key={`visit-${v.id || i}`}
              position={{ lat: Number(v.doctor_latitude), lng: Number(v.doctor_longitude) }}
              icon={v.status === 'completed' ? 'http://maps.google.com/mapfiles/ms/icons/green-dot.png' : 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'}
              label={{ text: String(i + 1), color: 'white', fontWeight: 'bold' }}
              onClick={() => setActiveMarker(v.id || i)}
            >
              {activeMarker === (v.id || i) && (
                <InfoWindowF onCloseClick={() => setActiveMarker(null)}>
                  <div style={{ fontFamily: 'Inter, sans-serif', fontSize: 13, color: '#000' }}>
                    <strong>{v.doctor_name}</strong><br />
                    {v.doctor_specialization}<br />
                    {v.priority_class && <>Priority: {v.priority_class}</>}
                  </div>
                </InfoWindowF>
              )}
            </MarkerF>
          );
        })}
      </GoogleMap>
    </div>
  );
}
