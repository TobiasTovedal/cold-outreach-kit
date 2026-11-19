# Inbox procedure (every daily run, first)

Read RULES.md and config.yaml first. Goal: Gmail and the CRM agree, no reply
goes unanswered, and no cold email is left without a sensible follow-up.
This is the only procedure that syncs Gmail into `outreach.csv`, changes
draft statuses in `drafts.csv`, and updates account notes.

Labels: use the ids in `config.yaml` (`gmail.labels`). If an id does not
work, look it up with list_labels by name (`<label_prefix>/Cold`, etc.).
If `crm.enabled` is false, skip every account-note step.

## 0. Load state
- From A: `outreach.csv`, `drafts.csv`, `leads.csv`, and `playbook.md`
  (sections "Facts we may state", "Rules for drafts" and "Follow-ups").
- All account notes in `<paths.accounts>`: name (file name), market, stage,
  status, contacts (emails), last_touch, next_action, next_action_date,
  `## Contact log`.
- Build lookups: email -> account (from contacts, and organisation email
  domain -> account; ignore webmail domains like gmail.com), email ->
  outreach row, email -> lead row.
- Read the latest entry in `<paths.logs>/Followup.md` so you know what was
  already handled.

`outreach.csv` columns: email, market, name, org, first_sent, last_sent,
sent_count, replied, first_reply, reply_type, last_checked, thread_id,
first_msg_id, fu_stage (0/1/2), fu1_date, fu2_date, outcome (open /
replied_positive / replied_neutral / redirect / replied_negative /
no_response / bounced), recycle_after. Keep all columns.

## 1. Sync sent mail and drafts
Search sent mail since the newest `last_checked` in `outreach.csv` minus one
day (`in:sent after:YYYY/MM/DD`; for an empty file, the last 14 days),
paging through all results. Tip: a sent message's view URL contains
`msg-a:<id>`, which is the same id as the draft it came from.
1. Drafts in `drafts.csv` with status `drafted` that now appear in Sent:
   set `status=sent`. Then by variant:
   - `A`/`B`/`RESEND`: add or update the person in `outreach.csv`
     (first_sent, last_sent, sent_count, thread_id, first_msg_id, fu_stage 0,
     outcome open) and label the thread Cold.
   - `FU1`/`FU2`: set fu1_date / fu2_date to the sent date, fu_stage to 1 / 2,
     last_sent, sent_count + 1, and switch the thread label to Follow-up 1 / 2.
   - `REPLY`: no outreach row. Update the account note (step 4).
2. Drafts with status `drafted` whose draft id no longer exists and with no
   matching sent email: `status=discarded`.
3. Cold emails the owner wrote by hand: any sent message to an email in
   `leads.csv` that has no outreach row and where there was no earlier
   inbound email from that person: add an outreach row (fu_stage 0, outcome
   open) and label the thread Cold.
4. Any other sent email to an account contact or account domain: update that
   account note (step 4).
5. Fill missing thread_id/first_msg_id with `in:sent to:<email>`. Make sure
   every outreach thread carries the label matching its state.
6. Set `last_checked` = today on every outreach row you checked. Rows with
   no reply 30+ days after first_sent get `replied=no` (outcome unchanged
   until step 3 closes them).

## 2. Replies (all inbound mail from the last 3 days)
Search inbound messages (not from the sender address) newer than 3 days
from any address in `outreach.csv`, any account contact or account domain,
plus any inbound message in a thread with one of the kit's labels. For each
message not yet handled (check the Followup log, `first_reply` and existing
drafts):
1. Read the whole thread. Ignore auto-replies and out-of-office (but note a
   return date, and any referral to a colleague, in the log). Bounces: see
   "Bounces" below. Spam-filter challenges ("click to deliver your
   message"): never click; list them for the owner.
2. Classify: `meeting` (wants to meet or see a demo), `question`, `redirect`
   (points to someone else), `not_now`, `no`, or `info` (an account contact
   writing about something else).
3. Draft a reply in the same thread (replyToMessageId), in the language they
   wrote in, following the playbook tone: short, humble, concrete. Record it
   in `drafts.csv` (variant `REPLY`).
   - meeting: if they proposed a time, accept it ("<their time> works for
     me, I'll send an invite") and flag it for the owner to put in the
     calendar. If they ask to be contacted on a date, confirm that the owner
     will get back then. If the owner has to propose times: when
     `email.calendar_connected` is true, read the calendar and offer 2–3
     free 30-minute slots inside `owner.call_hours`; otherwise do not draft,
     and ask the owner for 2–3 times under **Questions for you**.
   - question: answer only with facts from the playbook, the workspace or
     earlier emails. If any part needs the owner's own answer, do not draft:
     ask under **Questions for you**. Never put placeholders in a draft.
   - redirect: thank them; add the referred person to the account's
     contacts (create the account note if missing); draft a separate new
     email to the referred person that says who referred the owner
     (playbook rules apply; variant `RESEND`). If they point to a shared
     mailbox with no person, thank them and just log it.
   - not_now: thank them, ask whether it is ok to get back in about
     `limits.recycle_months` months; set recycle_after accordingly.
   - no: a short, gracious thank-you; no further follow-ups.
   - info: draft only if the message asks the owner something; otherwise
     just log it.
   Never draft a reply if the owner already answered after the inbound
   message, or if a reply draft for that thread already exists.
4. For outreach people: update `outreach.csv` (replied=yes, first_reply,
   reply_type = positive/neutral/negative, outcome) and label the thread
   Replied (remove the Cold / Follow-up label). For everyone: update the
   CRM (step 4).

### Bounces
Also search `from:(postmaster OR mailer-daemon) newer_than:3d` and match
each bounce to its outreach thread. For each bounced address not yet handled
(no `RESEND` row in `drafts.csv` for that person): set outcome `bounced`.
If the bounce says the address does not exist:
1. Look for the person's own published address (organisation staff page,
   publications, event programmes, other emails in Gmail).
2. If one is found that differs from the bounced address, add it to the
   account's contacts and draft a new email to it with the same body as the
   bounced email (new thread, variant `RESEND`).
3. Otherwise set next_action "Find email for <name> (bounced)" on the
   account and say in the summary that no address was found.
If the bounce is a policy or spam rejection, the address is probably fine:
do not resend; report it so the owner can reach the person another way.
Never resend to the same bounced address.

## 3. Follow-ups for no reply
`email.follow_ups` says how many follow-ups to send (0, 1 or 2). For every
`outreach.csv` row with outcome `open` and no reply:
- fu_stage 0, follow_ups ≥ 1, and ≥ `fu1_after_working_days` since
  first_sent -> follow-up 1.
- fu_stage 1, follow_ups = 2, and ≥ `fu2_after_working_days` since fu1_date
  -> follow-up 2.
- fu_stage = follow_ups (the last follow-up is sent) and ≥
  `close_after_working_days` since that follow-up's date -> outcome
  `no_response`, label No response, recycle_after = first_sent +
  `recycle_months`. No more emails.
- Skip anyone with an out-of-office return date in the future (wait until
  2 working days after it), anyone who has had a two-way email exchange
  with the owner in the last 14 days (the same person or the same thread),
  and anyone with a follow-up draft already pending. An exchange with a
  colleague at the same account does not block the follow-up, and a reply
  that refers the owner to this person never does.
- If the person's outreach row has a newer address than the one the
  original thread went to (e.g. after a redirect), do not reply in the old
  thread: draft a new email to the new address instead (variant `RESEND`).
Draft follow-ups as replies in the original thread (replyToMessageId = the
last message the owner sent there), using the playbook's "Follow-ups"
section and the same greeting as the first email. If FU1 should propose
call times (`email.propose_call_times`) and they cannot be read from a
calendar, ask the owner once for 2–3 times under **Questions for you**
(one question covers every pending FU1), and draft when they answer. Give
times in the recipient's local time zone with the zone name. Record drafts
in `drafts.csv` (variant `FU1`/`FU2`).

## 4. Keep the CRM up to date
For every email exchange found in steps 1–3, in the account note:
- `last_touch`: date of the latest email in either direction (only move it
  forward).
- `next_action` / `next_action_date`: e.g. "Book meeting with X",
  "Answer question from X", "Close X if no reply (FU1 sent)" with the
  planned date, "Get back to X in <month>" for not_now. If an email states
  a concrete next step with a date, use that.
- `contacts`: add people who clearly belong to the account (their email
  domain is the organisation's domain, or the thread is clearly about the
  account) as `"Name | role | email"` (role empty if unknown). Never edit or
  remove entries, never add the owner or colleagues. Keep valid YAML (turn
  `contacts: []` into a block list when adding the first entry).
- `stage`: only 0 -> 10 when someone replies `meeting` or with clear
  interest. Suggest other stage changes in the summary instead. If a `no`
  makes `lost` apt, suggest it; never change `status`.
- Append `- YYYY-MM-DD: <what happened, one factual line>` under
  `## Contact log` at the end of the note (create the heading if missing).
  Never copy email text beyond a few words.
- If an interested person has no account note yet, create one from
  `<paths.accounts>/_account-template.md` (stage 10, status active).
Change nothing else in account notes.

## 5. Due next actions
After step 4, list every account (any status except `lost` and `paused`)
whose `next_action_date` is today or earlier, oldest first, and any whose
`next_action` names a meeting today. Check Gmail briefly (contact
addresses, last 14 days): if an email already covers the action, say so
instead of flagging it. Do not draft for these; they are reminders.

## 6. Log
Prepend an entry to `<paths.logs>/Followup.md`:

    ## YYYY-MM-DD HH:MM
    ### Due today
    - [[Account]] – next_action (date, "n days overdue" if older than today)
    ### Replies
    - [[Account]] – Name: type, what they want, "draft ready" / what the owner must do
    ### Follow-ups
    - n FU1 drafts, n FU2 drafts, n closed without reply; anything waiting for the owner
    ### CRM
    - Changes to account notes (new contacts, stage changes, suggestions)

Write "Nothing due." under "Due today" when it is empty. Use plain names
instead of `[[...]]` links when `paths.obsidian_links` is false.

## 7. Summary
At most 3 lines: replies that need the owner (meeting requests first), due
actions today, and the number of drafts created. If nothing needs the owner,
one line saying so.
