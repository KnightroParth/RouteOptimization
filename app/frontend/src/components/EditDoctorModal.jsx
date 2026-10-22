import React, { useState, useEffect } from 'react';
import { X, Pencil, MapPin, Stethoscope, Phone, Clock, Building2, CheckCircle2 } from 'lucide-react';
import { doctorsAPI } from '../services/api';

export default function EditDoctorModal({ isOpen, onClose, doctor, onDoctorUpdated }) {
  const [formData, setFormData] = useState({
    name: '',
    specialization: 'Cardiology',
    hospital: '',
    territory: 'Pune Central',
    availability_start: '10:00',
    availability_end: '13:00',
    avg_consultation_time: 20,
    phone_number: '+91 98230 12345',
    prescription_volume: 'Medium',
    status: 'active',
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (doctor) {
      setFormData({
        name: doctor.name || '',
        specialization: doctor.specialization || doctor.specialty || 'Cardiology',
        hospital: doctor.hospital || '',
        territory: doctor.territory || 'Pune Central',
        availability_start: doctor.availability_start || '10:00',
        availability_end: doctor.availability_end || '13:00',
        avg_consultation_time: doctor.avg_consultation_time || 20,
        phone_number: doctor.phone_number || doctor.phone || '+91 98230 12345',
        prescription_volume: doctor.prescription_volume || 'Medium',
        status: doctor.status || 'active',
      });
      setError('');
    }
  }, [doctor]);

  if (!isOpen || !doctor) return null;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'avg_consultation_time' ? Number(value) : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.name) {
      setError('Please provide doctor name');
      return;
    }
    setError('');
    setSubmitting(true);
    try {
      const docId = doctor.id || doctor.doc_code;
      await doctorsAPI.update(docId, formData);
      if (onDoctorUpdated) {
        onDoctorUpdated({ ...doctor, ...formData });
      }
      onClose();
    } catch (err) {
      console.warn('API error updating doctor (falling back locally):', err);
      if (onDoctorUpdated) {
        onDoctorUpdated({ ...doctor, ...formData });
      }
      onClose();
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
            <h3>Edit Doctor Details</h3>
          </div>
          <button type="button" className="modal-close-btn" onClick={onClose}>
            <X size={18} />
          </button>
        </div>

        {error && <div className="alert-error-banner">{error}</div>}

        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-grid">
            <div className="form-group full">
              <label>Doctor Full Name *</label>
              <input
                type="text"
                name="name"
                placeholder="Dr. Anand Deshpande"
                value={formData.name}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label>Specialty</label>
              <select name="specialization" value={formData.specialization} onChange={handleChange}>
                <option value="Cardiology">Cardiology</option>
                <option value="Orthopedics">Orthopedics</option>
                <option value="Pediatrics">Pediatrics</option>
                <option value="Neurology">Neurology</option>
                <option value="General Medicine">General Medicine</option>
                <option value="Dermatology">Dermatology</option>
                <option value="Oncology">Oncology</option>
                <option value="Diabetology">Diabetology</option>
              </select>
            </div>

            <div className="form-group">
              <label>Prescription Volume</label>
              <select name="prescription_volume" value={formData.prescription_volume} onChange={handleChange}>
                <option value="High">High (Tier 1)</option>
                <option value="Medium">Medium (Tier 2)</option>
                <option value="Low">Low (Tier 3)</option>
              </select>
            </div>

            <div className="form-group">
              <label>Hospital / Clinic Name</label>
              <input
                type="text"
                name="hospital"
                placeholder="Deccan Heart Care"
                value={formData.hospital}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Territory / Beat</label>
              <select name="territory" value={formData.territory} onChange={handleChange}>
                <option value="Pune Central">Pune Central (Kothrud/Deccan)</option>
                <option value="Pune East">Pune East (Hadapsar)</option>
                <option value="Pune North">Pune North (Baner/Aundh)</option>
                <option value="Pune West">Pune West (Shivajinagar)</option>
                <option value="PCMC">PCMC (Pimpri-Chinchwad)</option>
                <option value="Pune South">Pune South (Katraj)</option>
              </select>
            </div>

            <div className="form-group">
              <label>Availability Start</label>
              <input
                type="time"
                name="availability_start"
                value={formData.availability_start}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Availability End</label>
              <input
                type="time"
                name="availability_end"
                value={formData.availability_end}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Status</label>
              <select name="status" value={formData.status} onChange={handleChange}>
                <option value="active">Active (Available)</option>
                <option value="on_leave">On Leave</option>
              </select>
            </div>

            <div className="form-group">
              <label>Phone / WhatsApp</label>
              <input
                type="text"
                name="phone_number"
                placeholder="+91 98230 12345"
                value={formData.phone_number}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="modal-actions">
            <button type="button" className="btn btn-secondary" onClick={onClose} disabled={submitting}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={submitting}>
              {submitting ? 'Saving...' : 'Update Doctor'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
