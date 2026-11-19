# How it works

## The pieces

| Piece | What it is |
|---|---|
| Scheduled tasks | Claude desktop app tasks that run on your computer at set times and work in your connected workspace folder |
| `RULES.md` | Safety rules, file ownership and the lock. Wins over the procedures |
| `INBOX.md` | Syncs Gmail, handles replies, bounces and follow-ups, updates the CRM |
| `PROSPECTING.md` | Picks a market, researches verified leads, drafts cold emails |
| `CRM.md` | Optional weekly sweep of your notes into account notes and deal notes |
| `config.yaml` | Your settings |
| `playbook.md` | How emails are written: facts, structure, tone, follow-ups, experiments |
| `criteria/criteria-<market>.md` | Who to target in each market and where to find them |
| `markets.md` | Market rotation (core every 14 days, expansion every 42) |
| `leads.csv` | Every researched lead, with its source page |
| `outreach.csv` | Everyone you have emailed: dates, replies, follow-up stage, outcome |
| `drafts.csv` | Every draft the kit created and what happened to it (drafted / sent / discarded) |
| `crm/accounts/*.md` | One note per organisation: stage, contacts, next action, contact log |
| `crm/logs/*.md` | What each run did, newest first |

## A day in the life

1. **08:40, inbox.** Claude looks at what you sent since the last run. Drafts
   you sent are marked `sent` and the person is added to `outreach.csv`.
   Drafts you deleted are marked `discarded`. Replies from the last three
   days are read and classified (meeting, question, redirect, not now, no).
   Claude drafts answers where it can, and asks you where it can't
   (e.g. "which times can you do?"). People who haven't replied after 6
   working days get a follow-up draft. Account notes get the new contact
   log lines, next actions and contacts.
2. **08:40, prospecting.** Claude picks the market that is most overdue,
   reads its criteria file, and researches up to 20 new named people,
   checking each one on a page it opened. It writes them to `leads.csv`,
   then drafts cold emails to those with a published address, alternating
   experiment arms A and B.
3. **You.** You get one push notification if something needs you. You read
   the drafts in Gmail, send the good ones, delete the rest, and answer any
   questions in the chat.
4. **12:40.** The same again: anything you sent in the morning is picked up,
   new replies are handled, and another market is researched.

## Why the rules look the way they do

- **Drafts only.** You stay in control of everything that leaves your
  outbox.
- **No placeholders.** A draft with "[insert time]" sent by mistake is
  worse than no draft. Claude asks instead.
- **Verified sources only.** Invented names or guessed addresses burn your
  domain's reputation fast.
- **One follow-up by default.** More follow-ups raise the risk of being
  marked as spam; one good one gets most of the replies.
- **The organisation's name is the only personal line.** Role-based
  "personalisation" ("As Head of X at Y, you...") reads as automated.
- **Labels.** `<prefix>/Cold`, `/Follow-up 1`, `/Follow-up 2`, `/Replied` and
  `/No response` let you see the state of every thread in Gmail.
- **The lock.** Stops a manual run and a scheduled run from editing the same
  files at once.

## Changing things

- Tone, structure, facts: edit `playbook.md`.
- Who to target: edit the market's criteria file.
- Which markets and how often: edit `markets.md`.
- Limits, follow-up timing, language: edit `config.yaml`.
- Anything else: ask Claude in a chat with the workspace connected, e.g.
  "Add Austria as an expansion market" or "Our new proof point is ...".
