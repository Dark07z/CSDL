// Script chính cho ứng dụng

document.addEventListener('DOMContentLoaded', function() {
    // Tự động ẩn alert sau 5 giây
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.display = 'none';
        }, 5000);
    });

    // Validate form input
    const forms = document.querySelectorAll('.form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#e74c3c';
                } else {
                    field.style.borderColor = '';
                }
            });

            if (!isValid) {
                e.preventDefault();
                alert('Vui lòng điền đầy đủ các trường bắt buộc!');
            }
        });

        // Remove error highlighting when user starts typing
        form.querySelectorAll('[required]').forEach(field => {
            field.addEventListener('input', function() {
                if (this.value.trim()) {
                    this.style.borderColor = '';
                }
            });
        });
    });

    // Filter table functionality
    const filterInputs = document.querySelectorAll('[data-filter]');
    filterInputs.forEach(input => {
        input.addEventListener('keyup', function() {
            const filterValue = this.value.toLowerCase();
            const tableRows = document.querySelectorAll('.table tbody tr');
            
            tableRows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(filterValue) ? '' : 'none';
            });
        });
    });
});

// Confirm delete action
function confirmDelete(message = 'Bạn chắc chắn muốn xóa?') {
    return confirm(message);
}

// Format currency
function formatCurrency(value) {
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND'
    }).format(value);
}

// Format date
function formatDate(date) {
    const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
    return new Date(date).toLocaleDateString('vi-VN', options);
}

// Print page
function printPage() {
    window.print();
}

// Export table to CSV
function exportTableToCSV(filename = 'export.csv') {
    const csv = [];
    const rows = document.querySelectorAll('.table tr');
    
    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const rowData = [];
        
        cols.forEach(col => {
            rowData.push('"' + col.textContent.trim() + '"');
        });
        
        csv.push(rowData.join(','));
    });
    
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const link = document.createElement('a');
    
    link.href = window.URL.createObjectURL(blob);
    link.download = filename;
    link.click();
}
