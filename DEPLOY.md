# Deploying

The site is public, published from this repository by GitHub Pages at
**<https://nkalauni.github.io/b2-workshop-2027/>**.

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

## Moving the repository to a department organization

The site currently lives under a personal account. Transferring it later
(**Settings → General → Transfer ownership**) keeps all history, and GitHub
redirects the old URL. If you transfer, the Pages URL changes to
`https://<org>.github.io/b2-workshop-2027/` unless a custom domain is set —
another reason to sort the domain out first.

## Taking the site private again

If you ever need to pull it back to a reviewers-only draft, set
`PRIVATE_DRAFT = True` in `tools/build.py` and rebuild. That restores the draft
banner and the `noindex` tag on every page. Note that this does *not* hide the
site: **a private repository still publishes a public website.** Access-
controlled Pages requires GitHub Enterprise Cloud. For a genuinely gated
preview you would need to host it elsewhere — Cloudflare Pages plus Cloudflare
Access does it on the free tier, with email one-time PINs.

## Still to do before this is print-ready

- [ ] Confirm `has.reasoning@arizona.edu` exists and is being read — it is the
      contact address on every page
- [ ] Registration page still says "date to be announced"
- [ ] Abstract submission system not chosen, so nothing is linked
- [ ] Workshop logo and flyer, once they exist
