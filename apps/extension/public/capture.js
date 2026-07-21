(() => {
  let lastCapturedValue = ''
  let lastCapturedAt = 0
  let lastClipboardProbeAt = 0

  const capture = (value) => {
    if (typeof value !== 'string' || !/^magnet:\?xt=urn:btih:/i.test(value)) return
    value = value.trim()
    const now = Date.now()
    if (value === lastCapturedValue && now - lastCapturedAt < 2000) return
    lastCapturedValue = value
    lastCapturedAt = now
    chrome.storage.local.set({ capturedMagnet: { value, title: document.title } })
    chrome.runtime.sendMessage({ type: 'magnet-captured' })
  }

  const findContextualMagnet = (target) => {
    if (!(target instanceof Element)) return null
    const clipboardValue = target.closest('[data-clipboard-text]')?.getAttribute('data-clipboard-text')
    if (clipboardValue) return clipboardValue
    const directLink = target.closest('a[href^="magnet:"]')
    if (directLink) return directLink.getAttribute('href')

    // The site's copy icon is an <i> sibling of the magnet <a> in the same
    // download-row <li>. Deliberately inspect only that immediate row: looking
    // through arbitrary ancestors makes unrelated page clicks false positives.
    const copyControl = target.closest('i, button, [role="button"], [data-copy], [class*="copy"]')
    const row = copyControl?.parentElement
    const siblingLink = row?.querySelector(':scope > a[href^="magnet:"]')
    return siblingLink?.getAttribute('href') || null
  }

  const probeClipboard = () => {
    const now = Date.now()
    if (now - lastClipboardProbeAt < 500) return
    lastClipboardProbeAt = now
    chrome.runtime.sendMessage({ type: 'read-clipboard' }, (response) => capture(response?.text))
  }

  window.addEventListener('message', (event) => {
    if (event.source !== window || event.data?.source !== 'mediabridge-page-hook') return
    if (event.data?.type === 'magnet-copied') capture(event.data.value)
    if (event.data?.type === 'copy-event') probeClipboard()
  })

  // Some sites render a styled copy control inside an ordinary magnet anchor.
  // The magnet is not visible in the UI, but is still available as the href.
  document.addEventListener('click', (event) => {
    capture(findContextualMagnet(event.target))
  }, true)

})()
