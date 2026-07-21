(() => {
  const isMagnet = (value) => typeof value === 'string' && /^magnet:\?xt=urn:btih:/i.test(value.trim())
  const emit = (value) => {
    if (isMagnet(value)) window.postMessage({ source: 'mediabridge-page-hook', type: 'magnet-copied', value: value.trim() }, '*')
  }
  try {
    const originalWriteText = navigator.clipboard?.writeText?.bind(navigator.clipboard)
    if (originalWriteText) {
      navigator.clipboard.writeText = (value) => {
        emit(value)
        return originalWriteText(value)
      }
    }
  } catch { /* A page may expose a read-only Clipboard implementation. */ }
  document.addEventListener('copy', (event) => emit(event.clipboardData?.getData('text/plain')), true)
})()
