(() => {
  window.addEventListener('message', (event) => {
    if (event.source !== window || event.data?.source !== 'mediabridge-page-hook' || event.data?.type !== 'magnet-copied') return
    const value = event.data.value
    if (typeof value !== 'string' || !/^magnet:\?xt=urn:btih:/i.test(value)) return
    chrome.storage.local.set({ capturedMagnet: { value, title: document.title } })
    chrome.runtime.sendMessage({ type: 'magnet-captured' })
  })
})()
