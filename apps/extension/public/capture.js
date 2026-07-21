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

  // Some sites render a styled copy control inside an ordinary magnet anchor.
  // The magnet is not visible in the UI, but is still available as the href.
  document.addEventListener('click', (event) => {
    let element = event.target instanceof Element ? event.target : null
    // A common layout places the copy icon and magnet anchor as siblings in a
    // small list item. Search that local container before trying Clipboard.
    for (let depth = 0; element && depth < 5; depth += 1, element = element.parentElement) {
      const link = element.matches('a[href^="magnet:"]')
        ? element
        : element.querySelector('a[href^="magnet:"]')
      if (link) {
        capture(link.getAttribute('href'))
        return
      }
    }
  }, true)

  // Some sites use an internal clipboard helper that cannot be patched from
  // the page world. Probe only after an intentional click on a copy/magnet UI.
  document.addEventListener('click', (event) => {
    let element = event.target instanceof Element ? event.target : null
    const labels = []
    // Copy icons often have no own text: inspect their small button/card
    // ancestor rather than requiring the clicked SVG itself to be labelled.
    for (let depth = 0; element && depth < 4; depth += 1, element = element.parentElement) {
      labels.push(element.textContent || '', element.getAttribute('aria-label') || '', element.getAttribute('title') || '')
    }
    const label = labels.join(' ')
    if (!/(magnet|磁力|copy|复制)/i.test(label)) return
    window.setTimeout(() => {
      chrome.runtime.sendMessage({ type: 'read-clipboard' }, (response) => capture(response?.text))
    }, 120)
  }, true)
})()
