/**
 * Dashboard ARCX - JavaScript Mínimo
 * 
 * Este arquivo contém APENAS funcionalidades essenciais de UI.
 * Não há dados mockados ou lógica de negócio.
 * Tudo deve vir do backend Django.
 */

document.addEventListener('DOMContentLoaded', function() {

    // ========== MOBILE MENU ==========
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const sidebar = document.querySelector('.sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function() {
            sidebar.classList.toggle('mobile-hidden');
            sidebarOverlay.classList.toggle('active');
        });
    }

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', function() {
            sidebar.classList.add('mobile-hidden');
            sidebarOverlay.classList.remove('active');
        });
    }

    // Fechar menu ao pressionar ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebar) {
            sidebar.classList.add('mobile-hidden');
            sidebarOverlay.classList.remove('active');
        }
    });


    // ========== SEARCH TOGGLE ==========
    const searchBtn = document.getElementById('searchBtn');
    const searchField = document.getElementById('searchField');
    const searchInput = document.getElementById('searchInput');

    if (searchBtn && searchField) {
        searchBtn.addEventListener('click', function() {
            searchField.classList.toggle('active');
            if (searchField.classList.contains('active') && searchInput) {
                setTimeout(() => searchInput.focus(), 300);
            }
        });
    }

    // Filtro de menu items (busca local)
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const query = e.target.value.toLowerCase().trim();
            const menuItems = document.querySelectorAll('.menu-item');

            menuItems.forEach(function(item) {
                const text = item.querySelector('span').textContent.toLowerCase();
                if (query === '' || text.includes(query)) {
                    item.style.display = 'flex';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }


    // ========== LOGOUT ==========
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            if (!confirm('Tem certeza que deseja sair?')) {
                e.preventDefault();
            }
        });
    }


    // ========== EXPANDIR/COLAPSAR SUBELEMENTOS ==========
    document.querySelectorAll('.toggle-subelements').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const row = this.closest('tr');
            const contractId = row.dataset.contractId;
            const subelementsRow = document.querySelector(`.subelements-section[data-parent="${contractId}"]`);

            if (subelementsRow) {
                if (subelementsRow.style.display === 'none' || subelementsRow.style.display === '') {
                    subelementsRow.style.display = 'table-row';
                    this.classList.remove('fa-chevron-down');
                    this.classList.add('fa-chevron-up');
                } else {
                    subelementsRow.style.display = 'none';
                    this.classList.remove('fa-chevron-up');
                    this.classList.add('fa-chevron-down');
                }
            }
        });
    });


    // ========== SELECT ALL CHECKBOXES ==========
    const selectAllCheckbox = document.getElementById('selectAll');
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            const checkboxes = document.querySelectorAll('input[name="contract_select"]');
            checkboxes.forEach(function(checkbox) {
                checkbox.checked = selectAllCheckbox.checked;
            });
        });
    }


    // ========== RESPONSIVE CHECK ==========
    function checkScreenSize() {
        const isMobile = window.innerWidth <= 768;
        if (isMobile && sidebar) {
            sidebar.classList.add('mobile-hidden');
        } else if (sidebar) {
            sidebar.classList.remove('mobile-hidden');
        }
        if (sidebarOverlay) {
            sidebarOverlay.classList.remove('active');
        }
    }

    // Check no load e resize
    checkScreenSize();
    window.addEventListener('resize', checkScreenSize);

});


// ========== HELPER: TOAST NOTIFICATION ==========
// Função opcional para mostrar notificações
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type} show`;

    const icons = {
        'success': 'fa-check-circle',
        'error': 'fa-exclamation-circle',
        'warning': 'fa-exclamation-triangle',
        'info': 'fa-info-circle'
    };

    toast.innerHTML = `
        <div class="toast-content">
            <i class="fas ${icons[type] || icons['info']}"></i>
            <span>${message}</span>
        </div>
        <button class="toast-close">
            <i class="fas fa-times"></i>
        </button>
    `;

    document.body.appendChild(toast);

    // Fechar ao clicar no X
    toast.querySelector('.toast-close').addEventListener('click', function() {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    });

    // Auto-fechar após 5 segundos
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

// Exportar para uso global (se necessário)
window.showToast = showToast;
