function showToast(title, message, type = 'normal', duration = 3000) {
    const toastComponent = document.getElementById('toast-component');
    const toastTitle = document.getElementById('toast-title');
    const toastMessage = document.getElementById('toast-message');
    const toastIcon = document.getElementById('toast-icon');
    const toastIconContainer = document.getElementById('toast-icon-container');
    
    if (!toastComponent) return;

    // Remove all border type classes first
    toastComponent.classList.remove(
        'border-green-500', 'border-red-500', 'border-yellow-500', 'border-blue-500', 'border-purple-500'
    );

    // Remove icon container classes
    toastIconContainer.classList.remove(
        'bg-green-600', 'bg-red-600', 'bg-yellow-600', 'bg-blue-600', 'bg-purple-600'
    );

    // Set type styles and icon based on dark theme
    if (type === 'success') {
        toastComponent.classList.add('border-green-500');
        toastIconContainer.classList.add('bg-green-600');
        toastIcon.innerHTML = '✓';
        toastIcon.className = 'text-xl font-bold text-white drop-shadow-sm';
    } else if (type === 'error') {
        toastComponent.classList.add('border-red-500');
        toastIconContainer.classList.add('bg-red-600');
        toastIcon.innerHTML = '✕';
        toastIcon.className = 'text-xl font-bold text-white drop-shadow-sm';
    } else if (type === 'warning') {
        toastComponent.classList.add('border-yellow-500');
        toastIconContainer.classList.add('bg-yellow-600');
        toastIcon.innerHTML = '⚠';
        toastIcon.className = 'text-xl font-bold text-white drop-shadow-sm';
    } else if (type === 'info') {
        toastComponent.classList.add('border-blue-500');
        toastIconContainer.classList.add('bg-blue-600');
        toastIcon.innerHTML = 'ℹ';
        toastIcon.className = 'text-xl font-bold text-white drop-shadow-sm';    
    } else {
        toastComponent.classList.add('border-purple-500');
        toastIconContainer.classList.add('bg-purple-600');
        toastIcon.innerHTML = '•';
        toastIcon.className = 'text-xl font-bold text-white drop-shadow-sm';
    }

    toastTitle.textContent = title;
    toastMessage.textContent = message;

    // Show toast
    toastComponent.classList.remove('opacity-0', 'translate-y-64');
    toastComponent.classList.add('opacity-100', 'translate-y-0');

    // Auto hide toast
    setTimeout(() => {
        hideToast();
    }, duration);
}

function hideToast() {
    const toastComponent = document.getElementById('toast-component');
    if (!toastComponent) return;

    toastComponent.classList.remove('opacity-100', 'translate-y-0');
    toastComponent.classList.add('opacity-0', 'translate-y-64');
}

// Helper functions for common toast types
function showSuccessToast(title, message = '', duration = 3000) {
    showToast(title, message, 'success', duration);
}

function showErrorToast(title, message = '', duration = 5000) {
    showToast(title, message, 'error', duration);
}

function showWarningToast(title, message = '', duration = 4000) {
    showToast(title, message, 'warning', duration);
}

function showInfoToast(title, message = '', duration = 3000) {
    showToast(title, message, 'info', duration);
}