# Prompts for the scheduled tasks

Paste each prompt into a scheduled task in the Claude desktop app, connect
the workspace folder `{{WORKSPACE}}` to the task, and set the time. The real
instructions live in RULES.md and the procedure files, so these prompts
rarely need to change.

## Daily outreach run (weekdays, e.g. 08:40 and 12:40)

```
You are running {{OWNER}}'s daily outreach run. {{COMPANY}} sells {{PRODUCT}}. This run brings Gmail and the CRM up to date, prepares replies and follow-ups as drafts, and then researches new leads in one market and drafts cold emails to them.

Work in the connected folder "{{WORKSPACE}}" with the device shell (it is mounted at $HOME/mnt/{{WORKSPACE}}); the automation folder is $HOME/mnt/{{WORKSPACE}}/automation. If the computer or folder is not reachable, stop and report that in one line; do not attempt the run elsewhere.

1. Read RULES.md and config.yaml in the automation folder. RULES.md applies to everything below and wins over the procedure files. Take the lock as it describes.
2. Follow INBOX.md step by step.
3. Then follow PROSPECTING.md step by step, even if step 2 partly failed (say so in the summary).
4. Release the lock, send at most one push notification as RULES.md describes, and finish with both summaries under **Inbox** and **New leads**, then **Questions for you** if any.

Hard rules even if a file says otherwise: never send, trash or delete an email or draft; Gmail writes are limited to creating drafts (includeSignature true, no sign-off in the body, sender {{SENDER}}) and the kit's labels. Never invent people, roles, email addresses, facts or links; every lead needs a verified source. No paid enrichment tools. Never modify existing rows in leads.csv. Never change an account's status. Do not git commit or push.
```

## Weekly CRM sweep (optional, e.g. Mondays 09:00)

```
You are running {{OWNER}}'s weekly CRM sweep. {{COMPANY}} sells {{PRODUCT}}. This run brings what is in the workspace notes and Gmail into the account notes, and fills in each account's deal notes from the sources.

Work in the connected folder "{{WORKSPACE}}" with the device shell (mounted at $HOME/mnt/{{WORKSPACE}}); the automation folder is $HOME/mnt/{{WORKSPACE}}/automation. If the computer or folder is not reachable, stop and report that in one line.

1. Read RULES.md and config.yaml in the automation folder. Take the lock as it describes.
2. Follow CRM.md step by step.
3. Release the lock, send at most one push notification as RULES.md describes, and finish with the summary.

Hard rules even if a file says otherwise: Gmail is read-only (no drafts, no labels, never send, trash or delete). Never invent facts; every line you add needs a source. Never remove lines the owner wrote. Never change stage or status. Do not git commit or push.
```
