// Use absolute path to avoid relative resolution issues when the page is under a
// nested route (e.g. /login). Leading slash ensures browser requests
// /static/js/api/axios.js regardless of current URL path.
import { auth } from '/static/js/api/axios.js';


class LoginForm {
    constructor() {
        this.form = document.getElementById('loginForm');
        // Suporta input id="username" ou id="email"
        this.usernameInput = document.getElementById('username') || document.getElementById('email');
        this.passwordInput = document.getElementById('password');
        this.loginBtn = document.getElementById('loginBtn');
        this.btnLoader = document.getElementById('btnLoader');
        this.btnText = document.querySelector('.btn-text');

        this.init();
    }

    init() {
        if (!this.form) {
            console.warn('Login form not found on page');
            return;
        }

        // Redireciona se já autenticado
        if (auth.isAuthenticated()) {
            window.location.href = '/home/';
            return;
        }

        this.form.addEventListener('submit', (e) => this.handleSubmit(e));

        if (this.usernameInput) this.usernameInput.addEventListener('input', () => this.clearError());
        if (this.passwordInput) this.passwordInput.addEventListener('input', () => this.clearError());
    }

    async handleSubmit(e) {
        e.preventDefault();

        const usernameOrEmail = this.usernameInput ? this.usernameInput.value.trim() : '';
        const password = this.passwordInput ? this.passwordInput.value.trim() : '';

        if (!usernameOrEmail || !password) {
            this.showError('Preencha email/usuário e senha');
            return;
        }

        this.setLoading(true);

        try {
            await auth.login(usernameOrEmail, password);
            // Redireciona após login bem-sucedido
            window.location.href = '/dashboard/';
        } catch (err) {
            let message = 'Erro ao autenticar.';
            if (err?.response?.status === 401) {
                message = 'Usuário ou senha inválidos.';
            } else if (err?.response?.data?.detail) {
                message = err.response.data.detail;
            }
            this.showError(message);
        } finally {
            this.setLoading(false);
        }
    }

    setLoading(loading) {
        if (!this.loginBtn) return;
        this.loginBtn.disabled = loading;
        if (this.btnLoader && this.btnText) {
            this.btnLoader.style.display = loading ? 'inline-block' : 'none';
            this.btnText.style.display = loading ? 'none' : 'inline';
        } else {
            this.loginBtn.innerHTML = loading
                ? '<i class="bi bi-arrow-clockwise"></i> Aguarde...'
                : '<i class="bi bi-door-open-fill"></i> Acessar';
        }
    }

    showError(msg) {
        const ids = ['usernameError', 'emailError', 'passwordError'];
        for (const id of ids) {
            const el = document.getElementById(id);
            if (el) {
                el.textContent = msg;
                el.style.display = 'block';
                return;
            }
        }
        alert(msg);
    }

    clearError() {
        const errors = ['usernameError', 'emailError', 'passwordError'];
        errors.forEach(id => {
            const el = document.getElementById(id);
            if (el) {
                el.textContent = '';
                el.style.display = 'none';
            }
        });
    }
}

function togglePassword() {
    const passwordInput = document.getElementById('password');
    const toggleIcon = document.getElementById('toggleIcon');
    if (!passwordInput) return;
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        if (toggleIcon) { toggleIcon.classList.remove('fa-eye'); toggleIcon.classList.add('fa-eye-slash'); }
    } else {
        passwordInput.type = 'password';
        if (toggleIcon) { toggleIcon.classList.remove('fa-eye-slash'); toggleIcon.classList.add('fa-eye'); }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new LoginForm();
    window.togglePassword = togglePassword; // deixa acessível ao onclick
});

console.log('Login script loaded');
