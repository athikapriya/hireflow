const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('sidebarToggle');

    toggleBtn.addEventListener('click', () => {
      if (window.innerWidth > 768) {
        
        sidebar.classList.toggle('collapsed');
      } else {
        
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