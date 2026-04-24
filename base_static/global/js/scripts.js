/* -------------------------------------------------
   DELETE CONFIRMATION MODAL
   ------------------------------------------------- */
document.addEventListener('DOMContentLoaded', () => {
    const deleteBtn = document.querySelector('.btn-delete');
    const modal = document.getElementById('confirm-delete-modal');
    const cancelBtn = document.getElementById('modal-cancel');
    const confirmBtn = document.getElementById('modal-confirm');
    const hiddenForm = document.getElementById('form-delete'); // já está no template
    if (!deleteBtn) return; // caso esteja na página de criação (sem receita)
    /* abrir modal */
    deleteBtn.addEventListener('click', e => {
        e.preventDefault();               // impede submit imediato
        modal.classList.remove('hidden');
        modal.classList.add('visible');
        cancelBtn.focus();                // foco para acessibilidade
    });
    /* fechar modal (cancel) */
    cancelBtn.addEventListener('click', () => {
        modal.classList.remove('visible');
        modal.classList.add('hidden');
    });
    /* confirmar exclusão */
    confirmBtn.addEventListener('click', () => {
        hiddenForm.submit();              // envia POST com CSRF já incluído
    });
    /* fechar ao pressionar ESC */
    document.addEventListener('keydown', e => {
        if (e.key === 'Escape' && modal.classList.contains('visible')) {
            modal.classList.remove('visible');
            modal.classList.add('hidden');
        }
    });
    /* trap focus dentro do modal (acessibilidade) */
    const focusable = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';
    const focusableEls = modal.querySelectorAll(focusable);
    const firstFocusable = focusableEls[0];
    const lastFocusable = focusableEls[focusableEls.length - 1];
    modal.addEventListener('keydown', e => {
        if (e.key !== 'Tab') return;
        if (e.shiftKey) { // shift + tab
            if (document.activeElement === firstFocusable) {
                e.preventDefault();
                lastFocusable.focus();
            }
        } else { // tab
            if (document.activeElement === lastFocusable) {
                e.preventDefault();
                firstFocusable.focus();
            }
        }
    });
});

(() => {
    const buttonCloseMenu = document.querySelector('.button-close-menu');
    const buttonShowMenu = document.querySelector('.button-show-menu');
    const menuSidebar = document.querySelector('.menu-sidebar');
    const menuOverlay = document.querySelector('.menu-overlay');

    const menuHiddenClass = 'menu-hidden';

    const closeMenu = () => {
        menuSidebar.classList.add(menuHiddenClass);
    };

    const showMenu = () => {
        menuSidebar.classList.remove(menuHiddenClass);
    };

    if (buttonCloseMenu) {
        buttonCloseMenu.removeEventListener('click', closeMenu);
        buttonCloseMenu.addEventListener('click', closeMenu);
    }

    if (buttonShowMenu) {
        buttonShowMenu.removeEventListener('click', showMenu);
        buttonShowMenu.addEventListener('click', showMenu);
    }

    if (menuOverlay) {
        menuOverlay.removeEventListener('click', closeMenu);
        menuOverlay.addEventListener('click', closeMenu);
    }
})();

(() => {
    const authorsLogoutLinks = document.querySelectorAll('.authors-logout-link');
    const formLogout = document.querySelector('.form-logout');

    for (const link of authorsLogoutLinks) {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            formLogout.submit();
        });
    }
})();