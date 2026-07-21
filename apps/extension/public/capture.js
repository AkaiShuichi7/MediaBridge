(() => {
  let lastCapturedValue = ''
  let lastCapturedAt = 0

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

  window.addEventListener('message', (event) => {
    if (event.source !== window || event.data?.source !== 'mediabridge-page-hook' || event.data?.type !== 'magnet-copied') return
    capture(event.data.value)
  })

  // Some sites render a styled copy control inside an ordinary magnet anchor.
  // The magnet is not visible in the UI, but is still available as the href.
  document.addEventListener('click', (event) => {
    capture(findContextualMagnet(event.target))
  }, true)

  // Some sites use an internal clipboard helper that cannot be patched from
  // the page world. Probe only after an intentional click on a copy/magnet UI.
  document.addEventListener('click', (event) => {
    // The preceding listener already captured a nearby magnet anchor. Do not
    // start the delayed Clipboard fallback for the same user click.
    if (findContextualMagnet(event.target)) return
    if (!(event.target instanceof Element)) return
    const copyControl = event.target.closest('i, button, [role="button"], [data-copy], [class*="copy"]')
    if (!copyControl) return
    let element = copyControl
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
