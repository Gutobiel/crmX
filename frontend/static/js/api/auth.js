// static/js/api/auth.js
const API_BASE_URL = '/api/v1';
const LOGIN_URL = `${API_BASE_URL}/authentication/token/`;
const REFRESH_URL = `${API_BASE_URL}/authentication/token/refresh/`;

// Dias máximos de validade do refresh (ex: 30 dias)
const REFRESH_MAX_DAYS = 30;

function nowUnixMs() {
    return Date.now();
}

function daysToMs(days) {
    return days * 24 * 60 * 60 * 1000;
}

function saveTokens({ access, refresh }) {
    const issuedAt = Date.now();
    const data = { access, refresh, issued_at: issuedAt };
    localStorage.setItem('auth_tokens', JSON.stringify(data));

    // Cookie de acesso para Django (como já fazia)
    try {
        const secureFlag = window.location.protocol === 'https:' ? '; Secure' : '';
        document.cookie = `access=${access}; Path=/; SameSite=Lax${secureFlag}`;
    } catch (e) {
        console.warn('Não foi possível setar cookie de acesso:', e);
    }
}

function loadTokens() {
    const raw = localStorage.getItem('auth_tokens');
    if (!raw) return null;
    try {
        return JSON.parse(raw);
    } catch {
        return null;
    }
}

function clearTokens() {
    localStorage.removeItem('auth_tokens');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    try {
        document.cookie = 'access=; Path=/; Max-Age=0; SameSite=Lax';
        document.cookie = 'access_token=; Path=/; Max-Age=0; SameSite=Lax';
    } catch (e) {
        console.warn('Não foi possível remover cookie de acesso:', e);
    }
}

function getAccessToken() {
    const data = loadTokens();
    if (!data || !data.access) return null;
    return data.access;
}

function getRefreshToken() {
    const data = loadTokens();
    if (!data || !data.refresh) return null;
    return data.refresh;
}

function isRefreshExpired() {
    const data = loadTokens();
    if (!data || !data.issued_at) return true;
    const elapsed = nowUnixMs() - data.issued_at;
    return elapsed > daysToMs(REFRESH_MAX_DAYS);
}

export async function login(usernameOrEmail, password) {
    const response = await axios.post(LOGIN_URL, {
        username: usernameOrEmail,
        password: password
    });
    const { access, refresh } = response.data;
    saveTokens({ access, refresh });
    return { success: true, access, refresh };
}

export function logout() {
    clearTokens();
}

export function isAuthenticated() {
    return !!getAccessToken();
}

// Tenta renovar o access token usando o refresh
export async function refreshToken() {
    const refresh = getRefreshToken();
    if (!refresh) return null;
    if (isRefreshExpired()) {
        // Refresh passou de 30 dias
        clearTokens();
        showReLoginAlert();
        return null;
    }

    try {
        const response = await axios.post(REFRESH_URL, { refresh });
        const { access } = response.data;
        // Mantém o mesmo issued_at para limitar a 30 dias desde o primeiro login
        const data = loadTokens() || {};
        saveTokens({
            access,
            refresh: data.refresh || refresh,
        });
        return access;
    } catch (error) {
        console.warn('Falha ao renovar token:', error.response?.data || error.message);
        clearTokens();
        showReLoginAlert();
        return null;
    }
}

// Headers para fetch simples
export async function getAuthHeaders() {
    const token = getAccessToken();
    const headers = {
        'Content-Type': 'application/json'
    };
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
}

// Instância Axios autenticada (não obrigatória)
export function createAuthenticatedAxios() {
    const instance = axios.create({
        baseURL: API_BASE_URL,
    });

    instance.interceptors.request.use(
        (config) => {
            const token = getAccessToken();
            if (token) {
                config.headers = {
                    ...config.headers,
                    Authorization: `Bearer ${token}`,
                };
            }
            return config;
        },
        (error) => Promise.reject(error)
    );

    return instance;
}

// Alerta padrão de precisar logar novamente
function showReLoginAlert() {
    try {
        const showBanner = () => {
            if (document.getElementById('relogin-alert')) return; // evita duplicar

            const container = document.createElement('div');
            container.id = 'relogin-alert';
            container.setAttribute('role', 'alert');
            container.style.position = 'fixed';
            container.style.top = '16px';
            container.style.right = '16px';
            container.style.zIndex = '9999';
            container.style.background = '#111827';
            container.style.color = '#fff';
            container.style.padding = '12px 16px';
            container.style.borderRadius = '10px';
            container.style.boxShadow = '0 10px 25px rgba(0,0,0,0.25)';
            container.style.display = 'flex';
            container.style.alignItems = 'center';
            container.style.gap = '12px';

            const icon = document.createElement('span');
            icon.innerHTML = '⚠️';
            icon.style.fontSize = '18px';

            const text = document.createElement('div');
            text.style.lineHeight = '1.2';
            text.innerHTML = '<strong>Sessão expirada</strong><br/>Faça login novamente para continuar.';

            const actions = document.createElement('div');
            actions.style.marginLeft = '8px';

            const loginBtn = document.createElement('button');
            loginBtn.textContent = 'Fazer login';
            loginBtn.style.background = '#2563eb';
            loginBtn.style.color = '#fff';
            loginBtn.style.border = 'none';
            loginBtn.style.borderRadius = '8px';
            loginBtn.style.padding = '8px 12px';
            loginBtn.style.cursor = 'pointer';
            loginBtn.onclick = () => { window.location.href = '/login/'; };

            const closeBtn = document.createElement('button');
            closeBtn.textContent = '×';
            closeBtn.setAttribute('aria-label', 'Fechar');
            closeBtn.style.background = 'transparent';
            closeBtn.style.color = '#9ca3af';
            closeBtn.style.border = 'none';
            closeBtn.style.fontSize = '20px';
            closeBtn.style.cursor = 'pointer';
            closeBtn.style.marginLeft = '4px';
            closeBtn.onclick = () => container.remove();

            actions.appendChild(loginBtn);
            actions.appendChild(closeBtn);

            container.appendChild(icon);
            container.appendChild(text);
            container.appendChild(actions);

            document.body.appendChild(container);

            // Auto-redirect suave após 3s, se ainda não clicou
            setTimeout(() => {
                if (document.body.contains(container)) {
                    window.location.href = '/login/';
                }
            }, 3000);
        };

        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', showBanner, { once: true });
        } else {
            showBanner();
        }
    } catch (e) {
        // Fallback simples
        alert('Sua sessão expirou. Por favor, faça login novamente.');
        window.location.href = '/login/';
    }
}

// Objeto para export default-like
const auth = {
    login,
    logout,
    getAccessToken,
    isAuthenticated,
    createAuthenticatedAxios,
    getAuthHeaders,
    refreshToken,
};

export { auth };

// Interceptors globais Axios para toda a app
document.addEventListener('DOMContentLoaded', async () => {
    if (window.axios?.__auth_interceptors_installed) return;
    window.axios.__auth_interceptors_installed = true;

    // Request: adiciona Authorization
    axios.interceptors.request.use(
        (config) => {
            const token = getAccessToken();
            if (token) {
                config.headers = {
                    ...config.headers,
                    Authorization: `Bearer ${token}`,
                };
            }
            return config;
        },
        (error) => Promise.reject(error)
    );

    // Response: tenta refresh em 401
    axios.interceptors.response.use(
        (response) => response,
        async (error) => {
            const originalRequest = error.config || {};

            if (error.response?.status === 401 && !originalRequest._retry) {
                originalRequest._retry = true;

                const newAccess = await refreshToken();
                if (newAccess) {
                    // Atualiza header e repete a requisição
                    originalRequest.headers = {
                        ...(originalRequest.headers || {}),
                        Authorization: `Bearer ${newAccess}`,
                    };
                    return axios(originalRequest);
                }
                // Se não conseguiu renovar, já limpou tokens e mostrou alerta
            }

            return Promise.reject(error);
        }
    );
});
