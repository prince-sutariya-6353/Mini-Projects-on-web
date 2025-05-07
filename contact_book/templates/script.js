document.addEventListener('DOMContentLoaded', function() {
  // Dark mode toggle
  const darkModeToggle = document.getElementById('darkModeToggle');

  // Check for saved theme preference or use preferred color scheme
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.body.classList.add('dark-mode');
    darkModeToggle.checked = true;
  }

  // Toggle dark mode
  darkModeToggle.addEventListener('change', function() {
    if (this.checked) {
      document.body.classList.add('dark-mode');
      localStorage.setItem('theme', 'dark');
    } else {
      document.body.classList.remove('dark-mode');
      localStorage.setItem('theme', 'light');
    }
  });

  // Add loading effect when submitting forms
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    form.addEventListener('submit', function() {
      this.classList.add('loading');
    });
  });

  // Show toast notifications for actions
  function showToast(message, isError = false) {
    const toast = document.createElement('div');
    toast.className = isError ? 'toast error' : 'toast';
    toast.textContent = message;
    document.body.appendChild(toast);

    // Remove toast after animation completes
    setTimeout(() => {
      document.body.removeChild(toast);
    }, 3500);
  }

  // Check for URL parameters to show appropriate toasts
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.has('added')) {
    showToast('Contact added successfully!');
  } else if (urlParams.has('updated')) {
    showToast('Contact updated successfully!');
  } else if (urlParams.has('deleted')) {
    showToast('Contact deleted successfully!');
  } else if (urlParams.has('error')) {
    showToast('An error occurred. Please try again.', true);
  } else if (urlParams.has('imported')) {
    const count = urlParams.get('imported');
    showToast(`Successfully imported ${count} contacts!`);
  }

  // Add confirmation for delete actions
  const deleteLinks = document.querySelectorAll('.btn-delete');
  deleteLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      if (!confirm('Are you sure you want to delete this contact?')) {
        e.preventDefault();
      }
    });
  });

  // Add inline editing functionality
  const tableInputs = document.querySelectorAll('table input, table select');
  tableInputs.forEach(input => {
    const originalValue = input.value;

    input.addEventListener('focus', function() {
      this.dataset.original = this.value;
    });

    input.addEventListener('blur', function() {
      if (this.value !== this.dataset.original) {
        this.closest('tr').classList.add('changed');
      } else {
        this.closest('tr').classList.remove('changed');
      }
    });
  });

  // Search functionality
  const searchBox = document.getElementById('searchBox');
  if (searchBox) {
    searchBox.addEventListener('input', function() {
      const searchTerm = this.value.toLowerCase().trim();
      const rows = document.querySelectorAll('table tbody tr');

      rows.forEach(row => {
        // Get values from input fields
        const inputs = row.querySelectorAll('input');
        let rowText = '';
        inputs.forEach(input => {
          rowText += input.value.toLowerCase() + ' ';
        });

        // Also check category
        const category = row.querySelector('select').value.toLowerCase();
        rowText += category;

        if (rowText.includes(searchTerm)) {
          row.style.display = '';
        } else {
          row.style.display = 'none';
        }
      });
    });
  }

  // Sorting functionality
  const sortableHeaders = document.querySelectorAll('th[data-sort]');
  sortableHeaders.forEach(header => {
    header.addEventListener('click', function() {
      const sortBy = this.dataset.sort;
      const tbody = document.querySelector('table tbody');
      const rows = Array.from(tbody.querySelectorAll('tr'));

      // Toggle sort direction
      const isAscending = !this.classList.contains('sorted-asc');

      // Remove sorted classes from all headers
      sortableHeaders.forEach(h => {
        h.classList.remove('sorted-asc', 'sorted-desc');
      });

      // Add sorted class to current header
      this.classList.add(isAscending ? 'sorted-asc' : 'sorted-desc');

      // Sort the rows
      rows.sort((a, b) => {
        const aValue = a.querySelector(`input[name="${sortBy}"]`).value.toLowerCase();
        const bValue = b.querySelector(`input[name="${sortBy}"]`).value.toLowerCase();

        if (isAscending) {
          return aValue.localeCompare(bValue);
        } else {
          return bValue.localeCompare(aValue);
        }
      });

      // Re-append rows in sorted order
      rows.forEach(row => {
        tbody.appendChild(row);
      });
    });
  });

  // Check for empty table and show message
  const tableBody = document.querySelector('table tbody');
  if (tableBody && tableBody.querySelectorAll('tr').length === 0) {
    const tableContainer = document.querySelector('.table-container');
    const emptyState = document.createElement('div');
    emptyState.className = 'empty-state';
    emptyState.innerHTML = `
      <p>No contacts found. Add your first contact using the form above.</p>
    `;
    tableContainer.innerHTML = '';
    tableContainer.appendChild(emptyState);
  }

  // File input styling
  const fileInput = document.getElementById('importFile');
  if (fileInput) {
    fileInput.addEventListener('change', function() {
      const fileName = this.files[0] ? this.files[0].name : 'Choose CSV';
      const fileLabel = document.querySelector('.file-label');
      fileLabel.textContent = fileName;
    });
  }
});