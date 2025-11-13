// Base scripts for theme toggle and comments toggle

// Toggle comments with ARIA support
function toggleComments(commentId, btn) {
  const commentSection = document.getElementById(commentId);
  if (!commentSection) return;
  
  const isHidden = commentSection.classList.contains('hidden');
  
  if (isHidden) {
    commentSection.classList.remove('hidden');
  } else {
    commentSection.classList.add('hidden');
  }
  
  try {
    if (btn) {
      const expanded = isHidden ? 'true' : 'false';
      btn.setAttribute('aria-expanded', expanded);
      btn.classList.toggle('active', isHidden);
    }
  } catch (e) {}
}

// Make toggleComments available globally for onclick handlers
window.toggleComments = toggleComments;

// Theme toggle initialization and handlers
(function attachThemeToggle(){
  try {
    const btns = [
      document.getElementById('themeToggle'), 
      document.getElementById('themeToggleBottom')
    ].filter(Boolean);
    
    if (!btns.length) return;
    
    function toggleTheme(){
      const root = document.documentElement;
      const isDark = root.classList.toggle('theme-dark');
      
      try { 
        localStorage.setItem('theme', isDark ? 'dark' : 'light'); 
      } catch(e) {}
      
      try { 
        btns.forEach(b => b.setAttribute('aria-pressed', isDark ? 'true' : 'false')); 
        
        // Announce theme change to screen readers
        const liveRegion = document.getElementById('aria-live-region');
        if (liveRegion) {
          liveRegion.textContent = isDark ? 'Dark mode enabled' : 'Light mode enabled';
          setTimeout(() => { liveRegion.textContent = ''; }, 1000);
        }
      } catch(e) {}
    }
    
    // Initialize aria-pressed to current theme
    try {
      const isDarkInit = document.documentElement.classList.contains('theme-dark');
      btns.forEach(b => b.setAttribute('aria-pressed', isDarkInit ? 'true' : 'false'));
    } catch(e) {}
    
    // Attach click handlers
    btns.forEach(b => b.addEventListener('click', toggleTheme));
  } catch (e) {}
})();
