    // Global variable to track which section we're currently editing
    let currentSection = '';
    let currentItemId = null;
    let isEditing = false;

    // Function to toggle between text and input fields for editing the profile
    function toggleEditProfile() {
        const nameText = document.getElementById('profile-name-text');
        const nameInput = document.getElementById('profile-name-input');
        const titleText = document.getElementById('profile-title-text');
        const titleInput = document.getElementById('profile-title-input');
        const editButton = document.querySelector('.edit-btn');
        
        // Check if we're in edit mode
        const isEditing = nameInput.style.display === 'none';
        
        if (isEditing) {
            // Switch to edit mode
            nameText.style.display = 'none';
            nameInput.style.display = 'inline-block';
            titleText.style.display = 'none';
            titleInput.style.display = 'inline-block';
            editButton.textContent = 'Save';
        } else {
            // Switch back to view mode
            nameText.style.display = 'inline-block';
            nameInput.style.display = 'none';
            titleText.style.display = 'inline-block';
            titleInput.style.display = 'none';
            editButton.textContent = 'Edit';

            // Save the updated name and title
            const updatedName = nameInput.value;
            const updatedTitle = titleInput.value;

            // Update the profile UI with new values
            nameText.textContent = updatedName;
            titleText.textContent = updatedTitle;

            // Optionally, send the updated data to the server or store it locally
            console.log('Updated Name:', updatedName);
            console.log('Updated Title:', updatedTitle);
        }
    }

    // Initialize the date picker when the page loads
    document.addEventListener('DOMContentLoaded', function() {
        // Handle form submission
        document.getElementById('modal-form').addEventListener('submit', handleFormSubmit);
        
        // Handle "currently work here" checkbox
        document.getElementById('current-checkbox').addEventListener('change', function(e) {
            const endDateInput = document.getElementById('end-date');
            if (e.target.checked) {
                endDateInput.value = '';
                endDateInput.disabled = true;
            } else {
                endDateInput.disabled = false;
            }
        });
    });

    function openModal(type, isAdding = false) {
        currentSection = type;
        isEditing = !isAdding;
        
        const modal = document.getElementById('modal');
        const modalOverlay = document.getElementById('modal-overlay');
        const modalForm = document.getElementById('modal-form');
        const modalTitle = document.getElementById('modal-title');
        
        modalOverlay.style.display = 'block';
        modal.style.display = 'block';
        modalTitle.textContent = isAdding ? `Add New ${capitalizeFirstLetter(type)}` : `Edit ${capitalizeFirstLetter(type)}`;
        
        // Reset form and remove any previous values
        modalForm.reset();
        document.getElementById('end-date').disabled = false;
        
        if (!isAdding && currentItemId) {
            // Fill form with existing data if editing
            fillFormWithExistingData(currentItemId);
        }
    }

    function fillFormWithExistingData(itemId) {
        const item = document.getElementById(itemId);
        if (!item) return;
        
        const title = item.querySelector('.item-title').textContent;
        const subtitle = item.querySelector('.item-subtitle').textContent;
        const description = item.querySelector('.item-description')?.textContent || '';
        const dateRange = item.querySelector('.date-range').textContent;
        
        document.getElementById('title').value = title;
        document.getElementById('subtitle').value = subtitle;
        document.getElementById('description').value = description;
        
        // Parse and set dates
        if (dateRange.includes('Present')) {
            document.getElementById('current-checkbox').checked = true;
            document.getElementById('end-date').disabled = true;
            
            // Extract start date
            const startDate = dateRange.split(' - ')[0];
            document.getElementById('start-date').value = formatDateForInput(startDate);
        } else {
            const [startDate, endDate] = dateRange.split(' - ');
            document.getElementById('start-date').value = formatDateForInput(startDate);
            document.getElementById('end-date').value = formatDateForInput(endDate);
        }
    }

    function formatDateForInput(dateStr) {
        const date = new Date(dateStr);
        return date.toISOString().split('T')[0];
    }

    function formatDateForDisplay(dateStr) {
        if (!dateStr) return '';
        const date = new Date(dateStr);
        return date.toLocaleString('default', { month: 'long', year: 'numeric' });
    }

    function handleFormSubmit(e) {
        e.preventDefault();
        
        const formData = {
            title: document.getElementById('title').value,
            subtitle: document.getElementById('subtitle').value,
            description: document.getElementById('description').value,
            startDate: document.getElementById('start-date').value,
            endDate: document.getElementById('current-checkbox').checked ? 'Present' : document.getElementById('end-date').value
        };
        
        if (isEditing && currentItemId) {
            updateExistingItem(currentItemId, formData);
        } else {
            addNewItem(formData);
        }
        
        closeModal();
    }

    function addNewItem(formData) {
        const container = document.getElementById(`${currentSection}-content`);
        
        // Remove empty state message if it exists
        const emptyState = container.querySelector('.empty-state');
        if (emptyState) {
            emptyState.remove();
        }
        
        const newId = `${currentSection.slice(0, 4)}-${Date.now()}`;
        
        const dateRange = formData.endDate === 'Present' 
            ? `${formatDateForDisplay(formData.startDate)} - Present`
            : `${formatDateForDisplay(formData.startDate)} - ${formatDateForDisplay(formData.endDate)}`;
        
        const itemHTML = `
            <div class="item" id="${newId}">
                <div class="item-title">${formData.title}</div>
                <div class="item-subtitle">${formData.subtitle}</div>
                <div class="date-range">${dateRange}</div>
                ${formData.description ? `<div class="item-description">${formData.description}</div>` : ''}
                <div class="item-actions">
                    <button onclick="edit${capitalizeFirstLetter(currentSection)}(this)">✎</button>
                    <button onclick="delete${capitalizeFirstLetter(currentSection)}(this)">🗑</button>
                </div>
            </div>
        `;
        
        container.insertAdjacentHTML('afterbegin', itemHTML);
    }

    function updateExistingItem(itemId, formData) {
        const item = document.getElementById(itemId);
        if (!item) return;
        
        const dateRange = formData.endDate === 'Present' 
            ? `${formatDateForDisplay(formData.startDate)} - Present`
            : `${formatDateForDisplay(formData.startDate)} - ${formatDateForDisplay(formData.endDate)}`;
        
        item.querySelector('.item-title').textContent = formData.title;
        item.querySelector('.item-subtitle').textContent = formData.subtitle;
        item.querySelector('.date-range').textContent = dateRange;
        
        const descriptionEl = item.querySelector('.item-description');
        if (formData.description) {
            if (descriptionEl) {
                descriptionEl.textContent = formData.description;
            } else {
                item.insertAdjacentHTML('beforeend', `<div class="item-description">${formData.description}</div>`);
            }
        } else if (descriptionEl) {
            descriptionEl.remove();
        }
    }

    function closeModal() {
        document.getElementById('modal').style.display = 'none';
        document.getElementById('modal-overlay').style.display = 'none';
        currentItemId = null;
        isEditing = false;
    }

    function checkEmptyState(sectionId) {
        const container = document.getElementById(sectionId);
        const items = container.querySelectorAll('.item');
        
        if (items.length === 0) {
            const emptyStateHTML = `<div class="empty-state">Click + to add your ${sectionId.replace('-content', '')}</div>`;
            container.innerHTML = emptyStateHTML;
        }
    }

    // Edit functions for each section
    function editAchievement(button) {
        currentItemId = button.closest('.item').id;
        openModal('achievements', false);
    }

    function editExperience(button) {
        currentItemId = button.closest('.item').id;
        openModal('experience', false);
    }

    function editProject(button) {
        currentItemId = button.closest('.item').id;
        openModal('projects', false);
    }

    // Delete functions
    function deleteAchievement(button) {
        if (confirm("Are you sure you want to delete this achievement?")) {
            const item = button.closest('.item');
            item.remove();
            checkEmptyState('achievements-content');
        }
    }

    function deleteExperience(button) {
        if (confirm("Are you sure you want to delete this experience?")) {
            const item = button.closest('.item');
            item.remove();
            checkEmptyState('experience-content');
        }
    }

    function deleteProject(button) {
        if (confirm("Are you sure you want to delete this project?")) {
            const item = button.closest('.item');
            item.remove();
            checkEmptyState('projects-content');
        }
    }

    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }