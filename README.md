# WellBeing+ Biometric Coach

An AI-powered biometric health coach. Adjust your biomarkers (or pull them from
Apple Health), then ask Claude for a structured health assessment — summary,
per-biomarker insights, a prioritised action plan, and today's focus.

- **`coach.html`** — the whole front-end (single self-contained page, React + Babel
  via CDN, no build step). Works on GitHub Pages.
- **`server/`** — a small Node backend that bridges the **Vital** wearables API so
  the app can read **live Apple Health** data.

## Running the app

Open `coach.html` (any static host works — it's already linked from `index.html`).
On first use, click **🔑 Set API key** and paste an Anthropic API key. The key is
stored only in your browser (`localStorage`) and sent directly to the Anthropic
API with the `anthropic-dangerous-direct-browser-access` header.

> This is a demo/personal tool. Sending your key from the browser is fine for
> your own use, but do **not** ship this pattern to other users — put the
> Anthropic call behind a backend instead.

## Getting biomarker data in

There are three ways to fill the sliders, in decreasing convenience:

### 1. Live Apple Health (via the Vital aggregator) — needs the backend

Apple Health / HealthKit has **no web API** — it is native-iOS only. To get live
data into a web app you use an aggregator. This project uses
[Vital](https://tryvital.io): its iOS SDK / Connect app reads HealthKit on your
iPhone and exposes the data through a REST API, which the `server/` backend reads
(the secret API key stays server-side, never in the browser).

Setup:

1. Create a Vital account and get an API key.
2. Deploy the backend:
   ```bash
   cd server
   cp .env.example .env      # fill in VITAL_API_KEY, VITAL_ENV, VITAL_REGION
   npm install
   npm start                 # listens on :8787
   ```
   Host it anywhere that runs Node (Render, Railway, Fly, a VM, …) and set
   `ALLOWED_ORIGIN` to your site's origin.
3. In the app's **Apple Health · Live** box, paste the backend URL, click
   **🍏 Connect**, and complete the Apple Health connection in the Vital iOS app.
4. Click **⟳ Sync latest** to pull your most recent sleep / activity / vitals
   onto the sliders.

Backend endpoints: `POST /api/user`, `POST /api/link-token`,
`GET /api/biomarkers?user_id=…`, `GET /health`.

### 2. Import your Apple Health export — no backend, no account

On your iPhone: **Health → profile photo → Export All Health Data**. Upload the
resulting `.zip` (or the `export.xml` inside it) via **⤓ Or import export file**.
Parsing happens entirely in the browser — nothing is uploaded to a server.

### 3. Manual — just drag the sliders

## Biomarker mapping

| Biomarker | Apple Health / Vital source |
|---|---|
| Heart Rate | `HKQuantityTypeIdentifierHeartRate` / sleep avg HR |
| HRV | `HeartRateVariabilitySDNN` / sleep RMSSD |
| Sleep Duration | `SleepAnalysis` asleep stages / sleep summary |
| Sleep Quality | sleep efficiency (Vital) |
| Blood Oxygen | `OxygenSaturation` |
| Daily Steps | `StepCount` (summed per day) |
| Respiratory Rate | `RespiratoryRate` |
| Body Temp | `BodyTemperature` (°F auto-converted) |
| Stress Level | manual (not in HealthKit) |

## Notes

- Not medical advice.
- `server/.env` is git-ignored — never commit real keys.
