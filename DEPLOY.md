# Hosting and sharing

Two separate questions, and they have different answers.

## 1. Sharing the draft privately, right now

**GitHub Pages cannot do this.** A private repository still publishes a
*public* website. Only GitHub Enterprise Cloud offers access-controlled Pages
("visible only to users with repository access"), and a personal account does
not have it. Making the repo private protects the source, not the site.

Since the Speakers page lists people who have been invited but have not
accepted, the preview needs to be genuinely gated, not merely at an
unguessable URL.

### Recommended: Cloudflare Pages + Cloudflare Access (free)

Cloudflare's Zero Trust free tier includes 50 seats, and Access can email a
one-time PIN to an allowlist of addresses. Nobody needs a Cloudflare account —
Bo just enters his email, gets a 6-digit code, and is in.

1. Create a free Cloudflare account at <https://dash.cloudflare.com/sign-up>.
2. **Workers & Pages → Create → Pages → Connect to Git**, authorise GitHub, and
   pick this repository. It can stay private.
3. Build settings: **framework preset = None**, **build command = empty**,
   **build output directory = `/`**. There is no build step.
4. Deploy. You get a URL like `b2-workshop-2027.pages.dev`.
5. **Zero Trust → Access → Applications → Add an application → Self-hosted.**
   - Application domain: your `*.pages.dev` hostname
   - Policy: **Action = Allow**, **Include = Emails**, then paste the
     organizing committee's addresses one per line.
   - Under login methods, leave **One-time PIN** enabled.
6. Send the committee the URL. First visit prompts for their email, then a PIN.

Add or remove reviewers by editing that email list. No repo access needed.

### Simpler alternatives, if Cloudflare is more setup than you want

- **Local preview.** `cd site && python3 -m http.server 8000`, then open
  <http://localhost:8000>. Good enough for showing someone in person.
- **Repository collaborators.** Add the committee to the private repo and let
  them clone and run the command above. Works, but expects them to use git.
- **Netlify / Vercel password protection.** Both have it; both put it behind a
  paid tier. Cloudflare's free tier is the reason it is recommended above.

## 2. Going public, later

When the committee signs off and speakers are confirmed:

1. In `tools/build.py`, set `PRIVATE_DRAFT = False` and re-run
   `python3 tools/build.py`. This removes the draft banner and the
   `noindex` meta tag from every page.
2. Delete `robots.txt`.
3. Make the repository public, then **Settings → Pages → Source: Deploy from a
   branch → `main` / `(root)`**. The site appears at
   `https://<user>.github.io/<repo>/` within a minute or two.
4. `.nojekyll` is already present, which stops GitHub trying to run Jekyll over
   the files.

### Custom domain

If you get a domain or an `arizona.edu` subdomain from UITS:

1. Add a file named `CNAME` at the repo root containing just the hostname,
   e.g. `b2workshop.arizona.edu`.
2. Point DNS at GitHub — a `CNAME` record to `<user>.github.io` for a
   subdomain, or the four `A` records in GitHub's docs for an apex domain.
3. **Settings → Pages → Custom domain**, enter it, and tick **Enforce HTTPS**
   once the certificate is issued.

A custom domain works the same way on Cloudflare Pages, which may be simpler if
you have already set it up for the private preview — in which case you can skip
GitHub Pages entirely and just remove the Access policy at launch.

## Checklist before the site goes public

- [ ] Committee has approved publishing invited-but-unconfirmed speaker names,
      or those names have been replaced with confirmed ones
- [ ] `has.reasoning@arizona.edu` exists and is being read
- [ ] `PRIVATE_DRAFT = False` and pages rebuilt
- [ ] `robots.txt` deleted
- [ ] Real photographs in `assets/img/` (see the README there)
- [ ] Registration page updated with actual dates and the fee
- [ ] Someone has opened every page on a phone
