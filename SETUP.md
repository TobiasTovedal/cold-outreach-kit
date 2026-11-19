# Guided setup (instructions for Claude)

You are setting up the Cold Outreach Kit for the person in this chat (called
"the user" below). Work through the phases in order. Be friendly and brief.
Ask questions in small batches (3–5 at a time, with AskUserQuestion when it
is available, otherwise in plain text), propose sensible defaults, and show
the user what you wrote before moving on. Write every file in the user's
language of choice for logs, but keep procedure files in English.

Never send, trash or delete emails during setup. Never invent facts about the
user's company: if you don't know something, ask.

Throughout, `KIT` is the folder holding this file and `WS` is the workspace
folder the user connected (the parent of `KIT` unless the user says
otherwise). In Cowork, run commands with the device shell; connected folders
are mounted at `$HOME/mnt/<folder name>`.

## Phase 0: Check the environment

1. Find `KIT` and `WS` (`ls $HOME/mnt/`). Confirm with the user that `WS` is
   where the workspace should live.
2. Check `python3 --version` in the device shell.
3. Check that a Gmail tool is available (search for it if tools are
   deferred). If not, tell the user to connect Gmail in the app and stop
   here until it is.
4. Check whether a Google Calendar tool is available. Note the answer; it
   decides how follow-ups get meeting times.
5. If `WS/automation/config.yaml` already exists, ask whether to update the
   existing setup or start over. Never overwrite the user's files without a
   clear yes.

## Phase 1: Interview

Collect the answers below. Offer examples and defaults; accept "skip" where
marked optional.

**A. You and your sender**
1. Full name, and the first name used in the emails.
2. The Gmail address the emails are sent from (send-as address).
3. Time zone, and working hours for calls (default 09:00–16:00).
4. Does your Gmail signature already contain a sign-off ("Best regards")
   and your details? (The kit always uses the Gmail signature and never
   writes a sign-off in the body. If they have no signature, help them
   set one up in Gmail settings first.)
5. Language for logs and summaries (default English).

**B. Company and offer**
6. Company name and website.
7. What you sell, in one plain sentence (what it does, for whom).
8. 2–4 concrete things a customer gets from it (outcomes, not features).
9. Proof points you can always state truthfully: named customers you may
   mention, results, awards, certifications. Mark any that may NOT be
   mentioned in emails.
10. The most common objection, and your one-sentence answer to it.
11. Anything that must never be said (claims, competitor names, prices).

**C. Who you sell to (ICP)**
12. Type of organisation, and the size signals that make it a fit
    (headcount, revenue, number of sites, tech stack...).
13. Segments to tag leads with (2–4 short values, e.g. `enterprise`,
    `midmarket`; or `university`, `chain`).
14. Role buckets: 2–4 groups of job titles you target, with example titles
    (e.g. "Operations leadership: COO, VP Operations"). Which bucket is
    most important?
15. Titles to exclude (e.g. IT, procurement), if any.
16. Research sources that name these people in your industry: association
    member lists, conference programmes, trade press, company "team" pages,
    public registers. (Claude will add general ones.)

**D. Markets**
17. Which countries or regions, in priority order. For each: `core`
    (revisited every 14 days) or `expansion` (every 42 days).
18. Email language per market (default: English everywhere, or the local
    language where the user writes it well).

**E. Email style**
19. Greeting style: first names, or "Dear Dr./Mr./Ms. Surname".
20. Tone words (default: short, humble, concrete, no hype).
21. Default subject line (plain topic, 3–5 words).
22. Do they want an A/B experiment? Default experiment E1: arm B adds a
    last line "If you're not the right person, who would you suggest I talk
    to?".
23. Follow-ups: how many (default 1, max 2), after how many working days
    (default 6), and close the lead after how many more (default 10).
    Should follow-ups propose concrete call times? (Uses Google Calendar if
    connected; otherwise Claude asks the user for times each time.)

**F. CRM and schedule**
24. Use the CRM (account notes)? Default yes. Folder for account notes
    (default `crm/accounts`). If the workspace is an Obsidian vault, links
    use `[[Account]]`.
25. Stages: default `0 no contact, 10 interested, 30 meeting held,
    60 proposal, 90 negotiation`.
26. Schedule: default weekdays 08:40 (inbox + prospecting) and 12:40
    (inbox + prospecting). Optional weekly CRM sweep, Mondays 09:00.
27. Leads per run (default 20) and maximum pending drafts (default 50 cold,
    50 inbox).
28. Label prefix in Gmail (default `Outreach`).

## Phase 2: Write the workspace

1. Run the init script. It copies the templates and creates empty data
   files; it never overwrites existing files:

       python3 "$KIT/scripts/init_workspace.py" --kit "$KIT" --workspace "$WS" \
         --accounts "<accounts folder>" --logs "crm/logs"

2. Fill `WS/automation/config.yaml` with the answers. Use a short
   read-modify-write script, not re-typing. Keep the comments.
3. Write `WS/automation/playbook.md` from `templates/automation/playbook.md`.
   Fill every `{{...}}` from the answers. Write one complete reference draft
   in each email language, 80–150 words, in the user's tone. Read it aloud in
   your head: if it sounds like a brochure, rewrite it plainer. Show it to
   the user and revise until they are happy.
4. Write `WS/automation/markets.md` with the markets table.
5. For the first market, write `WS/automation/criteria/criteria-<code>.md`
   from `criteria/_template.md`: local job titles per bucket, segment values,
   geography and research sources. Other markets get their criteria file
   automatically on their first run.
6. Add every market code to `VALID_MARKETS` in
   `WS/automation/scripts/validate_leads.py`, and the segment values to
   `VALID_SEGMENTS` (leave it empty to allow any).
7. Run `python3 WS/automation/scripts/validate_leads.py` and fix any problem.

## Phase 3: Gmail

1. Ask before creating anything. Then create these labels (with the user's
   prefix): `<prefix>/Cold`, `<prefix>/Follow-up 1`, `<prefix>/Follow-up 2`,
   `<prefix>/Replied`, `<prefix>/No response`. Skip any that exist.
2. Write their label ids into `config.yaml` (`gmail.labels`).

## Phase 4: Scheduled tasks

1. Copy `templates/automation/TASK-PROMPTS.md` to `WS/automation/` (the init
   script already did) and replace `{{OWNER}}`, `{{COMPANY}}`, `{{PRODUCT}}`,
   `{{WORKSPACE}}` and `{{SENDER}}` with the real values.
2. Show the user the prompts. Offer to create the scheduled tasks for them
   (requires their computer, since the tasks use the connected folder). If
   you have a tool to create scheduled tasks, use it, with the times from
   F26 (jitter a few minutes off the hour). Otherwise tell them how: in the
   Claude desktop app, open Scheduled, create a task per prompt, connect the
   workspace folder and set the time.
3. Explain approvals: runs need to create Gmail drafts and edit files in the
   workspace. If the user wants unattended runs, they can turn on automatic
   approval for the task in its settings, if their plan allows it.

## Phase 5: Dry run

With the user watching, run a short version of PROSPECTING.md for the first
market: research 3 leads and create drafts for those with a published email
(at most 3). Check the first draft's sender. Ask the user to read the drafts
in Gmail and give feedback; update `playbook.md` with what they say. Do not
mark the market as run in `markets.md` (the dry run doesn't count). Tell the
user they may delete the test drafts or send them.

## Phase 6: Wrap up

Give the user a short summary:
- where everything lives;
- when the tasks run, and what they will see (drafts in Gmail, a summary,
  a push notification when something needs them);
- how to change things: edit `playbook.md`, `config.yaml`, `markets.md` or a
  criteria file, or just ask Claude in a chat.

Remind them of compliance (`KIT/docs/compliance.md`) in one sentence.
