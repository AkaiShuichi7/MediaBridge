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
    const originalWrite = navigator.clipboard?.write?.bind(navigator.clipboard)
    if (originalWrite) {
      navigator.clipboard.write = (items) => {
        for (const item of items) {
          if (item.types?.includes('text/plain')) {
            item.getType('text/plain').then((blob) => blob.text()).then(emit).catch(() => {})
          }
        }
        return originalWrite(items)
      }
    }
  } catch { /* A page may expose a read-only Clipboard implementation. */ }
  document.addEventListener('copy', (event) => {
    emit(event.clipboardData?.getData('text/plain'))
    // execCommand('copy') and some libraries populate clipboardData after the
    // capture phase. Tell the isolated script to verify the final clipboard.
    window.setTimeout(() => window.postMessage({ source: 'mediabridge-page-hook', type: 'copy-event' }, '*'), 0)
  }, true)
})()
