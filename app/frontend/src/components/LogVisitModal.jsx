import React, { useEffect, useState } from 'react';
import { X, ClipboardList, Calendar, Clock, Stethoscope, FileText, CheckCircle2 } from 'lucide-react';
import { visitsAPI } from '../services/api';

export default function LogVisitModal({ isOpen, onClose, onVisitLogged, doctors = [], mrId }) {
  const [formData, setFormData] = useState({
    doctor_id: '',
    doctor: '',
    specialty: '',
    date: new Date().toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric' }),
    planned: '10:00 AM',
    actual: '10:15 AM',
    outcome: 'Visited',
    notes: '',
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (doctors.length > 0 && !formData.doctor_id) {
      setFormData((previous) => ({
        ...previous,
        doctor_id: doctors[0].id,
        doctor: doctors[0].name,
        specialty: doctors[0].specialization || '',
      }));
    }
  }, [doctors, formData.doctor_id]);

  if (!isOpen) return null;

  const handleDoctorChange = (e) => {
    const selectedDoc = doctors.find((d) => d.id === e.target.value);
    setFormData((prev) => ({
      ...prev,
      doctor_id: e.target.value,
      doctor: selectedDoc?.name || '',
      specialty: selectedDoc?.specialization || '',
    }));
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.doctor_id || !mrId || !formData.notes.trim()) {
      setError('Please provide visit detailing notes');
      return;
    }
    setError('');
    setSubmitting(true);
    try {
      const newRecord = {
        id: `v-${Date.now()}`,
        date: formData.date,
        doctor: formData.doctor,
        specialty: formData.specialty,
        planned: formData.planned,
        actual: formData.outcome === 'Missed' ? '—' : formData.actual,
        outcome: formData.outcome,
        notes: formData.notes,
      };

      await visitsAPI.create({
        doctor_id: formData.doctor_id,
        mr_id: mrId,
        visit_date: new Date().toISOString().split('T')[0],
        planned_time: formData.planned,
      });

      if (onVisitLogged) onVisitLogged(newRecord);
      onClose();
    } catch (err) {
      console.error('API error logging visit:', err);
      setError(err?.response?.data?.detail || 'Unable to save visit. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="modal-backdrop">
      <div className="modal-card">
        <div className="modal-header">
          <div className="modal-title-group">
            <ClipboardList size={18} />
            <h3>Log Clinic Detailing Visit</h3>
          </div>
          <button type="button" className="modal-close-btn" onClick={onClose}>
            <X size={18} />
          </button>
        </div>

        {error && <div className="alert-error-banner">{error}</div>}

        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-grid">
            <div className="form-group">
              <label>Doctor / Clinic *</label>
              <select name="doctor" value={formData.doctor} onChange={handleDoctorChange}>
                {doctors.map((d) => (
                  <option key={d.id} value={d.id}>
                    {d.name} ({d.specialization})
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Specialty</label>
              <input
                type="text"
                name="specialty"
                value={formData.specialty}
                onChange={handleChange}
                placeholder="Specialty"
              />
            </div>

            <div className="form-group">
              <label>Visit Date</label>
              <input
                type="text"
                name="date"
                value={formData.date}
                onChange={handleChange}
                placeholder="e.g. Sep 12, 2026"
              />
            </div>

            <div className="form-group">
              <label>Visit Outcome</label>
              <select name="outcome" value={formData.outcome} onChange={handleChange}>
                <option value="Visited">Visited (Completed)</option>
                <option value="Missed">Missed (Doctor Unavailable)</option>
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
                placeholder="e.g. 10:00 AM"
              />
            </div>

            <div className="form-group">
              <label>Actual Arrival Time</label>
              <input
                type="text"
                name="actual"
                value={formData.actual}
                onChange={handleChange}
                placeholder="e.g. 10:15 AM"
                disabled={formData.outcome === 'Missed'}
              />
            </div>

            <div className="form-group full">
              <label>Field Detailing Notes & Samples Pitched *</label>
              <textarea
                name="notes"
                rows={3}
                placeholder="E.g., Presented Cardivol 50mg trial data. Physician requested 10 sample blister packs and agreed to trial switch for 5 hypertensive patients."
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
              {submitting ? 'Saving Log...' : 'Record Visit'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
