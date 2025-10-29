import React from 'react'

export function Feed() {
  return (
    <div className="create-post-card" style={{ marginBottom: 16 }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12, flexWrap: 'wrap' }}>
        <div>
          <h3 style={{ marginBottom: 6 }}>Welcome back 👋</h3>
          <p style={{ color: 'var(--muted)' }}>Share how you feel today. Your words can help someone else feel seen.</p>
        </div>
        <a href="#post-composer" className="btn primary">Start a Post</a>
      </div>

      <div style={{ marginTop: 12, display: 'flex', gap: 8, flexWrap: 'wrap' }}>
        <span className="pill">Happy</span>
        <span className="pill">Sad</span>
        <span className="pill">Angry</span>
        <span className="pill">Surprise</span>
        <span className="pill">Fear</span>
        <span className="pill muted">Neutral</span>
      </div>

      <div style={{ marginTop: 10, fontSize: 12, color: 'var(--muted)' }}>
        Tip: Be kind. Mark supportive comments to spread a positive vibe.
      </div>
    </div>
  )
}


