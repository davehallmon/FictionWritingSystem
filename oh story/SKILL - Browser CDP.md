---
name: browser-cdp
description: "Use this skill when you need to control a Chrome browser via CDP (Chrome DevTools Protocol) to reuse existing login sessions. Covers: launching Chrome in debug mode, opening URLs, waiting for page load, evaluating JavaScript, taking snapshots, and extracting auth tokens. Trigger phrases: browser automation, CDP, agent-browser, 浏览器操作, 操作浏览器, Chrome CDP, 复用登录态, extract token from browser."
metadata: {"openclaw":{"requires":{"bins":["agent-browser"]},"source":"https://github.com/zenstory-ai/oh-story-claudecode"}}
---
# Browser CDP Operation Tool

Control Chrome via the CDP (Chrome DevTools Protocol) to reuse existing login sessions and run browser automation.

## Prerequisites

- macOS / Linux / Windows (experimental); Google Chrome installed
- Node.js 20+
- `agent-browser` installed: `npm install -g agent-browser`

> ⚠️ **First launch will kill the user's regular Chrome.** You must ask the user for confirmation before starting (see "Launch Procedure" below) — otherwise the user may lose unsaved tabs / drafts.

---

## Launch Procedure (mandatory steps in skill mode)

**Step 1: Detect current state (no side effects)**

```bash
node {SKILL_DIR}/scripts/setup-cdp-chrome.js 9222 --detect-only
```

Output shape:

```
CDP_STATUS=ready                        # Ready, can be reused directly
CDP_URL=http://127.0.0.1:9222/json/version
BROWSER=Chrome/148.0.7778.168
```

Or:

```
CDP_STATUS=needs-setup
CHROME_RUNNING=yes                      # User has Chrome running, launching will kill it
CHROME_PID_COUNT=3
```
**Step 2: Branch on the detection result**

- `CDP_STATUS=ready` → use `agent-browser --cdp 9222 ...` directly, **do not run setup**.
- `CDP_STATUS=needs-setup` and `CHROME_RUNNING=no` → safe launch:
  ```bash
  node {SKILL_DIR}/scripts/setup-cdp-chrome.js 9222 --yes
  ```
- `CDP_STATUS=needs-setup` and `CHROME_RUNNING=yes` → **ask the user first with the AskUserQuestion tool**: inform them that N Chrome processes will be killed and unsaved work may be lost; only after explicit consent may you pass `--yes`; if the user refuses, abandon this automation.

**Why you can't just pass `--yes` directly:** when the script runs in a non-TTY environment (skill mode / Bash tool), if it detects Chrome is running and `--yes` was not passed, it exits with code 3 and reports `NEEDS_CONSENT: ...`, and **does not** silently kill processes. This is an intentional safeguard — but the skill flow should still ask the user first, rather than blindly passing `--yes` upon seeing exit 3.

---

## Setup-Script Options

| Option | Description |
|------|------|
| `--detect-only` | Only detect, do not modify any state (used by skills) |
| `--yes` | Already have user consent, skip the interactive prompt |
| `--reset` | Wipe `~/chrome-debug-profile` before launching (use when login state is invalid) |
| `--profile <name>` | Use a non-Default Chrome profile (e.g., `"Profile 1"`) |
| `--dry-run` | Print the steps that would be executed, do not execute |

Exit codes: `0` success / `1` general error / `2` user refused (TTY) / `3` consent required but `--yes` missing.

---

## Common Operations

### Open a Page and Wait for Load

```bash
agent-browser --cdp 9222 open "<URL>"
agent-browser --cdp 9222 wait 3000
```

### Extract Page Text

```bash
agent-browser --cdp 9222 eval 'document.body.innerText.substring(0, 8000)'
```

### Extract Auth Token

```bash
agent-browser --cdp 9222 eval 'localStorage.getItem("token") || document.cookie'
```

### Complex JS (with quotes / `$` / backticks)

Shell escaping is error-prone. Use one of the two approaches below:

```bash
# 1) base64-wrap the JS
agent-browser --cdp 9222 eval -b "$(echo -n "document.querySelectorAll('a').length" | base64)"

# 2) heredoc + --stdin
cat <<'EOF' | agent-browser --cdp 9222 eval --stdin
const links = document.querySelectorAll('a');
links.length;
EOF
```

### Page Interaction (snapshot to get element refs)

```bash
agent-browser --cdp 9222 snapshot -i        # Interactive elements only
agent-browser --cdp 9222 click "<CSS or @e1>"
agent-browser --cdp 9222 type "<sel>" "<text>"
```

---

## Stop / Cleanup

- Close the debug Chrome window. If the window is unresponsive, first locate the debug instance's PID via the `--user-data-dir` and kill only that one:
  - macOS / Linux: `pgrep -af chrome-debug-profile`
  - Windows: `wmic process where "name='chrome.exe'" get ProcessId,CommandLine | findstr chrome-debug-profile`
  Once you have the PID, `kill -9 {PID}` / `taskkill /F /PID {PID}`. If you cannot confirm which instance owns the debug profile, stop; **do not perform manual cleanup by batch-killing processes named after the Chrome executable** — that would also kill the user's regular Chrome.
  Exception: `setup-cdp-chrome.js --reset` does perform one executable-name-based cleanup internally; that is the launch flow bundled with this skill, which requires explicit `--yes` consent. Do not copy that pattern for manual troubleshooting.
- Login state expired: `node {SKILL_DIR}/scripts/setup-cdp-chrome.js 9222 --reset --yes` (note that `--yes` here also requires asking the user first).

---

## OpenCode Environment Notes

opencode has no tool for running command lines in the background, so long-running CDP operations (e.g., waiting for page load, large-scale data scraping) will block the entire session, leaving the CLI unresponsive.

### Timeout Wrapping

On Windows, wrap CDP commands with a PowerShell Job for timeout:

```powershell
$job = Start-Job { agent-browser --cdp 9222 eval "window.location.replace('https://www.qidian.com/rank/')" }
Wait-Job $job -Timeout 30 | Out-Null
if ($job.State -eq 'Running') { Stop-Job $job; Write-Output "⏱ CDP operation timed out (30s), please retry or interrupt manually" }
else { Receive-Job $job }
Remove-Job $job -Force
```

On macOS / Linux, use the `timeout` command:

```bash
timeout 30 agent-browser --cdp 9222 eval "window.location.replace('https://www.qidian.com/rank/')" || echo "⏱ CDP operation timed out (30s), please retry or interrupt manually"
```

### Known Limitations

Even with timeout wrapping, the following scenarios may still have issues:

| Scenario | Risk | Mitigation |
|------|------|------|
| Page-load timeout | The eval command waits forever | Set a 30s timeout, retry after timeout |
| Large-scale data scraping | Cumulative wait time across multi-page scraping is long | Per-page independent timeout, resume from breakpoint on failure |
| Chrome process is stuck | CDP connection drops but process is not gone | First confirm the PID belonging to the debug profile, kill only that debug instance, then reconnect; do not also kill regular Chrome |
| Network instability | Request hangs with no timeout | Automatic one-shot retry after timeout |

If you hit a persistently stuck operation, press `ESC` in opencode to interrupt manually.

---

## FAQ

| Problem | Solution |
|------|----------|
| `NEEDS_CONSENT` + exit code 3 | Use AskUserQuestion to ask the user if killing Chrome is allowed; on consent, rerun with `--yes` |
| CDP port is not listening | Run `--detect-only` again to confirm; if the port is occupied, switch ports |
| Page redirects to login | `snapshot -i` to find the login button and operate it |
| `eval` returns `null` | Check the localStorage key name; for JS containing quotes, use `eval -b` or `--stdin` |
| Login state expired | `setup-cdp-chrome.js 9222 --reset --yes` to recopy |
| Multiple Chrome profiles | Specify with `--profile "Profile 1"` |
| Chrome fails to start (30s timeout) | Try `--reset`; check for port conflicts; check whether `~/chrome-debug-profile/` is corrupted |
