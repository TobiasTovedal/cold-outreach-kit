# Weekly CRM sweep (optional, e.g. Mondays)

Read RULES.md and config.yaml first. Goal: every account note reflects what
the owner knows, not only what passed through email, and each active
account has up-to-date deal notes. INBOX.md keeps the CRM in step with Gmail
every weekday; this sweep adds what lives in the rest of the workspace
(meeting notes, project notes, to-do lists, free text the owner wrote in
account notes), catches email the inbox run did not match to an account,
and maintains the deal notes.

Gmail is read-only in this run: no drafts, no labels.

## 0. Load state
- Today, and the date of the latest entry in `<paths.logs>/CRM-log.md` (the
  "last sweep"). If the file has no entries, use today minus 8 days.
- All account notes: name, market, stage, status, contacts, last_touch,
  next_action, next_action_date, `## Contact log` and `# Deal notes`.
- Lookups: account names and unambiguous short forms, contact names,
  contact emails and domains -> account.
- The latest entry in `<paths.logs>/Followup.md`.

## 1. Workspace sweep
Find every `.md` file in the workspace modified since the last sweep,
excluding hidden folders (`.git`, `.obsidian`, ...), the automation folder
and `<paths.logs>`. Also include notes that link to an account and have
dated sections newer than the last sweep.

Read each file in full. Note what is about a specific account and new:
- a meeting or call that took place (who, when, about what);
- a concrete next step, ideally with a date;
- a person at the account with name, and role or email if written;
- anything that answers a deal-notes question (step 4).
Skip the owner's internal matters unless they clearly name an account and a
step with it. When a note is ambiguous about which account it concerns,
change nothing and list it under "Unclear".

## 2. Gmail catch-up (read only, last 7 days)
1. Search mail from the last 7 days (both directions) for each account name,
   e.g. `newer_than:7d "Acme Corp"`. Skip newsletters.
2. Search calendar invitations from the last 7 days and match them to
   accounts by attendee domain or name.
3. Read every thread from the last 7 days with an account contact or domain
   for deal-note content.
4. Keep only exchanges not already in the Contact log or the Followup log.

## 3. Update the account basics
For each finding:
- `## Contact log`: append `- YYYY-MM-DD: <one factual line> (source:
  [[note]] or "email")`, using the date of the event. Keep date order;
  never edit or remove existing lines.
- `last_touch`: move forward to the latest real contact. Never back.
- `next_action` / `next_action_date`: set only when a source states a
  concrete next step, and only if the current date is empty, past, or later
  than the new one. Otherwise suggest it in the log.
- `contacts`: add people who clearly belong to the account as
  `"Name | role | email"` (never guess an email). Never edit or remove.
Never change `stage`, `status`, `market` or `note`, and never create
account notes. Suggest those in the log instead.

## 4. Deal notes
Each account note has a `# Deal notes (updated YYYY-MM-DD)` section directly
above `## Contact log`, with these parts (a light MEDDPICC):

    ### Metrics        their numbers and goals, any business case shared
    ### Buyer          who decides and pays; has the owner met them?
    ### Criteria       what they judge the offer on
    ### Process        steps and meetings from interest to decision, dates
    ### Paperwork      procurement, legal, contract, timeline
    ### Pain           what is wrong today, and the cost of doing nothing
    ### Champion       who sells it internally, with evidence
    ### Competition    other vendors, internal builds, status quo

Work on accounts with a finding this week, plus up to 8 accounts whose
section is still empty and that have history (stage > 0 or a non-empty
contact log), highest stage first.

How to write: short factual bullets, each ending with its source
(`(source: [[note]])`, `(email YYYY-MM-DD)`). Only what a source says; a
person's opinion is written as theirs. Never edit or remove a bullet
without a source ending: those are the owner's. If a source contradicts
one, add a bullet starting `**New YYYY-MM-DD:**` and mention it in the log.
When a part is still unknown, add one bullet `**Gap:** <what to find out>
(auto)` and remove it once filled. Set the date in the heading when you
change the section.

## 5. Health check (list only)
- Active accounts with stage > 0 whose last_touch is over 30 days old and
  with no future next_action: "Cold accounts".
- next_action_date more than 14 days in the past.
- Stage >= 30 with no named Buyer or Champion.
- The same email under two accounts, or broken contact lines.
At most 10 per list, highest stage first.

## 6. Log
Prepend to `<paths.logs>/CRM-log.md`:

    ## YYYY-MM-DD HH:MM
    ### Updated
    ### Deal notes
    ### Suggestions for the owner
    ### Cold accounts and overdue actions
    ### Unclear

Write "Nothing." under empty headings.

## 7. Summary
At most 3 lines: accounts updated, deal notes filled, and the most
important suggestion or overdue account.
