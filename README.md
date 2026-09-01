# etgar.bonar1.com

English human-facing executive profile and point-of-view site for Etgar Bonar, with supplemental machine-readable Hebrew resources.

## Public routes

| Route | Purpose |
|---|---|
| `/` | English executive profile |
| `/five-layers/` | English point of view, The cost-to-serve line |
| `/he/` | Legacy URL that sends visitors to `/` and is marked `noindex` |
| `/he/five-layers/` | Legacy URL that sends visitors to `/five-layers/` and is marked `noindex` |
| `/machine/he/profile.json` | Supplemental machine-readable Hebrew profile |
| `/machine/he/cost-to-serve-line.json` | Supplemental machine-readable Hebrew point of view |

## Source authority

- Positioning: `projects/career/job-search/_shared/linkedin-profile-repositioning-2026-08.md`
- Public claims: `projects/career/evidence/claims-ledger.md`
- Point of view: `projects/career/pov/README.md`
- Framework page: `projects/career/pov/framework/01-five-questions.md` and `02-job-completion-flow.md`
- Property roles and linking: `projects/bonar1-websites/etgar-ai-content-architecture.md`
- Findability requirements: `projects/bonar1-websites/web-findability-standard.md`
- Hebrew terminology: `projects/bonar1-websites/hebrew-localization-guide.md`

## Design

The current source restores the stronger editorial language of the original build and adds a restrained SharpLink-inspired motion layer: a dark cartographic hero, large serif typography, pointer depth, scroll reveals, image parallax, and animated system orbits. It does not reproduce SharpLink's graphics or layout.

The build uses exact logo assets for Amazon, Taboola, Rapyd, Lokalise, Johnson & Johnson, and London Business School. It also uses the supplied Rapyd rooftop scene, an official Lokalise and Claude case-study visual, and an official LBS campus image. The `EB` identity mark remains until a production headshot is available.

## Findability and accessibility

- Important content is delivered as static semantic HTML.
- Each human-facing page has one H1, unique metadata, a canonical URL, English `hreflang`, and accurate JSON-LD.
- The canonical Person identifier is `https://etgar.bonar1.com/#etgar`.
- `robots.txt` and `sitemap.xml` cover the canonical English pages. The supplemental `llms.txt` points machines to the Hebrew JSON resources.
- Hebrew is not hidden in the English HTML. The machine resources are public, receive the same response for every visitor, and are not presented as canonical search pages.
- Any material change to the English profile or point of view must be reflected in the matching Hebrew JSON resource in the same release. This is a manually maintained translation, not an independent source of truth.
- The framework diagram is implemented as text and HTML, not as an image-only argument.
- Layouts support narrow screens, RTL, reduced motion, keyboard focus, and print.

## Deliberate exclusions

- The business go-to-market renovation programme is not published while the executive seat search is active.
- The `ai-build.bonar1.com` link is not live until that hostname has DNS and HTTPS.
- No unsupported recommendation, testimonial, or unverified conversion claim is included.
- No external font, framework, or JavaScript dependency is required for the site to render.

## Launch checklist

- [x] Build the English profile and framework page.
- [x] Preserve Hebrew translations as supplemental structured JSON while keeping the normal website experience English-only.
- [x] Add direct profile-to-private-AI cross-link.
- [x] Add metadata, entity data, discovery files, social cards, and 404 page.
- [x] Run the static AI visibility probe with no findings.
- [x] Render-check desktop, narrow English, narrow Hebrew, and the point-of-view page.
- [x] Publish `mantaeb/etgar-bonar1-site` and enable GitHub Pages.
- [x] Add Cloudflare CNAME `etgar` to `mantaeb.github.io`, DNS only.
- [x] Verify public HTTPS, the valid certificate, and all canonical routes.
- [x] Add reciprocal English and Hebrew links from `ai.bonar1.com`, including the canonical Person identifier.
- [ ] Recheck the plain-HTTP redirect after GitHub Pages edge propagation. HTTPS enforcement is already enabled.
- [ ] Replace the monogram with the original high-resolution headshot, if desired.
- [ ] Have Etgar give the Hebrew copy a final native-speaker read before wider promotion.
- [x] Add a dedicated Cloudflare Web Analytics site tag.
- [x] Verify the `etgar.bonar1.com` Search Console property.
- [ ] Submit the sitemap through the `bonar1.com` Search Console Domain property.
- [x] Publish redesign commit `a58a9fe` after explicit approval of the public career-content update.
- [x] Replace the retired "frontier" name with "the cost-to-serve line" in English and "הקו שזז" in Hebrew.
- [x] Publish content refinement commit `9e50cfd` after explicit approval.
- [x] Introduce the initial "shape the commercial system" hero, localize it to Hebrew, and publish the responsive treatment in `4cfcde3`.
- [x] Restore the complete Lokalise/Claude graphic at its natural aspect ratio and link the English and Hebrew visual and caption to the Anthropic customer story in `1ff1fdc`.
- [x] Add operating ownership through "shape and run," update the Hebrew rendering, and preserve the narrow-screen hierarchy in `aa59748`.

## Local preview

```bash
python3 -m http.server 8765 --directory projects/bonar1-websites/etgar-site
```

Then open `http://127.0.0.1:8765/`.
