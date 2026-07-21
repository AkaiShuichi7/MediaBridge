const clipboardRequests = new Map()
let lastPopupOpenedAt = 0

async function ensureOffscreenDocument() {
  if (await chrome.offscreen.hasDocument()) return
  await chrome.offscreen.createDocument({
    url: 'offscreen.html',
    reasons: ['CLIPBOARD'],
    justification: 'Read a magnet link only after the user clicks a copy control.',
  })
}

async function readClipboard() {
  await ensureOffscreenDocument()
  const requestId = crypto.randomUUID()
  return new Promise((resolve, reject) => {
    clipboardRequests.set(requestId, { resolve, reject })
    chrome.runtime.sendMessage({ type: 'offscreen-read-clipboard', requestId })
  })
}

chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message?.type === 'magnet-captured') {
    chrome.action.setBadgeText({ text: '1' })
    // Chrome 127+ lets an extension open its action popup from this user
    // initiated capture path. Older browsers keep the badge as a fallback.
    if (typeof chrome.action.openPopup === 'function' && Date.now() - lastPopupOpenedAt > 500) {
      lastPopupOpenedAt = Date.now()
      chrome.action.openPopup().catch(() => {})
    }
  }
  if (message?.type === 'clipboard-read-result') {
    const request = clipboardRequests.get(message.requestId)
    if (!request) return
    clipboardRequests.delete(message.requestId)
    if (message.error) request.reject(new Error(message.error))
    else request.resolve(message.text)
  }
  if (message?.type === 'read-clipboard') {
    readClipboard().then((text) => sendResponse({ text })).catch(() => sendResponse({ text: '' }))
    return true
  }
})

chrome.runtime.onStartup.addListener(async () => {
  const { capturedMagnet } = await chrome.storage.local.get('capturedMagnet')
  chrome.action.setBadgeText({ text: capturedMagnet ? '1' : '' })
})
