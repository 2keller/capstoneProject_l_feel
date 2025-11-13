(function(){
  function show(el){ 
    if(!el) return; 
    el.classList.remove('hidden'); 
    el.setAttribute('aria-hidden','false'); 
    el.style.display = 'flex'; 
  }
  
  function hide(el){ 
    if(!el) return; 
    el.classList.add('hidden'); 
    el.setAttribute('aria-hidden','true'); 
    el.style.display = 'none'; 
  }

  // Simple focus trap
  function trapFocus(element) {
    const focusableElements = element.querySelectorAll(
      'a[href], button:not([disabled]), textarea:not([disabled]), input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])'
    );
    const firstFocusable = focusableElements[0];
    const lastFocusable = focusableElements[focusableElements.length - 1];

    function handleTabKey(e) {
      if (e.key !== 'Tab') return;
      if (e.shiftKey) {
        if (document.activeElement === firstFocusable) {
          lastFocusable.focus();
          e.preventDefault();
        }
      } else {
        if (document.activeElement === lastFocusable) {
          firstFocusable.focus();
          e.preventDefault();
        }
      }
    }

    element.addEventListener('keydown', handleTabKey);
    return () => element.removeEventListener('keydown', handleTabKey);
  }

  function ready(fn){ if(document.readyState !== 'loading') fn(); else document.addEventListener('DOMContentLoaded', fn); }

  ready(function(){
    var modal = document.getElementById('profileModal');
    var openBtn = document.getElementById('openProfileModal');
    var closeBtn = document.getElementById('closeProfileModal');

    if (!modal || !openBtn || !closeBtn) return;

    var cleanupFocusTrap = null;

    openBtn.addEventListener('click', function(){ 
      show(modal); 
      cleanupFocusTrap = trapFocus(modal);
      // Focus first input
      var firstInput = modal.querySelector('input, textarea');
      if (firstInput) setTimeout(function(){ firstInput.focus(); }, 100);
    });
    
    closeBtn.addEventListener('click', function(){ 
      hide(modal); 
      if (cleanupFocusTrap) cleanupFocusTrap();
      openBtn.focus(); // Return focus
    });

    modal.addEventListener('click', function(e){
      if (e.target === modal) {
        hide(modal);
        if (cleanupFocusTrap) cleanupFocusTrap();
        openBtn.focus();
      }
    });

    document.addEventListener('keydown', function(e){
      if (e.key === 'Escape' && !modal.classList.contains('hidden')) {
        hide(modal);
        if (cleanupFocusTrap) cleanupFocusTrap();
        openBtn.focus();
      }
    });
  });
})();
