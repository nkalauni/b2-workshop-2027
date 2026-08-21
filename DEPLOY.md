# Deploying

The site is public, published from this repository by GitHub Pages at
**<https://nkalauni.github.io/reasoning-workshop-2027/>**.

There is no build server and no Actions workflow. GitHub serves the `.html`
files in the repository root exactly as they are, so:

```sh
python3 tools/build.py     # only if you edited tools/build.py
git add -A
git commit -m "Update the program"
git push
```

The live site updates within a minute or two. `.nojekyll` is present, which
stops GitHub trying to run Jekyll over the files.

## Checking a change before you push

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000>. This serves the same files GitHub does, so
what you see is what will ship.

## Pages settings

Already configured, but for reference: **Settings → Pages → Source: Deploy from
a branch → `main` / `(root)`**.

## Custom domain

If the department gets a domain or an `arizona.edu` subdomain from UITS:

1. Add a file named `CNAME` in the repository root containing only the
   hostname, e.g. `b2workshop.arizona.edu`.
2. Point DNS at GitHub — a `CNAME` record to `nkalauni.github.io` for a
   subdomain, or GitHub's four `A` records for an apex domain.
3. **Settings → Pages → Custom domain**, enter it, and tick **Enforce HTTPS**
   once the certificate is issued.

Doing this also makes the site independent of whose personal account hosts it,
which is worth having before the URL goes out on a flyer.

## Moving the repository to the symposium's own account

The site currently lives under a personal account (`nkalauni`). The plan is to
move it to a GitHub account registered with the symposium's shared Gmail, so
that hosting does not depend on one student's account.

To move it, once the symposium account exists:

1. From the new account, accept the transfer. From this one:
   **Settings → General → Transfer ownership**, enter the new account name.
2. Everything transfers — commits, history, Pages settings.
3. **Settings → Pages** on the new account, confirm the source is
   `main` / `(root)`.

Two things to know before doing it:

- **The Pages URL changes** to
  `https://<newaccount>.github.io/reasoning-workshop-2027/`. GitHub redirects
  the old *repository* URL but **not** the old Pages URL, so any link already
  circulated stops working. Do it before the URL goes on a flyer, or set up a
  custom domain first so the public address never changes again.
- **Prefer a GitHub organization over a plain account** if it is no more
  trouble. An organization can have several owners, so Nabin, Mohammad and a
  faculty member all keep access without sharing one password — which matters
  for a site that has to outlive the current students. An account tied to a
  shared Gmail works, but it is one credential everybody has to share, and
  whoever holds it is a single point of failure. Either way the transfer steps
  above are the same.

A custom domain makes this moot for visitors: point it at whichever account
hosts the repository and the public URL never changes again.

## Taking the site private again

If you ever need to pull it back to a reviewers-only draft, set
`PRIVATE_DRAFT = True` in `tools/build.py` and rebuild. That restores the draft
banner and the `noindex` tag on every page. Note that this does *not* hide the
site: **a private repository still publishes a public website.** Access-
controlled Pages requires GitHub Enterprise Cloud. For a genuinely gated
preview you would need to host it elsewhere — Cloudflare Pages plus Cloudflare
Access does it on the free tier, with email one-time PINs.

## Still to do before this is print-ready

- [ ] Confirm `has-reasoning@arizona.edu` is live and being read — it is the
      contact address on every page
- [ ] Registration page still says "date to be announced"
- [ ] Abstract submission system not chosen, so nothing is linked
- [ ] Workshop logo and flyer, once they exist
- [ ] Move hosting to the symposium's own GitHub account (see below)
