(() => {
  const capture = (value) => {
    if (typeof value !== 'string' || !/^magnet:\?xt=urn:btih:/i.test(value)) return
    chrome.storage.local.set({ capturedMagnet: { value, title: document.title } })
    chrome.runtime.sendMessage({ type: 'magnet-captured' })
  }

  window.addEventListener('message', (event) => {
    if (event.source !== window || event.data?.source !== 'mediabridge-page-hook' || event.data?.type !== 'magnet-copied') return
    capture(event.data.value)
  })

  // Some sites use an internal clipboard helper that cannot be patched from
  // the page world. Probe only after an intentional click on a copy/magnet UI.
  document.addEventListener('click', (event) => {
    const trigger = event.target?.closest?.('button, a, [role="button"]')
    if (!trigger) return
    const label = `${trigger.textContent || ''} ${trigger.getAttribute('aria-label') || ''} ${trigger.getAttribute('title') || ''}`
    if (!/(magnet|磁力|copy|复制)/i.test(label)) return
    window.setTimeout(() => {
      chrome.runtime.sendMessage({ type: 'read-clipboard' }, (response) => capture(response?.text))
    }, 120)
  }, true)
})()
