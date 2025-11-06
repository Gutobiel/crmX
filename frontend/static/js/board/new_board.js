// Import auth and API utilities
import { auth } from '/static/js/api/auth.js';
import { boardsApi } from '/static/js/api/index.js';

class NewBoardForm {
    constructor() {
        this.form = document.getElementById('newBoardForm');
        this.nameInput = document.getElementById('board-name');
        this.submitButton = document.getElementById('saveBoardBtn');
        
        this.init();
    }

    init() {
        if (!this.form) return;
        
        // Verificar autenticação
        if (!auth.isAuthenticated()) {
            window.location.href = '/login/';
            return;
        }

        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    setLoading(loading) {
        if (loading) {
            this.submitButton.classList.add('loading');
            this.submitButton.disabled = true;
        } else {
            this.submitButton.classList.remove('loading');
            this.submitButton.disabled = false;
        }
    }

    showMessage(message, type = 'error') {
        // Remove mensagem anterior se existir
        const existingMessage = this.form.querySelector('.form-message');
        if (existingMessage) {
            existingMessage.remove();
        }

        // Criar nova mensagem
        const messageDiv = document.createElement('div');
        messageDiv.className = `form-message ${type}`;
        messageDiv.textContent = message;
        messageDiv.style.display = 'block';

        // Inserir no início do formulário
        this.form.insertBefore(messageDiv, this.form.firstChild);

        // Auto-remover após 5 segundos
        setTimeout(() => {
            messageDiv.style.opacity = '0';
            setTimeout(() => messageDiv.remove(), 300);
        }, 5000);
    }

    async handleSubmit(e) {
        e.preventDefault();
        
        const nome = this.nameInput.value.trim();
        
        if (!nome) {
            this.showMessage('Por favor, digite um nome para a área de trabalho');
            return;
        }

        this.setLoading(true);

        try {
            const response = await boardsApi.create({ nome });
            
            // Redirecionar para a página da área de trabalho criada
            window.location.href = `/board/${response.id}/`;
        } catch (error) {
            console.error('Erro ao criar área de trabalho:', error);
            
            let errorMessage = 'Erro ao criar área de trabalho.';
            if (error.response?.data?.nome) {
                errorMessage = error.response.data.nome[0];
            } else if (error.response?.data?.detail) {
                errorMessage = error.response.data.detail;
            }
            
            this.showMessage(errorMessage);
            this.setLoading(false);
        }
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    new NewBoardForm();
});