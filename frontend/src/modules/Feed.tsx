import React from 'react'

export function Feed() {
  const [q, setQ] = React.useState('')

  React.useEffect(() => {
    const cards = Array.from(document.querySelectorAll<HTMLElement>('.posts-list .post-card'))
    const query = q.trim().toLowerCase()
    if (!cards.length) return
    if (!query) {
      cards.forEach(c => c.style.display = '')
      return
    }
    cards.forEach(card => {
      const text = (card.textContent || '').toLowerCase()
      const match = text.includes(query)
      card.style.display = match ? '' : 'none'
    })
  }, [q])

  return (
    <div className="create-post-card" style={{ marginBottom: 16 }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12, flexWrap: 'wrap' }}>
        <div>
          <h3 style={{ marginBottom: 6 }}>Welcome back</h3>
          <p style={{ color: 'var(--muted)' }}>Share how you feel today. Your words can help someone else feel seen.</p>
        </div>
        <a href="#post-composer" className="btn primary">Start a Post</a>
      </div>

      <div className="feed-toolbar" style={{ marginTop: 12 }}>
        <input
          type="search"
          placeholder="Search posts and comments"
          value={q}
          onChange={e => setQ(e.target.value)}
          aria-label="Search posts"
          style={{ padding: '10px', borderRadius: 10, border: '1px solid var(--border)' }}
        />
        <div style={{ display: 'flex', gap: 8, alignItems: 'center', justifyContent: 'flex-end' }}>
          <span className="pill">Happy</span>
          <span className="pill">Sad</span>
          <span className="pill muted">All</span>
        </div>
      </div>

      <div style={{ marginTop: 10, fontSize: 12, color: 'var(--muted)' }}>
        Tip: Be kind. Mark supportive comments to spread a positive vibe.
      </div>
    </div>
  )
}


