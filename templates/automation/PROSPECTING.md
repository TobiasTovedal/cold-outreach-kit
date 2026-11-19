# Prospecting procedure (every daily run, after INBOX.md)

Read RULES.md and config.yaml first. Goal: find up to
`limits.leads_per_run` new named leads in the target role buckets at
organisations that fit the ICP in one market, and draft cold emails to them
following `playbook.md`. This procedure does not read or sync replies; the
inbox procedure owns `outreach.csv` and has just run.

## 1. Pick today's market
Read `markets.md`. For each market compute
`score = days since last_run - interval`, where interval is 14 days for
`core` and 42 days for `expansion`. A market that has never run gets
score 0 (due, but not more overdue than anything else).
1. If any core market has score >= 0, pick the core market with the highest
   score.
2. Otherwise, if any expansion market has score >= 0, pick the one with the
   highest score; ties go by table order.
3. Otherwise pick the core market with the highest score (ties by table
   order).

## 2. Read state for the market
- Read `criteria/criteria-{code}.md`. If it does not exist, create it from
  `criteria/_template.md` and the criteria file of another market: local
  job titles per bucket, organisation types and `segment` values,
  geography, and a Research sources section for that market. Add a
  changelog line "created by scheduled run". Add the code to
  `VALID_MARKETS` in `scripts/validate_leads.py` if it is missing.
- Dedup set: all `leads.csv` rows where `market == {code}` (name + org,
  case-insensitive), plus every email anywhere in `leads.csv`.
- Accounts: people at organisations that already have an account note are
  fine only if they are not already in the account's contacts; flag them in
  the log. Skip organisations whose account `status` is `customer` or
  `lost` unless the criteria file says otherwise.

## 3. Research up to `leads_per_run` new leads
- Spread the slots across the role buckets in the criteria file, at least
  one per bucket, with more to the bucket marked as most important.
- Follow the criteria file: organisation fit, target roles, research
  sources. Prefer the most senior person who owns the problem the product
  solves.
- Check that each person still holds the role (a recent page, no sign of
  leaving or retiring, no newer person in the role).
- Email: the person's own published address first. If none is published
  but a team or department mailbox is (e.g. `quality@`, `operations@`), put
  it in `email` and start `rationale` with "SHARED MAILBOX:". Company-wide
  general addresses (`info@`, `contact@`, `hello@`, reception) do not count.
  Never attribute another person's address to a lead; never guess.
- Every lead needs a real `source_url` that names the person and role. If
  you cannot verify a person on a page you opened, leave them out.
- Research is often fastest with 2–3 parallel subagents split by region or
  role bucket. Give them the dedup list and these rules; they return data
  only.

## 4. Append to leads.csv
Schema:
`date_added,market,org,segment,name,role,linkedin_url,email,phone,source_url,evidence_confidence,rationale,status,grade_reason,graded_date`
with `market={code}`, `status=pending`, `evidence_confidence` `high` or
`medium`, `grade_reason` and `graded_date` empty. `rationale` names the role
bucket and why the person fits (and where the email was found, if not on
`source_url`). Then run `python3 scripts/validate_leads.py` from A; if it
fails, fix only your new rows.

## 5. Draft cold emails
Read `playbook.md` and follow its "Rules for drafts" exactly.
- If `drafts.csv` already has `limits.max_pending_cold` or more rows with
  variant A/B and status `drafted`, create no drafts today and say so.
- For each new lead with a personal email and not already in
  `outreach.csv`, create one draft. Assign the experiment arm by
  alternating A/B from the last A/B row in `drafts.csv`; apply the active
  experiment's change (config `experiment`, playbook "Experiments") only to
  B drafts.
- Shared mailboxes: create one draft per mailbox (pick the most senior lead
  if several share it; skip the mailbox if it is already in
  `outreach.csv`). Subject: the usual subject plus " (for <Title>
  <Surname>)". First line of the body, its own paragraph: "For the
  attention of <Title> <First name> <Surname>". Then the normal email.
  Note "via shared mailbox" in the log.
- The only personal line is the playbook's line naming their organisation,
  and the organisation name must match the lead's verified `org`.
- Language and greeting per `config.yaml` and the playbook.
- After the first draft, check its sender (RULES.md).
- Append a row to `drafts.csv` for each (variant A/B, the experiment id,
  subject, draft id, status `drafted`).

## 6. Log and finish
Prepend an entry to `<paths.logs>/Leadlog.md`:

    ## YYYY-MM-DD HH:MM – <market>
    ### New leads (<n>)
    - **Name**, role – org (<email or "no email">) [source](url)
    ### Drafts
    Number of drafts (A/B split), or why none.
    ### Notes
    Only when needed: leads at existing accounts ([[Account]]), new
    criteria file, Gmail not connected, validation problems, why fewer
    leads than the target.

Then update today's market row in `markets.md` (`last_run`, and add the
number of new leads to `total_added`).

Summary, at most 3 lines: the market, new leads, drafts waiting for the
owner to review and send, and anything odd.
