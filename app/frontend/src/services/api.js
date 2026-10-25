import axios from 'axios';
import toast from 'react-hot-toast';

const API_BASE = import.meta.env.VITE_API_BASE_URL 
  || (import.meta.env.PROD ? '/api' : 'http://localhost:8000/api');

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
  timeout: 5000,
});

// Attach JWT token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle error responses with toast notifications
api.interceptors.response.use(
  (res) => {
    if (typeof res.data === 'string' && res.data.includes('<html')) {
      return Promise.reject(new Error('Backend unavailable (HTML fallback)'));
    }
    return res;
  },
  (err) => {
    const status = err.response?.status;
    const detail = err.response?.data?.detail;

    if (status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/#/login';
    } else if (status === 403) {
      toast.error(detail || 'Access denied — insufficient permissions');
    } else if (status === 422) {
      toast.error(detail || 'Validation error — please check your input');
    } else if (status >= 500) {
      toast.error('Server error — please try again later');
    } else if (!err.response) {
      toast.error('Network error — unable to reach the server');
    }

    return Promise.reject(err);
  }
);

// ── Auth ────────────────────────────────────────────────
export const authAPI = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  register: (data) => api.post('/auth/register', data),
};

// ── Doctors ─────────────────────────────────────────────
export const doctorsAPI = {
  list: (params) => api.get('/doctors', { params }),
  get: (id) => api.get(`/doctors/${id}`),
  create: (data) => api.post('/doctors', data),
  update: (id, data) => api.put(`/doctors/${id}`, data),
  delete: (id) => api.delete(`/doctors/${id}`),
};

// ── Visits ──────────────────────────────────────────────
export const visitsAPI = {
  list: (params) => api.get('/visits', { params }),
  daily: (mr_id, date) => api.get('/visits/daily', { params: { mr_id, date } }),
  create: (data) => api.post('/visits', data),
  update: (id, data) => api.put(`/visits/${id}`, data),
  updateStatus: (id, data) => api.patch(`/visits/${id}/status`, data),
  delete: (id) => api.delete(`/visits/${id}`),
};

// ── Routes ──────────────────────────────────────────────
export const routesAPI = {
  generate: (data) => api.post('/routes/generate', data),
  get: (id) => api.get(`/routes/${id}`),
  list: (params) => api.get('/routes', { params }),
};

// ── Dashboard ───────────────────────────────────────────
export const dashboardAPI = {
  mr: (mr_id, date) => api.get('/dashboard/mr', { params: { mr_id, date } }),
  manager: () => api.get('/dashboard/manager'),
};

// ── WhatsApp ────────────────────────────────────────────
export const whatsappAPI = {
  getTemplates: (data) => api.post('/whatsapp/templates', data),
  getDirectLink: (phone, message) => api.get('/whatsapp/direct-link', { params: { phone, message } }),
  sendTest: (data) => api.post('/whatsapp/send-test', data),
  getLogs: () => api.get('/whatsapp/logs'),
};

// ── ML Model ────────────────────────────────────────────
export const mlAPI = {
  getFeatureImportance: () => api.get('/ml/feature-importance'),
  runBatch: () => api.post('/ml/run-batch'),
  getResults: (params) => api.get('/ml/results', { params }),
};

// ── Settings ────────────────────────────────────────────
export const settingsAPI = {
  getProfile: () => api.get('/settings/profile'),
  updateProfile: (data) => api.patch('/settings/profile', data),
};

// ── Staff Management (Manager only) ─────────────────────
export const staffAPI = {
  list: () => api.get('/staff'),
  create: (data) => api.post('/staff', data),
  update: (userId, data) => api.patch(`/staff/${userId}`, data),
  remove: (userId) => api.delete(`/staff/${userId}`),
};
// ── Analytics ───────────────────────────────────────────
export const analyticsAPI = {
  overview: () => api.get('/analytics/overview'),
};

export default api;

