import axios from 'axios';
import {
  mockUsers,
  mockDoctors,
  mockMRDashboard,
  mockVisits,
  mockGeneratedRoute,
  mockManagerDashboard,
  mockStaff,
} from './mockData';

const API_BASE = import.meta.env.PROD 
  ? '/api' 
  : (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api');

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

// Handle 401 responses and HTML responses (Vercel SPA fallback)
api.interceptors.response.use(
  (res) => {
    if (typeof res.data === 'string' && res.data.includes('<html')) {
      return Promise.reject(new Error('Backend unavailable (HTML fallback)'));
    }
    return res;
  },
  (err) => {
    const token = localStorage.getItem('token');
    if (err.response?.status === 401 && !token?.startsWith('demo-')) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/#/login';
    }
    return Promise.reject(err);
  }
);

// Helper for demo fallback
const withFallback = async (apiCall, fallbackData) => {
  try {
    return await apiCall();
  } catch (err) {
    console.warn('Backend unavailable, using demo mode fallback:', err?.message || err);
    return { data: fallbackData, isDemoFallback: true };
  }
};

// ── Auth ────────────────────────────────────────────────
export const authAPI = {
  login: async (email, password) => {
    try {
      return await api.post('/auth/login', { email, password });
    } catch {
      // Demo fallback login
      const isMgr = (email || '').toLowerCase().includes('manager');
      return {
        data: isMgr ? mockUsers.manager : mockUsers.mr,
        isDemoFallback: true,
      };
    }
  },
  register: (data) => api.post('/auth/register', data),
};

// ── Doctors ─────────────────────────────────────────────
export const doctorsAPI = {
  list: (params) => withFallback(() => api.get('/doctors', { params }), { doctors: mockDoctors }),
  get: (id) => withFallback(() => api.get(`/doctors/${id}`), mockDoctors.find((d) => d.id === Number(id)) || mockDoctors[0]),
  create: (data) => withFallback(
    () => api.post('/doctors', data),
    { ...data, id: `doc-${Date.now()}` }
  ),
  update: (id, data) => withFallback(
    () => api.put(`/doctors/${id}`, data),
    { ...data, id }
  ),
  delete: (id) => withFallback(
    () => api.delete(`/doctors/${id}`),
    { message: 'Doctor deleted', id }
  ),
};

// ── Visits ──────────────────────────────────────────────
export const visitsAPI = {
  list: (params) => withFallback(() => api.get('/visits', { params }), mockVisits),
  daily: async (mr_id, date) => {
    try {
      const res = await api.get('/visits/daily', { params: { mr_id, date } });
      if (!res.data?.visits || res.data.visits.length === 0) {
        return { data: { visits: mockVisits }, isDemoFallback: true };
      }
      return res;
    } catch {
      return { data: { visits: mockVisits }, isDemoFallback: true };
    }
  },
  create: (data) => withFallback(
    () => api.post('/visits', data),
    { ...data, id: `visit-${Date.now()}`, status: 'planned' }
  ),
  update: (id, data) => withFallback(
    () => api.put(`/visits/${id}`, data),
    { ...data, id }
  ),
  updateStatus: async (id, data) => {
    try {
      return await api.patch(`/visits/${id}/status`, data);
    } catch {
      return { data: { id, ...data }, isDemoFallback: true };
    }
  },
  delete: (id) => withFallback(
    () => api.delete(`/visits/${id}`),
    { message: 'Visit deleted', id }
  ),
};

// ── Routes ──────────────────────────────────────────────
export const routesAPI = {
  generate: async (data) => {
    try {
      const res = await api.post('/routes/generate', data);
      if (!res.data || res.data.solver_status === 'error' || !res.data.stops?.length) {
        return { data: mockGeneratedRoute, isDemoFallback: true };
      }
      return res;
    } catch {
      return { data: mockGeneratedRoute, isDemoFallback: true };
    }
  },
  get: (id) => withFallback(() => api.get(`/routes/${id}`), mockGeneratedRoute),
  list: (params) => withFallback(() => api.get('/routes', { params }), [mockGeneratedRoute]),
};

// ── Dashboard ───────────────────────────────────────────
export const dashboardAPI = {
  mr: (mr_id, date) => withFallback(() => api.get('/dashboard/mr', { params: { mr_id, date } }), mockMRDashboard),
  manager: () => withFallback(() => api.get('/dashboard/manager'), mockManagerDashboard),
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
};

// ── Settings ────────────────────────────────────────────
export const settingsAPI = {
  getProfile: () => api.get('/settings/profile'),
  updateProfile: (data) => api.patch('/settings/profile', data),
};

// ── Staff Management (Manager only) ─────────────────────
export const staffAPI = {
  list: () => withFallback(() => api.get('/staff'), { staff: mockStaff, total: mockStaff.length }),
  create: (data) => withFallback(
    () => api.post('/staff', data),
    { message: 'Staff member created (demo)', user_id: `demo-${Date.now()}`, name: data.name, email: data.email, territory: data.territory }
  ),
  update: (userId, data) => withFallback(
    () => api.patch(`/staff/${userId}`, data),
    { message: 'Staff member updated (demo)', user_id: userId }
  ),
  remove: (userId) => withFallback(
    () => api.delete(`/staff/${userId}`),
    { message: 'Staff member removed (demo)', user_id: userId }
  ),
};

export default api;

