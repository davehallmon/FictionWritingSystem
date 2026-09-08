---
name: browser-cdp
description: "Use this skill when you need to control a Chrome browser via CDP (Chrome DevTools Protocol) to reuse existing login sessions. Covers: launching Chrome in debug mode, opening URLs, waiting for page load, evaluating JavaScript, taking snapshots, and extracting auth tokens. Trigger phrases: browser automation, CDP, agent-browser, 浏览器操作, 操作浏览器, Chrome CDP, 复用登录态, extract token from browser."
metadata: {"openclaw":{"requires":{"bins":["agent-browser"]},"source":"https://github.com/zenstory-ai/oh-story-claudecode"}}
---
# Browser CDP Operations Tool

Control Chrome through CDP, reuse an existing authenticated session, and perform browser-automation operations.

## Prerequisites

- macOS / Linux / Windows (experimental), with Google Chrome installed
- Node.js 20+
- `agent-browser` installed: `npm install -g agent-browser`

> ⚠️ **The first launch will kill the user's regular Chrome.** Obtain user consent before launching (see “Launch Process” below), or the user may lose unsaved tabs or drafts.

---

## Launch Process (Mandatory in Skill Mode)

**Step 1: Detect current state (no side effects)**

```bash
node {SKILL_DIR}/scripts/setup-cdp-chrome.js 9222 --detect-only
```

Example output:

```
CDP_STATUS=ready                        # 已就绪，可直接复用
CDP_URL=http://127.0.0.1:9222/json/version
BROWSER=Chrome/148.0.7778.168
```

Or:

```
CDP_STATUS=needs-setup
CHROME_RUNNING=yes                      # 用户有 Chrome 在跑，启动会杀掉
CHROME_PID_COUNT=3
```

**Step 2: Branch according to detection results**

- `CDP_STATUS=ready` → Use `agent-browser --cdp 9222 ...` directly; **do not run setup**.
- `CDP_STATUS=needs-setup` and `CHROME_RUNNING=no` → Launch safely:
  ```bash
  node {SKILL_DIR}/scripts/setup-cdp-chrome.js 9222 --yes
  ```
- `CDP_STATUS=needs-setup` and `CHROME_RUNNING=yes` → **First use the AskUserQuestion tool to obtain confirmation**. Explain that the action will kill N Chrome processes and may lose unsaved work. After consent, launch with `--yes`; if the user refuses, abandon this automation attempt.

**Why not pass `--yes` immediately:** In a non-TTY environment (skill mode / Bash tool), when Chrome is running and `--yes` is absent, the script reports `NEEDS_CONSENT: ...`, exits with code 3, and **does not** silently kill processes. This is an intentional safeguard—but the skill workflow must still ask the user first rather than seeing code 3 and blindly retrying with `--yes`.

---

## Launch Script Options

| Option | Description |
|------|------|
| `--detect-only` | Detect only; do not modify any state (for skill use) |
| `--yes` | Consent has been obtained; skip the interactive prompt |
| `--reset` | Clear `~/chrome-debug-profile` before launch (use when authentication is invalid) |
| `--profile <name>` | Use a Chrome profile other than Default (for example, `"Profile 1"`) |
| `--dry-run` | Print the steps that would run without executing them |

Exit codes: `0` success / `1` general error / `2` user refused (TTY) / `3` consent required but `--yes` absent.

---

## Common Operations

### Open a Page and Wait for Loading

```bash
agent-browser --cdp 9222 open "<URL>"
agent-browser --cdp 9222 wait 3000
```

### Extract Page Text

```bash
agent-browser --cdp 9222 eval 'document.body.innerText.substring(0, 8000)'
```

### Extract an Auth Token

```bash
agent-browser --cdp 9222 eval 'localStorage.getItem("token") || document.cookie'
```

### Complex JS (Containing Quotes / `$` / Backticks)

Shell escaping is error-prone. Use one of these methods:

```bash
# 1) base64 包裹
agent-browser --cdp 9222 eval -b "$(echo -n "document.querySelectorAll('a').length" | base64)"

# 2) heredoc + --stdin
cat <<'EOF' | agent-browser --cdp 9222 eval --stdin
const links = document.querySelectorAll('a');
links.length;
EOF
```

### Page Interaction (Use a Snapshot to Obtain Element References)

```bash
agent-browser --cdp 9222 snapshot -i        # 仅交互元素
agent-browser --cdp 9222 click "<CSS or @e1>"
agent-browser --cdp 9222 type "<sel>" "<text>"
```

---

## Stop / Clean Up

- Close the debug Chrome window. If it is unresponsive, first identify only the debug instance's PID by checking `--user-data-dir`:
  - macOS / Linux: `pgrep -af chrome-debug-profile`
  - Windows: `wmic process where "name='chrome.exe'" get ProcessId,CommandLine | findstr chrome-debug-profile`
  After obtaining the PID, use `kill -9 {PID}` / `taskkill /F /PID {PID}`. If ownership cannot be verified, stop. **Manual cleanup must never terminate processes in bulk by the Chrome executable name**, because that would also kill the user's regular Chrome.
  Exception: `setup-cdp-chrome.js --reset` does perform one executable-name cleanup internally. It is part of this skill's built-in launch flow and requires explicit `--yes` consent; do not copy this behavior during manual troubleshooting.
- If authentication expires: `node {SKILL_DIR}/scripts/setup-cdp-chrome.js 9222 --reset --yes` (remember that `--yes` still requires prior user consent).

---

## OpenCode Environment Considerations

OpenCode has no tool for running command lines in the background. Long-running CDP operations, such as waiting for a page to load or scraping data in bulk, block the entire session and may leave the CLI unresponsive.

### Timeout Wrappers

On Windows, wrap CDP commands in a PowerShell Job with a timeout:

```powershell
$job = Start-Job { agent-browser --cdp 9222 eval "window.location.replace('https://www.qidian.com/rank/')" }
Wait-Job $job -Timeout 30 | Out-Null
if ($job.State -eq 'Running') { Stop-Job $job; Write-Output "⏱ CDP 操作超时（30s），请重试或手动打断" }
else { Receive-Job $job }
Remove-Job $job -Force
```

On macOS / Linux, use the `timeout` command:

```bash
timeout 30 agent-browser --cdp 9222 eval "window.location.replace('https://www.qidian.com/rank/')" || echo "⏱ CDP 操作超时（30s），请重试或手动打断"
```

### Known Limitations

Even with timeout wrappers, the following situations may still cause problems:

| Scenario | Risk | Mitigation |
|------|------|------|
| Page-load timeout | The eval command waits forever | Set a 30-second timeout and retry after timeout |
| Bulk data scraping | Cumulative waits become excessive while paginating | Give every page an independent timeout and resume from the checkpoint after failure |
| Chrome process hangs | The CDP connection drops, but the process does not exit | First verify the PID belonging to the debug profile; terminate only that debug instance and reconnect, without affecting regular Chrome |
| Network instability | A request hangs without timing out | Retry once automatically after timeout |

If an operation remains stuck, press `ESC` in OpenCode to interrupt it manually.

---

## Common Problems

| Problem | Solution |
|------|----------|
| `NEEDS_CONSENT` + exit code 3 | Use AskUserQuestion to ask permission to kill Chrome, then rerun with `--yes` after consent |
| CDP port is not listening | Check again with `--detect-only`; if the port is occupied, choose another port |
| Page redirects to sign-in | Use `snapshot -i` to find and operate the sign-in button |
| `eval` returns `null` | Check the localStorage key; for JS containing quotes, use `eval -b` or `--stdin` |
| Authentication expired | Copy again with `setup-cdp-chrome.js 9222 --reset --yes` |
| Multiple Chrome profiles exist | Specify one with `--profile "Profile 1"` |
| Chrome does not launch (30-second timeout) | Try `--reset`; check for a port conflict; inspect `~/chrome-debug-profile/` for corruption |
