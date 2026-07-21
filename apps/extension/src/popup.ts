import './popup.css'

type Library = { name: string }
type Settings = { serverUrl: string; token: string }
type CapturedMagnet = { value: string; title?: string }

const app = document.querySelector<HTMLElement>('#app')!
const state: { settings: Settings; magnet?: CapturedMagnet; libraries: Library[] } = {
  settings: { serverUrl: '', token: '' },
  libraries: [],
}

function normalizedServerUrl(value: string) {
  return value.trim().replace(/\/+$/, '')
}

function show(message: string, error = false) {
  const notice = document.querySelector<HTMLElement>('#notice')!
  notice.textContent = message
  notice.className = error ? 'notice error' : 'notice success'
}

async function requestHostPermission(url: string) {
  const origin = new URL(url).origin
  return chrome.permissions.request({ origins: [`${origin}/*`] })
}

async function api(path: string, options: RequestInit = {}) {
  const response = await fetch(`${state.settings.serverUrl}${path}`, {
    ...options,
    headers: { Authorization: `Bearer ${state.settings.token}`, 'Content-Type': 'application/json', ...(options.headers || {}) },
    credentials: 'omit',
  })
  const payload = await response.json().catch(() => null)
  if (!response.ok || payload?.code !== 0) throw new Error(payload?.message || `请求失败 (${response.status})`)
  return payload.data
}

async function saveSettings() {
  const serverUrl = normalizedServerUrl((document.querySelector<HTMLInputElement>('#server-url')!).value)
  const token = (document.querySelector<HTMLInputElement>('#token')!).value.trim()
  if (!serverUrl || !token.startsWith('mb_')) return show('请填写 MediaBridge 地址和以 mb_ 开头的访问令牌。', true)
  try {
    if (!await requestHostPermission(serverUrl)) return show('需要允许该站点访问权限，才能连接 MediaBridge。', true)
    state.settings = { serverUrl, token }
    await chrome.storage.local.set({ settings: state.settings })
    show('连接设置已保存。')
    await loadLibraries()
  } catch {
    show('服务器地址无效。', true)
  }
}

async function loadLibraries() {
  if (!state.settings.serverUrl || !state.settings.token) return
  try {
    state.libraries = (await api('/api/libraries')).libraries
    render()
  } catch (error) {
    show(error instanceof Error ? error.message : '无法读取媒体库。', true)
  }
}

async function submitTask() {
  const libraryName = (document.querySelector<HTMLSelectElement>('#library')!).value
  if (!state.magnet || !libraryName) return show('请先选择媒体库。', true)
  try {
    await api('/api/tasks', { method: 'POST', body: JSON.stringify({ magnet: state.magnet.value, library_name: libraryName, name: state.magnet.title || undefined }) })
    await chrome.storage.local.remove('capturedMagnet')
    state.magnet = undefined
    chrome.action.setBadgeText({ text: '' })
    render()
    show('离线任务已提交到 MediaBridge。')
  } catch (error) {
    show(error instanceof Error ? error.message : '任务提交失败。', true)
  }
}

function render() {
  const configured = Boolean(state.settings.serverUrl && state.settings.token)
  const hasMagnet = Boolean(state.magnet)
  app.innerHTML = `
    <section class="header"><strong>MediaBridge</strong><span>磁力任务助手</span></section>
    <section class="card"><label>MediaBridge 地址<input id="server-url" type="url" placeholder="https://media.example.com" value="${state.settings.serverUrl}" /></label>
    <label>访问令牌<input id="token" type="password" placeholder="mb_…" value="${state.settings.token}" /></label>
    <button id="save" class="secondary">保存并连接</button></section>
    <section class="card ${hasMagnet ? '' : 'empty'}"><h2>已捕获的磁力链接</h2>
      ${hasMagnet ? `<p class="title">${state.magnet?.title || '当前页面资源'}</p><code>${state.magnet?.value}</code>
      <label>目标媒体库<select id="library"><option value="">请选择</option>${state.libraries.map((library) => `<option value="${library.name}">${library.name}</option>`).join('')}</select></label>
      <button id="submit" ${configured && state.libraries.length ? '' : 'disabled'}>发送到 MediaBridge</button>` : '<p>点击页面中的“复制磁力链接”按钮后，链接会显示在这里；插件不会自动提交。</p>'}
    </section><p id="notice" class="notice"></p>`
  document.querySelector('#save')?.addEventListener('click', () => void saveSettings())
  document.querySelector('#submit')?.addEventListener('click', () => void submitTask())
}

async function start() {
  const stored = await chrome.storage.local.get(['settings', 'capturedMagnet'])
  state.settings = stored.settings || state.settings
  state.magnet = stored.capturedMagnet
  render()
  await loadLibraries()
}

void start()
