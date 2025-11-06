// static/js/api/auth.js
const API_BASE_URL = '/api/v1';
const LOGIN_URL = `${API_BASE_URL}/authentication/token/`;

export async function login(usernameOrEmail, password) {
    try {
        const response = await axios.post(LOGIN_URL, {
            username: usernameOrEmail,
            password: password
        });

        const { access, refresh } = response.data;

        // Salva tokens localmente
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);

        // Também salva em cookie para que o servidor (views Django) consiga ler o token
        // Usa cookie de sessão (sem Max-Age) para expirar ao fechar o navegador
        try {
            const secureFlag = window.location.protocol === 'https:' ? '; Secure' : '';
            document.cookie = `access=${access}; Path=/; SameSite=Lax${secureFlag}`;
        } catch (e) {
            console.warn('Não foi possível setar cookie de acesso:', e);
        }

        // Return the tokens directly
        return { access, refresh };
    } catch (error) {
        console.error('Erro no login:', error.response?.data || error.message);
        return {
            success: false,
            error: error.response?.data?.detail || 'Erro ao fazer login. Verifique suas credenciais.'
        };
    }
}

export function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    try {
        // Remove o cookie de acesso
        document.cookie = 'access=; Path=/; Max-Age=0; SameSite=Lax';
        document.cookie = 'access_token=; Path=/; Max-Age=0; SameSite=Lax';
    } catch (e) {
        console.warn('Não foi possível remover cookie de acesso:', e);
    }
}

export function getAccessToken() {
    return localStorage.getItem('access_token');
}

export function isAuthenticated() {
    return !!getAccessToken();
}

// Exemplo opcional de helper: cria uma instância Axios autenticada
export function createAuthenticatedAxios() {
    const instance = axios.create({
        baseURL: API_BASE_URL,
        headers: {
            Authorization: `Bearer ${getAccessToken()}`
        }
    });
    return instance;
}

const auth = {
    login,
    logout,
    getAccessToken,
    isAuthenticated,
    createAuthenticatedAxios,
};

// Setup axios interceptors for authentication
document.addEventListener('DOMContentLoaded', async () => {
    // Avoid registering interceptors multiple times
    if (window.axios?.__auth_interceptors_installed) return;
    window.axios.__auth_interceptors_installed = true;

    // Request interceptor - add Authorization header
    axios.interceptors.request.use(
        (config) => {
            const token = auth.getAccessToken();
            if (token) {
                config.headers = {
                    ...config.headers,
                    'Authorization': `Bearer ${token}`
                };
            }
            return config;
        },
        (error) => Promise.reject(error)
    );

    // Response interceptor - handle 401s and token refresh
    axios.interceptors.response.use(
        (response) => response,
        async (error) => {
            if (error.response?.status === 401 && !error.config?._retry) {
                error.config._retry = true;
                try {
                    // Implement token refresh here if needed
                    // const newToken = await refreshToken();
                    // if (newToken) { retry request... }
                }
                catch (refreshError) {
                    auth.logout();
                    return Promise.reject(refreshError);
                }
            }
            return Promise.reject(error);
        }
    );
});

export { auth };
