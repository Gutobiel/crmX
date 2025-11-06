export class AuthService {
    constructor() {
        this.accessToken = localStorage.getItem('access_token');
        this.refreshToken = localStorage.getItem('refresh_token');
    }

    isAuthenticated() {
        return !!this.accessToken;
    }

    getAccessToken() {
        return this.accessToken;
    }

    setTokens(access, refresh) {
        this.accessToken = access;
        this.refreshToken = refresh;
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
    }

    clearTokens() {
        this.accessToken = null;
        this.refreshToken = null;
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    }

    async refreshAccessToken() {
        try {
            const response = await fetch('/api/token/refresh/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    refresh: this.refreshToken
                })
            });

            if (!response.ok) {
                throw new Error('Failed to refresh token');
            }

            const data = await response.json();
            this.setTokens(data.access, this.refreshToken);
            return true;
        } catch (error) {
            this.clearTokens();
            return false;
        }
    }

    saveCurrentState() {
        const currentPath = window.location.pathname;
        const formData = this.captureFormData();
        sessionStorage.setItem('auth_redirect', currentPath);
        if (formData) {
            sessionStorage.setItem('form_data', JSON.stringify(formData));
        }
    }

    captureFormData() {
        const forms = document.querySelectorAll('form');
        const formData = {};
        forms.forEach(form => {
            const formElements = Array.from(form.elements);
            formData[form.id || 'defaultForm'] = formElements.reduce((acc, element) => {
                if (element.name) {
                    acc[element.name] = element.value;
                }
                return acc;
            }, {});
        });
        return formData;
    }

    redirectToLogin() {
        this.saveCurrentState();
        window.location.href = '/login/';
    }
}

export const authService = new AuthService();