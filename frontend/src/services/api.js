import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

// Attach JWT to every request
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => Promise.reject(error)
);

// Auto-logout on 401
api.interceptors.response.use(
  (res) => res,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;

// ── Auth ─────────────────────────────────────────
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login:    (data) => api.post('/auth/login', data),
  me:       ()     => api.get('/auth/me'),
  logout:   ()     => api.post('/auth/logout'),
};

// ── Resume ────────────────────────────────────────
export const resumeAPI = {
  upload:  (file)      => {
    const fd = new FormData();
    fd.append('file', file);
    return api.post('/resume/upload', fd, { headers: { 'Content-Type': 'multipart/form-data' } });
  },
  list:    ()          => api.get('/resume/'),
  delete:  (id)        => api.delete(`/resume/${id}`),
};

// ── Job Description ───────────────────────────────
export const jdAPI = {
  upload: (description) => api.post('/jd/upload', { description }),
  list:   ()            => api.get('/jd/'),
};

// ── Interview ─────────────────────────────────────
export const interviewAPI = {
  start:        (resume_id, jd_id) => api.post('/interview/start', { resume_id, jd_id }),
  submitAnswer: (question_id, answer_text) => api.post('/interview/answer', { question_id, answer_text }),
};

// ── Reports ───────────────────────────────────────
export const reportsAPI = {
  generate: (session_id) => api.get(`/report/${session_id}`),
  downloadPdf: (report_id) => {
    const token = localStorage.getItem('token');
    return `${API_BASE_URL}/report/${report_id}/pdf${token ? `?token=${encodeURIComponent(token)}` : ''}`;
  },
};

// ── Dashboard ─────────────────────────────────────
export const dashboardAPI = {
  get: () => api.get('/dashboard/'),
};
