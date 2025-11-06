import { authService } from './services/auth.service.js';
import { httpClient } from './services/http.client.js';

class App {
    constructor() {
        this.initializeAuth();
        this.setupGlobalErrorHandler();
    }

    initializeAuth() {
        // Verifica se há um estado salvo após login
        const savedState = authService.getSavedState();
        if (savedState) {
            this.restoreState(savedState);
        }

        // Monitora o status de autenticação
        this.checkAuthStatus();
    }

    async checkAuthStatus() {
        try {
            // Verifica o status da autenticação a cada 5 minutos
            setInterval(async () => {
                if (!authService.isAuthenticated()) {
                    const message = 'Sua sessão expirou. Você precisa fazer login novamente.';
                    if (confirm(message)) {
                        authService.redirectToLogin();
                    }
                }
            }, 5 * 60 * 1000);

        } catch (error) {
            console.error('Erro ao verificar status de autenticação:', error);
        }
    }

    restoreState(state) {
        // Restaura dados de formulários
        if (state.formData) {
            Object.entries(state.formData).forEach(([formId, data]) => {
                const form = document.getElementById(formId);
                if (form) {
                    Object.entries(data).forEach(([key, value]) => {
                        const input = form.querySelector(`[name="${key}"]`);
                        if (input) {
                            input.value = value;
                        }
                    });
                }
            });
        }

        // Se a URL salva for diferente da atual, pergunta se deseja voltar
        if (state.url && state.url !== window.location.href) {
            if (confirm('Deseja voltar para a página onde estava antes de fazer login?')) {
                window.location.href = state.url;
            }
        }
    }

    setupGlobalErrorHandler() {
        // Intercepta erros de rede globalmente
        window.addEventListener('unhandledrejection', (event) => {
            if (event.reason instanceof Error) {
                if (event.reason.message.includes('Failed to fetch') || 
                    event.reason.message.includes('Network request failed')) {
                    this.handleNetworkError();
                }
            }
        });
    }

    handleNetworkError() {
        const message = 'Ocorreu um erro de conexão. Por favor, verifique sua internet e tente novamente.';
        // Você pode personalizar como exibir esta mensagem (toast, modal, etc)
        alert(message);
    }
}

// Inicializa a aplicação quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
});