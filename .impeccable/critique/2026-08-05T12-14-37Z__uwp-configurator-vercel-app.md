---
target: the new UWP website (uwp-configurator.vercel.app)
total_score: 33
max_score: 40
na_heuristics: 
p0_count: 1
p1_count: 2
timestamp: 2026-08-05T12-14-37Z
slug: uwp-configurator-vercel-app
---
Method: dual-agent (A: design review with full browser/screenshot evidence · B: detector CLI + in-page detector injection)

Target: uwp-configurator.vercel.app, reviewed via a local build of mylifepast30-sys/uwp-configurator (dev server, site-lock disabled, Sanity offline — no visible content gaps resulted; verified). Desktop 1440×900 + mobile 390×844, seven routes, live configurator interaction.

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 4 | Live price/drawing/summary recalc verified ($144→$224→$149→$174); stock dots; filter counts |
| 2 | Match System / Real World | 3 | Trade vocabulary right for primary audience; consumer surfaces hit unexplained jargon (20/20 policy, EGU, retro-fit) |
| 3 | User Control and Freedom | 3 | No configurator reset; no breadcrumbs on configurators; quote empty state offers one narrow escape |
| 4 | Consistency and Standards | 2 | Core system disciplined, but /wood-species abandons the design language and /find drops the site chrome |
| 5 | Error Prevention | 4 | Constrained selects, binary edge choice with consequences explained, template required for winder treads, file-type/size caps, honeypot |
| 6 | Recognition Rather Than Recall | 4 | Config summary restates everything; SKU+dims on tiles; guidance at point of need |
| 7 | Flexibility and Efficiency | 4 | /find SKU jump page, profile finder w/ stock filter, PDF export, trade routing, tel: links |
| 8 | Aesthetic and Minimalist Design | 2 | System is handsome; pages hoard content — /mouldings is a 28,269px single page; configurator carries ~4,000px of editorial below the tool |
| 9 | Error Recovery | 3 | Plain-language submit errors with phone fallback; but no inline field validation on a long form |
| 10 | Help and Documentation | 4 | Decision guides embedded where decisions happen; warranties; bilingual notices; Answers section |
| **Total** | | **33/40** | **Good — solid foundation, address weak areas** |

## Design Specificity Verdict

**LLM assessment: AUTHORED — unusually so.** The configurator renders a live dimensioned technical drawing (plan + side profile, return caps drawn when toggled); the moulding catalog uses real per-SKU cross-section SVGs; shop-floor language throughout ("will-call", "custom-knife runs", "20/20 short-length policy" with calculator and Spanish translation, "Tanner Rd yard"); trade-vs-retail routing on /contact; a /find page built for office staff phone orders. Nothing here could be reused by another company without a rewrite. One outlier: /wood-species reads like an import from a different system.

**Deterministic scan:** CLI scan of source: 27 findings, all one rule (side-tab accent border, `border-l-4`, mostly on success pages and configurator info boxes). In-page detector ran on 5 routes (injection verified, clean re-run with autoScan off): / 37, /mouldings 58, /stair-treads 42, /custom-1-inch-stair-tread 93, /request-quote 25. Dominant clusters: undersized-ui-text (10px uppercase meta labels — 52 hits on the configurator alone), low-contrast (recurring pairs: #C9A96E on #124E53 ≈4.2:1, #A89F91 on white/cream ≈2.4–2.6:1), line-length (25 hits on /mouldings, up to ~213 chars/line), all-caps-body, kicker-above-heading, cream-palette (fires per page for #F7F4EF — aligned with the client's white-background ask), one first-viewport-column-overflow on the configurator grid, one skipped heading (h2→h4, shared "What we mill" footer block). Detector confirmed A's two biggest visual findings independently (gold-on-light contrast; tiny label type). Likely false positives given the pinned brand: italic-serif-display on the Cormorant display headings (deliberate brand serif), image-hover-transform (advisory), em-dash-overuse (advisory, brand voice). Discarded: a contaminated first run where the detector flagged its own overlay.

**Visual overlays:** ran headlessly (no user-visible tab in this remote environment); findings captured from the in-page console/API instead.

## Overall Impression

This is a genuinely excellent trade website — best-in-category configurator UX, real token discipline, expert-path engineering (SKU finder, trade routing, PDF quotes). It scores 33/40 where most real sites land in the low-to-mid 20s. The gap to great is concentrated in four things: a conversion-killing dead end on the quote page, two pages that break the design system, gold text that fails contrast on light grounds, and pages that are simply too long. None require redesign; all are fixable within the existing system.

## What's Working

1. **The configurator feedback loop is best-in-class:** live dimensioned drawing + instant pricing + persistent summary + PDF export, all verified working, loaded with a sensible default ($144 White Oak 48") so a price is visible before any interaction.
2. **A real, documented token system:** tailwind.config.ts encodes the brand book with usage ratios in comments; Cormorant-display/Outfit-body discipline is enforced and obeyed.
3. **Expert paths:** /find paste-a-SKU page, profile finder with in-stock filter, cash-account fast path, will-call order codes, tel: links, sticky mobile QUOTE/CALL/LOCATIONS bar.

## Priority Issues

1. **[P0] "Get a Quote" dead-ends for anyone without a quote list.** RequestQuoteClient.tsx (lines 93–96) hard-rejects submission with zero items; the empty state's only CTA deep-links to a single baluster SKU; the submit button renders greyed. The header's primary CTA on every page leads here. Highest-intent visitors — including trade buyers who want to attach a takeoff PDF and submit without building line items — are turned away at the conversion moment. **Fix:** allow a "describe your project" submission mode (notes + attachment, no line items) and replace the empty-state CTA with the four product-family paths. **Command:** /impeccable harden (quote flow).
2. **[P1] /wood-species breaks the design system** (different heading type, card anatomy, palette; no serif display, no teal) and /find drops the site header/footer with a taupe button that reads disabled. **Fix:** re-skin both with site tokens; content is fine. **Command:** /impeccable polish.
3. **[P1] Gold-on-light text fails contrast.** #C9A96E text appears 494 times, including 10–11px uppercase meta labels on cream/white (~2.0:1 vs 4.5:1 required); detector independently flagged the same pairs plus #A89F91 on white. Gets worse on a white background. **Fix:** add a darkened gold text token (~#8A6D3B) for text on light grounds; keep #C9A96E for surfaces/borders/text-on-teal. Bump the 10px labels to ≥11–12px while in there. **Command:** /impeccable typeset (or fold into the white-background pass).
4. **[P2] Page mass.** /mouldings renders all 157 profiles in one 28k-px page; configurator and family pages append thousands of pixels of editorial; home repeats the quote CTA in five sections. **Fix:** collapse catalog sections behind category anchors/expanders with a sticky filter bar; move configurator editorial to a linked guide. **Command:** /impeccable distill.
5. **[P2] Twelve-option flat grid on /stair-treads** mixing stocked, oversized, landings, and customs. **Fix:** group under three labeled subheads — Stocked / Landings & platforms / Custom·configure — using metadata already on the cards. **Command:** /impeccable layout.

## Persona Red Flags

**Jordan (first-time homeowner):** must know "stair tread" ≠ "stair parts" (both cards exist); asked to choose 8070 vs 8071 before retro-fit is explained (guides sit below the grid); "20/20 policy" and "$125–$175 field-service fee" lack homeowner framing; hits the P0 dead end if they click GET A QUOTE early. The configurator itself, though, is novice-usable.

**Casey (mobile, from real 390px screenshots):** sticky QUOTE/CALL/LOCATIONS bottom bar is excellent; no horizontal overflow anywhere (verified scrollWidth 390). Red flags: "SWIPE TO COMPARE" carousel hides options from a distracted user; on the mobile configurator the price sits ~2,000px below the species picker — a sticky mini-price chip would close the loop.

**Trade buyer (GC purchasing agent):** exceptionally served overall (/find, spec-sheet band, two yards with hours). Red flags: the P0 hits them hardest (wants to attach a takeoff and submit without line items); "trade pricing after account" never stated on catalog cards; no per-profile spec-sheet download from the catalog grid.

## White Background & Layout (client's headline question)

**Current system, measured:** cream field #F7F4EF on `<html>` (485 uses) → pure-white cards #FFFFFF (404 uses) → teal #124E53 ceremonial bands (252 uses; hero band opens every interior page) → near-black utility bands #212223 (footer, spec panels). The page is already 60–65% cream/white; the "non-white" impression comes from the cream field plus the teal band openings.

**Recommendation: white fields, not a white site.**
- Change the global `<html>` background #F7F4EF → #FFFFFF — one change, ~485 surfaces.
- Invert the card relationship: white field + #F7F4EF cream card interiors (cream becomes the contained color, keeping the brand's warmth on an honestly white page). Alternative: keep white cards and strengthen borders (~#CFC9BD) or add a light warm shadow — the inversion is the better answer.
- Keep the teal hero bands, trade band, and black footer exactly as they are — on white they read crisper, and the brand book's own ratio (teal 48–52% identity presence) argues for one saturated band per viewport-journey. Concede interior-page heroes to white-with-teal-type only if pushed; defend the home hero and footer.
- Strengthen gold/stone hairlines between sections (white removes the subtle cream tonal shifts the current boundaries rely on).
- Ship the darkened gold text token in the same change — the contrast failure worsens on #FFFFFF.
- Do not whiten the footer, trade band, or the configurator's black spec/preview headers — Operate surfaces need instrument-panel weight.

**Layout verdict:** the current hero → proof stats → catalog/configurator → trade band → footer rhythm is right for this brand; the layout is not the problem — page length is (see P2s). Grid presentation of profile drawings, numbered configurator steps, and the sticky mobile bar should all stay.

## Minor Observations

"0 items · 0 units" count placed under the contact column on /request-quote · /find's taupe OPEN button reads disabled before typing · "Left Return" silently auto-checks "Left Nosing" (correct domain logic, unannounced) · desktop-only teal-dark band means mobile never sees one home section · "PHOTO · COMING SOON" placeholder cards are an honest, on-brand gap treatment · lazy-load blank tiles in full-page screenshots were verified as capture artifacts, not defects (160/160 images load).

## Questions to Consider

1. If the configurator is the crown jewel, why is it buried at `/custom-1-inch-stair-tread` behind a 12-card grid instead of being the home page's second act — "price a tread in 30 seconds"?
2. Who serves the buyer with a photo of a staircase and no vocabulary? Is a visual "which tread is this?" entry point worth building?
3. Is the white-background ask actually about whiteness — or a reaction to heaviness from the long cream/teal scroll? Halving page length might satisfy the instinct better than changing #F7F4EF.
