import React, { useState, useEffect } from 'react';
import { X, Pencil, ClipboardList, Calendar, Clock, FileText } from 'lucide-react';
import { visitsAPI } from '../services/api';

export default function EditVisitModal({ isOpen, onClose, record, onVisitUpdated }) {
  const [formData, setFormData] = useState({
    doctor: '',
    specialty: '',
    date: '',
    planned: '',
    actual: '',
    outcome: 'Visited',
    notes: '',
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (record) {
      setFormData({
        doctor: record.doctor || '',
        specialty: record.specialty || '',
        date: record.date || '',
        planned: record.planned || '',
        actual: record.actual || '',
        outcome: record.outcome || 'Visited',
        notes: record.notes || '',
      });
      setError('');
    }
  }, [record]);

  if (!isOpen || !record) return null;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.notes.trim()) {
      setError('Please provide visit detailing notes');
      return;
    }
    setError('');
    setSubmitting(true);
    try {
      const updated = {
        ...record,
        ...formData,
        actual: formData.outcome === 'Missed' ? '—' : formData.actual,
      };

      await visitsAPI.update(record.id, {
        outcome: formData.outcome,
        notes: formData.notes,
        actual_arrival: formData.actual,
        planned_time: formData.planned,
      });

      if (onVisitUpdated) onVisitUpdated(updated);
      onClose();
    } catch (err) {
      console.error('API error updating visit:', err);
      setError(err?.response?.data?.detail || 'Unable to update visit. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="modal-backdrop">
      <div className="modal-card">
        <div className="modal-header">
          <div className="modal-title-group">
            <Pencil size={18} />
            <h3>Edit Visit Record</h3>
          </div>
          <button type="button" className="modal-close-btn" onClick={onClose}>
            <X size={18} />
          </button>
        </div>

        {error && <div className="alert-error-banner">{error}</div>}

        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-grid">
            <div className="form-group">
              <label>Doctor Name</label>
              <input
                type="text"
                name="doctor"
                value={formData.doctor}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label>Specialty</label>
              <input
                type="text"
                name="specialty"
                value={formData.specialty}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Visit Date</label>
              <input
                type="text"
                name="date"
                value={formData.date}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Visit Outcome</label>
              <select name="outcome" value={formData.outcome} onChange={handleChange}>
                <option value="Visited">Visited (Completed)</option>
                <option value="Missed">Missed (Unavailable)</option>
                <option value="Rescheduled">Rescheduled</option>
              </select>
            </div>

            <div className="form-group">
              <label>Planned Time</label>
              <input
                type="text"
                name="planned"
                value={formData.planned}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Actual Arrival Time</label>
              <input
                type="text"
                name="actual"
                value={formData.actual}
                onChange={handleChange}
                disabled={formData.outcome === 'Missed'}
              />
            </div>

            <div className="form-group full">
              <label>Field Detailing Notes & Product Feedback *</label>
              <textarea
                name="notes"
                rows={3}
                value={formData.notes}
                onChange={handleChange}
                required
                style={{
                  width: '100%',
                  padding: '8px 12px',
                  borderRadius: '6px',
                  border: '1px solid #cbd5e1',
                  fontSize: '0.875rem',
                  fontFamily: 'inherit'
                }}
              />
            </div>
          </div>

          <div className="modal-actions">
            <button type="button" className="btn btn-secondary" onClick={onClose} disabled={submitting}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={submitting}>
              {submitting ? 'Updating...' : 'Update Record'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
