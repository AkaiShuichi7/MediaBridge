chrome.runtime.onMessage.addListener((message) => {
  if (message?.type === 'magnet-captured') chrome.action.setBadgeText({ text: '1' })
})

chrome.runtime.onStartup.addListener(async () => {
  const { capturedMagnet } = await chrome.storage.local.get('capturedMagnet')
  chrome.action.setBadgeText({ text: capturedMagnet ? '1' : '' })
})
