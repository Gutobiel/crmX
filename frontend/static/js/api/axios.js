// static/js/api/axios.js
import { auth } from './auth.js';
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
