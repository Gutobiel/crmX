// static/js/api/axios.js
// Import auth using absolute static path to avoid incorrect relative resolution
// when the page URL includes a path segment (for example /login).
import { auth } from '/static/js/api/auth.js';
export { auth };

const api = axios.create({
    baseURL: '/api/v1',
});

api.interceptors.request.use((config) => {
    const token = auth.getAccessToken();
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default api;
