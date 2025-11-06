import { authService } from './auth.service.js';

class HttpClient {
    async fetch(url, options = {}) {
        try {
            // Adiciona o token de acesso ao header se existir
            if (authService.isAuthenticated()) {
                options.headers = {
                    ...options.headers,
                    'Authorization': `Bearer ${authService.getAccessToken()}`
                };
            }

            let response = await fetch(url, options);

            // Se receber 401, tenta renovar o token
            if (response.status === 401) {
                const refreshSuccess = await authService.refreshAccessToken();
                
                if (refreshSuccess) {
                    // Tenta a requisição novamente com o novo token
                    options.headers = {
                        ...options.headers,
                        'Authorization': `Bearer ${authService.getAccessToken()}`
                    };
                    response = await fetch(url, options);
                } else {
                    // Se não conseguir renovar, redireciona para login
                    showToast('Sua sessão expirou. Por favor, faça login novamente.', 'warning');
                    authService.redirectToLogin();
                    throw new Error('Authentication required');
                }
            }

            return response;
        } catch (error) {
            console.error('HTTP Client Error:', error);
            throw error;
        }
    }
}

export const httpClient = new HttpClient();