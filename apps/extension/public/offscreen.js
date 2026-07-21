chrome.runtime.onMessage.addListener((message) => {
  if (message?.type !== 'offscreen-read-clipboard') return
  navigator.clipboard.readText()
    .then((text) => chrome.runtime.sendMessage({ type: 'clipboard-read-result', requestId: message.requestId, text }))
    .catch((error) => chrome.runtime.sendMessage({ type: 'clipboard-read-result', requestId: message.requestId, error: String(error) }))
})
