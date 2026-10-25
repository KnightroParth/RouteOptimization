import { useState, useEffect } from 'react';
import { doctorsAPI } from '../services/api';
import {
  Stethoscope, Search, MapPin, Clock, Loader2,
  Plus, Building2, ChevronLeft, ChevronRight, Filter,
  Pencil, Trash2, X, CheckCircle2, AlertCircle
} from 'lucide-react';
import AddDoctorModal from '../components/AddDoctorModal';
import EditDoctorModal from '../components/EditDoctorModal';

export default function DoctorList() {
  const [doctors, setDoctors] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [editingDoctor, setEditingDoctor] = useState(null);
  const [deletingDoctor, setDeletingDoctor] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [toast, setToast] = useState(null);
  const itemsPerPage = 8;

  useEffect(() => {
    loadDoctors();
  }, []);

  const showToast = (message, type = 'success') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3500);
  };

  const loadDoctors = async () => {
    try {
      setLoading(true);
      const res = await doctorsAPI.list();
      setDoctors(res.data.doctors || []);
    } catch (err) {
      console.error('Failed to load doctors:', err);
      showToast('Failed to load doctors from the server', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleDoctorAdded = () => {
    showToast('New doctor successfully added to network');
    loadDoctors();
  };

  const handleDoctorUpdated = (updatedDoc) => {
    setDoctors((prev) =>
      prev.map((d) => ((d.id === updatedDoc.id || d.doc_code === updatedDoc.doc_code) ? updatedDoc : d))
    );
    showToast(`${updatedDoc.name} updated successfully`);
    setEditingDoctor(null);
  };

  const handleConfirmDelete = async () => {
    if (!deletingDoctor) return;
    const targetId = deletingDoctor.id || deletingDoctor.doc_code;
    const docName = deletingDoctor.name;
    try {
      await doctorsAPI.delete(targetId);
      setDoctors((prev) => prev.filter((d) => (d.id !== targetId && d.doc_code !== targetId)));
      showToast(`${docName} removed from network`, 'success');
    } catch (err) {
      console.error('API error deleting doctor:', err);
      showToast(err?.response?.data?.detail || `Failed to remove ${docName}`, 'error');
    } finally {
      setDeletingDoctor(null);
    }
  };

  const filtered = doctors.filter((d) =>
    (d.name || '').toLowerCase().includes(search.toLowerCase()) ||
    (d.specialization || d.specialty || '').toLowerCase().includes(search.toLowerCase()) ||
    (d.territory || '').toLowerCase().includes(search.toLowerCase())
  );

  const totalPages = Math.ceil(filtered.length / itemsPerPage) || 1;
  const paginatedDoctors = filtered.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  if (loading) {
    return (
      <div className="page-loader">
        <Loader2 size={24} style={{ animation: 'spin 1s linear infinite' }} />
      </div>
    );
  }

  return (
    <div className="doctor-list-page">
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
          <h2>Doctors</h2>
          <p>Assigned clinic network, prescription potential metrics, and visit recency</p>
        </div>
        <div className="page-header-actions">
          <span className="badge-tag">
            <Building2 size={14} /> Total Assigned: {doctors.length} Clinics
          </span>
          <button 
            type="button" 
            className="btn btn-primary"
            onClick={() => setIsAddModalOpen(true)}
          >
            <Plus size={16} /> Add New Doctor
          </button>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="card mb-4">
        <div className="card-body py-3">
          <div className="filter-row">
            <div className="search-input-box">
              <Search size={16} className="search-icon" />
              <input
                id="doctor-search"
                type="text"
                placeholder="Search by doctor name, specialty, or territory..."
                value={search}
                onChange={(e) => {
                  setSearch(e.target.value);
                  setCurrentPage(1);
                }}
              />
            </div>
            <div className="text-muted small">
              Showing {paginatedDoctors.length} of {filtered.length} doctors
            </div>
          </div>
        </div>
      </div>

      {/* Table */}
      <div className="card">
        <div className="card-body p-0">
          {paginatedDoctors.length > 0 ? (
            <table className="data-table">
              <thead>
                <tr>
                  <th style={{ width: 80 }}>ID</th>
                  <th>Doctor Name</th>
                  <th>Specialty</th>
                  <th>Zone / Territory</th>
                  <th>Prescription Vol.</th>
                  <th>Last Visit</th>
                  <th>Status</th>
                  <th style={{ width: 100, textAlign: 'right' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {paginatedDoctors.map((doc) => (
                  <tr key={doc.id || doc.doc_code}>
                    <td>
                      <span className="text-muted font-mono small fw-semibold">
                        {doc.doc_code || `D${doc.id}`}
                      </span>
                    </td>
                    <td>
                      <div className="d-flex align-items-center gap-2">
                        <div className="doc-avatar-circle">
                          <Stethoscope size={14} />
                        </div>
                        <div>
                          <strong className="text-dark d-block">{doc.name}</strong>
                          {doc.hospital && (
                            <span className="text-muted text-xs">{doc.hospital}</span>
                          )}
                        </div>
                      </div>
                    </td>
                    <td>{doc.specialization || doc.specialty}</td>
                    <td>
                      <div className="d-flex align-items-center gap-1 text-muted small">
                        <MapPin size={12} />
                        <span>{doc.territory}</span>
                      </div>
                    </td>
                    <td>
                      <span className={`volume-badge volume-${(doc.prescription_volume || 'medium').toLowerCase()}`}>
                        {doc.prescription_volume || 'Medium'}
                      </span>
                    </td>
                    <td>
                      <span className="text-muted small">
                        {doc.last_visit_days ? `${doc.last_visit_days} days ago` : '20 days ago'}
                      </span>
                    </td>
                    <td>
                      <span className={`status-badge ${doc.status === 'on_leave' ? 'on-leave' : 'completed'}`}>
                        {doc.status === 'on_leave' ? 'On Leave' : 'Active'}
                      </span>
                    </td>
                    <td style={{ textAlign: 'right' }}>
                      <div style={{ display: 'inline-flex', gap: '6px', justifyContent: 'flex-end' }}>
                        <button
                          type="button"
                          className="btn-icon"
                          title="Edit Doctor"
                          onClick={() => setEditingDoctor(doc)}
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
                          title="Delete Doctor"
                          onClick={() => setDeletingDoctor(doc)}
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
              <Stethoscope size={36} />
              <p>No matching doctors found for "{search}"</p>
            </div>
          )}
        </div>

        {/* Pagination Controls */}
        {totalPages > 1 && (
          <div className="pagination-bar">
            <button
              className="pagination-btn"
              disabled={currentPage === 1}
              onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
            >
              <ChevronLeft size={16} /> Prev
            </button>
            <div className="pagination-pages">
              {Array.from({ length: totalPages }).map((_, i) => (
                <button
                  key={i + 1}
                  className={`pagination-number ${currentPage === i + 1 ? 'active' : ''}`}
                  onClick={() => setCurrentPage(i + 1)}
                >
                  {i + 1}
                </button>
              ))}
            </div>
            <button
              className="pagination-btn"
              disabled={currentPage === totalPages}
              onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
            >
              Next <ChevronRight size={16} />
            </button>
          </div>
        )}
      </div>

      {/* Add Doctor Modal */}
      <AddDoctorModal
        isOpen={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
        onDoctorAdded={handleDoctorAdded}
      />

      {/* Edit Doctor Modal */}
      <EditDoctorModal
        isOpen={!!editingDoctor}
        doctor={editingDoctor}
        onClose={() => setEditingDoctor(null)}
        onDoctorUpdated={handleDoctorUpdated}
      />

      {/* Delete Confirmation Modal */}
      {deletingDoctor && (
        <div className="modal-backdrop">
          <div className="modal-card" style={{ maxWidth: 450 }}>
            <div className="modal-header">
              <div className="modal-title-group" style={{ color: '#ef4444' }}>
                <Trash2 size={18} />
                <h3>Delete Doctor</h3>
              </div>
              <button type="button" className="modal-close-btn" onClick={() => setDeletingDoctor(null)}>
                <X size={18} />
              </button>
            </div>
            <div style={{ padding: '1.25rem' }}>
              <p style={{ margin: 0, fontSize: '0.95rem', color: '#1e293b' }}>
                Are you sure you want to remove <strong>{deletingDoctor.name}</strong> from the clinic directory?
              </p>
              <p style={{ margin: '0.5rem 0 0', fontSize: '0.825rem', color: '#64748b' }}>
                Specialty: {deletingDoctor.specialization || deletingDoctor.specialty} • Territory: {deletingDoctor.territory}
              </p>
            </div>
            <div className="modal-actions" style={{ padding: '1rem 1.25rem', background: '#f8fafc', borderTop: '1px solid #f1f5f9' }}>
              <button type="button" className="btn btn-secondary" onClick={() => setDeletingDoctor(null)}>
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
