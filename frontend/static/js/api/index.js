// Configurações base da API
const API_BASE_URL = '/api/v1';

// Simple helper: ensure axios is available (try CDN, otherwise dynamically load)
async function ensureAxios() {
	if (typeof window.axios !== 'undefined') return;

	// try to load from CDN dynamically as fallback
	await new Promise((resolve, reject) => {
		const s = document.createElement('script');
		s.src = 'https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js';
		s.async = true;
		s.onload = () => resolve();
		s.onerror = () => reject(new Error('Failed to load axios'));
		(document.head || document.documentElement).appendChild(s);
	}).catch((e) => {
		console.error('Could not load axios from CDN:', e);
		// if axios still undefined, fallback to fetch-based minimal wrapper
		if (typeof window.axios === 'undefined') {
			window.axios = {
				async post(url, data, config) {
					const res = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json', ...(config && config.headers) }, body: JSON.stringify(data) });
					const json = await res.json();
					if (!res.ok) {
						const err = new Error('HTTP error');
						err.response = { status: res.status, data: json };
						throw err;
					}
					return { data: json };
				},
				async get(url, config) {
					const res = await fetch(url, { method: 'GET', headers: { 'Content-Type': 'application/json', ...(config && config.headers) } });
					const json = await res.json();
					if (!res.ok) {
						const err = new Error('HTTP error');
						err.response = { status: res.status, data: json };
						throw err;
					}
					return { data: json };
				},
				async put(url, data, config) { return this.post(url, data, { method: 'PUT', ...(config||{}) }); },
				async delete(url, config) { return this.get(url, config); }
			};
		}
	});
}

// Auth helper object
const auth = {
	async login(email, password) {
		const url = `${API_BASE_URL}/authentication/token/`;
		if (!email || !password) throw new Error('Email e senha são obrigatórios');
		await ensureAxios();
		const response = await axios.post(url, { email, password });
		const { access, refresh } = response.data;
		if (!access) throw new Error('No access token returned');
		localStorage.setItem('access_token', access);
		if (refresh) localStorage.setItem('refresh_token', refresh);
		return response.data;
	},

	async refreshToken() {
		await ensureAxios();
		const refresh = localStorage.getItem('refresh_token');
		if (!refresh) return null;
		try {
			const resp = await axios.post(`${API_BASE_URL}/authentication/token/refresh/`, { refresh });
			const { access, refresh: newRefresh } = resp.data;
			if (access) localStorage.setItem('access_token', access);
			if (newRefresh) localStorage.setItem('refresh_token', newRefresh);
			return access;
		} catch (e) {
			// failed refresh
			return null;
		}
	},

	logout() {
		try { localStorage.removeItem('access_token'); localStorage.removeItem('refresh_token'); } catch (e) {}
		// avoid redirect loop: only redirect if not already on /login
		if (!window.location.pathname.startsWith('/login')) {
			window.location.href = '/login';
		}
	},

	getToken() {
		try { return localStorage.getItem('access_token'); } catch { return null; }
	},

	isAuthenticated() { return !!this.getToken(); }
};

// Register interceptors once after DOM is ready
document.addEventListener('DOMContentLoaded', async () => {
	await ensureAxios();

	// single registration guard
	if (axios.__auth_interceptors_installed) return;
	axios.__auth_interceptors_installed = true;

	axios.interceptors.request.use(
		(config) => {
			try {
				const token = auth.getToken();
				if (token) config.headers = { ...(config.headers || {}), Authorization: `Bearer ${token}` };
			} catch (e) { /* ignore */ }
			return config;
		},
		(error) => Promise.reject(error)
	);

	axios.interceptors.response.use(
		(response) => response,
		async (error) => {
			const originalRequest = error.config || {};
			const status = error.response?.status;

			// Only attempt refresh once per request
			if (status === 401 && !originalRequest._retry) {
				originalRequest._retry = true;
				const newToken = await auth.refreshToken();
				if (newToken) {
					originalRequest.headers = { ...(originalRequest.headers || {}), Authorization: `Bearer ${newToken}` };
					return axios(originalRequest);
				}
				// refresh failed, logout safely
				auth.logout();
			}
			return Promise.reject(error);
		}
	);
});

// API endpoints para boards
const boardsApi = {
	async getBoards() { await ensureAxios(); const response = await axios.get(`${API_BASE_URL}/boards/`); return response.data; },
	async getBoardById(id) { await ensureAxios(); const response = await axios.get(`${API_BASE_URL}/boards/${id}/`); return response.data; },
	async createBoard(data) { await ensureAxios(); const response = await axios.post(`${API_BASE_URL}/boards/`, data); return response.data; },
	async updateBoard(id, data) { await ensureAxios(); const response = await axios.put(`${API_BASE_URL}/boards/${id}/`, data); return response.data; },
	async deleteBoard(id) { await ensureAxios(); await axios.delete(`${API_BASE_URL}/boards/${id}/`); }
};

// API endpoints para elements
const elementsApi = {
	async getElements() { await ensureAxios(); const response = await axios.get(`${API_BASE_URL}/elements/`); return response.data; },
	async getElementById(id) { await ensureAxios(); const response = await axios.get(`${API_BASE_URL}/elements/${id}/`); return response.data; },
	async createElement(data) { await ensureAxios(); const response = await axios.post(`${API_BASE_URL}/elements/`, data); return response.data; },
	async updateElement(id, data) { await ensureAxios(); const response = await axios.put(`${API_BASE_URL}/elements/${id}/`, data); return response.data; },
	async deleteElement(id) { await ensureAxios(); await axios.delete(`${API_BASE_URL}/elements/${id}/`); }
};

export { auth, boardsApi, elementsApi };
