document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('host-form');
  const hostList = document.getElementById('host-list');

  if (form) {
    form.addEventListener('submit', async function(e) {
      e.preventDefault();
      
      const formData = new FormData(form);
      
      try {
        const response = await fetch('/hosts', {
          method: 'POST',
          body: formData
        });

        const result = await response.json();

        if (response.ok) {
          showAlert('Host added successfully!', 'success');
          form.reset();
          loadHosts();
        } else {
          showAlert(result.detail || 'Failed to add host', 'error');
        }
      } catch (error) {
        showAlert('Error adding host', 'error');
        console.error('Error:', error);
      }
    });
  }

  loadHosts();
});

async function loadHosts() {
  try {
    const response = await fetch('/hosts');
    const hosts = await response.json();
    
    const hostList = document.getElementById('host-list');
    if (!hostList) return;

    hostList.innerHTML = hosts.map(host => `
      <div class="host-item">
        <div>
          <div><strong>${host.host}</strong></div>
          <div class="text-sm text-gray-600">${host.email}</div>
        </div>
        <div class="host-status ${host.is_up ? 'status-up' : 'status-down'}">
          ${host.is_up ? '● Online' : '● Offline'}
        </div>
      </div>
    `).join('');
  } catch (error) {
    console.error('Error loading hosts:', error);
  }
}

function showAlert(message, type) {
  const alertContainer = document.getElementById('alert-container');
  if (!alertContainer) return;

  const alert = document.createElement('div');
  alert.className = `alert alert-${type}`;
  alert.textContent = message;

  alertContainer.innerHTML = '';
  alertContainer.appendChild(alert);

  setTimeout(() => {
    alert.remove();
  }, 5000);
}
