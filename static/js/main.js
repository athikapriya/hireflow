const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('sidebarToggle');

    toggleBtn.addEventListener('click', () => {
      if (window.innerWidth > 768) {
        // Desktop: collapse sidebar
        sidebar.classList.toggle('collapsed');
      } else {
        // Mobile: show offcanvas
        sidebar.classList.toggle('show');
      }
    });

    
    document.addEventListener('click', function(e) {
      if (window.innerWidth <= 768) {
        if (!sidebar.contains(e.target) && !toggleBtn.contains(e.target)) {
          sidebar.classList.remove('show');
        }
      }
    });