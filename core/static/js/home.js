(function(){
  function show(el){ if(!el) return; el.classList.remove('hidden'); el.setAttribute('aria-hidden','false'); el.style.display = 'flex'; }
  function hide(el){ if(!el) return; el.classList.add('hidden'); el.setAttribute('aria-hidden','true'); el.style.display = 'none'; }

  function ready(fn){ if(document.readyState !== 'loading') fn(); else document.addEventListener('DOMContentLoaded', fn); }

  ready(function(){
    var modal = document.getElementById('profileModal');
    var openBtn = document.getElementById('openProfileModal');
    var closeBtn = document.getElementById('closeProfileModal');

    if (!modal || !openBtn || !closeBtn) return;

    openBtn.addEventListener('click', function(){ show(modal); });
    closeBtn.addEventListener('click', function(){ hide(modal); });

    modal.addEventListener('click', function(e){
      if (e.target === modal) hide(modal);
    });

    document.addEventListener('keydown', function(e){
      if (e.key === 'Escape') hide(modal);
    });
  });
})();
