# Shared rules for the outreach tasks

Every scheduled task reads this file first, then `config.yaml`, then its
own procedure file. If a procedure file and this file disagree, this file
wins. The owner (see `config.yaml`) can edit anything; the owner's edits win
over everything.

`A` below is the automation folder (`<workspace>/<paths.automation>`). In
Cowork the workspace is mounted at `$HOME/mnt/<workspace folder name>`; use
the device shell for all file work.

## The tasks

| Task | Does, in this order |
|---|---|
| Daily run (morning and midday) | INBOX.md, then PROSPECTING.md |
| Weekly CRM sweep (optional) | CRM.md |

Procedures run one after the other in the same session. If one fails
partway, note it and still do the next one. Exception: if the computer or
the workspace folder is unreachable, stop and report that in one line.

### Lock
Runs started by hand could overlap with a scheduled one, so every run uses
`A/.lock`:
- At the start, read it. If it says `busy` and is less than 60 minutes old,
  wait 2 minutes and check again, for up to 20 minutes; then go ahead anyway
  and mention it in the summary.
- Then overwrite it with `busy <task name> <YYYY-MM-DD HH:MM>`.
- At the very end, overwrite it with `free <YYYY-MM-DD HH:MM>`.

## Time
Use the owner's time zone from `config.yaml`:
`TZ=<owner.timezone> date +%F` for today, `+%H:%M` for the time.
"Working days" are Monday to Friday.

## Who writes what

| File | Owner | Others |
|---|---|---|
| `outreach.csv` | Inbox | – |
| `drafts.csv` | Inbox (all status changes) | Prospecting appends rows for its drafts |
| Account notes: `last_touch`, `next_action`, `next_action_date`, `contacts`, `stage` (0→10 only), `## Contact log` | Inbox | CRM sweep may update them as CRM.md says (never `stage`) |
| New account notes | Inbox | – |
| `<logs>/Followup.md` | Inbox | – |
| `leads.csv`, `markets.md`, `criteria/*` | Prospecting | – |
| `<logs>/Leadlog.md` | Prospecting | – |
| `<logs>/CRM-log.md`, the `# Deal notes` section of account notes | CRM sweep | – |
| `playbook.md`, `config.yaml` | The owner | – |

Nobody ever changes an account's `status`, `market` or `note`, or any file
not listed above. Never modify or delete existing rows in `leads.csv`.

## Email
- Never send, trash or delete an email or a draft. The only Gmail writes
  allowed are creating drafts and (Inbox only) adding or removing the kit's
  labels (`gmail.labels` in config).
- Create every draft with includeSignature: true and write no sign-off in
  the body (the Gmail signature has it).
- After the first draft of a run, get it and check that the sender is
  `owner.sender_email`. If not, stop drafting and report it.
- Never edit a draft after creating it (updating can strip the signature).
  Create a new one instead.
- Never invent facts, people, roles, email addresses, times, numbers or
  commitments. Only claims listed in `playbook.md` may be made about the
  owner's company.
- No placeholders in drafts, ever. A draft contains nothing addressed to the
  owner: no `[...]`, no "TODO", no "insert", no bracketed notes. Every draft
  must be safe to send exactly as it is. If a draft would need something
  only the owner knows (meeting times, an answer, a price, a confirmation),
  do not create it. Ask under a heading **Questions for you** in the run's
  final message (one line per question: who, what you need), mention it in
  the notification, and note "waiting for owner" in the log. When the owner
  answers in that chat, create the draft then.
- Never mention sensitive or negative news about the recipient's
  organisation (accidents, lawsuits, layoffs, bad press) in a draft.
- Every draft gets a row in `drafts.csv`:
  `date,email,market,name,org,variant,experiment,subject,draft_id,status`
  with status `drafted`. Variants: `A`/`B` (cold, Prospecting), `FU1`/`FU2`,
  `RESEND` and `REPLY` (Inbox). `market` is the lowercase market code.
- Pending-draft limits (rows with status `drafted`): `limits.max_pending_cold`
  for A/B and `limits.max_pending_inbox` for Inbox variants.
- If Gmail tools are unavailable, skip every Gmail step, do the rest, and
  say "Gmail not connected" in the log entry and the summary.

## Research
- Every person, fact and link must come from a page you actually opened.
  Never guess an email address or build one from a naming pattern.
- No paid enrichment tools (Hunter, RocketReach, Apollo, ZoomInfo, Clearbit,
  Lusha and similar). LinkedIn only as individually viewed public pages;
  never scrape.
- If you delegate research to subagents, they return data only; the run
  writes every row itself and spot-checks emails it did not open itself.

## Files
- Never re-type file content from tool output. Edit with a short python
  read-modify-write; use python's csv module for CSV files.
- Log entries are written in `owner.log_language` and prepended directly
  above the first line that starts with `## ` (keep frontmatter, title and
  intro on top). Start each with `## YYYY-MM-DD HH:MM`.
- Do not git commit or push.
- Temporary files go outside the workspace folder (e.g. `$HOME/tmp`).

## Notifications
At the very end of a run, send at most one push notification, and only if
something needs the owner: a reply (meeting requests first), questions for
the owner, new drafts waiting, or a failure. At most 3 short lines, most
important first. Never for "nothing new".

The run's final message has each procedure's summary (at most 3 lines each)
under short headings (**Inbox**, **New leads**), then **Questions for you**
if there are any.
