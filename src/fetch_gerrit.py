import os, json, time, random, sys
from datetime import datetime, timedelta
import requests
from config import BASE_URL, PAGE_SIZE, CHANGES_ROOT, CHECKPOINTS, REQUEST_OPTS

s = requests.Session(); s.headers["Accept"] = "application/json"
def strip(x): return x.split("\n",1)[1] if x.startswith(")]}'") else x

def month_bounds(y,m):
    d = datetime(y,m,1)
    e = (d.replace(day=28)+timedelta(days=4)).replace(day=1)
    return d.date().isoformat(), e.date().isoformat()

def shard(created, project, num):
    # this fuction is to handle different timestamp formats from Gerrit
    def strip_fractional_seconds(ts):
        ts = ts.replace("Z", "").replace("T", " ")
        if "." in ts:
            ts = ts.split(".")[0]
        else:
            ts = ts.split("+")[0]
        return ts.strip()

    created_clean = created.replace("Z", "").replace("T", " ")
    # this part is to ensure nanoseconds are handled properly
    if "." in created_clean:
        parts = created_clean.split(".")
        if len(parts) == 2 and len(parts[1]) > 6:
            created_clean = parts[0] + "." + parts[1][:6]
    try:
        dt = datetime.strptime(created_clean, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        try:
            dt = datetime.strptime(created_clean, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # Fallback: try ISO format
            dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
    
    ym = f"{dt.year:04d}-{dt.month:02d}"
    safe = project.replace("/", "__")
    d = os.path.join(CHANGES_ROOT, ym)
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, f"{safe}__{num}.json")

def cp_path(ym):
    os.makedirs(CHECKPOINTS, exist_ok=True)
    return os.path.join(CHECKPOINTS, f"{ym}.json")

def gget(params):
    for i in range(10): #to ensure the script does not crash due to transient network issues or temporary server load
        try:
            r = s.get(f"{BASE_URL}/changes/", params=params, timeout=(15, 300))
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep((2 ** i) + 0.5); continue
            r.raise_for_status()
            return json.loads(strip(r.text))
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
            time.sleep((2 ** i) + 0.5); continue
    raise RuntimeError("Repeated timeouts reaching Gerrit")

def fetch_month(y,m):
    after,before = month_bounds(y,m); ym = f"{y:04d}-{m:02d}"
    start = 0 # ensure data complesteness across multiple runs AND SAVING API CALLS
    cp = cp_path(ym)
    if os.path.exists(cp):
        try: start = json.load(open(cp))["start"]
        except: pass
    while True:#Ensure all closed changes in the month are fetched
        p = {"q": f"status:closed after:{after} before:{before}", "n": PAGE_SIZE, "S": start, "o": REQUEST_OPTS}
        data = gget(p)
        if not data: break
        for ch in data:
            path = shard(ch["created"], ch["project"], ch["_number"])
            if not os.path.exists(path):
                with open(path,"w",encoding="utf-8") as f:
                    json.dump(ch,f,ensure_ascii=False)
        with open(cp,"w") as f:
            json.dump({"start": start + PAGE_SIZE}, f)
        if len(data) < PAGE_SIZE or not data[-1].get("_more_changes"):
            break
        start += PAGE_SIZE
        time.sleep(0.4 + random.random()*0.2)

if __name__ == "__main__":
    y = int(sys.argv[1]) if len(sys.argv)>1 else 2023
    m = int(sys.argv[2]) if len(sys.argv)>2 else 1
    fetch_month(y,m)
