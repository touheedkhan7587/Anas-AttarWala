
/* ── CUSTOM CURSOR ─────────────────────────── */
const cur = document.getElementById("cur");
if (cur) {
  document.addEventListener("mousemove", e => {
    cur.style.left = e.clientX + "px";
    cur.style.top  = e.clientY + "px";
  });
}

/* ── PARTICLE CANVAS ───────────────────────── */
const canvas = document.getElementById("canvas");
if (canvas) {
  const ctx = canvas.getContext("2d");
  let W, H;

  const resize = () => {
    W = canvas.width  = window.innerWidth;
    H = canvas.height = window.innerHeight;
  };
  resize();
  window.addEventListener("resize", resize);

  class P {
    constructor() { this.reset(true); }
    reset(init) {
      this.x  = Math.random() * W;
      this.y  = init ? Math.random() * H : H + 4;
      this.r  = Math.random() * 1.4 + 0.3;
      this.vx = (Math.random() - 0.5) * 0.25;
      this.vy = -(Math.random() * 0.45 + 0.12);
      this.a  = Math.random() * 0.5 + 0.08;
      this.h  = Math.random() < 0.65 ? 44 : 33;
    }
    update() {
      this.x += this.vx;
      this.y += this.vy;
      if (this.y < -5 || this.x < -5 || this.x > W + 5) this.reset(false);
    }
    draw() {
      ctx.save();
      ctx.globalAlpha = this.a;
      ctx.fillStyle   = `hsl(${this.h},88%,64%)`;
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }
  }

  const ps = Array.from({ length: 90 }, () => new P());

  (function loop() {
    ctx.clearRect(0, 0, W, H);
    ps.forEach(p => { p.update(); p.draw(); });
    requestAnimationFrame(loop);
  })();

  /* Orb parallax */
  const bg = document.querySelector(".bg");
  document.addEventListener("mousemove", e => {
    const dx = (e.clientX / window.innerWidth  - 0.5) * 40;
    const dy = (e.clientY / window.innerHeight - 0.5) * 30;
    if (bg) bg.style.transform = `translate(${dx * 0.4}px, ${dy * 0.3}px) scale(1.02)`;
  });
}

/* ── LIVE COUNTDOWN ─────────────────────────── */
const elD = document.getElementById("d");
const elH = document.getElementById("h");
const elM = document.getElementById("m");
const elS = document.getElementById("s");

const launchDate = new Date("2026-06-01T00:00:00");

function pad(n) { return String(n).padStart(2, "0"); }

function flip(el, val) {
  if (!el) return;
  const v = pad(val);
  if (el.textContent === v) return;
  el.style.transform  = "translateY(-10px)";
  el.style.opacity    = "0";
  el.style.transition = "transform .18s ease,opacity .18s ease";
  setTimeout(() => {
    el.textContent      = v;
    el.style.transition = "none";
    el.style.transform  = "translateY(10px)";
    el.style.opacity    = "0";
    requestAnimationFrame(() => requestAnimationFrame(() => {
      el.style.transition = "transform .3s ease,opacity .3s ease";
      el.style.transform  = "translateY(0)";
      el.style.opacity    = "1";
    }));
  }, 190);
}

function tick() {
  const diff = launchDate - Date.now();
  if (diff <= 0) {
    [elD, elH, elM, elS].forEach(e => { if (e) e.textContent = "00"; });
    return;
  }
  flip(elD, Math.floor(diff / 86400000));
  flip(elH, Math.floor((diff % 86400000) / 3600000));
  flip(elM, Math.floor((diff % 3600000)  / 60000));
  flip(elS, Math.floor((diff % 60000)    / 1000));
}
tick();
setInterval(tick, 1000);
