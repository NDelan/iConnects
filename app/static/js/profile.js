// Global state to store items for each section
const state = {
    projects: [],
    experiences: [],
    achievements: []
};

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    // Load existing items for each section
    loadSection('projects');
    loadSection('experiences');
    loadSection('achievements');

    // Set up profile edit functionality
    setupProfileEditing();

    // Set up modal form handlers
    setupModalHandlers();
});

// Profile editing functionality
function setupProfileEditing() {
    const nameText = document.getElementById('profile-name-text');
    const nameInput = document.getElementById('profile-name-input');
    const titleText = document.getElementById('profile-title-text');
    const titleInput = document.getElementById('profile-title-input');
    const profilePictureInput = document.getElementById('profile-picture-input');
    const profilePicturePreview = document.getElementById('profile-picture-preview');
    const saveButton = document.getElementById('save-btn');

    window.toggleEditProfile = function() {
        const isEditing = nameInput.style.display === 'block';
        if (isEditing) {
            nameText.style.display = 'block';
            nameInput.style.display = 'none';
            titleText.style.display = 'block';
            titleInput.style.display = 'none';
            profilePictureInput.style.display = 'none';
            saveButton.style.display = 'none';
        } else {
            nameInput.style.display = 'block';
            nameText.style.display = 'none';
            titleInput.style.display = 'block';
            titleText.style.display = 'none';
            profilePictureInput.style.display = 'block';
            saveButton.style.display = 'inline-block';
        }
    };

    window.previewProfilePicture = function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                profilePicturePreview.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    };
}

// Modal handling
function setupModalHandlers() {
    const modal = document.getElementById('modal');
    const modalOverlay = document.getElementById('modal-overlay');
    const form = document.getElementById('modal-form');
    const currentCheckbox = document.getElementById('current-checkbox');
    const endDateInput = document.getElementById('end-date');

    currentCheckbox.addEventListener('change', function() {
        endDateInput.disabled = this.checked;
        if (this.checked) {
            endDateInput.value = '';
        }
    });

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        handleFormSubmit();
    });

    window.openModal = function(section, isAdd = true) {
        const modalTitle = document.getElementById('modal-title');
        // Handle plural form in display
        const displaySection = section.endsWith('s') ? section.slice(0, -1) : section;
        modalTitle.textContent = `${isAdd ? 'Add' : 'Edit'} ${displaySection.charAt(0).toUpperCase() + displaySection.slice(1)}`;
        
        modal.setAttribute('data-section', section);
        modal.setAttribute('data-mode', isAdd ? 'add' : 'edit');
        
        modal.style.display = 'block';
        modalOverlay.style.display = 'block';
    };

    window.closeModal = function() {
        modal.style.display = 'none';
        modalOverlay.style.display = 'none';
        form.reset();
    };
}

// Load items for a specific section
async function loadSection(section) {
    try {
        const response = await fetch(`/api/profile/${section}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const items = await response.json();
        state[section] = items;
        renderSection(section);
    } catch (error) {
        console.error(`Error loading ${section}:`, error);
        showNotification(`Failed to load ${section}`, 'error');
    }
}

// Render items for a specific section
function renderSection(section) {
    const container = document.getElementById(`${section}-content`);
    if (!container) return;

    if (state[section].length === 0) {
        container.innerHTML = `<div class="empty-state">Click + to add your ${section}</div>`;
        return;
    }

    container.innerHTML = state[section].map(item => createItemHTML(section, item)).join('');
}

// Create HTML for an item
function createItemHTML(section, item) {
    return `
        <div class="content-item" data-id="${item.id}">
            <div class="item-content">
                <div class="item-title-group">
                    <h4>${item.title}</h4>
                    ${item.subtitle ? `<h5>${item.subtitle}</h5>` : ''}
                </div>
                ${item.description ? `<p class="item-description">${item.description}</p>` : ''}
                <div class="item-dates">
                    ${formatDate(item.startDate)} - ${item.endDate === 'Present' ? 'Present' : formatDate(item.endDate)}
                </div>
            </div>
            <div class="item-actions">
                <button class="action-btn edit-btn" 
                        aria-label="Edit"
                        onclick="editItem('${section}', ${item.id})">
                </button>
                <button class="action-btn delete-btn" 
                        aria-label="Delete"
                        onclick="deleteItem('${section}', ${item.id})">
                </button>
            </div>
        </div>
    `;
}

function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short'
    });
}

// Handle form submission
function handleFormSubmit() {
    const modal = document.getElementById('modal');
    const section = modal.getAttribute('data-section');
    const mode = modal.getAttribute('data-mode');
    const itemId = modal.getAttribute('data-item-id');

    const data = {
        title: document.getElementById('title').value,
        subtitle: document.getElementById('subtitle').value,
        description: document.getElementById('description').value,
        startDate: document.getElementById('start-date').value,
        endDate: document.getElementById('current-checkbox').checked ? 'Present' : document.getElementById('end-date').value
    };

    if (mode === 'add') {
        addItem(section, data);
    } else {
        updateItem(section, parseInt(itemId), data);
    }

    closeModal();
}

// Add new item
async function addItem(section, data) {
    try {
        const response = await fetch(`/api/profile/${section}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const newItem = await response.json();
        state[section].push(newItem);
        renderSection(section);
        showNotification(`${section} added successfully`, 'success');
    } catch (error) {
        console.error(`Error adding ${section}:`, error);
        showNotification(`Failed to add ${section}`, 'error');
    }
}

// Edit existing item
function editItem(section, itemId) {
    const item = state[section].find(i => i.id === itemId);
    if (!item) return;

    const modal = document.getElementById('modal');
    modal.setAttribute('data-section', section);
    modal.setAttribute('data-mode', 'edit');
    modal.setAttribute('data-item-id', itemId);

    document.getElementById('title').value = item.title;
    document.getElementById('subtitle').value = item.subtitle || '';
    document.getElementById('description').value = item.description || '';
    document.getElementById('start-date').value = item.startDate || '';
    
    const currentCheckbox = document.getElementById('current-checkbox');
    const endDateInput = document.getElementById('end-date');
    
    if (item.endDate === 'Present') {
        currentCheckbox.checked = true;
        endDateInput.disabled = true;
        endDateInput.value = '';
    } else {
        currentCheckbox.checked = false;
        endDateInput.disabled = false;
        endDateInput.value = item.endDate || '';
    }

    openModal(section, false);
}

// Update existing item
async function updateItem(section, itemId, data) {
    try {
        const response = await fetch(`/api/profile/${section}/${itemId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const updatedItem = await response.json();
        const index = state[section].findIndex(item => item.id === itemId);
        if (index !== -1) {
            state[section][index] = updatedItem;
            renderSection(section);
            showNotification(`${section} updated successfully`, 'success');
        }
    } catch (error) {
        console.error(`Error updating ${section}:`, error);
        showNotification(`Failed to update ${section}`, 'error');
    }
}

// Delete item
async function deleteItem(section, itemId) {
    if (!confirm('Are you sure you want to delete this item?')) return;
    
    try {
        const response = await fetch(`/api/profile/${section}/${itemId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        state[section] = state[section].filter(item => item.id !== itemId);
        renderSection(section);
        showNotification(`${section} deleted successfully`, 'success');
    } catch (error) {
        console.error(`Error deleting ${section}:`, error);
        showNotification(`Failed to delete ${section}`, 'error');
    }
}

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Remove notification after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Update existing item
async function updateItem(section, itemId, data) {
    try {
        const response = await fetch(`/api/profile/${section}/${itemId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const updatedItem = await response.json();
        const index = state[section].findIndex(item => item.id === itemId);
        if (index !== -1) {
            state[section][index] = updatedItem;
            renderSection(section);
            showNotification(`${section.slice(0, -1)} updated successfully`, 'success');
        }
    } catch (error) {
        console.error(`Error updating ${section}:`, error);
        showNotification(`Failed to update ${section}`, 'error');
    }
}

// Delete item with confirmation
async function deleteItem(section, itemId) {
    if (!confirm('Are you sure you want to delete this item?')) return;
    
    try {
        const response = await fetch(`/api/profile/${section}/${itemId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        state[section] = state[section].filter(item => item.id !== itemId);
        renderSection(section);
        showNotification(`${section.slice(0, -1)} deleted successfully`, 'success');
    } catch (error) {
        console.error(`Error deleting ${section}:`, error);
        showNotification(`Failed to delete ${section}`, 'error');
    }
}