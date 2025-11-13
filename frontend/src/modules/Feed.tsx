import React from 'react'

export function Feed() {
  const [q, setQ] = React.useState('')
  const [filter, setFilter] = React.useState('all')
  const [debouncedQ, setDebouncedQ] = React.useState('')

  // Debounce search input
  React.useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedQ(q)
    }, 300)
    return () => clearTimeout(timer)
  }, [q])

  // Filter posts based on search and emotion
  React.useEffect(() => {
    const cards = Array.from(document.querySelectorAll<HTMLElement>('.posts-list .post-card'))
    if (!cards.length) return
    
    const query = debouncedQ.trim().toLowerCase()
    
    cards.forEach(card => {
      let show = true
      
      // Text search filter
      if (query) {
        const text = (card.textContent || '').toLowerCase()
        show = text.includes(query)
      }
      
      // Emotion filter
      if (show && filter !== 'all') {
        const badge = card.querySelector('.badge')
        const emotion = badge ? badge.textContent?.toLowerCase().trim() : ''
        show = emotion === filter.toLowerCase()
      }
      
      card.style.display = show ? '' : 'none'
    })
    
    // Announce filter results to screen readers
    const visibleCount = cards.filter(c => c.style.display !== 'none').length
    const liveRegion = document.getElementById('aria-live-region')
    if (liveRegion && (query || filter !== 'all')) {
      liveRegion.textContent = `Showing ${visibleCount} post${visibleCount !== 1 ? 's' : ''}`
      setTimeout(() => { liveRegion.textContent = '' }, 1000)
    }
  }, [debouncedQ, filter])

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
        <div style={{ display: 'flex', gap: 8, alignItems: 'center', justifyContent: 'flex-end', flexWrap: 'wrap' }}>
          <button 
            className={filter === 'all' ? 'pill' : 'pill muted'} 
            onClick={() => setFilter('all')}
            aria-pressed={filter === 'all'}
            style={{ cursor: 'pointer', border: 'none', background: 'transparent' }}
          >
            All
          </button>
          <button 
            className={filter === 'happy' ? 'pill' : 'pill muted'} 
            onClick={() => setFilter('happy')}
            aria-pressed={filter === 'happy'}
            style={{ cursor: 'pointer', border: 'none', background: 'transparent' }}
          >
            Happy
          </button>
          <button 
            className={filter === 'sad' ? 'pill' : 'pill muted'} 
            onClick={() => setFilter('sad')}
            aria-pressed={filter === 'sad'}
            style={{ cursor: 'pointer', border: 'none', background: 'transparent' }}
          >
            Sad
          </button>
        </div>
      </div>

      <div style={{ marginTop: 10, fontSize: 12, color: 'var(--muted)' }}>
        Tip: Be kind. Mark supportive comments to spread a positive vibe.
      </div>
    </div>
  )
}


