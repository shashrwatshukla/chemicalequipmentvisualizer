import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use((config) => {
  const csrfToken = getCookie('csrftoken');
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const api = {
  // Authentication
  login: (username, password) => {
    return apiClient.post('/login/', { username, password });
  },

  register: (username, email, password) => {
    return apiClient.post('/register/', { username, email, password });
  },

  verifyEmail: (username, code) => {
    return apiClient.post('/verify-email/', { username, code });
  },

  googleAuth: (token) => {
    return apiClient.post('/auth/google/', { token });
  },

  forgotPassword: (email) => {
    return apiClient.post('/forgot-password/', { email });
  },

  resetPassword: (email, code, new_password) => {
    return apiClient.post('/reset-password/', { email, code, new_password });
  },

  logout: () => {
    return apiClient.post('/logout/');
  },

  getCurrentUser: () => {
    return apiClient.get('/user/');
  },

  // Settings
  changePassword: (current_password, new_password) => {
    return apiClient.post('/settings/change-password/', { current_password, new_password });
  },

  deleteAccount: (password) => {
    return apiClient.post('/settings/delete-account/', { password });
  },

  // Datasets
  uploadDataset: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return apiClient.post('/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  getDatasets: () => {
    return apiClient.get('/datasets/');
  },

  getDatasetDetail: (id) => {
    return apiClient.get(`/datasets/${id}/`);
  },

  getDatasetSummary: (id) => {
    return apiClient.get(`/datasets/${id}/summary/`);
  },

  deleteDataset: (id) => {
    return apiClient.delete(`/datasets/${id}/delete/`);
  },

  downloadReport: (id) => {
    return apiClient.get(`/datasets/${id}/report/`, {
      responseType: 'blob',
    });
  },
};

export default api;