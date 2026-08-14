# Connecting Apple Health to a Lovable wellbeing app

A build guide for wiring Apple Health data into an app built with Lovable,
including paste-ready prompts for the Lovable agent.

## The constraint that shapes everything

**Apple Health has no API.** There is no OAuth flow, no REST endpoint, and no
MCP server for HealthKit. HealthKit is an on-device iOS framework; the data
never leaves the iPhone unless a *native iOS app* reads it and pushes it
somewhere.

Lovable builds React web apps. A web app cannot read HealthKit — not with a
better prompt, not with a clever library. So "connect Apple Health" always
decomposes into two halves:

- **Lovable's half**: the database, the ingest API, the sync UI, the charts.
- **The bridge's half**: something native (or semi-native) that reads HealthKit
  and POSTs to the ingest API.

Design the ingest API first and every bridge below becomes interchangeable.

## The four bridges

| Path | Native code | Mac + Xcode | Apple Dev account | Time to working | Best for |
|---|---|---|---|---|---|
| **A. Health Auto Export → webhook** | no | no | no | ~1 day | shipping now, personal use |
| **B. Capacitor wrapper + HealthKit plugin** | yes | yes | yes ($99/yr) | 2–4 weeks | a real App Store product |
| **C. Aggregator (Terra / Vital / Rook / Spike)** | their SDK | yes for Apple Health | yes | ~1 week | also want Whoop/Oura/Garmin |
| **D. `export.zip` upload** | no | no | no | ~2 hours | one-time historical backfill |

**Recommended sequence:** build **A** now and **D** alongside it for history,
with the backend structured so **B** drops in later without backend changes.
All four hit the *same* ingest endpoint.

### Path A — Health Auto Export → webhook

The iOS app *Health Auto Export – JSON+CSV* can POST HealthKit data to an
arbitrary REST endpoint on a schedule (a paid feature). Apple Shortcuts can do
a narrower version of the same thing with "Find Health Samples" plus "Get
Contents of URL".

No Apple Developer account, no App Store review, no Mac. This is a genuinely
working Apple Health connection, just with the bridge outsourced to an app the
user installs.

Limits: hourly-ish rather than instant, depends on a third-party app staying
alive, and the user has to paste a token during setup.

### Path B — Capacitor wrapper

What a production app does, and what the reference app in the design
screenshots does.

1. Export the Lovable project to GitHub.
2. `npm i @capacitor/core @capacitor/ios && npx cap add ios`
3. Add a HealthKit plugin — `@perfood/capacitor-healthkit` or
   `cordova-plugin-health` are the common choices. Verify current versions and
   maintenance status before committing; this corner of the ecosystem moves.
4. In Xcode: enable the **HealthKit** capability, add
   `NSHealthShareUsageDescription` (and `NSHealthUpdateUsageDescription` if
   writing back) to `Info.plist`.
5. Background auto-sync = `HKObserverQuery` + `enableBackgroundDelivery`.

App Review notes: the app needs a genuine health purpose and a privacy policy;
Apple prohibits using HealthKit data for advertising, and prohibits storing
HealthKit data in iCloud.

### Path C — aggregator API

Terra, Vital, Rook, Spike and similar vendors provide an iOS SDK for Apple
Health plus server-side webhooks. Apple Health still requires their native SDK
in a wrapper, so it does not remove the Xcode step — but Whoop, Oura, Garmin,
Fitbit and Polar are pure web OAuth through them and work from a Lovable app
with no native code at all.

Worth it when the app targets multiple wearables. Overkill for Apple Health
alone.

### Path D — `export.zip` upload

Health app → profile picture → **Export All Health Data** produces a
`export.zip` containing `export.xml` with the full history. Parse it
server-side and feed it through the same upsert path as live syncing.

This is how to deliver a "backfilling N days of history" feature on day one.
`export.xml` is routinely hundreds of megabytes — it must be stream-parsed,
never loaded whole.

## Two design details worth copying

**Staged permissions.** Rather than asking for every HealthKit type up front,
ask for new types when a new feature ships by calling `requestAuthorization`
with *only* the new identifiers. iOS then shows a short permission sheet
listing just those, and existing grants are untouched.

**Per-metric sync anchors.** Store an `HKAnchoredObjectQuery` anchor per metric
so each sync reads only what changed since last time. Combined with idempotent
upserts keyed on `(user_id, provider, metric, started_at, external_id)`, syncs
become cheap and safe to retry.

---

## Lovable prompts

Paste in order. Each assumes the previous one succeeded.

### 1 — Data model

```
Enable the database. Create an Apple Health ingest schema, source-agnostic so
any device can write to it.

Tables:
- health_connections: id, user_id, provider (text: 'apple_health'|'whoop'|'oura'),
  status ('connected'|'disconnected'|'error'), last_synced_at, ingest_token_hash,
  scopes jsonb, backfill_total_days int, backfill_done_days int, created_at
- health_samples: id, user_id, provider, metric (text), value numeric, unit text,
  started_at timestamptz, ended_at timestamptz, source_name text,
  external_id text, raw jsonb, created_at
- health_workouts: id, user_id, provider, activity_type, started_at, ended_at,
  duration_s int, active_kcal numeric, total_kcal numeric, distance_m numeric,
  avg_hr int, max_hr int, external_id text, raw jsonb
- health_daily: user_id, day date, steps int, active_kcal numeric,
  resting_hr int, hrv_ms numeric, sleep_minutes int, weight_kg numeric,
  vo2max numeric, kcal_in numeric, protein_g numeric, carbs_g numeric,
  fat_g numeric, alcohol_units numeric  -- primary key (user_id, day)

Constraints and indexes:
- UNIQUE (user_id, provider, metric, started_at, external_id) on health_samples
  so re-sending the same sample is a no-op
- UNIQUE (user_id, provider, external_id) on health_workouts
- index on (user_id, metric, started_at desc)

RLS on every table: users can only read/write rows where user_id = auth.uid().
The ingest edge function uses the service role and sets user_id explicitly.

Allowed `metric` values (document them in a TS enum too):
steps, heart_rate, resting_heart_rate, hrv_sdnn, sleep_analysis, body_mass,
body_fat_pct, vo2_max, active_energy, basal_energy, distance_walking_running,
dietary_energy, dietary_protein, dietary_carbs, dietary_fat, blood_oxygen,
respiratory_rate, mindful_minutes, alcohol_units
```

### 2 — The ingest endpoint

```
Create a public edge function `apple-health-ingest` (POST, no Supabase auth
header required — it is called by an iOS Shortcut / native app).

Auth: Bearer token in the Authorization header. Hash it (sha256) and look it up
in health_connections.ingest_token_hash to resolve user_id. Reject 401 otherwise.
Never log the raw token.

Accept a JSON body in this shape and tolerate partial/duplicate payloads:
{
  "device": "iphone",
  "samples": [
    {"metric":"steps","value":8421,"unit":"count","start":"2026-08-14T00:00:00Z",
     "end":"2026-08-14T23:59:59Z","source":"Apple Watch","external_id":"uuid"}
  ],
  "workouts": [
    {"activity_type":"running","start":"...","end":"...","active_kcal":540,
     "distance_m":8100,"avg_hr":152,"external_id":"uuid"}
  ]
}

Behavior:
- Validate with zod; return 400 with a per-item error list, never a 500
- Batch upsert on the unique constraints (idempotent — same payload twice
  changes nothing)
- Cap 5000 items per request, return 413 above that
- After the upsert, recompute health_daily rows for every affected day
  (sum steps/energy/nutrition, average resting HR and HRV, take last weight)
- Update health_connections.last_synced_at
- Return {accepted, skipped_duplicates, days_updated}

Also create `apple-health-token` (authenticated): generates a new random ingest
token for the signed-in user, stores only the hash, and returns the plaintext
once so the UI can display it.
```

### 3 — The Devices screen

```
Build a /devices page, dark theme, deep teal background (#0E2B2B) with mint
accent (#7DE3B0).

Card: "Apple Health" with a right-aligned status pill (Connected / Not connected
/ Error), description text, and "Last synced <relative time>".

Below it a highlighted sub-card "NEW: CALORIES, MACROS AND ALCOHOL" with a
primary button "Enable Macros & Calories" — this expands the requested scopes
array on health_connections and shows the updated setup instructions.

Actions row: "Sync now" (primary, Apple logo), "Reconnect" (link),
"Disconnect" (destructive link, asks to confirm, and offers "also delete my
synced data").

When connected, show a backfill progress bar reading
backfill_done_days / backfill_total_days with the percentage.

When NOT connected, show a step-by-step setup panel:
1. the user's personal ingest URL and token (masked, with copy buttons and a
   "regenerate" action)
2. instructions for the Health Auto Export app: REST API destination, POST,
   JSON, add the Authorization header, pick the metrics, schedule hourly
3. a "Send test payload" button that posts one fake sample and reports whether
   the round trip worked

Everything must be responsive and work as a PWA on iPhone.
```

### 4 — Historical backfill

```
Add /devices/import: drag-and-drop upload of Apple Health's export.zip
(Health app → profile picture → Export All Health Data).

Upload to Supabase storage, then an edge function `apple-health-import`:
- streams the zip, reads export.xml (it can be 500MB+, so parse as a stream,
  never JSON.parse the whole thing)
- maps HKQuantityTypeIdentifier* / HKCategoryTypeIdentifier* records onto our
  metric enum
- writes in chunks of 2000 rows through the same upsert path as the ingest
  function, so imports and live syncs deduplicate against each other
- updates backfill_done_days / backfill_total_days as it goes

The UI polls progress and shows the same progress bar as the Devices card.
Handle the file being partially unsupported: report which HK types were skipped.
```

### 5 — Make the data useful

```
Build the Today dashboard on top of health_daily: Fit Score ring (weighted:
30% training load, 25% sleep, 20% recovery from HRV+resting HR, 15% steps,
10% nutrition adherence), plus 7/30/90-day trend charts for steps, sleep,
resting HR, HRV, weight, and macros. Show a "no data yet" empty state per card
rather than a zero value, and mark days that came from Apple Health with a
small source badge.
```

### 6 — Prepare for the native wrapper

```
Prepare this project to be wrapped in Capacitor for iOS. Add capacitor.config.ts,
add the @capacitor/core + @capacitor/ios dependencies, and create a
src/lib/health-bridge.ts abstraction with two implementations behind one
interface: 'webhook' (current) and 'healthkit' (calls a Capacitor HealthKit
plugin when running natively, detected via Capacitor.isNativePlatform()).
The healthkit implementation should request read authorization for our scopes,
run anchored queries per metric, persist the anchor per metric in local storage
so each sync is incremental, and POST the results to the same
apple-health-ingest endpoint. Stub the plugin calls behind a typed interface
so the web build still compiles.
```

### 7 — Optional: other wearables with no native code

```
Add Whoop and Oura as additional providers using their web OAuth flows.
Store tokens in the health_connections table (encrypted), refresh them in a
scheduled edge function, and normalise their responses into the same
health_samples / health_daily tables so the dashboard code is unchanged.
Add their cards to /devices using the same card component as Apple Health.
```

## Manual steps outside Lovable

**For Path A**, on the iPhone: install *Health Auto Export – JSON+CSV*, add a
REST API destination pointing at the `apple-health-ingest` URL, add the
`Authorization: Bearer <token>` header, select the metrics, set an hourly
schedule.

**For Path B**: export the Lovable project to GitHub, run the Capacitor steps
above on a Mac, and ship through TestFlight.

## Where MCP actually fits

MCP connects AI clients to services; it is not a device-to-cloud sync
protocol, so it cannot be the Apple Health bridge. It is, however, the right
tool for the reverse direction: once the app holds the data, expose it as an
MCP server so Claude can read the metrics and answer questions about them
directly.
