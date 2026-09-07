import json
import streamlit as st
import streamlit.components.v1 as components
from physics import (
    speed, position, convert_distance_to_m, convert_time_to_s,
    speed_in_units,
)
from config import (
    DISTANCE_MIN, DISTANCE_MAX, TIME_MIN, TIME_MAX,
    SLIDER_DISTANCE_MAX, SLIDER_TIME_MAX, DISPLAY_DECIMALS,
)

st.set_page_config(
    page_title="Speed Explorer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Session defaults ----------
defaults = {
    "language": "Indonesia",
    "distance_unit": "m",
    "time_unit": "s",
    "distance": 100.0,
    "time_value": 10.0,
}
for key, value in defaults.items():
    st.session_state.setdefault(key, value)

# ---------- Helpers ----------
def fmt(value):
    return f"{value:.{DISPLAY_DECIMALS}f}".rstrip("0").rstrip(".")

def speed_text(mps, d_unit, t_unit):
    selected = speed_in_units(mps, d_unit, t_unit)
    return f"{fmt(selected)} {d_unit}/{t_unit}", selected

# ---------- CSS ----------
st.markdown("""
<style>
.block-container {max-width: 1250px; padding-top: 1.5rem;}
.hero {
    padding: 22px 24px;
    border-radius: 18px;
    background: linear-gradient(135deg,#eff6ff,#f8fafc);
    border: 1px solid #dbeafe;
    margin-bottom: 16px;
}
.hero h1 {margin:0 0 5px 0;}
.hero p {margin:0;color:#475569;}
.card {
    padding: 16px;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    background: white;
}
div[data-testid="stMetric"] {
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Language ----------
lang = st.sidebar.selectbox(
    "Language / Bahasa",
    ["Indonesia", "English"],
    index=0 if st.session_state.language == "Indonesia" else 1,
)
st.session_state.language = lang
idn = lang == "Indonesia"

# ---------- Header ----------
st.markdown(
    f"""
    <div class="hero">
      <h1>🚀 Speed Explorer</h1>
      <p>{"Simulator interaktif untuk mengeksplorasi hubungan jarak, waktu, dan kecepatan."
         if idn else
         "Interactive simulator for exploring the relationship between distance, time, and speed."}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Sidebar controls ----------
st.sidebar.header("⚙️ Parameter / Parameters")

new_d_unit = st.sidebar.selectbox(
    "Jarak / Distance unit", ["m", "km"], 
    index=["m", "km"].index(st.session_state.distance_unit),
)
new_t_unit = st.sidebar.selectbox(
    "Waktu / Time unit", ["s", "min", "h"],
    index=["s", "min", "h"].index(st.session_state.time_unit),
)

# Preserve physical values when switching units.
old_d_m = convert_distance_to_m(st.session_state.distance, st.session_state.distance_unit)
old_t_s = convert_time_to_s(st.session_state.time_value, st.session_state.time_unit)

if new_d_unit != st.session_state.distance_unit:
    st.session_state.distance_unit = new_d_unit
    st.session_state.distance = old_d_m / {"m": 1, "km": 1000}[new_d_unit]

if new_t_unit != st.session_state.time_unit:
    st.session_state.time_unit = new_t_unit
    st.session_state.time_value = old_t_s / {"s": 1, "min": 60, "h": 3600}[new_t_unit]

d_unit = st.session_state.distance_unit
t_unit = st.session_state.time_unit

# Number inputs are the precise controls.
distance = st.sidebar.number_input(
    "Nilai jarak / Distance value",
    min_value=DISTANCE_MIN,
    max_value=DISTANCE_MAX,
    value=float(st.session_state.distance),
    step=1.0,
    format="%.2f",
    key="distance_input",
)
time_value = st.sidebar.number_input(
    "Nilai waktu / Time value",
    min_value=TIME_MIN,
    max_value=TIME_MAX,
    value=float(st.session_state.time_value),
    step=1.0,
    format="%.2f",
    key="time_input",
)

st.session_state.distance = distance
st.session_state.time_value = time_value

# Sliders are exploration controls. They cover a practical SD range.
slider_d = st.sidebar.slider(
    "Slider jarak / Distance slider",
    1.0, float(SLIDER_DISTANCE_MAX),
    float(min(distance, SLIDER_DISTANCE_MAX)),
    1.0,
    key="distance_slider",
)
slider_t = st.sidebar.slider(
    "Slider waktu / Time slider",
    1.0, float(SLIDER_TIME_MAX),
    float(min(time_value, SLIDER_TIME_MAX)),
    1.0,
    key="time_slider",
)

# A slider change should be easy to use; if it differs from the current
# value and the current value is inside the slider domain, use it.
if abs(slider_d - distance) > 1e-9 and distance <= SLIDER_DISTANCE_MAX:
    st.session_state.distance = slider_d
    distance = slider_d

if abs(slider_t - time_value) > 1e-9 and time_value <= SLIDER_TIME_MAX:
    st.session_state.time_value = slider_t
    time_value = slider_t

# ---------- Physics ----------
distance_m = convert_distance_to_m(distance, d_unit)
time_s = convert_time_to_s(time_value, t_unit)

try:
    v_mps = speed(distance_m, time_s)
except ValueError as exc:
    st.error(str(exc))
    st.stop()

selected_speed_text, v_selected = speed_text(v_mps, d_unit, t_unit)

# ---------- Metrics ----------
m1, m2, m3 = st.columns(3)
m1.metric("📏 Distance / Jarak", f"{fmt(distance)} {d_unit}")
m2.metric("⏱️ Time / Waktu", f"{fmt(time_value)} {t_unit}")
m3.metric("⚡ Speed / Kecepatan", selected_speed_text)

st.markdown(
    f"""
    <div class="card">
      <h3>📐 {"Rumus" if idn else "Formula"}</h3>
      <div style="font-size:1.15rem">
        <b>v = s ÷ t</b>
        &nbsp;→&nbsp;
        <b>v = {fmt(distance)} {d_unit} ÷ {fmt(time_value)} {t_unit}
        = {fmt(v_selected)} {d_unit}/{t_unit}</b>
      </div>
      <p style="color:#475569;margin-bottom:0;">
        {"Nilai standar:" if idn else "Standard value:"}
        <b>{fmt(v_mps)} m/s</b>
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Browser simulator ----------
labels = {
    "position": "Posisi / Position",
    "elapsed": "Waktu berjalan / Elapsed time",
    "ready": "Siap / Ready",
    "running": "Berjalan / Running",
    "paused": "Dijeda / Paused",
    "complete": "Eksperimen selesai / Experiment complete",
    "play": "▶ Mulai / Play",
    "pause": "⏸ Jeda / Pause",
    "step": "👣 Step +1 detik",
    "reset": "↻ Reset",
    "formula": "Rumus / Formula",
    "reflection": (
        "Jika jarak tetap tetapi waktunya dibuat lebih lama, apakah objek akan lebih cepat atau lebih lambat?"
        if idn else
        "If the distance stays the same but the time becomes longer, will the object be faster or slower?"
    ),
}
payload = json.dumps({
    "distance_m": distance_m,
    "time_s": time_s,
    "speed_mps": v_mps,
    "distance_unit": d_unit,
    "labels": labels,
    "decimals": DISPLAY_DECIMALS,
})

html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:Arial,sans-serif; color:#0f172a; }}
.sim {{ border:1px solid #e2e8f0; border-radius:18px; background:#fff; padding:16px; }}
canvas {{ width:100%; height:330px; display:block; border-radius:14px; background:#f8fafc; }}
.controls {{ display:flex; gap:10px; flex-wrap:wrap; margin-top:14px; }}
button {{ border:0; border-radius:10px; padding:11px 16px; font-weight:700; cursor:pointer; background:#e2e8f0; color:#0f172a; }}
button.primary {{ background:#2563eb; color:white; }}
button:disabled {{ opacity:.45; cursor:not-allowed; }}
.readout {{ display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:12px; }}
.box {{ background:#f8fafc; border-radius:12px; padding:12px; }}
.big {{ font-size:22px; font-weight:800; }}
.status {{ margin-top:12px; padding:10px 12px; border-radius:10px; background:#eff6ff; }}
.reflection {{ margin-top:8px; padding:12px; border-radius:10px; background:#f8fafc; }}
</style>
</head>
<body>
<div class="sim">
<canvas id="track"></canvas>
<div class="controls">
  <button id="play" class="primary"></button>
  <button id="pause"></button>
  <button id="step"></button>
  <button id="reset"></button>
</div>
<div class="readout">
  <div class="box"><div id="posLabel"></div><div class="big" id="position">0.00 m</div></div>
  <div class="box"><div id="timeLabel"></div><div class="big" id="elapsed">0.00 s</div></div>
</div>
<div class="status" id="status"></div>
<div class="reflection">💡 <b>Think / Coba pikirkan:</b> <span id="reflection"></span></div>
</div>

<script>
const cfg = {payload};
const canvas = document.getElementById("track");
const ctx = canvas.getContext("2d");
const play = document.getElementById("play");
const pause = document.getElementById("pause");
const step = document.getElementById("step");
const reset = document.getElementById("reset");
const posLabel = document.getElementById("posLabel");
const timeLabel = document.getElementById("timeLabel");
const positionEl = document.getElementById("position");
const elapsedEl = document.getElementById("elapsed");
const statusEl = document.getElementById("status");
const reflection = document.getElementById("reflection");

play.textContent = cfg.labels.play;
pause.textContent = cfg.labels.pause;
step.textContent = cfg.labels.step;
reset.textContent = cfg.labels.reset;
posLabel.textContent = cfg.labels.position;
timeLabel.textContent = cfg.labels.elapsed;
reflection.textContent = cfg.labels.reflection;

let elapsed = 0;
let running = false;
let lastTimestamp = null;

function fmt(x) {{
  return Number(x).toFixed(cfg.decimals).replace(/\.?0+$/,"");
}}

function resizeCanvas() {{
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();
  canvas.width = Math.round(rect.width*dpr);
  canvas.height = Math.round(rect.height*dpr);
  ctx.setTransform(dpr,0,0,dpr,0,0);
  draw();
}}

function niceInterval(distance) {{
  const raw = distance/10;
  if(raw<=1) return 1;
  if(raw<=2) return 2;
  if(raw<=5) return 5;
  if(raw<=10) return 10;
  if(raw<=20) return 20;
  if(raw<=50) return 50;
  if(raw<=100) return 100;
  return Math.max(1,Math.round(raw/100)*100);
}}

function draw() {{
  const r = canvas.getBoundingClientRect();
  const w = r.width, h = r.height;
  ctx.clearRect(0,0,w,h);

  const left=55, right=w-55, y=h*0.55;
  const ratio=Math.min(1,Math.max(0,elapsed/cfg.time_s));
  const x=left+ratio*(right-left);

  // Track
  ctx.strokeStyle="#334155"; ctx.lineWidth=5;
  ctx.beginPath(); ctx.moveTo(left,y); ctx.lineTo(right,y); ctx.stroke();

  // Progress
  ctx.strokeStyle="#2563eb"; ctx.lineWidth=7;
  ctx.beginPath(); ctx.moveTo(left,y); ctx.lineTo(x,y); ctx.stroke();

  // Distance markers
  const interval=niceInterval(cfg.distance_m);
  const n=Math.floor(cfg.distance_m/interval);
  ctx.font="12px Arial"; ctx.textAlign="center";
  for(let i=0;i<=n;i++) {{
    const d=Math.min(i*interval,cfg.distance_m);
    const xx=left+(d/cfg.distance_m)*(right-left);
    ctx.strokeStyle="#64748b"; ctx.lineWidth=1;
    ctx.beginPath(); ctx.moveTo(xx,y-10); ctx.lineTo(xx,y+10); ctx.stroke();
    ctx.fillStyle="#475569"; ctx.fillText(fmt(d)+" m",xx,y+32);
  }}

  // Finish
  ctx.strokeStyle="#0f172a"; ctx.lineWidth=2;
  ctx.beginPath(); ctx.moveTo(right,y-35); ctx.lineTo(right,y+35); ctx.stroke();
  ctx.fillStyle="#0f172a"; ctx.fillText("FINISH",right,y-47);

  // Trail
  for(let k=1;k<=8;k++) {{
    const tr=Math.max(0,ratio-k*0.025);
    const tx=left+tr*(right-left);
    ctx.fillStyle=`rgba(37,99,235,${Math.max(0.05,0.32-k*0.03)})`;
    ctx.beginPath(); ctx.arc(tx,y,3,0,Math.PI*2); ctx.fill();
  }}

  // Object
  ctx.fillStyle="#2563eb"; ctx.strokeStyle="#1e3a8a"; ctx.lineWidth=2;
  ctx.beginPath(); ctx.arc(x,y,15,0,Math.PI*2); ctx.fill(); ctx.stroke();

  const currentPosition=cfg.speed_mps*elapsed;
  positionEl.textContent=fmt(currentPosition)+" m";
  elapsedEl.textContent=fmt(elapsed)+" s";
}}

function statusText() {{
  if(running) return cfg.labels.running;
  if(elapsed>=cfg.time_s) return cfg.labels.complete;
  if(elapsed>0) return cfg.labels.paused;
  return cfg.labels.ready;
}}

function updateControls() {{
  statusEl.textContent=statusText();
  pause.disabled=!running;
  play.disabled=running || elapsed>=cfg.time_s;
  step.disabled=running || elapsed>=cfg.time_s;
}}

function frame(timestamp) {{
  if(!running) return;
  if(lastTimestamp===null) lastTimestamp=timestamp;
  const dt=(timestamp-lastTimestamp)/1000;
  lastTimestamp=timestamp;
  elapsed=Math.min(cfg.time_s,elapsed+dt);
  draw();
  updateControls();

  if(elapsed>=cfg.time_s) {{
    elapsed=cfg.time_s;
    running=false;
    lastTimestamp=null;
    draw();
    updateControls();
    return;
  }}
  requestAnimationFrame(frame);
}}

play.onclick=()=>{{
  if(elapsed>=cfg.time_s) elapsed=0;
  running=true; lastTimestamp=null; updateControls();
  requestAnimationFrame(frame);
}};
pause.onclick=()=>{{
  running=false; lastTimestamp=null; updateControls(); draw();
}};
step.onclick=()=>{{
  elapsed=Math.min(cfg.time_s,elapsed+1);
  draw(); updateControls();
}};
reset.onclick=()=>{{
  running=false; lastTimestamp=null; elapsed=0;
  draw(); updateControls();
}};

window.addEventListener("resize",resizeCanvas);
resizeCanvas();
draw();
updateControls();
</script>
</body>
</html>
"""

# st.components.v1.html is intentionally used for a self-contained browser animation.
components.html(html, height=560, scrolling=False)

# ---------- Explanation ----------
st.subheader("📘 " + ("Penjelasan" if idn else "Explanation"))
st.info(
    (
        f"Objek menempuh {fmt(distance)} {d_unit} dalam {fmt(time_value)} {t_unit}. "
        f"Kecepatannya adalah {fmt(v_selected)} {d_unit}/{t_unit} "
        f"atau {fmt(v_mps)} m/s."
        if idn else
        f"The object covers {fmt(distance)} {d_unit} in {fmt(time_value)} {t_unit}. "
        f"Its speed is {fmt(v_selected)} {d_unit}/{t_unit} "
        f"or {fmt(v_mps)} m/s."
    )
)

with st.expander("🧪 " + ("Contoh eksperimen" if idn else "Experiment ideas")):
    st.markdown(
        """
        1. **Keep time fixed, increase distance.** Observe what happens to speed.
        2. **Keep distance fixed, increase time.** Observe what happens to speed.
        3. **Use Step +1 second.** Predict the position before pressing Step.
        4. Compare `36 km/h` with `10 m/s`.
        """ if not idn else """
        1. **Pertahankan waktu, naikkan jarak.** Amati perubahan kecepatan.
        2. **Pertahankan jarak, naikkan waktu.** Amati perubahan kecepatan.
        3. **Gunakan Step +1 detik.** Prediksi posisi sebelum menekan Step.
        4. Bandingkan `36 km/h` dengan `10 m/s`.
        """
    )
