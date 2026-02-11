import os, json, csv
from datetime import datetime
from config import CHANGES_ROOT, OUT_ROOT

def iso_dt(s):
    s = s.replace("Z", "+00:00")
    if "." in s:
        parts = s.split(".")
        s = parts[0] + "+00:00"
    return datetime.fromisoformat(s)

def scan_messages(msgs):
    abandon = restore = None
    for m in msgs:
        text = (m.get("message") or "").lower()
        date = m.get("date")

        if not abandon and "abandoned" in text:
            abandon = date

        elif abandon and not restore and (
            text.startswith("restored") or text.startswith("reopened")
        ):
            restore = date

    return abandon, restore

rows = []

print(f"Scanning {CHANGES_ROOT} for abandoned-but-not-reopened changes...")

for root, _, files in os.walk(CHANGES_ROOT):
    for fn in files:
        if not fn.endswith(".json"):
            continue

        path = os.path.join(root, fn)
        try:
            ch = json.load(open(path, encoding="utf-8"))
        except:
            continue

        msgs = ch.get("messages", [])
        abandon_ts, reopen_ts = scan_messages(msgs)

        # keep only: abandoned AND NOT reopened
        if not abandon_ts:
            continue
        if reopen_ts:  # skip reopened
            continue

        owner = (ch.get("owner") or {}).get("_account_id")

        rows.append({
            "change_id": ch.get("change_id"),
            "numeric_id": ch.get("_number"),
            "project": ch.get("project"),
            "branch": ch.get("branch"),
            "owner_id": owner,
            "abandon_ts": abandon_ts,
            "reopen_ts": None,
            "final_status": "ABANDONED",
        })

output_file = os.path.join(OUT_ROOT, "abandoned_only.csv")

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

print(f"Done! {len(rows)} abandoned-only changes saved to {output_file}")
