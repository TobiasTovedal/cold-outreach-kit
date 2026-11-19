#!/usr/bin/env python3
"""Create the outreach workspace from the kit's templates.

Usage:
  python3 init_workspace.py --kit <kit folder> --workspace <workspace folder>
                            [--accounts crm/accounts] [--logs crm/logs]
                            [--automation automation]

Copies templates/automation into <workspace>/<automation>, creates empty
data files and the CRM folders and log files. Never overwrites a file that
already exists; prints what it created and what it skipped.
"""
import argparse
import csv
import shutil
from pathlib import Path

DATA_FILES = {
    "leads.csv": [
        "date_added", "market", "org", "segment", "name", "role",
        "linkedin_url", "email", "phone", "source_url",
        "evidence_confidence", "rationale", "status", "grade_reason", "graded_date",
    ],
    "outreach.csv": [
        "email", "market", "name", "org", "first_sent", "last_sent", "sent_count",
        "replied", "first_reply", "reply_type", "last_checked", "thread_id",
        "first_msg_id", "fu_stage", "fu1_date", "fu2_date", "outcome", "recycle_after",
    ],
    "drafts.csv": [
        "date", "email", "market", "name", "org", "variant", "experiment",
        "subject", "draft_id", "status",
    ],
}

LOGS = {
    "Followup.md": ("followup-log", "Follow-up log",
                    "The daily inbox run puts replies, follow-up drafts and CRM changes at the top."),
    "Leadlog.md": ("lead-log", "Lead log",
                   "Each prospecting run adds its new leads and drafts at the top."),
    "CRM-log.md": ("crm-log", "CRM log",
                   "The weekly CRM sweep adds its updates and suggestions at the top."),
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--kit", required=True)
    p.add_argument("--workspace", required=True)
    p.add_argument("--automation", default="automation")
    p.add_argument("--accounts", default="crm/accounts")
    p.add_argument("--logs", default="crm/logs")
    a = p.parse_args()

    kit = Path(a.kit).expanduser().resolve()
    ws = Path(a.workspace).expanduser().resolve()
    auto = ws / a.automation
    created, skipped = [], []

    def put(dst, writer):
        if dst.exists():
            skipped.append(dst)
            return
        dst.parent.mkdir(parents=True, exist_ok=True)
        writer(dst)
        created.append(dst)

    src = kit / "templates" / "automation"
    for f in sorted(src.rglob("*")):
        if f.is_file():
            put(auto / f.relative_to(src), lambda d, f=f: shutil.copy2(f, d))

    for name, header in DATA_FILES.items():
        def w(d, header=header):
            with open(d, "w", newline="", encoding="utf-8") as fh:
                csv.writer(fh).writerow(header)
        put(auto / name, w)

    put(auto / ".lock", lambda d: d.write_text("free\n"))

    tpl = kit / "templates" / "crm" / "accounts" / "_account-template.md"
    put(ws / a.accounts / "_account-template.md", lambda d: shutil.copy2(tpl, d))

    for name, (typ, title, intro) in LOGS.items():
        put(ws / a.logs / name,
            lambda d, typ=typ, title=title, intro=intro:
            d.write_text(f"---\ntype: {typ}\n---\n# {title}\n\n{intro}\n"))

    for c in created:
        print("created ", c.relative_to(ws))
    for s in skipped:
        print("exists  ", s.relative_to(ws), "(left unchanged)")


if __name__ == "__main__":
    main()
