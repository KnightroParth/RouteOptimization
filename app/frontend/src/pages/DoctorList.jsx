import { useState, useEffect } from 'react';
import { doctorsAPI } from '../services/api';
import { Stethoscope, Search, MapPin, Clock, Loader2 } from 'lucide-react';

export default function DoctorList() {
  const [doctors, setDoctors] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDoctors();
  }, []);

  const loadDoctors = async () => {
    try {
      const res = await doctorsAPI.list();
      setDoctors(res.data.doctors || []);
    } catch (err) {
      console.error('Failed to load doctors:', err);
    } finally {
      setLoading(false);
    }
  };

  const filtered = doctors.filter((d) =>
    d.name?.toLowerCase().includes(search.toLowerCase()) ||
    d.specialization?.toLowerCase().includes(search.toLowerCase()) ||
    d.territory?.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) {
    return (
      <div className="page-loader">
        <Loader2 size={24} style={{ animation: 'spin 1s linear infinite' }} />
      </div>
    );
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Doctors</h2>
          <p>{doctors.length} doctors in the system</p>
        </div>
      </div>

      {/* Search */}
      <div style={{ marginBottom: 16, position: 'relative', maxWidth: 360 }}>
        <Search size={16} style={{
          position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)',
          color: 'var(--muted-foreground)',
        }} />
        <input
          id="doctor-search"
          type="text"
          className="form-input"
          placeholder="Search by name, specialization, or territory..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ paddingLeft: 36 }}
        />
      </div>

      {/* Table */}
      <div className="card">
        <div className="card-body" style={{ padding: 0 }}>
          {filtered.length > 0 ? (
            <table className="data-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Specialization</th>
                  <th>Territory</th>
                  <th>Availability</th>
                  <th>Duration</th>
                  <th>Priority</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((doc) => (
                  <tr key={doc.id}>
                    <td style={{ fontWeight: 500 }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <div style={{
                          width: 28, height: 28, borderRadius: '50%',
                          background: 'var(--muted)', display: 'flex',
                          alignItems: 'center', justifyContent: 'center',
                        }}>
                          <Stethoscope size={14} color="var(--muted-foreground)" />
                        </div>
                        {doc.name}
                      </div>
                    </td>
                    <td>{doc.specialization}</td>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 4, color: 'var(--muted-foreground)', fontSize: 13 }}>
                        <MapPin size={12} /> {doc.territory}
                      </div>
                    </td>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 4, fontSize: 13 }}>
                        <Clock size={12} color="var(--muted-foreground)" />
                        {doc.availability_start} – {doc.availability_end}
                      </div>
                    </td>
                    <td>{doc.typical_visit_duration} min</td>
                    <td>
                      {doc.priority_category && (
                        <span className={`priority-badge ${doc.priority_category}`}>
                          {doc.priority_category}
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="empty-state">
              <Stethoscope size={32} />
              <p>No doctors found</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
