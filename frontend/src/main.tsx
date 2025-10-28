import React from 'react'
import { createRoot } from 'react-dom/client'
import { Feed } from './modules/Feed'

const candidates = ['react-feed-root', 'root']
for (const id of candidates) {
  const el = document.getElementById(id)
  if (el) {
    const root = createRoot(el)
    root.render(<Feed />)
    break
  }
}


