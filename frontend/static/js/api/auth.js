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

        return { success: true, data: response.data };
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
