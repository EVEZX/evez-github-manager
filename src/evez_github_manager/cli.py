"""EVEZ GitHub Manager - autonomous repo management via the GitHub REST API.

Pure stdlib. Zero dependencies. Built for the EVEZ-OS mesh.
"""
import json
import os
import sys
import urllib.request

API = "https://api.github.com"


def _token():
    tok = os.environ.get("GITHUB_TOKEN")
    if not tok:
        print("[!] GITHUB_TOKEN not set. Export it first.")
        sys.exit(1)
    return tok


def _req(method, path, body=None):
    url = f"{API}{path}"
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, method=method, data=data)
    r.add_header("Authorization", f"Bearer {_token()}")
    r.add_header("Accept", "application/vnd.github+json")
    r.add_header("User-Agent", "evez-github-manager")
    try:
        with urllib.request.urlopen(r) as resp:
            txt = resp.read().decode()
            return json.loads(txt) if txt.strip() else {}
    except urllib.error.HTTPError as e:
        print(f"[!] HTTP {e.code}: {e.read().decode()[:300]}")
        sys.exit(1)


def cmd_status():
    me = _req("GET", "/user")
    rl = _req("GET", "/rate_limit")
    core = rl.get("resources", {}).get("core", {})
    print(f"[*] Authenticated as: {me.get('login')} ({me.get('name', 'no name')})")
    print(f"[*] Rate limit: {core.get('remaining')}/{core.get('limit')} remaining")


def cmd_repos(args):
    if not args:
        repos = _req("GET", "/user/repos?per_page=100&sort=updated")
        for r in repos[:100]:
            arch = " [ARCHIVED]" if r.get("archived") else ""
            print(f"- {r['name']}{arch}")
        print(f"[*] {len(repos)} repos listed")
        return
    if args[0] == "create" and len(args) >= 2:
        name = args[1]
        priv = "--private" in args
        r = _req("POST", "/user/repos", {"name": name, "private": priv, "auto_init": True})
        print(f"[+] Created {r.get('full_name')} -> {r.get('html_url')}")
        return
    print("[!] Usage: evez-ghm repos [list | create NAME [--private]]")


def cmd_issue(args):
    if len(args) < 2:
        print("[!] Usage: evez-ghm issue [list REPO | create REPO 'TITLE']")
        return
    action, repo = args[0], args[1]
    if action == "list":
        issues = _req("GET", f"/repos/EvezArt/{repo}/issues?state=open")
        for i in issues:
            if "pull_request" not in i:
                print(f"#{i['number']} {i['title']}")
        print(f"[*] {len(issues)} open issues in {repo}")
        return
    if action == "create" and len(args) >= 3:
        title = " ".join(args[2:]).strip("'\"")
        i = _req("POST", f"/repos/EvezArt/{repo}/issues", {"title": title})
        print(f"[+] Issue #{i.get('number')} opened: {i.get('html_url')}")
        return
    print("[!] Usage: evez-ghm issue [list REPO | create REPO 'TITLE']")


def cmd_release(args):
    if len(args) >= 3 and args[0] == "create":
        repo, tag = args[1], args[2]
        r = _req("POST", f"/repos/EvezArt/{repo}/releases",
                 {"tag_name": tag, "name": tag})
        print(f"[+] Release {r.get('name')} -> {r.get('html_url')}")
    else:
        print("[!] Usage: evez-ghm release create REPO TAG")


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd = args[0]
    if cmd == "status":
        cmd_status()
    elif cmd == "repos":
        cmd_repos(args[1:])
    elif cmd == "issue":
        cmd_issue(args[1:])
    elif cmd == "release":
        cmd_release(args[1:])
    else:
        print(f"[!] Unknown command: {cmd}")


if __name__ == "__main__":
    main()
