import { useState, useEffect } from 'react';
import { staffAPI } from '../services/api';
import {
  Users, UserPlus, Trash2, Pencil, CheckCircle2, XCircle,
  Loader2, X, MapPin, Clock, Mail, Shield, Search, ChevronDown
} from 'lucide-react';

const TERRITORIES = [
  'Pune Central (Kothrud & Deccan Zone)',
  'Pune East (Hadapsar & Wanowrie)',
  'Pune North (Baner & Aundh)',
  'Pune West (Shivajinagar & FC Road)',
  'PCMC (Pimpri-Chinchwad)',
  'Pune South (Sinhagad Road & Katraj)',
  'Nagpur Central',
  'Nashik East',
  'Mumbai Western Suburbs',
  'Solapur',
];

const defaultForm = {
  name: '',
  email: '',
  password: '',
  territory: TERRITORIES[0],
  working_start: '09:30',
  working_end: '18:30',
};

const defaultEditForm = {
  name: '',
  territory: '',
  working_start: '',
  working_end: '',
};

export default function ManageStaff() {
  const [staff, setStaff] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  // Modal state
  const [showAddModal, setShowAddModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(null); // user_id to delete

  // Form state
  const [addForm, setAddForm] = useState(defaultForm);
  const [editForm, setEditForm] = useState(defaultEditForm);
  const [editTarget, setEditTarget] = useState(null);

  // Action feedback
  const [saving, setSaving] = useState(false);
  const [toast, setToast] = useState(null);

  useEffect(() => { loadStaff(); }, []);

  const showToast = (msg, type = 'success') => {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 3500);
  };

  const loadStaff = async () => {
    try {
      setLoading(true);
      const res = await staffAPI.list();
      setStaff(res.data?.staff || []);
    } catch (err) {
      console.error('Failed to load staff:', err);
      showToast('Failed to load staff list', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = async (e) => {
    e.preventDefault();
    if (!addForm.name.trim() || !addForm.email.trim() || !addForm.password.trim()) return;
    try {
      setSaving(true);
      const res = await staffAPI.create(addForm);
      const newMember = {
        user_id: res.data?.user_id || `local-${Date.now()}`,
        mr_id: res.data?.mr_id,
        name: addForm.name,
        email: addForm.email,
        territory: addForm.territory,
        working_start: addForm.working_start,
        working_end: addForm.working_end,
        status: 'active',
        created_at: new Date().toISOString(),
      };
      setStaff((prev) => [newMember, ...prev]);
      setAddForm(defaultForm);
      setShowAddModal(false);
      showToast(`${addForm.name} added successfully`);
    } catch (err) {
      showToast(err?.response?.data?.detail || 'Failed to add staff member', 'error');
    } finally {
      setSaving(false);
    }
  };

  const openEdit = (member) => {
    setEditTarget(member);
    setEditForm({
      name: member.name,
      territory: member.territory,
      working_start: member.working_start,
      working_end: member.working_end,
    });
    setShowEditModal(true);
  };

  const handleEdit = async (e) => {
    e.preventDefault();
    if (!editTarget) return;
    try {
      setSaving(true);
      await staffAPI.update(editTarget.user_id, editForm);
      setStaff((prev) =>
        prev.map((m) =>
          m.user_id === editTarget.user_id ? { ...m, ...editForm } : m
        )
      );
      setShowEditModal(false);
      setEditTarget(null);
      showToast(`${editForm.name} updated successfully`);
    } catch (err) {
      showToast(err?.response?.data?.detail || 'Failed to update staff member', 'error');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (userId) => {
    const member = staff.find((m) => m.user_id === userId);
    try {
      setSaving(true);
      await staffAPI.remove(userId);
      setStaff((prev) => prev.filter((m) => m.user_id !== userId));
      setShowDeleteConfirm(null);
      showToast(`${member?.name || 'Staff member'} removed`);
    } catch (err) {
      showToast(err?.response?.data?.detail || 'Failed to remove staff member', 'error');
    } finally {
      setSaving(false);
    }
  };

  const filtered = staff.filter(
    (m) =>
      m.name.toLowerCase().includes(search.toLowerCase()) ||
      m.email.toLowerCase().includes(search.toLowerCase()) ||
      m.territory.toLowerCase().includes(search.toLowerCase())
  );

  const activeCount = staff.filter((m) => m.status !== 'inactive').length;

  if (loading) {
    return (
      <div className="page-loader">
        <Loader2 size={24} className="animate-spin" />
      </div>
    );
  }

  return (
    <div className="manage-staff-page">
      {/* Toast */}
      {toast && (
        <div className={`staff-toast ${toast.type}`}>
          {toast.type === 'success' ? <CheckCircle2 size={15} /> : <XCircle size={15} />}
          {toast.msg}
        </div>
      )}

      {/* Page Header */}
      <div className="page-header">
        <div>
          <h2>Manage Staff</h2>
          <p>Add, edit, and remove Medical Representatives from your team</p>
        </div>
        <div className="page-header-actions">
          <span className="badge-tag">
            <Users size={14} /> {activeCount} Active MRs
          </span>
          <button
            type="button"
            className="btn btn-primary"
            onClick={() => setShowAddModal(true)}
          >
            <UserPlus size={15} /> Add New MR
          </button>
        </div>
      </div>

      {/* KPI Strip */}
      <div className="stats-grid mb-4" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(160px,1fr))' }}>
        <div className="stat-card">
          <div className="stat-card-header">
            <span className="stat-card-label">Total MRs</span>
            <div className="stat-card-icon"><Users size={16} /></div>
          </div>
          <div className="stat-card-value">{staff.length}</div>
          <div className="stat-card-subtitle">Registered representatives</div>
        </div>
        <div className="stat-card">
          <div className="stat-card-header">
            <span className="stat-card-label">Active</span>
            <div className="stat-card-icon"><CheckCircle2 size={16} /></div>
          </div>
          <div className="stat-card-value text-success">{activeCount}</div>
          <div className="stat-card-subtitle">Currently in field</div>
        </div>
        <div className="stat-card">
          <div className="stat-card-header">
            <span className="stat-card-label">Inactive</span>
            <div className="stat-card-icon"><XCircle size={16} /></div>
          </div>
          <div className="stat-card-value text-danger">{staff.length - activeCount}</div>
          <div className="stat-card-subtitle">On leave / disabled</div>
        </div>
        <div className="stat-card">
          <div className="stat-card-header">
            <span className="stat-card-label">Territories</span>
            <div className="stat-card-icon"><MapPin size={16} /></div>
          </div>
          <div className="stat-card-value">{new Set(staff.map((m) => m.territory)).size}</div>
          <div className="stat-card-subtitle">Unique zones covered</div>
        </div>
      </div>

      {/* Search + Table */}
      <div className="card">
        <div className="card-header">
          <div className="card-title-group">
            <Users size={18} />
            <h3>Field Representative Roster</h3>
          </div>
          <div className="search-input-box" style={{ width: 280 }}>
            <Search size={15} className="search-icon" />
            <input
              type="text"
              placeholder="Search by name, email, territory..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
        </div>
        <div className="card-body p-0">
          {filtered.length > 0 ? (
            <table className="data-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Territory</th>
                  <th>Shift</th>
                  <th>Status</th>
                  <th style={{ textAlign: 'right' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((member) => (
                  <tr key={member.user_id}>
                    <td>
                      <div className="d-flex align-items-center gap-2">
                        <div className="staff-avatar">
                          {member.name.split(' ').map((w) => w[0]).join('').toUpperCase().slice(0, 2)}
                        </div>
                        <div>
                          <strong className="text-dark d-block">{member.name}</strong>
                          <span className="text-muted small">MR</span>
                        </div>
                      </div>
                    </td>
                    <td>
                      <span className="text-muted small d-flex align-items-center gap-1">
                        <Mail size={12} /> {member.email}
                      </span>
                    </td>
                    <td>
                      <span className="d-flex align-items-center gap-1 text-muted small">
                        <MapPin size={12} /> {member.territory}
                      </span>
                    </td>
                    <td>
                      <span className="d-flex align-items-center gap-1 text-muted small">
                        <Clock size={12} /> {member.working_start} – {member.working_end}
                      </span>
                    </td>
                    <td>
                      <span className={`status-badge ${member.status === 'inactive' ? 'on-leave' : 'completed'}`}>
                        {member.status === 'inactive' ? 'Inactive' : 'Active'}
                      </span>
                    </td>
                    <td>
                      <div className="staff-row-actions">
                        <button
                          type="button"
                          className="btn-icon-action edit"
                          title="Edit staff member"
                          onClick={() => openEdit(member)}
                        >
                          <Pencil size={14} />
                        </button>
                        <button
                          type="button"
                          className="btn-icon-action delete"
                          title="Remove staff member"
                          onClick={() => setShowDeleteConfirm(member.user_id)}
                        >
                          <Trash2 size={14} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="empty-state">
              <Users size={32} />
              <p>{search ? `No staff found matching "${search}"` : 'No staff members yet. Add your first MR.'}</p>
            </div>
          )}
        </div>
      </div>

      {/* ── Add Modal ── */}
      {showAddModal && (
        <div className="modal-overlay" onClick={() => setShowAddModal(false)}>
          <div className="modal-panel" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div className="modal-header-left">
                <UserPlus size={18} />
                <h3>Add New Medical Representative</h3>
              </div>
              <button type="button" className="modal-close-btn" onClick={() => setShowAddModal(false)}>
                <X size={18} />
              </button>
            </div>
            <form onSubmit={handleAdd} className="modal-body">
              <div className="form-grid">
                <div className="form-group">
                  <label>Full Name <span className="required">*</span></label>
                  <input
                    type="text"
                    placeholder="e.g. Rahul Sharma"
                    value={addForm.name}
                    onChange={(e) => setAddForm({ ...addForm, name: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Email Address <span className="required">*</span></label>
                  <input
                    type="email"
                    placeholder="e.g. rahul@company.com"
                    value={addForm.email}
                    onChange={(e) => setAddForm({ ...addForm, email: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Temporary Password <span className="required">*</span></label>
                  <input
                    type="password"
                    placeholder="Min 6 characters"
                    value={addForm.password}
                    onChange={(e) => setAddForm({ ...addForm, password: e.target.value })}
                    minLength={6}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Assigned Territory <span className="required">*</span></label>
                  <select
                    value={addForm.territory}
                    onChange={(e) => setAddForm({ ...addForm, territory: e.target.value })}
                  >
                    {TERRITORIES.map((t) => (
                      <option key={t} value={t}>{t}</option>
                    ))}
                  </select>
                </div>
                <div className="form-group">
                  <label>Shift Start</label>
                  <input
                    type="time"
                    value={addForm.working_start}
                    onChange={(e) => setAddForm({ ...addForm, working_start: e.target.value })}
                  />
                </div>
                <div className="form-group">
                  <label>Shift End</label>
                  <input
                    type="time"
                    value={addForm.working_end}
                    onChange={(e) => setAddForm({ ...addForm, working_end: e.target.value })}
                  />
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-outline" onClick={() => setShowAddModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary" disabled={saving}>
                  {saving ? <><Loader2 size={14} className="animate-spin" /> Creating...</> : <><UserPlus size={14} /> Create MR</>}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ── Edit Modal ── */}
      {showEditModal && editTarget && (
        <div className="modal-overlay" onClick={() => setShowEditModal(false)}>
          <div className="modal-panel" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div className="modal-header-left">
                <Pencil size={18} />
                <h3>Edit Staff Member</h3>
              </div>
              <button type="button" className="modal-close-btn" onClick={() => setShowEditModal(false)}>
                <X size={18} />
              </button>
            </div>
            <form onSubmit={handleEdit} className="modal-body">
              <div className="form-grid">
                <div className="form-group">
                  <label>Full Name</label>
                  <input
                    type="text"
                    value={editForm.name}
                    onChange={(e) => setEditForm({ ...editForm, name: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Email</label>
                  <input type="email" value={editTarget.email} disabled style={{ opacity: 0.55 }} />
                  <span className="field-hint">Email cannot be changed</span>
                </div>
                <div className="form-group">
                  <label>Territory</label>
                  <select
                    value={editForm.territory}
                    onChange={(e) => setEditForm({ ...editForm, territory: e.target.value })}
                  >
                    {TERRITORIES.map((t) => (
                      <option key={t} value={t}>{t}</option>
                    ))}
                  </select>
                </div>
                <div className="form-group">
                  <label>Shift Start</label>
                  <input
                    type="time"
                    value={editForm.working_start}
                    onChange={(e) => setEditForm({ ...editForm, working_start: e.target.value })}
                  />
                </div>
                <div className="form-group">
                  <label>Shift End</label>
                  <input
                    type="time"
                    value={editForm.working_end}
                    onChange={(e) => setEditForm({ ...editForm, working_end: e.target.value })}
                  />
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-outline" onClick={() => setShowEditModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary" disabled={saving}>
                  {saving ? <><Loader2 size={14} className="animate-spin" /> Saving...</> : <><CheckCircle2 size={14} /> Save Changes</>}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ── Delete Confirm ── */}
      {showDeleteConfirm && (
        <div className="modal-overlay" onClick={() => setShowDeleteConfirm(null)}>
          <div className="modal-panel modal-sm" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div className="modal-header-left">
                <Trash2 size={18} style={{ color: 'var(--danger)' }} />
                <h3>Remove Staff Member</h3>
              </div>
              <button type="button" className="modal-close-btn" onClick={() => setShowDeleteConfirm(null)}>
                <X size={18} />
              </button>
            </div>
            <div className="modal-body">
              <p style={{ color: 'var(--muted-foreground)', marginBottom: 8 }}>
                You are about to remove{' '}
                <strong>{staff.find((m) => m.user_id === showDeleteConfirm)?.name}</strong> from the team.
              </p>
              <p style={{ color: 'var(--danger)', fontSize: 13 }}>
                This will delete their account, MR profile, and cannot be undone.
              </p>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-outline" onClick={() => setShowDeleteConfirm(null)}>
                Cancel
              </button>
              <button
                type="button"
                className="btn btn-danger"
                disabled={saving}
                onClick={() => handleDelete(showDeleteConfirm)}
              >
                {saving ? <><Loader2 size={14} className="animate-spin" /> Removing...</> : <><Trash2 size={14} /> Remove</>}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
