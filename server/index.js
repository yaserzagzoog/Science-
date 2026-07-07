// ─────────────────────────────────────────────────────────────────────────────
// WellBeing+ Coach — backend bridge to the Vital wearables API.
//
// Why this server exists:
//   Apple Health / HealthKit has NO web API. To get live data into a web app you
//   use an aggregator (here: Vital, https://tryvital.io). Vital reads HealthKit
//   through its iOS SDK / Connect app on the user's iPhone and exposes the data
//   via a REST API secured by a secret key. That secret key must NEVER live in
//   the browser — it lives here, server-side.
//
// Flow:
//   1. Browser -> POST /api/user           (ensure a Vital user for this person)
//   2. Browser -> POST /api/link-token     (get a Link token; open Vital Link)
//   3. User connects Apple Health in the Vital iOS app / Link flow
//   4. Browser -> GET  /api/biomarkers     (we pull sleep/activity/vitals and map
//                                           them to the app's biomarker sliders)
//
// Config via environment variables (see .env.example):
//   VITAL_API_KEY   — required, your Vital API key (secret)
//   VITAL_ENV       — "sandbox" | "production"  (default: sandbox)
//   VITAL_REGION    — "us" | "eu"               (default: us)
//   PORT            — default 8787
//   ALLOWED_ORIGIN  — CORS origin for the web app (default: * )
// ─────────────────────────────────────────────────────────────────────────────

const express = require("express");
const cors = require("cors");

const {
  VITAL_API_KEY,
  VITAL_ENV = "sandbox",
  VITAL_REGION = "us",
  PORT = 8787,
  ALLOWED_ORIGIN = "*",
} = process.env;

function vitalBaseUrl() {
  // https://docs.tryvital.io/api-reference — regional + environment hostnames.
  const region = VITAL_REGION.toLowerCase() === "eu" ? "eu" : "us";
  const env = VITAL_ENV.toLowerCase() === "production" ? "" : "sandbox.";
  return `https://api.${region}.${env}tryvital.io`;
}

// Thin wrapper around the Vital REST API.
async function vital(path, { method = "GET", body } = {}) {
  if (!VITAL_API_KEY) {
    const err = new Error("VITAL_API_KEY is not configured on the server.");
    err.status = 500;
    throw err;
  }
  const res = await fetch(vitalBaseUrl() + path, {
    method,
    headers: {
      "x-vital-api-key": VITAL_API_KEY,
      "Content-Type": "application/json",
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  let data;
  try { data = text ? JSON.parse(text) : {}; } catch { data = { raw: text }; }
  if (!res.ok) {
    const err = new Error(data?.detail || data?.message || `Vital API error ${res.status}`);
    err.status = res.status;
    err.body = data;
    throw err;
  }
  return data;
}

// ─── Biomarker mapping ────────────────────────────────────────────────────────
// Pull the most recent sleep + activity + body summaries and reduce them to the
// nine biomarkers the coach UI uses. Anything missing is simply omitted so the
// UI keeps its current slider value.
function isoDaysAgo(days) {
  const ms = Date.now() - days * 86400000;
  return new Date(ms).toISOString().slice(0, 10);
}

function pickLatest(items, dateKey = "date") {
  if (!Array.isArray(items) || !items.length) return null;
  return items
    .slice()
    .sort((a, b) => String(a[dateKey]).localeCompare(String(b[dateKey])))
    .pop();
}

async function fetchBiomarkers(userId) {
  const start = isoDaysAgo(7);
  const end = isoDaysAgo(0);
  const q = `?start_date=${start}&end_date=${end}`;

  const out = {};
  const sources = {};

  // Sleep summary -> sleepHours, sleepQuality, hrv, respiratoryRate, avg HR, spo2
  try {
    const sleep = await vital(`/v2/summary/sleep/${userId}${q}`);
    const s = pickLatest(sleep?.sleep || sleep?.data || [], "calendar_date") ||
              pickLatest(sleep?.sleep || sleep?.data || [], "date");
    if (s) {
      if (s.duration != null) out.sleepHours = round(s.duration / 3600, 1);
      if (s.efficiency != null) out.sleepQuality = Math.round(s.efficiency > 1 ? s.efficiency : s.efficiency * 100);
      if (s.hrv_rmssd_milli != null) out.hrv = Math.round(s.hrv_rmssd_milli);
      else if (s.hrv?.rmssd != null) out.hrv = Math.round(s.hrv.rmssd);
      if (s.respiratory_rate != null) out.respiratoryRate = Math.round(s.respiratory_rate);
      if (s.average_hr_bpm != null) out.heartRate = Math.round(s.average_hr_bpm);
      else if (s.heart_rate?.avg != null) out.heartRate = Math.round(s.heart_rate.avg);
      if (s.average_oxygen_saturation != null) {
        const v = s.average_oxygen_saturation;
        out.spo2 = Math.round(v <= 1 ? v * 100 : v);
      }
      sources.sleep = s.calendar_date || s.date || null;
    }
  } catch (e) { sources.sleepError = e.message; }

  // Activity summary -> steps (thousands)
  try {
    const activity = await vital(`/v2/summary/activity/${userId}${q}`);
    const a = pickLatest(activity?.activity || activity?.data || [], "calendar_date") ||
              pickLatest(activity?.activity || activity?.data || [], "date");
    if (a && a.steps != null) {
      out.steps = round(a.steps / 1000, 1);
      sources.activity = a.calendar_date || a.date || null;
    }
  } catch (e) { sources.activityError = e.message; }

  // Resting heart rate can override the sleep-derived HR if present.
  try {
    const body = await vital(`/v2/summary/body/${userId}${q}`);
    const b = pickLatest(body?.body || body?.data || [], "calendar_date") ||
              pickLatest(body?.body || body?.data || [], "date");
    if (b) {
      if (b.body_temperature_celsius != null) out.bodyTemp = round(b.body_temperature_celsius, 1);
      sources.body = b.calendar_date || b.date || null;
    }
  } catch (e) { sources.bodyError = e.message; }

  return { biomarkers: out, sources };
}

function round(n, dp) {
  const f = Math.pow(10, dp);
  return Math.round(n * f) / f;
}

// ─── HTTP server ──────────────────────────────────────────────────────────────
const app = express();
app.use(express.json());
app.use(cors({ origin: ALLOWED_ORIGIN }));

app.get("/health", (_req, res) => {
  res.json({ ok: true, env: VITAL_ENV, region: VITAL_REGION, configured: !!VITAL_API_KEY });
});

// Ensure a Vital user exists for a stable client_user_id supplied by the browser.
app.post("/api/user", async (req, res) => {
  try {
    const clientUserId = String(req.body?.client_user_id || "").trim();
    if (!clientUserId) return res.status(400).json({ error: "client_user_id required" });

    // Try to resolve an existing user first; create if missing.
    let user;
    try {
      user = await vital(`/v2/user/resolve/${encodeURIComponent(clientUserId)}`);
    } catch {
      user = await vital("/v2/user", { method: "POST", body: { client_user_id: clientUserId } });
    }
    res.json({ user_id: user.user_id || user.id, client_user_id: clientUserId });
  } catch (e) {
    res.status(e.status || 500).json({ error: e.message, detail: e.body });
  }
});

// Issue a Link token so the user can connect a provider (Apple Health via SDK).
app.post("/api/link-token", async (req, res) => {
  try {
    const userId = String(req.body?.user_id || "").trim();
    if (!userId) return res.status(400).json({ error: "user_id required" });
    const token = await vital("/v2/link/token", {
      method: "POST",
      body: { user_id: userId },
    });
    const linkToken = token.link_token;
    const region = VITAL_REGION.toLowerCase() === "eu" ? "eu" : "us";
    const env = VITAL_ENV.toLowerCase() === "production" ? "" : "sandbox.";
    res.json({
      link_token: linkToken,
      // Web Link works for OAuth providers; Apple Health specifically is completed
      // in the Vital iOS SDK / Vital Connect app using the same token.
      link_url: `https://link.${env}tryvital.io/?token=${linkToken}&region=${region}`,
    });
  } catch (e) {
    res.status(e.status || 500).json({ error: e.message, detail: e.body });
  }
});

// Pull the latest health data and map to the coach's biomarkers.
app.get("/api/biomarkers", async (req, res) => {
  try {
    const userId = String(req.query.user_id || "").trim();
    if (!userId) return res.status(400).json({ error: "user_id required" });
    const data = await fetchBiomarkers(userId);
    res.json(data);
  } catch (e) {
    res.status(e.status || 500).json({ error: e.message, detail: e.body });
  }
});

app.listen(PORT, () => {
  console.log(`WellBeing+ backend on :${PORT}  (Vital ${VITAL_ENV}/${VITAL_REGION}, key ${VITAL_API_KEY ? "set" : "MISSING"})`);
});
