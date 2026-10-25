import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import {
  ClipboardList, CheckCircle2, XCircle, Clock, Calendar,
  Search, Filter, FileText, ArrowUpDown, Plus, Pencil, Trash2, X, AlertCircle
} from 'lucide-react';
import LogVisitModal from '../components/LogVisitModal';
import EditVisitModal from '../components/EditVisitModal';
import { doctorsAPI, visitsAPI } from '../services/api';

export default function VisitHistory() {
  const { user } = useAuth();
  const mrId = user?.mr_id;
  const [filterPeriod, setFilterPeriod] = useState('7days');
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [historyRecords, setHistoryRecords] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(true);

  // CRUD Modals
  const [isLogModalOpen, setIsLogModalOpen] = useState(false);
  const [editingRecord, setEditingRecord] = useState(null);
  const [deletingRecord, setDeletingRecord] = useState(null);
  const [toast, setToast] = useState(null);

  useEffect(() => {
    if (!mrId) return;
    const loadHistory = async () => {
      try {
        setLoading(true);
        const [visitsResponse, doctorsResponse] = await Promise.all([
          visitsAPI.list({ mr_id: mrId }),
          doctorsAPI.list(),
        ]);
        const records = (visitsResponse.data?.visits || []).map((visit) => ({
          id: visit.id,
          doctor_id: visit.doctor_id,
          date: visit.visit_date,
          doctor: visit.doctor_name || 'Unknown Doctor',
          specialty: visit.doctor_specialization || 'General',
          planned: visit.planned_time || '—',
          actual: visit.actual_arrival || '—',
          outcome: visit.status === 'completed' ? 'Visited' : visit.status === 'missed' ? 'Missed' : visit.status,
          notes: visit.outcome || visit.field_notes || '',
        }));
        setHistoryRecords(records);
        setDoctors(doctorsResponse.data?.doctors || []);
      } catch (err) {
        console.error('Failed to load visit history:', err);
        showToast('Unable to load visit history from the server', 'error');
      } finally {
        setLoading(false);
      }
    };
    loadHistory();
  }, [mrId]);

  const showToast = (message, type = 'success') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3500);
  };

  const handleVisitLogged = (newRecord) => {
    setHistoryRecords((prev) => [newRecord, ...prev]);
    showToast(`Visit for ${newRecord.doctor} logged successfully`);
  };

  if (loading) {
    return <div className="page-loader">Loading visit history...</div>;
  }

  const handleVisitUpdated = (updatedRecord) => {
    setHistoryRecords((prev) =>
      prev.map((r) => (r.id === updatedRecord.id ? updatedRecord : r))
    );
    showToast(`Visit record for ${updatedRecord.doctor} updated`);
    setEditingRecord(null);
  };

  const handleConfirmDelete = async () => {
    if (!deletingRecord) return;
    const docName = deletingRecord.doctor;
    try {
      await visitsAPI.delete(deletingRecord.id);
      setHistoryRecords((prev) => prev.filter((r) => r.id !== deletingRecord.id));
      showToast(`Visit record for ${docName} deleted`, 'success');
    } catch (err) {
      console.error('Delete error:', err);
      showToast(err?.response?.data?.detail || `Failed to delete visit record for ${docName}`, 'error');
    } finally {
      setDeletingRecord(null);
    }
  };

  const filtered = historyRecords.filter((rec) => {
    const matchesSearch =
      (rec.doctor || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
      (rec.specialty || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
      (rec.notes || '').toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus =
      statusFilter === 'all' || (rec.outcome || '').toLowerCase() === statusFilter.toLowerCase();
    return matchesSearch && matchesStatus;
  });

  const totalVisited = historyRecords.filter((r) => r.outcome === 'Visited').length;
  const totalMissed = historyRecords.filter((r) => r.outcome === 'Missed').length;
  const adherence = historyRecords.length
    ? Math.round((totalVisited / historyRecords.length) * 100)
    : 100;

  return (
    <div className="visit-history-page">
      {/* Toast Alert */}
      {toast && (
        <div style={{
          position: 'fixed',
          top: '24px',
          right: '24px',
          zIndex: 9999,
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          padding: '12px 18px',
          borderRadius: '8px',
          background: toast.type === 'error' ? '#fef2f2' : '#f0fdf4',
          color: toast.type === 'error' ? '#991b1b' : '#166534',
          border: `1px solid ${toast.type === 'error' ? '#fecaca' : '#bbf7d0'}`,
          boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
          fontWeight: 500,
          fontSize: '0.9rem'
        }}>
          {toast.type === 'error' ? <AlertCircle size={18} /> : <CheckCircle2 size={18} />}
          <span>{toast.message}</span>
        </div>
      )}

      <div className="page-header">
        <div>
          <h2>Visit History & Field Logs</h2>
          <p>Historical audit trail of completed clinic details, planned vs actual timings, and outcome notes</p>
        </div>
        <div className="page-header-actions">
          <div className="button-group-pills">
            <button
              className={`pill-btn ${filterPeriod === '7days' ? 'active' : ''}`}
              onClick={() => setFilterPeriod('7days')}
            >
              Past 7 Days
            </button>
            <button
              className={`pill-btn ${filterPeriod === '30days' ? 'active' : ''}`}
              onClick={() => setFilterPeriod('30days')}
            >
              Past 30 Days
            </button>
            <button
              className={`pill-btn ${filterPeriod === 'all' ? 'active' : ''}`}
              onClick={() => setFilterPeriod('all')}
            >
              All Records
            </button>
          </div>
          <button
            type="button"
            className="btn btn-primary"
            onClick={() => setIsLogModalOpen(true)}
          >
            <Plus size={16} /> Log New Visit
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="stats-grid mb-4">
        <div className="stat-card">
          <div className="stat-card-header">
            <span className="stat-card-label">Logged Visits</span>
            <div className="stat-card-icon"><ClipboardList size={16} /></div>
          </div>
          <div className="stat-card-value">{historyRecords.length}</div>
          <div className="stat-card-subtitle">Audited clinic appointments</div>
        </div>

        <div className="stat-card">
          <div className="stat-card-header">
            <span className="stat-card-label">Completed Detailing</span>
            <div className="stat-card-icon"><CheckCircle2 size={16} color="#22c55e" /></div>
          </div>
          <div className="stat-card-value">{totalVisited}</div>
          <div className="stat-card-subtitle">Successful doctor meetings</div>
        </div>

        <div className="stat-card">
          <div className="stat-card-header">
            <span className="stat-card-label">Missed / Postponed</span>
            <div className="stat-card-icon"><XCircle size={16} color="#ef4444" /></div>
          </div>
          <div className="stat-card-value">{totalMissed}</div>
          <div className="stat-card-subtitle">Hospital emergency / doctor leave</div>
        </div>

        <div className="stat-card">
          <div className="stat-card-header">
            <span className="stat-card-label">Schedule Adherence</span>
            <div className="stat-card-icon"><Clock size={16} /></div>
          </div>
          <div className="stat-card-value">{adherence}%</div>
          <div className="stat-card-subtitle">On-time arrival compliance</div>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="card mb-4">
        <div className="card-body py-3">
          <div className="filter-row">
            <div className="search-input-box">
              <Search size={16} className="search-icon" />
              <input
                type="text"
                placeholder="Search by doctor, specialty, or notes..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>

            <div className="filter-select-box">
              <Filter size={15} />
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
              >
                <option value="all">All Outcomes</option>
                <option value="visited">Visited Only</option>
                <option value="missed">Missed Only</option>
                <option value="rescheduled">Rescheduled Only</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* History Table */}
      <div className="card">
        <div className="card-header">
          <div className="card-title-group">
            <FileText size={18} />
            <h3>Visit History Audit Trail</h3>
          </div>
          <span className="badge-subtle">Showing {filtered.length} entries</span>
        </div>
        <div className="card-body p-0">
          {filtered.length > 0 ? (
            <table className="data-table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Doctor Clinic</th>
                  <th>Planned Time</th>
                  <th>Actual Arrival</th>
                  <th>Outcome</th>
                  <th style={{ minWidth: 260 }}>Field Representative Detailing Notes</th>
                  <th style={{ width: 100, textAlign: 'right' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((row) => (
                  <tr key={row.id}>
                    <td className="text-muted small fw-medium">{row.date}</td>
                    <td>
                      <div className="fw-semibold">{row.doctor}</div>
                      <span className="text-muted small">{row.specialty}</span>
                    </td>
                    <td>
                      <span className="time-pill planned">{row.planned}</span>
                    </td>
                    <td>
                      <span className="time-pill actual">{row.actual}</span>
                    </td>
                    <td>
                      <span className={`status-badge ${row.outcome === 'Visited' ? 'completed' : row.outcome === 'Missed' ? 'missed' : 'on-leave'}`}>
                        {row.outcome}
                      </span>
                    </td>
                    <td>
                      <p className="visit-notes-text">{row.notes}</p>
                    </td>
                    <td style={{ textAlign: 'right' }}>
                      <div style={{ display: 'inline-flex', gap: '6px', justifyContent: 'flex-end' }}>
                        <button
                          type="button"
                          className="btn-icon"
                          title="Edit Visit Record"
                          onClick={() => setEditingRecord(row)}
                          style={{
                            padding: '6px 8px',
                            borderRadius: '6px',
                            border: '1px solid #e2e8f0',
                            background: '#ffffff',
                            cursor: 'pointer',
                            color: '#475569',
                            display: 'flex',
                            alignItems: 'center',
                            transition: 'all 0.15s ease'
                          }}
                        >
                          <Pencil size={13} />
                        </button>
                        <button
                          type="button"
                          className="btn-icon text-danger"
                          title="Delete Visit Record"
                          onClick={() => setDeletingRecord(row)}
                          style={{
                            padding: '6px 8px',
                            borderRadius: '6px',
                            border: '1px solid #fee2e2',
                            background: '#ffffff',
                            cursor: 'pointer',
                            color: '#ef4444',
                            display: 'flex',
                            alignItems: 'center',
                            transition: 'all 0.15s ease'
                          }}
                        >
                          <Trash2 size={13} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="empty-state">
              <ClipboardList size={36} />
              <p>No matching visit logs found</p>
            </div>
          )}
        </div>
      </div>

      {/* Log Visit Modal */}
      <LogVisitModal
        isOpen={isLogModalOpen}
        onClose={() => setIsLogModalOpen(false)}
        onVisitLogged={handleVisitLogged}
        doctors={doctors}
        mrId={mrId}
      />

      {/* Edit Visit Modal */}
      <EditVisitModal
        isOpen={!!editingRecord}
        record={editingRecord}
        onClose={() => setEditingRecord(null)}
        onVisitUpdated={handleVisitUpdated}
      />

      {/* Delete Confirmation Modal */}
      {deletingRecord && (
        <div className="modal-backdrop">
          <div className="modal-card" style={{ maxWidth: 450 }}>
            <div className="modal-header">
              <div className="modal-title-group" style={{ color: '#ef4444' }}>
                <Trash2 size={18} />
                <h3>Delete Visit Record</h3>
              </div>
              <button type="button" className="modal-close-btn" onClick={() => setDeletingRecord(null)}>
                <X size={18} />
              </button>
            </div>
            <div style={{ padding: '1.25rem' }}>
              <p style={{ margin: 0, fontSize: '0.95rem', color: '#1e293b' }}>
                Are you sure you want to delete this visit log for <strong>{deletingRecord.doctor}</strong>?
              </p>
              <p style={{ margin: '0.5rem 0 0', fontSize: '0.825rem', color: '#64748b' }}>
                Date: {deletingRecord.date} • Outcome: {deletingRecord.outcome}
              </p>
            </div>
            <div className="modal-actions" style={{ padding: '1rem 1.25rem', background: '#f8fafc', borderTop: '1px solid #f1f5f9' }}>
              <button type="button" className="btn btn-secondary" onClick={() => setDeletingRecord(null)}>
                Cancel
              </button>
              <button
                type="button"
                className="btn btn-danger"
                onClick={handleConfirmDelete}
                style={{ background: '#ef4444', color: '#fff', border: 'none' }}
              >
                Confirm Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
