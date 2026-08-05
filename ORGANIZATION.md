# David's Work Organization Playbook (UWP)

A simple system for keeping Unique Wood Products work organized. The rule of
thumb behind everything here: **one home per thing, one name per project, and a
15-minute weekly reset.** If a step takes more than a minute to decide, the
system is too complicated — simplify it.

---

## 1. Active projects (name them the same way everywhere)

Use these exact project names in email labels, Claude session titles, Drive
folders, and file names, so everything about one project sorts together:

| Project name    | What it covers                                                        |
|-----------------|-----------------------------------------------------------------------|
| `Dust Collector`| LBR-C purchase, VFD comparison, Flamex spec, Houston permits, tax exemption |
| `Wisenbaker`    | Email access, tooling coordination, tolerance specifications          |
| `Catalog`       | Website product data: SKUs, images, mouldings, stair parts, menu structure |
| `Website`       | Hosting, Kinsta, SSL, SEO / Search Console, Elementor                 |
| `Trade Shows`   | IWF Atlanta, Coverings, NATT                                          |

When a project finishes, retire the name. When something new starts, add a row.

## 2. Where things live

| Kind of thing            | Home                                                       |
|--------------------------|------------------------------------------------------------|
| Website code             | GitHub → `UWP-Website`                                     |
| Product configurator     | GitHub → `uwp-configurator`                                |
| Email signatures/assets  | GitHub → `uwp-email-assets` (this repo)                    |
| Specs, comparisons, PDFs | Google Drive → one folder per deliverable                  |
| Conversations with Claude| One long-running session per project, not one per question |

## 3. File naming (keep doing what you're doing)

The Drive convention already in use works — keep it:

```
UWP_<Project>_<Topic>_<YYMMDD>_v<##>
e.g.  UWP_LBR_VFD_Comparison_260804_v03
```

Date goes in the name, version bumps on every revision, and the latest version
lives in the same folder as the old ones (don't scatter copies).

## 4. Gmail system (set up 2026-08-05)

Labels (already created):

- 🔴 **UWP/Action Needed** — anything that needs a decision or reply. This is
  the only label to check daily. Remove the label once handled.
- 🔵 **UWP/Website & Hosting** — Kinsta, SSL, Search Console, domains
- 🟠 **UWP/Dust Collector** — vendor quotes, permits, specs
- 🟢 **UWP/Trade Shows** — IWF, Coverings, NATT deadlines and bookings

How to keep it working with ~1,500 unread emails already in the inbox:

1. **Don't try to clear the backlog.** Declare inbox bankruptcy: select all →
   archive everything older than 2 weeks. It stays searchable forever.
2. **Unsubscribe ruthlessly** from the daily noise (Groupon, Temu, Starbucks,
   LinkedIn digests). Ten clicks now saves 50 emails a week.
3. In Gmail, add filters so newsletters skip the inbox: search the sender →
   "Filter messages like these" → *Skip the Inbox*.
4. New real email gets one project label; if it needs action, it also gets
   **UWP/Action Needed**.

## 5. Claude sessions

- Title sessions `<Project> — <topic>` (e.g. `Dust Collector — VFD comparison`)
  so the sidebar groups visually.
- Reuse one main session per active project instead of opening a new one per
  question — the context carries over and answers get better.
- Archive sessions when the question is answered; they stay searchable.

## 6. The 15-minute weekly reset (Friday or Monday morning)

1. Open the **UWP/Action Needed** label — handle or reply to each, then remove
   the label. Target: empty.
2. Skim the inbox top 20; label anything real, archive the rest.
3. Check upcoming deadlines (trade show bookings, permit dates) and put each
   one on the calendar the moment you learn about it.
4. Archive finished Claude sessions; rename any that aren't `Project — Topic`.

## 7. Open items found during setup (2026-08-05)

- [ ] **Expired SSL certificate** on Houstoncarpetservice (Kinsta email, Aug 5) — urgent
- [ ] **15 WordPress plugin vulnerabilities** flagged by Kinsta for uniquewoodproducts.com
- [ ] **IWF Atlanta hotel block** closing soon — book the room
- [ ] **Coverings 2027 speaker deadline: August 7**
- [ ] `uwp-email-assets` repo is **public** but contains staff email signatures — consider making it private
- [ ] Google Calendar connector in Claude is disconnected — reauthorize it in
      claude.ai connector settings so deadlines can be tracked automatically
