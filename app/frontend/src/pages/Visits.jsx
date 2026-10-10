import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { visitsAPI } from '../services/api';
import { CalendarDays, Loader2 } from 'lucide-react';

export default function Visits() {
  const { user } = useAuth();
  const mrId = user?.mr_id;
  const today = new Date().toISOString().split('T')[0];

  const [visits, setVisits] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!mrId) return;
    loadData();
  }, [mrId]);

  const loadData = async () => {
    try {
      setLoading(true);
      const res = await visitsAPI.daily(mrId, today);
      setVisits(res.data.visits || []);
    } catch (err) {
      console.error('Failed to load visits:', err);
    } finally {
      setLoading(false);
    }
  };

  const updateVisitStatus = async (visitId, newStatus) => {
    try {
      await visitsAPI.updateStatus(visitId, { status: newStatus });
      loadData();
    } catch (err) {
      console.error('Status update failed:', err);
    }
  };

  if (loading) {
    return (
      <div className="page-loader">
        <Loader2 size={24} className="animate-spin" style={{ animation: 'spin 1s linear infinite' }} />
      </div>
    );
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>My Visits</h2>
          <p>Detailed view of your scheduled appointments for {today}</p>
        </div>
      </div>

      <div className="card">
        <div className="card-body">
          {visits.length === 0 ? (
            <div className="empty-state">
              <CalendarDays size={32} />
              <p>No visits scheduled for today</p>
            </div>
          ) : (
            <div className="visits-list">
              {visits.map((v, i) => (
                <div className="visit-card" key={v.id}>
                  <div className="visit-sequence">{i + 1}</div>
                  <div className="visit-info">
                    <div className="visit-doctor-name">
                      {v.doctor_name || 'Unknown Doctor'}
                    </div>
                    <div className="visit-doctor-spec">
                      {v.doctor_specialization || 'General'}
                    </div>
                  </div>
                  <div className="visit-meta">
                    {v.priority_class && (
                      <span className={`priority-badge ${v.priority_class}`}>
                        {v.priority_class}
                      </span>
                    )}
                    <span className={`status-badge ${v.status}`}>
                      {v.status?.replace('_', ' ')}
                    </span>
                    {v.status === 'planned' && (
                      <button
                        className="btn btn-ghost btn-sm"
                        onClick={() => updateVisitStatus(v.id, 'in_progress')}
                      >
                        Start
                      </button>
                    )}
                    {v.status === 'in_progress' && (
                      <button
                        className="btn btn-ghost btn-sm"
                        onClick={() => updateVisitStatus(v.id, 'completed')}
                      >
                        Complete
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
