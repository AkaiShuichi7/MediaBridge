# MediaBridge browser extension

The first version captures a magnet link only after the user clicks a site's
copy action or a magnet link styled as a copy control. It also detects copy
icons placed beside a magnet link in the same download row. It never submits a
task automatically: open the extension popup,
select a library, then confirm the submission.

Use **Cancel** to discard a captured link. Cancelling or submitting a task
clears the pending capture and closes the automatically opened popup.

## Install for development

```bash
npm ci
npm run build
```

Open `chrome://extensions`, enable Developer mode, choose **Load unpacked**,
and select `apps/extension/dist`. The manifest includes a stable development
key, so builds extracted to different folders keep the same extension ID.

Before loading this version, remove every older MediaBridge unpacked extension
from `chrome://extensions`. Keep exactly one enabled copy; otherwise a content
script from one extension and a popup from another use separate storage.

## Configure

1. In the MediaBridge Web UI, create an access token in **System settings →
   Access tokens**.
2. Open the extension popup and enter the public MediaBridge URL plus that
   `mb_…` token. The browser asks for permission only for that server origin.
3. On a resource site, click its magnetic-link copy button. The popup badge
   becomes `1`; on Chrome 127 or later the popup opens automatically. Choose a
   media library and send the task. Older Chrome versions keep the badge as a
   fallback and require opening the popup manually.

If a site uses an unusual copy implementation and no badge appears, open the
popup and choose **Read magnet link from clipboard**. This reads the clipboard
only for that explicit popup click and is the reliable manual fallback.

After installing or reloading the extension, refresh any resource tab that was
already open so the capture script can be injected.

The extension does run a small content script on pages in order to observe a
site writing a magnet link to the clipboard. For sites that use an internal
clipboard helper, it reads the clipboard once immediately after a user clicks a
control labelled magnet/copy. It only stores values matching
`magnet:?xt=urn:btih:…`; it does not continuously read the clipboard and does
not submit anything without a final user click.

## Packaging

The `extension-package.yml` workflow builds a loadable extension directory and
uploads a ZIP artifact when only `apps/extension` changes. It is intentionally
independent of the main Docker image workflow.
