# Collective AI

An open research organisation — *a CERN for the AI era* — giving a distributed cohort shared,
frontier-scale AI capacity to work together on open problems in fundamental physics.

This repository is the public site and the collaborative **research workspace**.

## Pages

| File | What it is |
|------|-----------|
| `index.html` | Landing page — mission, the three research tracks, how the AI hub accelerates the work, progress, and how to join. |
| `workspace.html` | Per-problem research rooms where the cohort chats with Claude and shares history. |
| `dark-matter.html`, `fine-structure.html`, `quantum-gravity.html` | Curated arXiv references and sources for each track. |
| `refs.css` | Shared styles for the reference pages. |

## The research workspace

`workspace.html` gives each open problem its own room. Researchers chat with Claude (with a
problem-specific system prompt) and, when a sync backend is configured, share the conversation and
history with everyone else in the room.

Architecture (server-free):

- **Bring your own key.** Each researcher enters their own Anthropic API key in **Settings**. It is
  stored only in their browser (`localStorage`) and sent directly to `api.anthropic.com` — never to the
  shared database. Calls use the `anthropic-dangerous-direct-browser-access` header.
- **Shared rooms + history.** Optional. Point the workspace at a free [Supabase](https://supabase.com)
  project (URL + public *anon* key in Settings) and messages are shared and synced live across the
  cohort. With no backend configured, the workspace works locally in the browser.

### Enable shared rooms (Supabase)

1. Create a free project at [supabase.com](https://supabase.com).
2. In the SQL editor, run:

   ```sql
   create table if not exists messages (
     id uuid primary key default gen_random_uuid(),
     room text not null,
     author text not null,
     role text not null check (role in ('user','assistant')),
     content text not null,
     created_at timestamptz not null default now()
   );

   alter table messages enable row level security;

   -- Open read/insert for the cohort; the anon key is safe to expose under RLS.
   create policy "cohort can read"   on messages for select using (true);
   create policy "cohort can insert" on messages for insert with check (true);
   ```

3. **Database → Replication** (or **Realtime**): enable realtime for the `messages` table so live
   updates work.
4. In the workspace **Settings**, paste your **Project URL** and the **anon public** key. The badge in
   the top bar switches from *Local only* to *Shared rooms*.

> Tighten the policies (e.g. require auth, restrict inserts) before any sensitive or public deployment —
> the defaults above are open to anyone with the anon key.

### Model

Defaults to **Claude Opus 4.8**; Sonnet 5 and Haiku 4.5 are selectable in Settings.

## Deploying

The site is fully static. A GitHub Actions workflow (`.github/workflows/deploy.yml`) publishes it to
GitHub Pages on every push to `main`. To go live: merge to `main`, then enable **Settings → Pages →
Source: "GitHub Actions."**

## License

Public domain — [The Unlicense](./UNLICENSE).
