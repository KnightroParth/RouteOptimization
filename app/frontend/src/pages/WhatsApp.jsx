import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { doctorsAPI, whatsappAPI } from '../services/api';
import {
  MessageSquare, Send, CheckCircle2, AlertCircle, Phone,
  ExternalLink, Clock, Copy, ShieldAlert, RefreshCw
} from 'lucide-react';

export default function WhatsApp() {
  const { user } = useAuth();
  const [selectedTemplate, setSelectedTemplate] = useState('en_route');
  const [targetDoctor, setTargetDoctor] = useState('Dr. Anand Sharma');
  const [testNumber, setTestNumber] = useState('+91 98765 43210');
  const [sending, setSending] = useState(false);
  const [sentAlert, setSentAlert] = useState(false);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState('');
  const [doctors, setDoctors] = useState([]);
  const [recentLogs, setRecentLogs] = useState([]);

  useEffect(() => {
    Promise.all([doctorsAPI.list(), whatsappAPI.getLogs()])
      .then(([doctorsResponse, logsResponse]) => {
        const loadedDoctors = doctorsResponse.data?.doctors || [];
        setDoctors(loadedDoctors);
        if (loadedDoctors[0]) {
          setTargetDoctor(loadedDoctors[0].name);
        }
        setRecentLogs((logsResponse.data?.logs || []).map((log) => ({
          id: log.id,
          time: log.sent_at || '—',
          to: log.to || '—',
          doctor: '—',
          type: log.template || 'custom',
          status: log.status || 'unknown',
        })));
      })
      .catch(() => setError('Unable to load doctors or notification history.'));
  }, []);

  const templates = {
    en_route: {
      title: 'En Route / 15-Min ETA Alert',
      body: `Hello ${targetDoctor}, this is ${user?.name || 'Rahul Sharma'} from MedRoute Pharma. I am currently en route to your clinic with an estimated arrival in 15 minutes. Looking forward to our detailing session.`,
    },
    confirmation: {
      title: 'Appointment Confirmation',
      body: `Respected ${targetDoctor}, confirming our scheduled medical detailing appointment today at 11:30 AM at your clinic. Please let us know if there are any emergency schedule adjustments.`,
    },
    delayed: {
      title: 'Traffic Delay Notice',
      body: `Dear ${targetDoctor}, apologies for the slight delay due to unexpected traffic congestion on the beat route. Revised ETA is in 20 minutes (approx 12:15 PM). Thank you for your patience!`,
    },
    post_visit: {
      title: 'Post-Visit Sample Acknowledgment',
      body: `Thank you ${targetDoctor} for your valuable time today! As discussed, samples of the new cardiovascular formulation have been handed over. Wishing you a great day ahead.`,
    },
  };

  const [messageBody, setMessageBody] = useState(templates.en_route.body);

  const handleTemplateSelect = (key) => {
    setSelectedTemplate(key);
    setMessageBody(templates[key].body);
  };

  const handleOpenWhatsAppWeb = () => {
    const cleanPhone = testNumber.replace(/[^0-9]/g, '');
    const encoded = encodeURIComponent(messageBody);
    const url = `https://wa.me/${cleanPhone}?text=${encoded}`;
    window.open(url, '_blank');
  };

  const handleSendTestSandbox = async () => {
    setSending(true);
    setError('');
    try {
      await whatsappAPI.sendTest({
        to_number: testNumber,
        message: messageBody,
        template_type: selectedTemplate,
      });
      setSending(false);
      setSentAlert(true);
      setTimeout(() => setSentAlert(false), 4000);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Unable to send test notification.');
    } finally {
      setSending(false);
    }
  };

  const handleCopyText = () => {
    navigator.clipboard.writeText(messageBody);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="whatsapp-page">
      <div className="page-header">
        <div>
          <h2>WhatsApp Field Communication Hub</h2>
          <p>Strictly test mode sandbox & direct zero-verification wa.me quick messaging</p>
        </div>
        <div className="page-header-actions">
          <span className="badge-tag sandbox-tag">
            <ShieldAlert size={14} /> Test Mode • No Business Verification Required
          </span>
        </div>
      </div>

      {sentAlert && (
        <div className="alert-success-banner mb-4">
          <CheckCircle2 size={18} />
          <span>Test WhatsApp notification dispatched to sandbox receiver ({testNumber})!</span>
        </div>
      )}

      {error && <div className="alert-error-banner mb-4">{error}</div>}

      <div className="dashboard-grid mb-4">
        {/* Template Selector & Composer */}
        <div className="card">
          <div className="card-header">
            <div className="card-title-group">
              <MessageSquare size={18} />
              <h3>Doctor Notification Composer</h3>
            </div>
            <span className="badge-subtle">Quick Dispatch</span>
          </div>
          <div className="card-body">
            <div className="form-group mb-3">
              <label>Select Target Doctor</label>
              <select 
                value={targetDoctor} 
                onChange={(e) => {
                  setTargetDoctor(e.target.value);
                  setMessageBody(templates[selectedTemplate].body.replace(targetDoctor, e.target.value));
                }}
              >
                {doctors.map((doctor) => (
                  <option key={doctor.id} value={doctor.name}>
                    {doctor.name} ({doctor.specialization})
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group mb-3">
              <label>Recipient Test Phone (Safe sandbox)</label>
              <input
                type="text"
                value={testNumber}
                onChange={(e) => setTestNumber(e.target.value)}
                placeholder="+91 98765 43210"
              />
            </div>

            <div className="form-group mb-3">
              <label>Message Template</label>
              <div className="template-pills-row">
                {Object.entries(templates).map(([key, t]) => (
                  <button
                    key={key}
                    type="button"
                    className={`template-pill ${selectedTemplate === key ? 'active' : ''}`}
                    onClick={() => handleTemplateSelect(key)}
                  >
                    {t.title}
                  </button>
                ))}
              </div>
            </div>

            <div className="form-group mb-3">
              <div className="d-flex justify-content-between align-items-center mb-1">
                <label className="m-0">Customized Message Preview</label>
                <button 
                  type="button" 
                  className="btn btn-ghost btn-xs"
                  onClick={handleCopyText}
                >
                  <Copy size={12} />
                  {copied ? 'Copied!' : 'Copy Text'}
                </button>
              </div>
              <textarea
                rows={4}
                value={messageBody}
                onChange={(e) => setMessageBody(e.target.value)}
                className="message-composer-textarea"
              />
            </div>

            <div className="composer-actions">
              <button
                type="button"
                className="btn btn-secondary"
                onClick={handleSendTestSandbox}
                disabled={sending}
              >
                {sending ? <RefreshCw size={14} className="animate-spin" /> : <Send size={14} />}
                Send to Test Sandbox
              </button>

              <button
                type="button"
                className="btn btn-primary"
                onClick={handleOpenWhatsAppWeb}
              >
                <ExternalLink size={14} />
                Open in WhatsApp Web / App
              </button>
            </div>
          </div>
        </div>

        {/* Live Mobile Chat Simulation */}
        <div className="card">
          <div className="card-header">
            <div className="card-title-group">
              <Phone size={18} />
              <h3>Doctor Chat Interface Preview</h3>
            </div>
            <span className="badge-live-pulse">Simulation</span>
          </div>
          <div className="card-body p-0">
            <div className="whatsapp-preview-device">
              <div className="whatsapp-preview-header">
                <div className="chat-avatar">DR</div>
                <div className="chat-user-info">
                  <strong>{targetDoctor}</strong>
                  <span>Online • Clinic Reception</span>
                </div>
              </div>
              <div className="whatsapp-preview-messages">
                <div className="chat-bubble doctor-bubble">
                  Good morning, are you scheduled for clinic visit today?
                  <div className="chat-time">09:12 AM</div>
                </div>

                <div className="chat-bubble rep-bubble">
                  {messageBody}
                  <div className="chat-time">Just now ✓✓</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Sent Logs Table */}
        <div className="card full-width">
          <div className="card-header">
            <div className="card-title-group">
              <Clock size={18} />
              <h3>Test Dispatched Notifications Audit</h3>
            </div>
            <span className="badge-subtle">Audit Trail</span>
          </div>
          <div className="card-body p-0">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Recipient Number</th>
                  <th>Clinic / Doctor</th>
                  <th>Template Type</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {recentLogs.map((log) => (
                  <tr key={log.id}>
                    <td>{log.time}</td>
                    <td className="fw-medium">{log.to}</td>
                    <td>{log.doctor}</td>
                    <td><span className="badge-pill">{log.type}</span></td>
                    <td>
                      <span className="status-badge completed">{log.status}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
