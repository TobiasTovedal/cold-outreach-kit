# Cold email playbook

This file decides how every email is written. The owner edits it freely;
the owner's edits win over everything else. Lines marked
"(owner's decision YYYY-MM-DD)" must never be removed by any task.

## Who we are

- Company: {{COMPANY}} ({{WEBSITE}})
- What we sell: {{PRODUCT_SENTENCE}}
- Sender: {{OWNER_NAME}}, {{SENDER_EMAIL}}

## Facts we may state

Only these claims may be made about us in any email. Add to this list as
things become true; remove what stops being true.

- {{PROOF_POINT_1}}
- {{PROOF_POINT_2}}
- {{PROOF_POINT_3}}

Never say: {{NEVER_SAY}}

## What the customer gets

Two or three plain sentences used in every first email (from the setup
interview, in the owner's words):

{{OUTCOME_SENTENCES}}

## The common objection

{{OBJECTION}} Our answer, as its own paragraph:
"{{OBJECTION_ANSWER}}"

## Rules for drafts

1. One person per email. Greeting: {{GREETING_RULE}}. Use titles such as
   "Dr." or "Prof." only when the title is verified on the person's own
   organisation's page.
2. 80–150 words in the body. No tables, no attachments, no bullet lists.
3. Structure:
   (a) one sentence on what we do;
   (b) the strongest proof point, as its own one-sentence paragraph;
   (c) the outcome sentences above;
   (d) the objection answer, as its own paragraph;
   (e) one short line naming only their organisation, e.g. "I'm curious
       whether {{COMPANY_PRODUCT_NAME}} could be useful at <Organisation>.";
   (f) one question asking for a short call, e.g. "Would you be open to a
       short call where I show you how it works?"
   Never mention the person's role, title or department in the email (it
   reads as automated), and never "I am writing to you because ...".
4. Tone: {{TONE}}. Short, plain sentences in the owner's voice. No sales
   jargon, no superlatives. Avoid "it's not X, it's Y" contrasts, lists of
   three, em dashes, and phrases like "seamless", "empower",
   "data-driven", "take it to the next level". If it sounds like a
   brochure, rewrite it plainer.
5. Subject: plain topic, default "{{DEFAULT_SUBJECT}}".
6. Language: {{LANGUAGE_RULE}}.
7. No sign-off in the body; the Gmail signature has it. Create every draft
   with includeSignature true.
8. Never claim things about the recipient's organisation that you did not
   verify, and never mention bad news about it.

## Reference draft ({{LANGUAGE}})

    Subject: {{DEFAULT_SUBJECT}}

    {{REFERENCE_DRAFT}}

## Follow-ups

Drafted by the inbox procedure as replies in the original thread, same
language and greeting as the first email, no sign-off.

- **FU1 (~{{FU1_DAYS}} working days):** 2–3 sentences. Do not open by saying
  you are following up or that the email may have been buried. Go straight
  to the ask, propose 2–3 concrete 30-minute slots (recipient's time zone,
  with the zone name), and end with a redirect line. Example: "Would you be
  open to a 30-minute call where I show you how it works? I could do
  Wednesday 2 December at 10:00, Thursday 3 December at 14:00 or Friday
  4 December at 09:30 (CET), or another time that suits you better. If
  someone else on your team is a better contact, a pointer would be much
  appreciated."
- **FU2 (only if config follow_ups is 2):** one new, concrete angle from
  "Facts we may state" in 3–4 sentences, then close the loop politely: "If
  now isn't the right time, no problem, and thank you for reading."

Plain "just bumping this" emails get no replies: every follow-up must add
something.

## Experiments

Each new cold draft is assigned arm A (current rules) or B (one change),
alternating, and logged in `drafts.csv`. When both arms have at least 15
sent emails with 30 days of follow-up time, compare reply rates; adopt B if
it beat A by 5 percentage points or more, then start the next experiment.

- **Active:** E1. B adds a final line: "If you're not the right person, who
  would you suggest I talk to?"
- **Backlog:** E2 subject line variant; E3 local language vs. English;
  E4 a different proof point; E5 send day (Tue–Thu morning vs. other).

## Results log

(Add dated notes here when you learn something, e.g. which proof point gets
replies.)
