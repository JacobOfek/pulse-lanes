# Pulse Lanes – standalone site

- Live: https://pulse-lanes.pages.dev (Cloudflare Pages, project `pulse-lanes`, connected to this repo, branch `main`, output dir `site`, no build command).
- Open to anyone with the link. No worker, no database: every device keeps its own songs, charts and scores (IndexedDB + localStorage).
- The Claude-only features (saving songs to the Claude account, the `downloads` capability) are off here: the game falls back to device storage and a normal file download for chart export.

## Update ("הפץ")
1. Save the latest artifact page to `build/source.html`.
2. `python3 build/build.py build/source.html b`  (b = the chosen icon; this also bumps the service-worker cache).
3. Test locally: `cd site && python3 -m http.server 8790`, then iPhone / iPad / desktop sizes.
4. Commit and push to `main`; Cloudflare publishes in about half a minute.
5. On iPhone: close the home-screen app fully and open it again to get the new version.

Never commit a wrangler.toml.
