#!/usr/bin/env python3
import os, sys, csv, time, html, pathlib, datetime as dt
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# ---------- Config & defaults ----------
HOME = pathlib.Path.home()
ENV_FILE = HOME / ".jobbot.env"

def load_env(env_path: pathlib.Path):
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line=line.strip()
            if not line or line.startswith("#"): 
                continue
            if "=" in line:
                k,v = line.split("=",1)
                os.environ.setdefault(k.strip(), v.strip())

load_env(ENV_FILE)

API_KEY = os.getenv("GOOGLE_API_KEY", "")
CSE_ID  = os.getenv("GOOGLE_CSE_ID", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", "")
EMAIL_TO   = os.getenv("EMAIL_TO", "")
APP_PW     = os.getenv("GMAIL_APP_PASSWORD", "")
RESULTS_PER_QUERY = int(os.getenv("RESULTS_PER_QUERY", "4"))
DATE_RESTRICT = os.getenv("DATE_RESTRICT", "w1")  # e.g., d1, w1, m1 or ""

if not API_KEY or not CSE_ID:
    print("Missing GOOGLE_API_KEY or GOOGLE_CSE_ID in ~/.jobbot.env", file=sys.stderr)
    sys.exit(2)

ROLES = [
    "DevOps engineer",
    "Cloud engineer",
    "GCP engineer",
    "Kubernetes engineer",
]
EXP_CLAUSES = ['"3 years"','"3+ years"','"4 years"','"4+ years"','"3-4 years"','"3 to 4 years"']

SITES = [
    "www.naukri.com",
    "in.indeed.com",
    "www.shine.com",
    "www.timesjobs.com",
    "www.foundit.in",
    "www.instahyre.com",
    "www.hirist.com",
    "www.cutshort.io",
]

SEARCH_ENDPOINT = "https://customsearch.googleapis.com/customsearch/v1"

def search_google(query: str, num: int = 4):
    params = {
        "key": API_KEY,
        "cx": CSE_ID,
        "q": query,
        "num": num,
        "gl": "in",          # bias to India
        "safe": "off",
    }
    if DATE_RESTRICT:
        params["dateRestrict"] = DATE_RESTRICT
    r = requests.get(SEARCH_ENDPOINT, params=params, timeout=20)
    r.raise_for_status()
    return r.json()

def gen_queries():
    queries = []
    exp = " OR ".join(EXP_CLAUSES)
    for role in ROLES:
        for site in SITES:
            q = f'{role} ({exp}) site:{site}'
            queries.append((role, site, q))
    return queries

def dedupe(items):
    seen = set()
    out = []
    for it in items:
        url = it.get("link") or it.get("formattedUrl")
        if not url or url in seen:
            continue
        seen.add(url)
        out.append(it)
    return out

def collect_results():
    collected = []
    for role, site, q in gen_queries():
        try:
            data = search_google(q, num=RESULTS_PER_QUERY)
            for it in data.get("items", []):
                collected.append({
                    "role": role,
                    "site": site,
                    "title": it.get("title",""),
                    "link": it.get("link",""),
                    "snippet": it.get("snippet",""),
                    "displayLink": it.get("displayLink",""),
                })
            time.sleep(0.4)  # be nice to quota
        except requests.HTTPError as e:
            print(f"[WARN] HTTPError for {site} / {role}: {e}", file=sys.stderr)
        except Exception as e:
            print(f"[WARN] Error for {site} / {role}: {e}", file=sys.stderr)
    return dedupe(collected)

def render_html(rows):
    if not rows:
        return "<p>No fresh results found today.</p>"
    out = []
    out.append("<h2>Daily DevOps/Cloud job picks (3–4+ yrs)</h2>")
    out.append(f"<p>Date: {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}</p>")
    out.append('<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;font-family:Arial,Helvetica,sans-serif;font-size:14px;">')
    out.append("<thead><tr><th>Role</th><th>Site</th><th>Title</th><th>Snippet</th></tr></thead><tbody>")
    for r in rows:
        title = html.escape(r["title"] or "")
        snippet = html.escape(r["snippet"] or "")
        link = html.escape(r["link"] or "")
        site = html.escape(r["displayLink"] or r["site"])
        role = html.escape(r["role"])
        out.append(f'<tr><td>{role}</td><td>{site}</td><td><a href="{link}">{title}</a></td><td>{snippet}</td></tr>')
    out.append("</tbody></table>")
    return "\n".join(out)

def save_csv(rows, outdir: pathlib.Path):
    outdir.mkdir(parents=True, exist_ok=True)
    ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = outdir / f"jobs_{ts}.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["role","site","title","link","snippet"])
        for r in rows:
            w.writerow([r["role"], r["site"], r["title"], r["link"], r["snippet"]])
    return path

def send_email(subject: str, html_body: str):
    if not EMAIL_FROM or not EMAIL_TO or not APP_PW:
        print("[INFO] Skipping email (EMAIL_FROM/EMAIL_TO/GMAIL_APP_PASSWORD not set).", file=sys.stderr)
        return False
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    part = MIMEText(html_body, "html", "utf-8")
    msg.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as s:
        s.starttls()
        s.login(EMAIL_FROM, APP_PW)
        s.sendmail(EMAIL_FROM, [e.strip() for e in EMAIL_TO.split(",")], msg.as_string())
    return True

def main():
    rows = collect_results()
    html_body = render_html(rows)
    out_csv = save_csv(rows, HOME / "jobbot_output")
    subject = f"[JobBot] {len(rows)} results • {dt.date.today().isoformat()}"
    emailed = send_email(subject, html_body)
    print(f"Saved: {out_csv}")
    print(f"Emailed: {'yes' if emailed else 'no'}")

if __name__ == "__main__":
    main()
