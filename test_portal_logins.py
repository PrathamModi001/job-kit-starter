import subprocess
import json
import os
import sys
import time

EXTENSION_ID = "mmlmfjhmonkocbjadbfplnigmagldckm"
EXTENSION_URL = f"https://chromewebstore.google.com/detail/playwright-extension/{EXTENSION_ID}"
CHROME_EXT_DIR = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Extensions")

PORTALS = [
    {"name": "Naukri", "url": "https://www.naukri.com/mnjuser/homepage", "logged_in_markers": ["my-naukri", "profile", "logout", "mnjuser", "dashboard", "view & update profile"]},
    {"name": "Instahyre", "url": "https://www.instahyre.com/candidate/opportunities/", "logged_in_markers": ["opportunities", "logout", "profile", "inbox", "candidate"]},
    {"name": "Cutshort", "url": "https://cutshort.io/profile/all-jobs", "logged_in_markers": ["matches", "profile", "logout", "dashboard", "applied"]},
    {"name": "Wellfound", "url": "https://wellfound.com/jobs", "logged_in_markers": ["overview", "logout", "saved", "applied", "profile"]},
    {"name": "Indeed", "url": "https://in.indeed.com/", "logged_in_markers": ["profile", "sign out", "my jobs", "messages", "account"]},
    {"name": "Jobfound", "url": "https://jobfound.org/", "logged_in_markers": ["profile", "dashboard", "logout", "applications"]}
]

def check_extension_installed():
    ext_path = os.path.join(CHROME_EXT_DIR, EXTENSION_ID)
    return os.path.exists(ext_path)

def test_via_mcp():
    if not check_extension_installed():
        return {
            "status": "missing_extension",
            "message": f"Playwright Extension is not installed in Chrome yet. Install it from: {EXTENSION_URL}",
            "extension_url": EXTENSION_URL
        }

    proc = subprocess.Popen(
        ['npx.cmd', '-y', '@playwright/mcp@latest', '--extension'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True
    )

    req_id = 1
    def send_rpc(method, params=None):
        nonlocal req_id
        msg = {'jsonrpc': '2.0', 'id': req_id, 'method': method}
        if params is not None:
            msg['params'] = params
        req_id += 1
        proc.stdin.write(json.dumps(msg) + '\n')
        proc.stdin.flush()
        line = proc.stdout.readline()
        return json.loads(line) if line else {}

    try:
        init_res = send_rpc('initialize', {
            'protocolVersion': '2024-11-05',
            'capabilities': {},
            'clientInfo': {'name': 'portal-checker', 'version': '1.0'}
        })

        results = []
        for portal in PORTALS:
            nav_res = send_rpc('tools/call', {
                'name': 'browser_navigate',
                'arguments': {'url': portal['url']}
            })
            time.sleep(2)
            snap_res = send_rpc('tools/call', {
                'name': 'browser_snapshot',
                'arguments': {}
            })
            snap_text = json.dumps(snap_res).lower()
            is_logged_in = any(marker in snap_text for marker in portal['logged_in_markers'])
            results.append({
                "portal": portal['name'],
                "url": portal['url'],
                "logged_in": is_logged_in,
                "detail": "Logged In" if is_logged_in else "Not Logged In or Login button detected"
            })
        
        proc.kill()
        return {"status": "success", "results": results}
    except Exception as e:
        proc.kill()
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    if not check_extension_installed():
        print(f"EXTENSION_STATUS: NOT_INSTALLED")
        print(f"INSTALL_URL: {EXTENSION_URL}")
        sys.exit(1)
    else:
        print("EXTENSION_STATUS: INSTALLED")
        res = test_via_mcp()
        print(json.dumps(res, indent=2))
