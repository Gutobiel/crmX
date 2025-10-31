// Configurações e funcionalidades do Dashboard
class Dashboard {
    constructor() {
        this.sidebar = document.querySelector('.sidebar');
        this.mobileMenuBtn = document.getElementById('mobileMenuBtn');
        this.sidebarOverlay = document.getElementById('sidebarOverlay');
        this.searchBtn = document.getElementById('searchBtn');
        this.searchField = document.getElementById('searchField');
        this.searchInput = document.getElementById('searchInput');
        this.addBtn = document.getElementById('addBtn');
        this.addBtn = document.getElementById('addBtn');
        this.logoutBtn = document.getElementById('logoutBtn');
        this.menuItems = document.querySelectorAll('.menu-item');
        this.pageTitle = document.getElementById('pageTitle');
        this.contentSections = document.querySelectorAll('.content-section');
        
        this.init();
    }

    init() {
        // Verificar autenticação
        this.checkAuthentication();
        
        this.setupEventListeners();
        this.setupSearch();
        this.setupMenuNavigation();
        this.checkScreenSize();
        
        // Carregar seção inicial
        this.loadSection('contratos');
    }

    setupEventListeners() {
        // Menu mobile
        if (this.mobileMenuBtn) {
            this.mobileMenuBtn.addEventListener('click', () => this.toggleMobileSidebar());
        }
        
        // Overlay mobile
        if (this.sidebarOverlay) {
            this.sidebarOverlay.addEventListener('click', () => this.closeMobileSidebar());
        }
        
        // Botão de busca
        if (this.searchBtn) {
            this.searchBtn.addEventListener('click', () => this.toggleSearch());
        }
        
        // Botão adicionar
        if (this.addBtn) {
            this.addBtn.addEventListener('click', () => this.handleAddNew());
        }
        
        // Botão logout
        if (this.logoutBtn) {
            this.logoutBtn.addEventListener('click', () => this.handleLogout());
        }
        
        // Redimensionamento da janela
        window.addEventListener('resize', () => this.checkScreenSize());
        
        // Escape key para fechar mobile sidebar
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeMobileSidebar();
            }
        });
    }

    setupSearch() {
        if (this.searchInput) {
            this.searchInput.addEventListener('input', (e) => this.filterMenuItems(e.target.value));
            
            // Fechar busca ao pressionar Escape
            this.searchInput.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    this.toggleSearch();
                }
            });
        }
    }

    setupMenuNavigation() {
        this.menuItems.forEach(item => {
            item.addEventListener('click', () => {
                const section = item.getAttribute('data-section');
                this.navigateToSection(section, item);
            });
        });
    }

    toggleMobileSidebar() {
        this.sidebar.classList.toggle('mobile-hidden');
        this.sidebarOverlay.classList.toggle('active');
        
        // Prevenir scroll do body quando sidebar está aberto
        if (!this.sidebar.classList.contains('mobile-hidden')) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = 'auto';
        }
    }

    closeMobileSidebar() {
        this.sidebar.classList.add('mobile-hidden');
        this.sidebarOverlay.classList.remove('active');
        document.body.style.overflow = 'auto';
    }

    toggleSearch() {
        this.searchField.classList.toggle('active');
        
        if (this.searchField.classList.contains('active')) {
            setTimeout(() => {
                this.searchInput.focus();
            }, 300);
        } else {
            this.searchInput.value = '';
            this.filterMenuItems('');
        }
    }

    filterMenuItems(query) {
        const searchTerm = query.toLowerCase().trim();
        
        this.menuItems.forEach(item => {
            const text = item.querySelector('span').textContent.toLowerCase();
            
            if (searchTerm === '' || text.includes(searchTerm)) {
                item.style.display = 'flex';
                
                // Highlight do termo pesquisado
                if (searchTerm !== '') {
                    item.classList.add('search-highlight');
                } else {
                    item.classList.remove('search-highlight');
                }
            } else {
                item.style.display = 'none';
                item.classList.remove('search-highlight');
            }
        });
    }

    navigateToSection(sectionId, menuItem) {
        // Remover classe active de todos os itens
        this.menuItems.forEach(item => item.classList.remove('active'));
        
        // Adicionar classe active ao item clicado
        menuItem.classList.add('active');
        
        // Carregar seção
        this.loadSection(sectionId);
        
        // Fechar sidebar mobile se estiver aberto
        if (window.innerWidth <= 768) {
            this.closeMobileSidebar();
        }
    }

    loadSection(sectionId) {
        // Esconder todas as seções
        this.contentSections.forEach(section => {
            section.classList.remove('active');
        });
        
        // Mostrar seção selecionada
        const targetSection = document.getElementById(`${sectionId}-content`);
        if (targetSection) {
            targetSection.classList.add('active');
        }
        
        // Atualizar título da página
        this.updatePageTitle(sectionId);
        
        // Carregar dados da seção
        this.loadSectionData(sectionId);
    }

    updatePageTitle(sectionId) {
        const titles = {
            'contratos': 'Contratos',
            'saldo-contrato': 'Saldo Contrato',
            'saldo-sebrae': 'Saldo SEBRAE',
            'contrato-novacia': 'Contrato Novacia',
            'custo-colaboradores': 'Custo Colaboradores',
            'fluxo-caixa-2024': 'Fluxo de Caixa 2024',
            'os-sebrae-2024': 'O.S SEBRAE 2024',
            'fluxo-caixa-2025': 'Fluxo de Caixa 2025',
            'os-sebrae-2025': 'O.S SEBRAE 2025'
        };
        
        this.pageTitle.textContent = titles[sectionId] || 'Dashboard';
    }

    loadSectionData(sectionId) {
        // Simular carregamento de dados
        console.log(`Carregando dados para: ${sectionId}`);
        
        // Aqui você faria chamadas à API para carregar dados específicos
        // da seção selecionada
        
        // Exemplo de como você pode gerenciar diferentes seções:
        switch (sectionId) {
            case 'contratos':
                this.loadContractsData();
                break;
            case 'saldo-contrato':
                this.loadContractBalanceData();
                break;
            case 'saldo-sebrae':
                this.loadSebraeBalanceData();
                break;
            // ... outras seções
            default:
                console.log(`Seção ${sectionId} ainda não implementada`);
        }
    }

    loadContractsData() {
        // Simular carregamento de contratos
        console.log('📋 Carregando dados de contratos...');
        
        // Inicializar tabela de contratos
        setTimeout(() => {
            if (typeof ContractsTable !== 'undefined') {
                window.contractsTable = new ContractsTable();
            }
        }, 100);
        
        // Aqui você faria uma chamada à API
        // fetch('/api/contracts')
        //   .then(response => response.json())
        //   .then(data => this.renderContractsTable(data));
    }

    loadContractBalanceData() {
        console.log('Carregando saldo de contratos...');
        // Implementar carregamento específico
    }

    loadSebraeBalanceData() {
        console.log('Carregando saldo SEBRAE...');
        // Implementar carregamento específico
    }

    handleAddNew() {
        const activeItem = document.querySelector('.menu-item.active');
        const section = activeItem ? activeItem.getAttribute('data-section') : 'contratos';
        
        console.log(`Adicionando novo item para: ${section}`);
        
        // Aqui você abriria um modal ou redirecionaria para formulário de criação
        this.showNotification(`Criando novo item em ${this.pageTitle.textContent}`, 'info');
    }

    checkScreenSize() {
        const isMobile = window.innerWidth <= 768;
        
        if (isMobile) {
            this.sidebar.classList.add('mobile-hidden');
            this.sidebarOverlay.classList.remove('active');
            document.body.style.overflow = 'auto';
        } else {
            this.sidebar.classList.remove('mobile-hidden');
            this.sidebarOverlay.classList.remove('active');
            document.body.style.overflow = 'auto';
        }
    }

    showNotification(message, type = 'info') {
        // Criar toast notification
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <i class="fas ${this.getToastIcon(type)}"></i>
                <span>${message}</span>
            </div>
            <button class="toast-close">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        document.body.appendChild(toast);
        
        // Mostrar toast
        setTimeout(() => toast.classList.add('show'), 100);
        
        // Auto-hide após 3 segundos
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => document.body.removeChild(toast), 300);
        }, 3000);
        
        // Botão de fechar
        toast.querySelector('.toast-close').addEventListener('click', () => {
            toast.classList.remove('show');
            setTimeout(() => document.body.removeChild(toast), 300);
        });
    }

    getToastIcon(type) {
        const icons = {
            'success': 'fa-check-circle',
            'error': 'fa-exclamation-circle',
            'warning': 'fa-exclamation-triangle',
            'info': 'fa-info-circle'
        };
        return icons[type] || icons.info;
    }
}

// Estilos para toast notifications
const toastStyles = `
    .toast {
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        border-left: 4px solid #333781;
        padding: 15px;
        min-width: 300px;
        max-width: 400px;
        z-index: 1000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .toast.show {
        transform: translateX(0);
    }
    
    .toast-success { border-left-color: #00b894; }
    .toast-error { border-left-color: #c90022; }
    .toast-warning { border-left-color: #ffc107; }
    .toast-info { border-left-color: #333781; }
    
    .toast-content {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #302754;
    }
    
    .toast-content i {
        font-size: 16px;
    }
    
    .toast-close {
        background: none;
        border: none;
        color: #666;
        cursor: pointer;
        padding: 4px;
    }
    
    .search-highlight {
        background: rgba(255, 255, 255, 0.2) !important;
    }
`;

// Adicionar estilos de toast
const styleSheet = document.createElement('style');
styleSheet.textContent = toastStyles;
document.head.appendChild(styleSheet);

// Inicializar dashboard quando DOM estiver carregado
document.addEventListener('DOMContentLoaded', () => {
    new Dashboard();
});

// Adicionar animações de entrada
window.addEventListener('load', () => {
    // Animar entrada dos cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'all 0.4s ease';
            
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 50);
        }, index * 100);
    });
});

// === FUNCIONALIDADE DA TABELA DE CONTRATOS ===
class ContractsTable {
    constructor() {
        this.contracts = [
            {
                id: 1,
                element: '001',
                company: 'SEBRAE',
                object: 'Contratação de serviços de consultoria empresarial',
                qty: 150,
                valuePrev: 125000.00,
                valueAdj: 135000.00,
                docs: '85%'
            },
            {
                id: 2,
                element: '002',
                company: 'SENAI',
                object: 'Desenvolvimento de sistema de gestão de projetos',
                qty: 200,
                valuePrev: 250000.00,
                valueAdj: 275000.00,
                docs: '70%'
            },
            {
                id: 3,
                element: '003',
                company: 'FIESP',
                object: 'Implementação de infraestrutura de rede',
                qty: 100,
                valuePrev: 180000.00,
                valueAdj: 195000.00,
                docs: '90%'
            }
        ];
        
        this.selectedContracts = new Set();
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.renderTable();
        this.updateTotals();
    }

    setupEventListeners() {
        // Selecionar todos
        const selectAllCheckbox = document.getElementById('selectAll');
        if (selectAllCheckbox) {
            selectAllCheckbox.addEventListener('change', (e) => {
                this.selectAll(e.target.checked);
            });
        }

        // Adicionar elemento
        const addElementBtn = document.getElementById('addElementBtn');
        if (addElementBtn) {
            addElementBtn.addEventListener('click', () => {
                this.addElement();
            });
        }
    }

    renderTable() {
        const tableBody = document.getElementById('contractsTableBody');
        if (!tableBody) return;

        tableBody.innerHTML = '';

        this.contracts.forEach(contract => {
            const row = this.createTableRow(contract);
            tableBody.appendChild(row);
        });
    }

    createTableRow(contract) {
        const row = document.createElement('tr');
        row.className = 'contract-row';
        row.dataset.id = contract.id;

        row.innerHTML = `
            <td class="checkbox-col">
                <input type="checkbox" class="row-checkbox" value="${contract.id}">
            </td>
            <td class="element-col">
                <div class="element-info">
                    <span class="element-number">${contract.element}</span>
                    <div class="element-icons">
                        <i class="fas fa-edit" title="Editar" onclick="contractsTable.editContract(${contract.id})"></i>
                        <i class="fas fa-comment" title="Comentários"></i>
                    </div>
                </div>
            </td>
            <td class="company-col">
                <span class="company-tag">${contract.company}</span>
            </td>
            <td class="object-col">
                <span class="object-text" title="${contract.object}">${contract.object}</span>
            </td>
            <td class="qty-col">
                <span class="qty-value">${contract.qty}</span>
            </td>
            <td class="value-prev-col">
                <span class="value-amount">R$ ${this.formatCurrency(contract.valuePrev)}</span>
            </td>
            <td class="value-adj-col">
                <span class="value-amount">R$ ${this.formatCurrency(contract.valueAdj)}</span>
            </td>
            <td class="docs-col">
                <span class="doc-percentage">${contract.docs}</span>
            </td>
            <td class="actions-col">
                <button class="btn-icon" title="Visualizar" onclick="contractsTable.viewContract(${contract.id})">
                    <i class="fas fa-eye"></i>
                </button>
                <button class="btn-icon" title="Excluir" onclick="contractsTable.deleteContract(${contract.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;

        // Adicionar event listener para o checkbox
        const checkbox = row.querySelector('.row-checkbox');
        checkbox.addEventListener('change', (e) => {
            this.toggleSelection(contract.id, e.target.checked);
        });

        return row;
    }

    selectAll(checked) {
        const checkboxes = document.querySelectorAll('.row-checkbox');
        checkboxes.forEach(checkbox => {
            checkbox.checked = checked;
            this.toggleSelection(parseInt(checkbox.value), checked);
        });
    }

    toggleSelection(contractId, selected) {
        if (selected) {
            this.selectedContracts.add(contractId);
        } else {
            this.selectedContracts.delete(contractId);
        }

        // Atualizar estado do "selecionar todos"
        const selectAllCheckbox = document.getElementById('selectAll');
        const totalRows = document.querySelectorAll('.row-checkbox').length;
        const selectedRows = this.selectedContracts.size;

        if (selectAllCheckbox) {
            selectAllCheckbox.indeterminate = selectedRows > 0 && selectedRows < totalRows;
            selectAllCheckbox.checked = selectedRows === totalRows && totalRows > 0;
        }
    }

    addElement() {
        const newId = Math.max(...this.contracts.map(c => c.id), 0) + 1;
        const newContract = {
            id: newId,
            element: String(newId).padStart(3, '0'),
            company: 'Nova Empresa',
            object: 'Descrição do novo contrato',
            qty: 0,
            valuePrev: 0,
            valueAdj: 0,
            docs: '0%'
        };

        this.contracts.push(newContract);
        this.renderTable();
        this.updateTotals();
        
        // Mostrar toast de sucesso
        this.showToast('Elemento adicionado com sucesso!', 'success');
    }

    editContract(contractId) {
        const contract = this.contracts.find(c => c.id === contractId);
        if (!contract) return;

        // Aqui você pode implementar um modal de edição
        const newObject = prompt('Editar objeto do contrato:', contract.object);
        if (newObject !== null) {
            contract.object = newObject;
            this.renderTable();
            this.showToast('Contrato atualizado com sucesso!', 'success');
        }
    }

    viewContract(contractId) {
        const contract = this.contracts.find(c => c.id === contractId);
        if (!contract) return;

        alert(`
            Elemento: ${contract.element}
            Empresa: ${contract.company}
            Objeto: ${contract.object}
            Quantidade: ${contract.qty}
            Valor Anterior: R$ ${this.formatCurrency(contract.valuePrev)}
            Valor Reajustado: R$ ${this.formatCurrency(contract.valueAdj)}
            Documentação: ${contract.docs}
        `);
    }

    deleteContract(contractId) {
        if (confirm('Tem certeza que deseja excluir este contrato?')) {
            this.contracts = this.contracts.filter(c => c.id !== contractId);
            this.selectedContracts.delete(contractId);
            this.renderTable();
            this.updateTotals();
            this.showToast('Contrato excluído com sucesso!', 'error');
        }
    }

    updateTotals() {
        const totalCount = this.contracts.length;
        const totalQty = this.contracts.reduce((sum, c) => sum + c.qty, 0);
        const totalValue = this.contracts.reduce((sum, c) => sum + c.valueAdj, 0);

        const totalsInfo = document.getElementById('totalsInfo');
        if (totalsInfo) {
            totalsInfo.innerHTML = `
                Total de linhas: <span class="total-count">${totalCount}</span> |
                Qtd Total Itens: <span class="total-qty">${totalQty}</span> |
                Valor Total: <span class="total-value">R$ ${this.formatCurrency(totalValue)}</span>
            `;
        }
    }

    formatCurrency(value) {
        return new Intl.NumberFormat('pt-BR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(value);
    }

    showToast(message, type = 'success') {
        // Criar elemento do toast
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        const iconMap = {
            success: 'fa-check-circle',
            error: 'fa-exclamation-circle',
            warning: 'fa-exclamation-triangle',
            info: 'fa-info-circle'
        };

        toast.innerHTML = `
            <div class="toast-content">
                <i class="fas ${iconMap[type]}"></i>
                <span>${message}</span>
            </div>
            <button class="toast-close">
                <i class="fas fa-times"></i>
            </button>
        `;

        // Adicionar ao DOM
        document.body.appendChild(toast);

        // Mostrar toast
        setTimeout(() => toast.classList.add('show'), 100);

        // Remover toast após 4 segundos
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 4000);

        // Event listener para fechar manualmente
        toast.querySelector('.toast-close').addEventListener('click', () => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        });
    }
}

// Variável global para a tabela de contratos
let contractsTable;



console.log('🚀 Dashboard CRM carregado com sucesso!');
console.log('📱 Use o menu lateral para navegar entre as seções');
console.log('🔍 Use a busca para encontrar seções rapidamente');