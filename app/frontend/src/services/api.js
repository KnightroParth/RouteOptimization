import axios from 'axios';
import {
  mockUsers,
  mockDoctors,
  mockMRDashboard,
  mockVisits,
  mockGeneratedRoute,
  mockManagerDashboard,
} from './mockData';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

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
    if (err.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
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
  create: (data) => api.post('/doctors', data),
  update: (id, data) => api.put(`/doctors/${id}`, data),
  delete: (id) => api.delete(`/doctors/${id}`),
};

// ── Visits ──────────────────────────────────────────────
export const visitsAPI = {
  list: (params) => withFallback(() => api.get('/visits', { params }), mockVisits),
  daily: (mr_id, date) => withFallback(() => api.get('/visits/daily', { params: { mr_id, date } }), { visits: mockVisits }),
  create: (data) => api.post('/visits', data),
  updateStatus: async (id, data) => {
    try {
      return await api.patch(`/visits/${id}/status`, data);
    } catch {
      return { data: { id, ...data }, isDemoFallback: true };
    }
  },
};

// ── Routes ──────────────────────────────────────────────
export const routesAPI = {
  generate: (data) => withFallback(() => api.post('/routes/generate', data), mockGeneratedRoute),
  get: (id) => withFallback(() => api.get(`/routes/${id}`), mockGeneratedRoute),
  list: (params) => withFallback(() => api.get('/routes', { params }), [mockGeneratedRoute]),
};

// ── Dashboard ───────────────────────────────────────────
export const dashboardAPI = {
  mr: (mr_id, date) => withFallback(() => api.get('/dashboard/mr', { params: { mr_id, date } }), mockMRDashboard),
  manager: () => withFallback(() => api.get('/dashboard/manager'), mockManagerDashboard),
};

export default api;
