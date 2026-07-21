declare const chrome: {
  permissions: {
    request: (permissions: { origins: string[] }) => Promise<boolean>
  }
  storage: {
    local: {
      get: (keys: string | string[]) => Promise<Record<string, any>>
      set: (items: Record<string, any>) => Promise<void>
      remove: (keys: string | string[]) => Promise<void>
    }
  }
  action: {
    setBadgeText: (details: { text: string }) => Promise<void>
  }
  runtime: {
    sendMessage: (message: unknown) => void
    onMessage: { addListener: (listener: (message: any) => void) => void }
    onStartup: { addListener: (listener: () => void) => void }
  }
}
