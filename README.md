# Cold Outreach Kit

A Claude-run B2B outreach routine. Every weekday, scheduled Claude tasks:

1. **Inbox**: sync what you sent from Gmail, read replies, draft answers and
   follow-ups, handle bounces, and keep a small CRM up to date.
2. **Prospecting**: research up to 20 new, verified, named leads in one
   market, and draft cold emails to them as an A/B experiment.

Claude only ever creates **drafts**. You read them and press send yourself.
Nothing is sent, trashed or deleted by the automation.

It works for any industry. A guided setup asks you about your company,
product, buyers and markets. From your answers it writes your config, email
playbook, targeting criteria and the prompts for your scheduled tasks.

## What you need

- The **Claude desktop app** with Cowork (a paid Claude plan with scheduled
  tasks).
- The **Gmail** connector, signed in to the account you send from.
  **Google Calendar** is optional. With it, follow-ups can propose meeting
  times from your free slots; without it, Claude asks you for times.
- A folder on your computer for the workspace, connected to Claude. An
  [Obsidian](https://obsidian.md) vault works well, because the CRM is plain
  Markdown notes, but any folder works.
- Python 3 on your computer (macOS has it already).

## Quick start

1. Download or clone this repo into the folder you will use as your workspace,
   e.g. `~/Documents/Outreach/cold-outreach-kit`.
2. In the Claude desktop app, start a new Cowork task and connect the
   workspace folder.
3. Paste this:

   ```
   Read cold-outreach-kit/SETUP.md in my connected folder and walk me through
   setting up my cold outreach automation.
   ```

4. Answer Claude's questions (about 20 minutes). Claude then:
   - writes `automation/config.yaml`, `automation/playbook.md` and a criteria
     file for your first market;
   - creates the data files (`leads.csv`, `outreach.csv`, `drafts.csv`) and
     the CRM folders;
   - creates the Gmail labels, with your OK;
   - writes `automation/TASK-PROMPTS.md` with your two scheduled-task prompts,
     and helps you create the tasks;
   - does a dry run: 3 leads and 3 drafts so you can check the tone.

## Your daily loop

- Open Gmail drafts, read, edit if you like, and send. Delete the drafts you
  don't want; the next run notices and marks them discarded.
- Read the run summary (and push notification). Answer any
  **Questions for you**, for example meeting times. Claude creates the
  waiting drafts when you answer in that chat.
- Edit `automation/playbook.md` whenever you learn what works. Your edits
  win over everything else.

## Folder layout after setup

```
<workspace>/
  automation/
    config.yaml        your settings
    RULES.md           shared rules (safety, ownership, locks)
    INBOX.md           inbox + follow-up procedure
    PROSPECTING.md     lead research + cold drafts procedure
    CRM.md             optional weekly CRM sweep
    playbook.md        how your emails are written (yours to edit)
    markets.md         market rotation
    criteria/          one targeting file per market
    leads.csv  outreach.csv  drafts.csv
    scripts/validate_leads.py
    TASK-PROMPTS.md    prompts for your scheduled tasks
  crm/
    accounts/          one note per account (company you sell to)
    logs/              Followup.md, Leadlog.md, CRM-log.md
```

## Safety by design

- Drafts only. Gmail writes are limited to drafts and the kit's own labels.
- No invented people, roles, emails or facts. Every lead needs a source page
  that Claude actually opened. Email addresses are never guessed from a
  pattern.
- No placeholders in drafts. If a draft needs something only you know,
  Claude asks you instead of writing `[insert time]`.
- No paid enrichment tools (Hunter, Apollo and similar) and no LinkedIn
  scraping.
- Respect your local rules on cold email (e.g. GDPR legitimate interest and
  an easy opt-out in the EU, CAN-SPAM in the US). The kit does not give
  legal advice; see `docs/compliance.md`.

More detail: `docs/how-it-works.md`. Example config for a made-up company:
`examples/acme/`.

## License

MIT
