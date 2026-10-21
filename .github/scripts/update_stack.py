"""
Auto-detects language breakdown from all public repos and patches
the ## Stack section in README.md.
Triggered by GitHub Actions on schedule or manually.
Requires: GITHUB_TOKEN env var (automatically provided in Actions).
"""
import os
import re
import json
import urllib.request
import urllib.error
USERNAME = "Dammar-Sanggalie"
README_PATH = "README.md"
# Languages to skip (markup/config, not "real" code for display)
SKIP_LANGS = {"CMake", "Makefile", "Shell", "Batchfile", "Dockerfile",
              "YAML", "JSON", "TOML", "Objective-C", "Swift", "PowerShell"}
BAR_FULL  = "█"
BAR_EMPTY = "░"
BAR_WIDTH = 20
def gh_get(url: str) -> dict | list:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", "")
    req = urllib.request.Request(url, headers={
        "User-Agent": "readme-updater/1.0",
        "Accept": "application/vnd.github+json",
        **({"Authorization": f"Bearer {token}"} if token else {}),
    })
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())
def bar(pct: float) -> str:
    filled = round(pct / 100 * BAR_WIDTH)
    return BAR_FULL * filled + BAR_EMPTY * (BAR_WIDTH - filled)
def fetch_lang_bytes() -> dict[str, int]:
    repos = gh_get(f"https://api.github.com/users/{USERNAME}/repos?per_page=100")
    totals: dict[str, int] = {}
    for repo in repos:
        if repo.get("fork"):
            continue
        try:
            langs = gh_get(repo["languages_url"])
            for lang, nbytes in langs.items():
                if lang not in SKIP_LANGS:
                    totals[lang] = totals.get(lang, 0) + nbytes
        except urllib.error.HTTPError:
            pass
    return totals

def build_table(lang_bytes: dict[str, int]) -> str:
    sorted_langs = sorted(lang_bytes.items(), key=lambda x: x[1], reverse=True)
    total = sum(v for _, v in sorted_langs)
    if total == 0:
        return "*(no data)*"
    # Show top 8 languages
    rows = ["| Language | Share |", "|---|---|"]
    for lang, nbytes in sorted_langs[:8]:
        pct = nbytes / total * 100
        rows.append(f"| {lang} | {bar(pct)} {pct:.1f}% |")
    return "\n".join(rows)
def patch_readme(new_table: str) -> None:
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    # Replace the block between the "> Auto-detected" line and the next ---
    pattern = re.compile(
        r"(> \*Auto-detected.*?\*\n\n)### Most Used by Code Volume\n\n.*?(\n---)",
        re.DOTALL,
    )
    replacement = (
        r"\g<1>"
        "### Most Used by Code Volume\n\n"
        + new_table
        + r"\g<2>"
    )
    new_content, n = pattern.subn(replacement, content)
    if n == 0:
        print("WARNING: Stack section not found — README unchanged.")
        return
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("README.md patched successfully.")
if __name__ == "__main__":
    print("Fetching language data from GitHub API...")
    lang_bytes = fetch_lang_bytes()
    print(f"Found languages: {list(lang_bytes.keys())}")
    table = build_table(lang_bytes)
    print("Generated table:\n", table)
    patch_readme(table)