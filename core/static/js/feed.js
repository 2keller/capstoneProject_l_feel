(function(){
  function getCookie(name){
    const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return m ? m.pop() : '';
  }
  const csrf = getCookie('csrftoken');

  function isAjaxOk(res){ return res && (res.ok || res.status === 200); }

  async function ajaxSubmit(form){
    const action = form.getAttribute('action');
    const method = (form.getAttribute('method') || 'POST').toUpperCase();
    const fd = new FormData(form);
    const res = await fetch(action, {
      method,
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': csrf
      },
      body: fd
    });
    const data = await res.json();
    return data;
  }

  function updateCounts(postId, counts){
    const likeEl = document.getElementById(`like-count-${postId}`);
    const dislikeEl = document.getElementById(`dislike-count-${postId}`);
    const commentEl = document.getElementById(`comment-count-${postId}`);
    if (likeEl && typeof counts.like_count !== 'undefined') likeEl.textContent = counts.like_count;
    if (dislikeEl && typeof counts.dislike_count !== 'undefined') dislikeEl.textContent = counts.dislike_count;
    if (commentEl && typeof counts.comment_count !== 'undefined') commentEl.textContent = counts.comment_count;
  }

  function appendComment(postId, comment){
    const container = document.getElementById(`comments-${postId}`);
    if (!container) return;
    const addFormBlock = container.querySelector('.add-comment');
    const div = document.createElement('div');
    div.className = 'comment' + (comment.is_supportive ? ' highlight-support' : '');
    div.innerHTML = `<strong>${comment.user}</strong>: ${comment.content}<small>${comment.created_at}</small>`;
    if (addFormBlock) {
      container.insertBefore(div, addFormBlock);
    } else {
      container.appendChild(div);
    }
  }

  function setBusy(btn, busy){
    if (!btn) return;
    btn.disabled = !!busy;
    btn.classList.toggle('is-disabled', !!busy);
  }

  function findPostId(form){
    var postEl = form.closest('[data-post-id]');
    return postEl ? postEl.getAttribute('data-post-id') : null;
  }

  document.addEventListener('submit', async function(e){
    const form = e.target;
    if (!(form instanceof HTMLFormElement)) return;

    // Like
    if (form.classList.contains('js-like-form')){
      e.preventDefault();
      const btn = form.querySelector('button');
      const postId = findPostId(form);
      const likeCountEl = postId && document.getElementById(`like-count-${postId}`);
      const original = likeCountEl ? parseInt(likeCountEl.textContent || '0', 10) : 0;
      // optimistic UI
      if (likeCountEl) likeCountEl.textContent = String(original + 1);
      if (btn) btn.classList.add('active');
      setBusy(btn, true);
      try {
        const data = await ajaxSubmit(form);
        if (data && data.ok){ updateCounts(data.post_id, data); }
        else { if (likeCountEl) likeCountEl.textContent = String(original); if (btn) btn.classList.remove('active'); }
      } catch(err) { if (likeCountEl) likeCountEl.textContent = String(original); if (btn) btn.classList.remove('active'); }
      finally { setBusy(btn, false); }
      return;
    }

    // Dislike
    if (form.classList.contains('js-dislike-form')){
      e.preventDefault();
      const btn = form.querySelector('button');
      const postId = findPostId(form);
      const dislikeCountEl = postId && document.getElementById(`dislike-count-${postId}`);
      const original = dislikeCountEl ? parseInt(dislikeCountEl.textContent || '0', 10) : 0;
      if (dislikeCountEl) dislikeCountEl.textContent = String(original + 1);
      if (btn) btn.classList.add('active');
      setBusy(btn, true);
      try {
        const data = await ajaxSubmit(form);
        if (data && data.ok){ updateCounts(data.post_id, data); }
        else { if (dislikeCountEl) dislikeCountEl.textContent = String(original); if (btn) btn.classList.remove('active'); }
      } catch(err) { if (dislikeCountEl) dislikeCountEl.textContent = String(original); if (btn) btn.classList.remove('active'); }
      finally { setBusy(btn, false); }
      return;
    }

    // Comment
    if (form.classList.contains('js-comment-form')){
      e.preventDefault();
      try {
        const data = await ajaxSubmit(form);
        if (data && data.ok){
          updateCounts(data.post_id, { comment_count: data.comment_count });
          appendComment(data.post_id, data.comment);
          // reset textarea
          const ta = form.querySelector('textarea');
          if (ta) ta.value = '';
        }
      } catch(err) { /* noop */ }
      return;
    }
  });
})();
