## Keep It Fresh with GitHub Actions
Want the stack table above to always reflect your latest repos? Drop this workflow in your profile repo:
**`.github/workflows/update-stack.yml`**
```yaml
name: Auto-detect Stack
on:
  schedule:
    - cron: "0 0 * * 0"   # every Sunday midnight
  workflow_dispatch:
jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Fetch language stats & patch README
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: python .github/scripts/update_stack.py
      - uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "chore: auto-update stack from repos [skip ci]"
```
*(See the companion script below — it patches the `## Stack` section automatically.)*
---
## Contact
<div align="center">
[![Email](https://img.shields.io/badge/Email-dammarsanggalie%40gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:dammarsanggalie@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Dammar_Sanggalie-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/dammar-sanggalie-67a452281/)
[![Instagram](https://img.shields.io/badge/Instagram-@dammarsanggalie-E4405F?style=flat-square&logo=instagram&logoColor=white)](https://www.instagram.com/dammarsanggalie/)
[![Spotify](https://img.shields.io/badge/Spotify-coding_playlist-1DB954?style=flat-square&logo=spotify&logoColor=white)](https://open.spotify.com/user/31vr4ktsc3xpwfr4hnv2nob2hy6e?si=9c16200ca91a450d)
</div>
---
<div align="center">
<sub>Profile views: <img src="https://komarev.com/ghpvc/?username=Dammar-Sanggalie&style=flat-square&color=58a6ff" /></sub>
</div>

    
    
  