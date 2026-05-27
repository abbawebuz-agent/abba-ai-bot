var __defProp = Object.defineProperty;
var __defProps = Object.defineProperties;
var __getOwnPropDescs = Object.getOwnPropertyDescriptors;
var __getOwnPropSymbols = Object.getOwnPropertySymbols;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __propIsEnum = Object.prototype.propertyIsEnumerable;
var __defNormalProp = (obj, key, value) => key in obj ? __defProp(obj, key, { enumerable: true, configurable: true, writable: true, value }) : obj[key] = value;
var __spreadValues = (a, b) => {
  for (var prop in b || (b = {}))
    if (__hasOwnProp.call(b, prop))
      __defNormalProp(a, prop, b[prop]);
  if (__getOwnPropSymbols)
    for (var prop of __getOwnPropSymbols(b)) {
      if (__propIsEnum.call(b, prop))
        __defNormalProp(a, prop, b[prop]);
    }
  return a;
};
var __spreadProps = (a, b) => __defProps(a, __getOwnPropDescs(b));
var __objRest = (source, exclude) => {
  var target = {};
  for (var prop in source)
    if (__hasOwnProp.call(source, prop) && exclude.indexOf(prop) < 0)
      target[prop] = source[prop];
  if (source != null && __getOwnPropSymbols)
    for (var prop of __getOwnPropSymbols(source)) {
      if (exclude.indexOf(prop) < 0 && __propIsEnum.call(source, prop))
        target[prop] = source[prop];
    }
  return target;
};
const __TWEAKS_STYLE = `
  .twk-panel{position:fixed;right:16px;bottom:16px;z-index:2147483646;width:280px;
    max-height:calc(100vh - 32px);display:flex;flex-direction:column;
    transform:scale(var(--dc-inv-zoom,1));transform-origin:bottom right;
    background:rgba(250,249,247,.78);color:#29261b;
    -webkit-backdrop-filter:blur(24px) saturate(160%);backdrop-filter:blur(24px) saturate(160%);
    border:.5px solid rgba(255,255,255,.6);border-radius:14px;
    box-shadow:0 1px 0 rgba(255,255,255,.5) inset,0 12px 40px rgba(0,0,0,.18);
    font:11.5px/1.4 ui-sans-serif,system-ui,-apple-system,sans-serif;overflow:hidden}
  .twk-hd{display:flex;align-items:center;justify-content:space-between;
    padding:10px 8px 10px 14px;cursor:move;user-select:none}
  .twk-hd b{font-size:12px;font-weight:600;letter-spacing:.01em}
  .twk-x{appearance:none;border:0;background:transparent;color:rgba(41,38,27,.55);
    width:22px;height:22px;border-radius:6px;cursor:default;font-size:13px;line-height:1}
  .twk-x:hover{background:rgba(0,0,0,.06);color:#29261b}
  .twk-body{padding:2px 14px 14px;display:flex;flex-direction:column;gap:10px;
    overflow-y:auto;overflow-x:hidden;min-height:0;
    scrollbar-width:thin;scrollbar-color:rgba(0,0,0,.15) transparent}
  .twk-body::-webkit-scrollbar{width:8px}
  .twk-body::-webkit-scrollbar-track{background:transparent;margin:2px}
  .twk-body::-webkit-scrollbar-thumb{background:rgba(0,0,0,.15);border-radius:4px;
    border:2px solid transparent;background-clip:content-box}
  .twk-body::-webkit-scrollbar-thumb:hover{background:rgba(0,0,0,.25);
    border:2px solid transparent;background-clip:content-box}
  .twk-row{display:flex;flex-direction:column;gap:5px}
  .twk-row-h{flex-direction:row;align-items:center;justify-content:space-between;gap:10px}
  .twk-lbl{display:flex;justify-content:space-between;align-items:baseline;
    color:rgba(41,38,27,.72)}
  .twk-lbl>span:first-child{font-weight:500}
  .twk-val{color:rgba(41,38,27,.5);font-variant-numeric:tabular-nums}

  .twk-sect{font-size:10px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;
    color:rgba(41,38,27,.45);padding:10px 0 0}
  .twk-sect:first-child{padding-top:0}

  .twk-field{appearance:none;box-sizing:border-box;width:100%;min-width:0;height:26px;padding:0 8px;
    border:.5px solid rgba(0,0,0,.1);border-radius:7px;
    background:rgba(255,255,255,.6);color:inherit;font:inherit;outline:none}
  .twk-field:focus{border-color:rgba(0,0,0,.25);background:rgba(255,255,255,.85)}
  select.twk-field{padding-right:22px;
    background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6'><path fill='rgba(0,0,0,.5)' d='M0 0h10L5 6z'/></svg>");
    background-repeat:no-repeat;background-position:right 8px center}

  .twk-slider{appearance:none;-webkit-appearance:none;width:100%;height:4px;margin:6px 0;
    border-radius:999px;background:rgba(0,0,0,.12);outline:none}
  .twk-slider::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;
    width:14px;height:14px;border-radius:50%;background:#fff;
    border:.5px solid rgba(0,0,0,.12);box-shadow:0 1px 3px rgba(0,0,0,.2);cursor:default}
  .twk-slider::-moz-range-thumb{width:14px;height:14px;border-radius:50%;
    background:#fff;border:.5px solid rgba(0,0,0,.12);box-shadow:0 1px 3px rgba(0,0,0,.2);cursor:default}

  .twk-seg{position:relative;display:flex;padding:2px;border-radius:8px;
    background:rgba(0,0,0,.06);user-select:none}
  .twk-seg-thumb{position:absolute;top:2px;bottom:2px;border-radius:6px;
    background:rgba(255,255,255,.9);box-shadow:0 1px 2px rgba(0,0,0,.12);
    transition:left .15s cubic-bezier(.3,.7,.4,1),width .15s}
  .twk-seg.dragging .twk-seg-thumb{transition:none}
  .twk-seg button{appearance:none;position:relative;z-index:1;flex:1;border:0;
    background:transparent;color:inherit;font:inherit;font-weight:500;min-height:22px;
    border-radius:6px;cursor:default;padding:4px 6px;line-height:1.2;
    overflow-wrap:anywhere}

  .twk-toggle{position:relative;width:32px;height:18px;border:0;border-radius:999px;
    background:rgba(0,0,0,.15);transition:background .15s;cursor:default;padding:0}
  .twk-toggle[data-on="1"]{background:#34c759}
  .twk-toggle i{position:absolute;top:2px;left:2px;width:14px;height:14px;border-radius:50%;
    background:#fff;box-shadow:0 1px 2px rgba(0,0,0,.25);transition:transform .15s}
  .twk-toggle[data-on="1"] i{transform:translateX(14px)}

  .twk-num{display:flex;align-items:center;box-sizing:border-box;min-width:0;height:26px;padding:0 0 0 8px;
    border:.5px solid rgba(0,0,0,.1);border-radius:7px;background:rgba(255,255,255,.6)}
  .twk-num-lbl{font-weight:500;color:rgba(41,38,27,.6);cursor:ew-resize;
    user-select:none;padding-right:8px}
  .twk-num input{flex:1;min-width:0;height:100%;border:0;background:transparent;
    font:inherit;font-variant-numeric:tabular-nums;text-align:right;padding:0 8px 0 0;
    outline:none;color:inherit;-moz-appearance:textfield}
  .twk-num input::-webkit-inner-spin-button,.twk-num input::-webkit-outer-spin-button{
    -webkit-appearance:none;margin:0}
  .twk-num-unit{padding-right:8px;color:rgba(41,38,27,.45)}

  .twk-btn{appearance:none;height:26px;padding:0 12px;border:0;border-radius:7px;
    background:rgba(0,0,0,.78);color:#fff;font:inherit;font-weight:500;cursor:default}
  .twk-btn:hover{background:rgba(0,0,0,.88)}
  .twk-btn.secondary{background:rgba(0,0,0,.06);color:inherit}
  .twk-btn.secondary:hover{background:rgba(0,0,0,.1)}

  .twk-swatch{appearance:none;-webkit-appearance:none;width:56px;height:22px;
    border:.5px solid rgba(0,0,0,.1);border-radius:6px;padding:0;cursor:default;
    background:transparent;flex-shrink:0}
  .twk-swatch::-webkit-color-swatch-wrapper{padding:0}
  .twk-swatch::-webkit-color-swatch{border:0;border-radius:5.5px}
  .twk-swatch::-moz-color-swatch{border:0;border-radius:5.5px}

  .twk-chips{display:flex;gap:6px}
  .twk-chip{position:relative;appearance:none;flex:1;min-width:0;height:46px;
    padding:0;border:0;border-radius:6px;overflow:hidden;cursor:default;
    box-shadow:0 0 0 .5px rgba(0,0,0,.12),0 1px 2px rgba(0,0,0,.06);
    transition:transform .12s cubic-bezier(.3,.7,.4,1),box-shadow .12s}
  .twk-chip:hover{transform:translateY(-1px);
    box-shadow:0 0 0 .5px rgba(0,0,0,.18),0 4px 10px rgba(0,0,0,.12)}
  .twk-chip[data-on="1"]{box-shadow:0 0 0 1.5px rgba(0,0,0,.85),
    0 2px 6px rgba(0,0,0,.15)}
  .twk-chip>span{position:absolute;top:0;bottom:0;right:0;width:34%;
    display:flex;flex-direction:column;box-shadow:-1px 0 0 rgba(0,0,0,.1)}
  .twk-chip>span>i{flex:1;box-shadow:0 -1px 0 rgba(0,0,0,.1)}
  .twk-chip>span>i:first-child{box-shadow:none}
  .twk-chip svg{position:absolute;top:6px;left:6px;width:13px;height:13px;
    filter:drop-shadow(0 1px 1px rgba(0,0,0,.3))}
`;
function useTweaks(defaults) {
  const [values, setValues] = React.useState(defaults);
  const setTweak = React.useCallback((keyOrEdits, val) => {
    const edits = typeof keyOrEdits === "object" && keyOrEdits !== null ? keyOrEdits : { [keyOrEdits]: val };
    setValues((prev) => __spreadValues(__spreadValues({}, prev), edits));
    window.parent.postMessage({ type: "__edit_mode_set_keys", edits }, "*");
    window.dispatchEvent(new CustomEvent("tweakchange", { detail: edits }));
  }, []);
  return [values, setTweak];
}
function TweaksPanel({ title = "Tweaks", children }) {
  const [open, setOpen] = React.useState(false);
  const dragRef = React.useRef(null);
  const offsetRef = React.useRef({ x: 16, y: 16 });
  const PAD = 16;
  const clampToViewport = React.useCallback(() => {
    const panel = dragRef.current;
    if (!panel) return;
    const w = panel.offsetWidth, h = panel.offsetHeight;
    const maxRight = Math.max(PAD, window.innerWidth - w - PAD);
    const maxBottom = Math.max(PAD, window.innerHeight - h - PAD);
    offsetRef.current = {
      x: Math.min(maxRight, Math.max(PAD, offsetRef.current.x)),
      y: Math.min(maxBottom, Math.max(PAD, offsetRef.current.y))
    };
    panel.style.right = offsetRef.current.x + "px";
    panel.style.bottom = offsetRef.current.y + "px";
  }, []);
  React.useEffect(() => {
    if (!open) return;
    clampToViewport();
    if (typeof ResizeObserver === "undefined") {
      window.addEventListener("resize", clampToViewport);
      return () => window.removeEventListener("resize", clampToViewport);
    }
    const ro = new ResizeObserver(clampToViewport);
    ro.observe(document.documentElement);
    return () => ro.disconnect();
  }, [open, clampToViewport]);
  React.useEffect(() => {
    const onMsg = (e) => {
      var _a;
      const t = (_a = e == null ? void 0 : e.data) == null ? void 0 : _a.type;
      if (t === "__activate_edit_mode") setOpen(true);
      else if (t === "__deactivate_edit_mode") setOpen(false);
    };
    window.addEventListener("message", onMsg);
    window.parent.postMessage({ type: "__edit_mode_available" }, "*");
    return () => window.removeEventListener("message", onMsg);
  }, []);
  const dismiss = () => {
    setOpen(false);
    window.parent.postMessage({ type: "__edit_mode_dismissed" }, "*");
  };
  const onDragStart = (e) => {
    const panel = dragRef.current;
    if (!panel) return;
    const r = panel.getBoundingClientRect();
    const sx = e.clientX, sy = e.clientY;
    const startRight = window.innerWidth - r.right;
    const startBottom = window.innerHeight - r.bottom;
    const move = (ev) => {
      offsetRef.current = {
        x: startRight - (ev.clientX - sx),
        y: startBottom - (ev.clientY - sy)
      };
      clampToViewport();
    };
    const up = () => {
      window.removeEventListener("mousemove", move);
      window.removeEventListener("mouseup", up);
    };
    window.addEventListener("mousemove", move);
    window.addEventListener("mouseup", up);
  };
  if (!open) return null;
  return /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("style", null, __TWEAKS_STYLE), /* @__PURE__ */ React.createElement(
    "div",
    {
      ref: dragRef,
      className: "twk-panel",
      "data-omelette-chrome": "",
      style: { right: offsetRef.current.x, bottom: offsetRef.current.y }
    },
    /* @__PURE__ */ React.createElement("div", { className: "twk-hd", onMouseDown: onDragStart }, /* @__PURE__ */ React.createElement("b", null, title), /* @__PURE__ */ React.createElement(
      "button",
      {
        className: "twk-x",
        "aria-label": "Close tweaks",
        onMouseDown: (e) => e.stopPropagation(),
        onClick: dismiss
      },
      "\u2715"
    )),
    /* @__PURE__ */ React.createElement("div", { className: "twk-body" }, children)
  ));
}
function TweakSection({ label, children }) {
  return /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("div", { className: "twk-sect" }, label), children);
}
function TweakRow({ label, value, children, inline = false }) {
  return /* @__PURE__ */ React.createElement("div", { className: inline ? "twk-row twk-row-h" : "twk-row" }, /* @__PURE__ */ React.createElement("div", { className: "twk-lbl" }, /* @__PURE__ */ React.createElement("span", null, label), value != null && /* @__PURE__ */ React.createElement("span", { className: "twk-val" }, value)), children);
}
function TweakSlider({ label, value, min = 0, max = 100, step = 1, unit = "", onChange }) {
  return /* @__PURE__ */ React.createElement(TweakRow, { label, value: `${value}${unit}` }, /* @__PURE__ */ React.createElement(
    "input",
    {
      type: "range",
      className: "twk-slider",
      min,
      max,
      step,
      value,
      onChange: (e) => onChange(Number(e.target.value))
    }
  ));
}
function TweakToggle({ label, value, onChange }) {
  return /* @__PURE__ */ React.createElement("div", { className: "twk-row twk-row-h" }, /* @__PURE__ */ React.createElement("div", { className: "twk-lbl" }, /* @__PURE__ */ React.createElement("span", null, label)), /* @__PURE__ */ React.createElement(
    "button",
    {
      type: "button",
      className: "twk-toggle",
      "data-on": value ? "1" : "0",
      role: "switch",
      "aria-checked": !!value,
      onClick: () => onChange(!value)
    },
    /* @__PURE__ */ React.createElement("i", null)
  ));
}
function TweakRadio({ label, value, options, onChange }) {
  var _a;
  const trackRef = React.useRef(null);
  const [dragging, setDragging] = React.useState(false);
  const valueRef = React.useRef(value);
  valueRef.current = value;
  const labelLen = (o) => String(typeof o === "object" ? o.label : o).length;
  const maxLen = options.reduce((m, o) => Math.max(m, labelLen(o)), 0);
  const fitsAsSegments = maxLen <= ((_a = { 2: 16, 3: 10 }[options.length]) != null ? _a : 0);
  if (!fitsAsSegments) {
    const resolve = (s) => {
      const m = options.find((o) => String(typeof o === "object" ? o.value : o) === s);
      return m === void 0 ? s : typeof m === "object" ? m.value : m;
    };
    return /* @__PURE__ */ React.createElement(
      TweakSelect,
      {
        label,
        value,
        options,
        onChange: (s) => onChange(resolve(s))
      }
    );
  }
  const opts = options.map((o) => typeof o === "object" ? o : { value: o, label: o });
  const idx = Math.max(0, opts.findIndex((o) => o.value === value));
  const n = opts.length;
  const segAt = (clientX) => {
    const r = trackRef.current.getBoundingClientRect();
    const inner = r.width - 4;
    const i = Math.floor((clientX - r.left - 2) / inner * n);
    return opts[Math.max(0, Math.min(n - 1, i))].value;
  };
  const onPointerDown = (e) => {
    setDragging(true);
    const v0 = segAt(e.clientX);
    if (v0 !== valueRef.current) onChange(v0);
    const move = (ev) => {
      if (!trackRef.current) return;
      const v = segAt(ev.clientX);
      if (v !== valueRef.current) onChange(v);
    };
    const up = () => {
      setDragging(false);
      window.removeEventListener("pointermove", move);
      window.removeEventListener("pointerup", up);
    };
    window.addEventListener("pointermove", move);
    window.addEventListener("pointerup", up);
  };
  return /* @__PURE__ */ React.createElement(TweakRow, { label }, /* @__PURE__ */ React.createElement(
    "div",
    {
      ref: trackRef,
      role: "radiogroup",
      onPointerDown,
      className: dragging ? "twk-seg dragging" : "twk-seg"
    },
    /* @__PURE__ */ React.createElement(
      "div",
      {
        className: "twk-seg-thumb",
        style: {
          left: `calc(2px + ${idx} * (100% - 4px) / ${n})`,
          width: `calc((100% - 4px) / ${n})`
        }
      }
    ),
    opts.map((o) => /* @__PURE__ */ React.createElement("button", { key: o.value, type: "button", role: "radio", "aria-checked": o.value === value }, o.label))
  ));
}
function TweakSelect({ label, value, options, onChange }) {
  return /* @__PURE__ */ React.createElement(TweakRow, { label }, /* @__PURE__ */ React.createElement("select", { className: "twk-field", value, onChange: (e) => onChange(e.target.value) }, options.map((o) => {
    const v = typeof o === "object" ? o.value : o;
    const l = typeof o === "object" ? o.label : o;
    return /* @__PURE__ */ React.createElement("option", { key: v, value: v }, l);
  })));
}
function TweakText({ label, value, placeholder, onChange }) {
  return /* @__PURE__ */ React.createElement(TweakRow, { label }, /* @__PURE__ */ React.createElement(
    "input",
    {
      className: "twk-field",
      type: "text",
      value,
      placeholder,
      onChange: (e) => onChange(e.target.value)
    }
  ));
}
function TweakNumber({ label, value, min, max, step = 1, unit = "", onChange }) {
  const clamp = (n) => {
    if (min != null && n < min) return min;
    if (max != null && n > max) return max;
    return n;
  };
  const startRef = React.useRef({ x: 0, val: 0 });
  const onScrubStart = (e) => {
    e.preventDefault();
    startRef.current = { x: e.clientX, val: value };
    const decimals = (String(step).split(".")[1] || "").length;
    const move = (ev) => {
      const dx = ev.clientX - startRef.current.x;
      const raw = startRef.current.val + dx * step;
      const snapped = Math.round(raw / step) * step;
      onChange(clamp(Number(snapped.toFixed(decimals))));
    };
    const up = () => {
      window.removeEventListener("pointermove", move);
      window.removeEventListener("pointerup", up);
    };
    window.addEventListener("pointermove", move);
    window.addEventListener("pointerup", up);
  };
  return /* @__PURE__ */ React.createElement("div", { className: "twk-num" }, /* @__PURE__ */ React.createElement("span", { className: "twk-num-lbl", onPointerDown: onScrubStart }, label), /* @__PURE__ */ React.createElement(
    "input",
    {
      type: "number",
      value,
      min,
      max,
      step,
      onChange: (e) => onChange(clamp(Number(e.target.value)))
    }
  ), unit && /* @__PURE__ */ React.createElement("span", { className: "twk-num-unit" }, unit));
}
function __twkIsLight(hex) {
  const h = String(hex).replace("#", "");
  const x = h.length === 3 ? h.replace(/./g, (c) => c + c) : h.padEnd(6, "0");
  const n = parseInt(x.slice(0, 6), 16);
  if (Number.isNaN(n)) return true;
  const r = n >> 16 & 255, g = n >> 8 & 255, b = n & 255;
  return r * 299 + g * 587 + b * 114 > 148e3;
}
const __TwkCheck = ({ light }) => /* @__PURE__ */ React.createElement("svg", { viewBox: "0 0 14 14", "aria-hidden": "true" }, /* @__PURE__ */ React.createElement(
  "path",
  {
    d: "M3 7.2 5.8 10 11 4.2",
    fill: "none",
    strokeWidth: "2.2",
    strokeLinecap: "round",
    strokeLinejoin: "round",
    stroke: light ? "rgba(0,0,0,.78)" : "#fff"
  }
));
function TweakColor({ label, value, options, onChange }) {
  if (!options || !options.length) {
    return /* @__PURE__ */ React.createElement("div", { className: "twk-row twk-row-h" }, /* @__PURE__ */ React.createElement("div", { className: "twk-lbl" }, /* @__PURE__ */ React.createElement("span", null, label)), /* @__PURE__ */ React.createElement(
      "input",
      {
        type: "color",
        className: "twk-swatch",
        value,
        onChange: (e) => onChange(e.target.value)
      }
    ));
  }
  const key = (o) => String(JSON.stringify(o)).toLowerCase();
  const cur = key(value);
  return /* @__PURE__ */ React.createElement(TweakRow, { label }, /* @__PURE__ */ React.createElement("div", { className: "twk-chips", role: "radiogroup" }, options.map((o, i) => {
    const colors = Array.isArray(o) ? o : [o];
    const [hero, ...rest] = colors;
    const sup = rest.slice(0, 4);
    const on = key(o) === cur;
    return /* @__PURE__ */ React.createElement(
      "button",
      {
        key: i,
        type: "button",
        className: "twk-chip",
        role: "radio",
        "aria-checked": on,
        "data-on": on ? "1" : "0",
        "aria-label": colors.join(", "),
        title: colors.join(" \xB7 "),
        style: { background: hero },
        onClick: () => onChange(o)
      },
      sup.length > 0 && /* @__PURE__ */ React.createElement("span", null, sup.map((c, j) => /* @__PURE__ */ React.createElement("i", { key: j, style: { background: c } }))),
      on && /* @__PURE__ */ React.createElement(__TwkCheck, { light: __twkIsLight(hero) })
    );
  })));
}
function TweakButton({ label, onClick, secondary = false }) {
  return /* @__PURE__ */ React.createElement(
    "button",
    {
      type: "button",
      className: secondary ? "twk-btn secondary" : "twk-btn",
      onClick
    },
    label
  );
}
Object.assign(window, {
  useTweaks,
  TweaksPanel,
  TweakSection,
  TweakRow,
  TweakSlider,
  TweakToggle,
  TweakRadio,
  TweakSelect,
  TweakText,
  TweakNumber,
  TweakColor,
  TweakButton
});
const { useState, useEffect, useRef, useMemo, Fragment } = React;
function Icon({ name, size = 16, className = "", strokeWidth = 1.75 }) {
  const paths = {
    // navigation
    home: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M3 9.5L12 3l9 6.5V20a1 1 0 01-1 1h-5v-7H9v7H4a1 1 0 01-1-1V9.5z" })),
    users: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("circle", { cx: "9", cy: "8", r: "3.5" }), /* @__PURE__ */ React.createElement("path", { d: "M15 11a3 3 0 100-6" }), /* @__PURE__ */ React.createElement("path", { d: "M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6" }), /* @__PURE__ */ React.createElement("path", { d: "M16 14c2.5.4 5 2.3 5 6" })),
    user: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("circle", { cx: "12", cy: "8", r: "4" }), /* @__PURE__ */ React.createElement("path", { d: "M4 21c0-4.4 3.6-8 8-8s8 3.6 8 8" })),
    qrcode: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("rect", { x: "3", y: "3", width: "7", height: "7", rx: "1" }), /* @__PURE__ */ React.createElement("rect", { x: "14", y: "3", width: "7", height: "7", rx: "1" }), /* @__PURE__ */ React.createElement("rect", { x: "3", y: "14", width: "7", height: "7", rx: "1" }), /* @__PURE__ */ React.createElement("path", { d: "M14 14h3v3h-3zM20 14v3M14 20h3M20 20h1" })),
    box: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M21 8l-9-5-9 5 9 5 9-5z" }), /* @__PURE__ */ React.createElement("path", { d: "M3 8v8l9 5 9-5V8" }), /* @__PURE__ */ React.createElement("path", { d: "M12 13v8" })),
    store: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M3 9l1.5-5h15L21 9" }), /* @__PURE__ */ React.createElement("path", { d: "M3 9v11h18V9" }), /* @__PURE__ */ React.createElement("path", { d: "M3 9h18" }), /* @__PURE__ */ React.createElement("path", { d: "M9 21v-6h6v6" })),
    gift: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("rect", { x: "3", y: "8", width: "18", height: "4", rx: "1" }), /* @__PURE__ */ React.createElement("path", { d: "M5 12v9h14v-9" }), /* @__PURE__ */ React.createElement("path", { d: "M12 8v13" }), /* @__PURE__ */ React.createElement("path", { d: "M12 8c-3-1-5-3-3-5s4 1 3 5z" }), /* @__PURE__ */ React.createElement("path", { d: "M12 8c3-1 5-3 3-5s-4 1-3 5z" })),
    "gift-redeem": /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2v-7" }), /* @__PURE__ */ React.createElement("rect", { x: "2", y: "7", width: "20", height: "5", rx: "1" }), /* @__PURE__ */ React.createElement("path", { d: "M12 22V7" }), /* @__PURE__ */ React.createElement("path", { d: "M12 7c-3 0-6-2-6-4s3-2 6 4z" }), /* @__PURE__ */ React.createElement("path", { d: "M12 7c3 0 6-2 6-4s-3-2-6 4z" })),
    coin: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("circle", { cx: "12", cy: "12", r: "9" }), /* @__PURE__ */ React.createElement("path", { d: "M9 9.5C9 8 10 7 12 7s3 1 3 2.5-1.2 2-3 2.5-3 1-3 2.5S10 17 12 17s3-1 3-2.5" })),
    "credit-card": /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("rect", { x: "2", y: "5", width: "20", height: "14", rx: "2" }), /* @__PURE__ */ React.createElement("path", { d: "M2 10h20" }), /* @__PURE__ */ React.createElement("path", { d: "M6 15h4" })),
    "id-card": /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("rect", { x: "2", y: "5", width: "20", height: "14", rx: "2" }), /* @__PURE__ */ React.createElement("circle", { cx: "9", cy: "12", r: "2.5" }), /* @__PURE__ */ React.createElement("path", { d: "M14 10h5M14 13h5M14 16h3" })),
    video: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("rect", { x: "3", y: "6", width: "14", height: "12", rx: "2" }), /* @__PURE__ */ React.createElement("path", { d: "M17 10l5-3v10l-5-3" })),
    bell: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M12 3a6 6 0 016 6v4l2 3H4l2-3V9a6 6 0 016-6z" }), /* @__PURE__ */ React.createElement("path", { d: "M10 21a2 2 0 004 0" })),
    activity: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M3 12h4l3-8 4 16 3-8h4" })),
    radio: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("circle", { cx: "12", cy: "12", r: "2" }), /* @__PURE__ */ React.createElement("path", { d: "M16.24 7.76a6 6 0 010 8.49M7.76 7.76a6 6 0 000 8.49" }), /* @__PURE__ */ React.createElement("path", { d: "M19.07 4.93a10 10 0 010 14.14M4.93 4.93a10 10 0 000 14.14" })),
    send: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M22 2L11 13" }), /* @__PURE__ */ React.createElement("path", { d: "M22 2l-7 20-4-9-9-4z" })),
    phone: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M22 16.92v3a2 2 0 01-2.18 2 19.86 19.86 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.86 19.86 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72c.13.96.37 1.9.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.91.33 1.85.57 2.81.7A2 2 0 0122 16.92z" })),
    lock: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("rect", { x: "4", y: "11", width: "16", height: "10", rx: "2" }), /* @__PURE__ */ React.createElement("path", { d: "M8 11V7a4 4 0 018 0v4" })),
    shield: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" })),
    settings: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("circle", { cx: "12", cy: "12", r: "3" }), /* @__PURE__ */ React.createElement("path", { d: "M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 11-2.83 2.83l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 11-4 0v-.09a1.65 1.65 0 00-1-1.51 1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 11-2.83-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 110-4h.09a1.65 1.65 0 001.51-1 1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 112.83-2.83l.06.06a1.65 1.65 0 001.82.33h0a1.65 1.65 0 001-1.51V3a2 2 0 114 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 112.83 2.83l-.06.06a1.65 1.65 0 00-.33 1.82v0a1.65 1.65 0 001.51 1H21a2 2 0 110 4h-.09a1.65 1.65 0 00-1.51 1z" })),
    "bar-chart": /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M3 21V3" }), /* @__PURE__ */ React.createElement("path", { d: "M3 21h18" }), /* @__PURE__ */ React.createElement("rect", { x: "7", y: "13", width: "3", height: "5" }), /* @__PURE__ */ React.createElement("rect", { x: "12", y: "9", width: "3", height: "9" }), /* @__PURE__ */ React.createElement("rect", { x: "17", y: "5", width: "3", height: "13" })),
    // ui
    search: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("circle", { cx: "11", cy: "11", r: "7" }), /* @__PURE__ */ React.createElement("path", { d: "M21 21l-4.3-4.3" })),
    filter: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M3 4h18l-7 9v6l-4 2v-8z" })),
    plus: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M12 5v14M5 12h14" })),
    download: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" }), /* @__PURE__ */ React.createElement("path", { d: "M7 10l5 5 5-5" }), /* @__PURE__ */ React.createElement("path", { d: "M12 15V3" })),
    upload: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" }), /* @__PURE__ */ React.createElement("path", { d: "M17 8l-5-5-5 5" }), /* @__PURE__ */ React.createElement("path", { d: "M12 3v12" })),
    edit: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" }), /* @__PURE__ */ React.createElement("path", { d: "M18.5 2.5a2.12 2.12 0 113 3L12 15l-4 1 1-4 9.5-9.5z" })),
    eye: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" }), /* @__PURE__ */ React.createElement("circle", { cx: "12", cy: "12", r: "3" })),
    "eye-off": /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94" }), /* @__PURE__ */ React.createElement("path", { d: "M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19" }), /* @__PURE__ */ React.createElement("path", { d: "M14.12 14.12a3 3 0 11-4.24-4.24" }), /* @__PURE__ */ React.createElement("path", { d: "M1 1l22 22" })),
    check: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M20 6L9 17l-5-5" })),
    x: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M18 6L6 18M6 6l12 12" })),
    chevron: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M9 18l6-6-6-6" })),
    "chevron-down": /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M6 9l6 6 6-6" })),
    "chevron-up": /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M18 15l-6-6-6 6" })),
    "chevron-left": /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M15 18l-6-6 6-6" })),
    "chevron-right": /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M9 18l6-6-6-6" })),
    menu: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M3 6h18M3 12h18M3 18h18" })),
    plug: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M9 2v6M15 2v6M6 8h12v3a6 6 0 11-12 0z" }), /* @__PURE__ */ React.createElement("path", { d: "M12 17v5" })),
    history: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M3 12a9 9 0 109-9 9.74 9.74 0 00-7 3.16L3 8" }), /* @__PURE__ */ React.createElement("path", { d: "M3 3v5h5" }), /* @__PURE__ */ React.createElement("path", { d: "M12 7v5l4 2" })),
    clock: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("circle", { cx: "12", cy: "12", r: "9" }), /* @__PURE__ */ React.createElement("path", { d: "M12 7v5l3 2" })),
    map: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M3 6v15l6-3 6 3 6-3V3l-6 3-6-3-6 3z" }), /* @__PURE__ */ React.createElement("path", { d: "M9 3v15M15 6v15" })),
    "map-pin": /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z" }), /* @__PURE__ */ React.createElement("circle", { cx: "12", cy: "10", r: "3" })),
    layers: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M12 2l10 6-10 6L2 8z" }), /* @__PURE__ */ React.createElement("path", { d: "M2 14l10 6 10-6" }), /* @__PURE__ */ React.createElement("path", { d: "M2 18l10 6 10-6" })),
    sparkles: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M12 3l2 5 5 2-5 2-2 5-2-5-5-2 5-2z" }), /* @__PURE__ */ React.createElement("path", { d: "M19 17l1 2 2 1-2 1-1 2-1-2-2-1 2-1z" })),
    "message-circle": /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M21 12a9 9 0 11-3.94-7.43L21 3l-1.43 3.94A8.96 8.96 0 0121 12z" })),
    "message-square": /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M21 11.5a8.38 8.38 0 01-9 8.5 8.5 8.5 0 01-4-1l-5 1 1-5a8.5 8.5 0 014-9 8.38 8.38 0 019-1 8.5 8.5 0 014 9z" })),
    sliders: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3" }), /* @__PURE__ */ React.createElement("path", { d: "M1 14h6M9 8h6M17 16h6" })),
    "trending-up": /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M22 7l-9.5 9.5-5-5L1 18" }), /* @__PURE__ */ React.createElement("path", { d: "M16 7h6v6" })),
    "trending-down": /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M22 17l-9.5-9.5-5 5L1 6" }), /* @__PURE__ */ React.createElement("path", { d: "M16 17h6v-6" })),
    zap: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M13 2L3 14h7l-1 8 10-12h-7z" })),
    flame: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M14 7c-3 5-7 6-7 10a5 5 0 0010 0c0-3-2-4-3-7zM10 14a3 3 0 003 3" })),
    "arrow-right": /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M5 12h14M12 5l7 7-7 7" })),
    "arrow-up-right": /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M7 17L17 7M7 7h10v10" })),
    "more-horizontal": /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("circle", { cx: "5", cy: "12", r: "1" }), /* @__PURE__ */ React.createElement("circle", { cx: "12", cy: "12", r: "1" }), /* @__PURE__ */ React.createElement("circle", { cx: "19", cy: "12", r: "1" })),
    trash: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M3 6h18M8 6V4a1 1 0 011-1h6a1 1 0 011 1v2M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6" })),
    "file-text": /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M14 3H6a2 2 0 00-2 2v14a2 2 0 002 2h12a2 2 0 002-2V9z" }), /* @__PURE__ */ React.createElement("path", { d: "M14 3v6h6" }), /* @__PURE__ */ React.createElement("path", { d: "M8 13h8M8 17h8M8 9h2" })),
    archive: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("rect", { x: "2", y: "3", width: "20", height: "5", rx: "1" }), /* @__PURE__ */ React.createElement("path", { d: "M4 8v11a2 2 0 002 2h12a2 2 0 002-2V8" }), /* @__PURE__ */ React.createElement("path", { d: "M10 12h4" })),
    image: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("rect", { x: "3", y: "3", width: "18", height: "18", rx: "2" }), /* @__PURE__ */ React.createElement("circle", { cx: "9", cy: "9", r: "2" }), /* @__PURE__ */ React.createElement("path", { d: "M21 15l-5-5L5 21" })),
    calendar: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("rect", { x: "3", y: "4", width: "18", height: "18", rx: "2" }), /* @__PURE__ */ React.createElement("path", { d: "M16 2v4M8 2v4M3 10h18" })),
    "log-out": /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4" }), /* @__PURE__ */ React.createElement("path", { d: "M16 17l5-5-5-5M21 12H9" })),
    "help-circle": /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("circle", { cx: "12", cy: "12", r: "9" }), /* @__PURE__ */ React.createElement("path", { d: "M9.1 9a3 3 0 015.8 1c0 2-3 2-3 4" }), /* @__PURE__ */ React.createElement("circle", { cx: "12", cy: "17", r: "0.5" })),
    flag: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M4 22V4M4 4l14 4-6 5 6 4H4" })),
    "flag-uz": /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("rect", { x: "2", y: "6", width: "20", height: "12", rx: "1", fill: "#0099b5", stroke: "none" }), /* @__PURE__ */ React.createElement("rect", { x: "2", y: "9.7", width: "20", height: "4.6", fill: "#fff", stroke: "none" }), /* @__PURE__ */ React.createElement("rect", { x: "2", y: "11", width: "20", height: "2", fill: "#1eb53a", stroke: "none" })),
    "flag-ru": /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("rect", { x: "2", y: "6", width: "20", height: "4", fill: "#fff", stroke: "none" }), /* @__PURE__ */ React.createElement("rect", { x: "2", y: "10", width: "20", height: "4", fill: "#0039a6", stroke: "none" }), /* @__PURE__ */ React.createElement("rect", { x: "2", y: "14", width: "20", height: "4", fill: "#d52b1e", stroke: "none" })),
    play: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M5 3l14 9-14 9z" })),
    code: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M16 18l6-6-6-6M8 6l-6 6 6 6" })),
    "shopping-cart": /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("circle", { cx: "9", cy: "21", r: "1" }), /* @__PURE__ */ React.createElement("circle", { cx: "20", cy: "21", r: "1" }), /* @__PURE__ */ React.createElement("path", { d: "M1 1h4l2.7 13.4a2 2 0 002 1.6h9.7a2 2 0 002-1.6L23 6H6" })),
    wrench: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M14.7 6.3a4 4 0 00-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 005.4-5.4l-2.7 2.7-2.6-2.6z" })),
    sun: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("circle", { cx: "12", cy: "12", r: "4" }), /* @__PURE__ */ React.createElement("path", { d: "M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41" })),
    moon: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" }))
  };
  const path = paths[name];
  if (!path) return /* @__PURE__ */ React.createElement("span", { style: { display: "inline-block", width: size, height: size } });
  return /* @__PURE__ */ React.createElement(
    "svg",
    {
      width: size,
      height: size,
      viewBox: "0 0 24 24",
      fill: "none",
      stroke: "currentColor",
      strokeWidth,
      strokeLinecap: "round",
      strokeLinejoin: "round",
      className,
      style: { flexShrink: 0 }
    },
    path
  );
}
function Badge({ children, variant = "neutral", icon, dot, outline, size = "md" }) {
  const cls = ["badge", `badge-${variant}`, outline ? "badge-outline" : "", size === "sm" ? "badge-sm" : ""].join(" ");
  return /* @__PURE__ */ React.createElement("span", { className: cls }, dot && /* @__PURE__ */ React.createElement("span", { className: "badge-dot" }), icon && /* @__PURE__ */ React.createElement(Icon, { name: icon, size: 11 }), children);
}
const StatusBadges = {
  active: () => /* @__PURE__ */ React.createElement(Badge, { variant: "success", dot: true }, "\u0410\u043A\u0442\u0438\u0432\u0435\u043D"),
  inactive: () => /* @__PURE__ */ React.createElement(Badge, { variant: "neutral", dot: true }, "\u041D\u0435\u0430\u043A\u0442\u0438\u0432\u0435\u043D"),
  approved: () => /* @__PURE__ */ React.createElement(Badge, { variant: "success", icon: "check" }, "Tasdiqlangan"),
  pending: () => /* @__PURE__ */ React.createElement(Badge, { variant: "warning", icon: "clock" }, "Kutilmoqda"),
  cancelled: () => /* @__PURE__ */ React.createElement(Badge, { variant: "danger", icon: "x" }, "Bekor qilindi"),
  santenik: () => /* @__PURE__ */ React.createElement(Badge, { variant: "warning", icon: "wrench" }, "Santenik"),
  sotuvchi: () => /* @__PURE__ */ React.createElement(Badge, { variant: "info", icon: "store" }, "Sotuvchi"),
  scanned: () => /* @__PURE__ */ React.createElement(Badge, { variant: "success", icon: "check" }, "\u0418\u0441\u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u043D"),
  unscanned: () => /* @__PURE__ */ React.createElement(Badge, { variant: "warning", icon: "clock" }, "\u041D\u0435 \u0438\u0441\u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u043D"),
  langUz: () => /* @__PURE__ */ React.createElement(Badge, { variant: "neutral" }, /* @__PURE__ */ React.createElement(Icon, { name: "flag-uz", size: 11 }), "O'zbek"),
  langRu: () => /* @__PURE__ */ React.createElement(Badge, { variant: "neutral" }, /* @__PURE__ */ React.createElement(Icon, { name: "flag-ru", size: 11 }), "\u0420\u0443\u0441\u0441\u043A\u0438\u0439")
};
function Button({ variant = "secondary", size = "md", icon, children, onClick, type = "button", disabled }) {
  const cls = ["btn", `btn-${variant}`, size === "sm" ? "btn-sm" : size === "lg" ? "btn-lg" : ""].join(" ");
  return /* @__PURE__ */ React.createElement("button", { type, className: cls, onClick, disabled }, icon && /* @__PURE__ */ React.createElement(Icon, { name: icon, size: 14 }), children);
}
function Sparkline({ values = [], color = "#6366f1" }) {
  if (!values.length) return null;
  const max = Math.max(...values);
  const min = Math.min(...values);
  const w = 100;
  const h = 30;
  const points = values.map((v, i) => {
    const x = i / (values.length - 1) * w;
    const y = h - (v - min) / Math.max(max - min, 1) * h;
    return `${x},${y}`;
  }).join(" ");
  return /* @__PURE__ */ React.createElement("svg", { viewBox: `0 0 ${w} ${h}`, preserveAspectRatio: "none", className: "sparkline-svg" }, /* @__PURE__ */ React.createElement("defs", null, /* @__PURE__ */ React.createElement("linearGradient", { id: `spark-${color.replace("#", "")}`, x1: "0", x2: "0", y1: "0", y2: "1" }, /* @__PURE__ */ React.createElement("stop", { offset: "0%", stopColor: color, stopOpacity: "0.5" }), /* @__PURE__ */ React.createElement("stop", { offset: "100%", stopColor: color, stopOpacity: "0" }))), /* @__PURE__ */ React.createElement("polyline", { points, fill: "none", stroke: color, strokeWidth: "1.5", vectorEffect: "non-scaling-stroke" }), /* @__PURE__ */ React.createElement("polygon", { points: `0,${h} ${points} ${w},${h}`, fill: `url(#spark-${color.replace("#", "")})` }));
}
function KPI({ label, value, icon, delta, deltaDir = "up", hint, color = "indigo", spark, onClick }) {
  const colors = {
    indigo: { bg: "var(--primary-soft)", fg: "var(--primary)" },
    emerald: { bg: "var(--success-soft)", fg: "var(--success)" },
    amber: { bg: "var(--warning-soft)", fg: "var(--warning)" },
    rose: { bg: "var(--danger-soft)", fg: "var(--danger)" },
    blue: { bg: "var(--info-soft)", fg: "var(--info)" }
  };
  const c = colors[color];
  return /* @__PURE__ */ React.createElement("div", { className: "kpi", onClick, role: onClick ? "button" : void 0 }, /* @__PURE__ */ React.createElement("div", { className: "kpi-head" }, /* @__PURE__ */ React.createElement("span", { className: "kpi-label" }, label), /* @__PURE__ */ React.createElement("span", { className: "kpi-icon", style: { background: c.bg, color: c.fg } }, /* @__PURE__ */ React.createElement(Icon, { name: icon, size: 16 }))), /* @__PURE__ */ React.createElement("div", { className: "kpi-value" }, value), /* @__PURE__ */ React.createElement("div", { className: "kpi-meta" }, delta && /* @__PURE__ */ React.createElement("span", { className: deltaDir === "up" ? "delta-up" : "delta-down" }, /* @__PURE__ */ React.createElement(Icon, { name: deltaDir === "up" ? "trending-up" : "trending-down", size: 12 }), " ", delta), hint && /* @__PURE__ */ React.createElement("span", null, hint)), spark && /* @__PURE__ */ React.createElement("div", { className: "kpi-spark" }, /* @__PURE__ */ React.createElement(Sparkline, { values: spark, color: c.fg.startsWith("var(") ? "#6366f1" : c.fg })));
}
function Avatar({ name, size = 32, color }) {
  const initials = (name || "?").split(" ").map((s) => s[0]).slice(0, 2).join("").toUpperCase();
  const hash = (name || "").split("").reduce((a, c) => a + c.charCodeAt(0), 0);
  const gradients = [
    "linear-gradient(135deg, #6366f1, #4338ca)",
    "linear-gradient(135deg, #10b981, #047857)",
    "linear-gradient(135deg, #f59e0b, #d97706)",
    "linear-gradient(135deg, #ec4899, #9333ea)",
    "linear-gradient(135deg, #3b82f6, #1e40af)",
    "linear-gradient(135deg, #14b8a6, #0f766e)"
  ];
  return /* @__PURE__ */ React.createElement("div", { style: {
    width: size,
    height: size,
    borderRadius: 999,
    background: color || gradients[hash % gradients.length],
    display: "grid",
    placeItems: "center",
    color: "white",
    fontSize: size * 0.36,
    fontWeight: 600,
    flexShrink: 0
  } }, initials);
}
function PageHeader({ title, subtitle, actions }) {
  return /* @__PURE__ */ React.createElement("div", { className: "page-header" }, /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("h2", null, title), subtitle && /* @__PURE__ */ React.createElement("div", { className: "subtitle" }, subtitle)), actions && /* @__PURE__ */ React.createElement("div", { className: "page-actions" }, actions));
}
function FormBlock({ title, badge, children, single, icon }) {
  return /* @__PURE__ */ React.createElement("div", { className: "form-block" }, /* @__PURE__ */ React.createElement("div", { className: "form-block-header" }, icon && /* @__PURE__ */ React.createElement("span", { style: {
    width: 24,
    height: 24,
    display: "grid",
    placeItems: "center",
    borderRadius: 6,
    background: "var(--primary-soft)",
    color: "var(--primary)"
  } }, /* @__PURE__ */ React.createElement(Icon, { name: icon, size: 13 })), /* @__PURE__ */ React.createElement("h3", null, title), badge), /* @__PURE__ */ React.createElement("div", { className: "form-block-body" + (single ? " single" : "") }, children));
}
function Field({ label, hint, required, children, span2 }) {
  return /* @__PURE__ */ React.createElement("div", { className: "field" + (span2 ? " span-2" : "") }, label && /* @__PURE__ */ React.createElement("label", { className: "field-label" }, label, required && /* @__PURE__ */ React.createElement("span", { className: "req" }, "*")), children, hint && /* @__PURE__ */ React.createElement("span", { className: "field-hint" }, hint));
}
function Input(props) {
  return /* @__PURE__ */ React.createElement("input", __spreadValues({ className: "input" }, props));
}
function Textarea(props) {
  return /* @__PURE__ */ React.createElement("textarea", __spreadValues({ className: "textarea" }, props));
}
function Select(_a) {
  var _b = _a, { children } = _b, props = __objRest(_b, ["children"]);
  return /* @__PURE__ */ React.createElement("select", __spreadValues({ className: "select" }, props), children);
}
function Toggle({ on, onChange }) {
  return /* @__PURE__ */ React.createElement("button", { type: "button", className: "toggle" + (on ? " on" : ""), onClick: () => onChange(!on) });
}
function SearchBar({ placeholder = "\u041F\u043E\u0438\u0441\u043A...", value, onChange }) {
  return /* @__PURE__ */ React.createElement("div", { className: "input-group", style: { minWidth: 260, height: 32 } }, /* @__PURE__ */ React.createElement("span", { className: "prefix" }, /* @__PURE__ */ React.createElement(Icon, { name: "search", size: 14 })), /* @__PURE__ */ React.createElement("input", { className: "input", placeholder, value: value || "", onChange: (e) => onChange == null ? void 0 : onChange(e.target.value), style: { height: 30, fontSize: 13 } }));
}
function FilterChip({ active, onClick, children, icon }) {
  return /* @__PURE__ */ React.createElement("button", { className: "filter-chip" + (active ? " active" : ""), onClick }, icon && /* @__PURE__ */ React.createElement(Icon, { name: icon, size: 12 }), children, /* @__PURE__ */ React.createElement(Icon, { name: "chevron-down", size: 11 }));
}
function EmptyState({ icon = "box", title, hint }) {
  return /* @__PURE__ */ React.createElement("div", { className: "empty" }, /* @__PURE__ */ React.createElement("div", { className: "empty-icon" }, /* @__PURE__ */ React.createElement(Icon, { name: icon, size: 20 })), /* @__PURE__ */ React.createElement("h4", null, title), hint && /* @__PURE__ */ React.createElement("div", null, hint));
}
function Pagination({ total, page = 1, perPage = 25, onChange }) {
  const pages = Math.ceil(total / perPage);
  const start = (page - 1) * perPage + 1;
  const end = Math.min(page * perPage, total);
  return /* @__PURE__ */ React.createElement("div", { className: "pagination" }, /* @__PURE__ */ React.createElement("span", null, "\u041F\u043E\u043A\u0430\u0437\u0430\u043D\u043E ", /* @__PURE__ */ React.createElement("strong", null, start, "\u2013", end), " \u0438\u0437 ", /* @__PURE__ */ React.createElement("strong", null, total.toLocaleString("ru"))), /* @__PURE__ */ React.createElement("div", { className: "pager" }, /* @__PURE__ */ React.createElement("button", { className: "page-btn", onClick: () => onChange == null ? void 0 : onChange(Math.max(1, page - 1)) }, /* @__PURE__ */ React.createElement(Icon, { name: "chevron-left", size: 14 })), Array.from({ length: Math.min(5, pages) }, (_, i) => i + 1).map((p) => /* @__PURE__ */ React.createElement("button", { key: p, className: "page-btn" + (p === page ? " active" : ""), onClick: () => onChange == null ? void 0 : onChange(p) }, p)), pages > 5 && /* @__PURE__ */ React.createElement("span", { style: { padding: "0 6px", color: "var(--text-dim)" } }, "\u2026"), pages > 5 && /* @__PURE__ */ React.createElement("button", { className: "page-btn", onClick: () => onChange == null ? void 0 : onChange(pages) }, pages), /* @__PURE__ */ React.createElement("button", { className: "page-btn", onClick: () => onChange == null ? void 0 : onChange(Math.min(pages, page + 1)) }, /* @__PURE__ */ React.createElement(Icon, { name: "chevron-right", size: 14 }))));
}
function DateHierarchy({ items = ["2026", "\u041C\u0430\u0439", "22", "23", "25", "26"], active = 0 }) {
  return /* @__PURE__ */ React.createElement("div", { className: "date-strip" }, /* @__PURE__ */ React.createElement("span", { style: { marginRight: 8, color: "var(--text-dim)" } }, /* @__PURE__ */ React.createElement(Icon, { name: "calendar", size: 12 })), items.map((d, i) => /* @__PURE__ */ React.createElement("span", { key: i, className: "crumb-item" + (i === active ? " active" : "") }, d)));
}
function RecentActions({ items }) {
  return /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "card-header" }, /* @__PURE__ */ React.createElement("h3", null, "\u041F\u043E\u0441\u043B\u0435\u0434\u043D\u0438\u0435 \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u044F"), /* @__PURE__ */ React.createElement(Icon, { name: "activity", size: 14, className: "text-muted" })), /* @__PURE__ */ React.createElement("div", { style: { padding: "4px 0" } }, items.map((a, i) => /* @__PURE__ */ React.createElement(
    "div",
    {
      key: i,
      style: {
        padding: "10px 20px",
        borderBottom: i < items.length - 1 ? "1px solid var(--border)" : 0,
        display: "flex",
        flexDirection: "column",
        gap: 2,
        cursor: "pointer",
        transition: "background 100ms"
      },
      onMouseEnter: (e) => e.currentTarget.style.background = "rgba(255,255,255,0.02)",
      onMouseLeave: (e) => e.currentTarget.style.background = "transparent"
    },
    /* @__PURE__ */ React.createElement("div", { style: { fontSize: 13, color: "var(--text-strong)", fontWeight: 500 } }, a.object),
    /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "space-between", alignItems: "center", gap: 8 } }, /* @__PURE__ */ React.createElement("span", { style: { fontSize: 12, color: "var(--text-muted)" } }, a.action), /* @__PURE__ */ React.createElement("span", { style: { fontSize: 11, color: "var(--text-dim)", fontFamily: "var(--font-mono)" } }, a.time))
  ))));
}
function Modal({ open, title, onClose, children, footer, icon }) {
  if (!open) return null;
  return /* @__PURE__ */ React.createElement("div", { className: "modal-backdrop", onClick: onClose }, /* @__PURE__ */ React.createElement("div", { className: "modal", onClick: (e) => e.stopPropagation() }, /* @__PURE__ */ React.createElement("div", { className: "modal-header" }, icon && /* @__PURE__ */ React.createElement(Icon, { name: icon, size: 16, className: "text-muted" }), /* @__PURE__ */ React.createElement("h3", { style: { margin: 0, fontSize: 14, fontWeight: 600, color: "var(--text-strong)" } }, title), /* @__PURE__ */ React.createElement("button", { className: "icon-btn", style: { marginLeft: "auto", width: 28, height: 28 }, onClick: onClose }, /* @__PURE__ */ React.createElement(Icon, { name: "x", size: 14 }))), /* @__PURE__ */ React.createElement("div", { className: "modal-body" }, children), footer && /* @__PURE__ */ React.createElement("div", { className: "modal-footer" }, footer)));
}
Object.assign(window, {
  Icon,
  Badge,
  StatusBadges,
  Button,
  KPI,
  Sparkline,
  Avatar,
  PageHeader,
  FormBlock,
  Field,
  Input,
  Textarea,
  Select,
  Toggle,
  SearchBar,
  FilterChip,
  EmptyState,
  Pagination,
  DateHierarchy,
  RecentActions,
  Modal
});
const NAV_GROUPS = [
  {
    label: "Boshqaruv",
    items: [
      { route: "/dashboard", label: "Dashboard", icon: "home", count: null },
      { route: "/analytics", label: "\u0410\u043D\u0430\u043B\u0438\u0442\u0438\u043A\u0430", icon: "bar-chart", count: null }
    ]
  },
  {
    label: "Foydalanuvchilar",
    items: [
      { route: "/users", label: "Telegram users", icon: "users", count: 23 },
      { route: "/users/send-region", label: "Xabar (viloyat)", icon: "send", count: null },
      { route: "/users/send-single", label: "Xabar (single)", icon: "message-circle", count: null },
      { route: "/auth/users", label: "Admin users", icon: "user", count: 4 },
      { route: "/auth/groups", label: "Guruhlar", icon: "shield", count: 4 }
    ]
  },
  {
    label: "QR & \u041F\u0430\u0440\u0442\u0438\u0438",
    items: [
      { route: "/qrcodes", label: "QR kodlar", icon: "qrcode", count: 239 },
      { route: "/qrcodes/generate", label: "QR generatsiya", icon: "plus", count: null },
      { route: "/batches", label: "\u041F\u0430\u0440\u0442\u0438\u0438", icon: "box", count: 17 },
      { route: "/batches/add", label: "Yangi \u043F\u0430\u0440\u0442\u0438\u044F", icon: "plus", count: null },
      { route: "/stores", label: "Do'konlar", icon: "store", count: 12 }
    ]
  },
  {
    label: "Sovg'alar",
    items: [
      { route: "/gifts", label: "Sovg'alar katalogi", icon: "gift", count: 8 },
      { route: "/redemptions", label: "Sovg'a so'rovlari", icon: "gift-redeem", count: 15 }
    ]
  },
  {
    label: "Sotuvchilar",
    items: [
      { route: "/transactions", label: "Tranzaksiyalar", icon: "credit-card", count: 1117 },
      { route: "/seller-codes", label: "Sotuvchi ID lar", icon: "id-card", count: 25 }
    ]
  },
  {
    label: "Kontent",
    items: [
      { route: "/livestreams", label: "Jonli efirlar", icon: "radio", count: 4 },
      { route: "/videos", label: "Videolar", icon: "video", count: 5 },
      { route: "/privacy", label: "Maxfiylik", icon: "file-text", count: null }
    ]
  },
  {
    label: "Tizim",
    items: [
      { route: "/activity", label: "Faollik tarixi", icon: "history", count: 264 },
      { route: "/regionlog", label: "Viloyat logi", icon: "map", count: null },
      { route: "/monthly", label: "Oylik eslatma", icon: "bell", count: null },
      { route: "/monthly-log", label: "Eslatma logi", icon: "clock", count: null },
      { route: "/contacts", label: "Admin kontakt", icon: "phone", count: null }
    ]
  }
];
const PAGE_META = {
  "/dashboard": { title: "Dashboard", crumbs: ["Bosh", "Dashboard"] },
  "/analytics": { title: "\u0410\u043D\u0430\u043B\u0438\u0442\u0438\u043A\u0430", crumbs: ["Bosh", "\u0410\u043D\u0430\u043B\u0438\u0442\u0438\u043A\u0430"] },
  "/users": { title: "\u041F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u0435\u043B\u0438 Telegram", crumbs: ["Bosh", "Core", "Telegram \u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u0435\u043B\u0438"] },
  "/users/santenik": { title: "\u0421\u0430\u043D\u0442\u0435\u0445\u043D\u0438\u043A", crumbs: ["Bosh", "Core", "Telegram \u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u0435\u043B\u0438", "\u0418\u0437\u043C\u0435\u043D\u0438\u0442\u044C"] },
  "/users/sotuvchi": { title: "\u041F\u0440\u043E\u0434\u0430\u0432\u0435\u0446", crumbs: ["Bosh", "Core", "Telegram \u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u0435\u043B\u0438", "\u0418\u0437\u043C\u0435\u043D\u0438\u0442\u044C"] },
  "/users/send-region": { title: "\u041E\u0442\u043F\u0440\u0430\u0432\u0438\u0442\u044C \u043F\u043E \u043E\u0431\u043B\u0430\u0441\u0442\u0438", crumbs: ["Bosh", "Telegram \u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u0435\u043B\u0438", "\u0420\u0430\u0441\u0441\u044B\u043B\u043A\u0430"] },
  "/users/send-single": { title: "\u041E\u0442\u043F\u0440\u0430\u0432\u0438\u0442\u044C \u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u0435\u043B\u044E", crumbs: ["Bosh", "Telegram \u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u0435\u043B\u0438", "\u0421\u043E\u043E\u0431\u0449\u0435\u043D\u0438\u0435"] },
  "/auth/users": { title: "Admin foydalanuvchilar", crumbs: ["Bosh", "Auth", "Users"] },
  "/auth/groups": { title: "Guruhlar", crumbs: ["Bosh", "Auth", "Groups"] },
  "/qrcodes": { title: "QR kodlar", crumbs: ["Bosh", "Core", "QR \u043A\u043E\u0434\u044B"] },
  "/qrcodes/edit": { title: "QR \u043A\u043E\u0434 \xB7 #001", crumbs: ["Bosh", "Core", "QR \u043A\u043E\u0434\u044B", "\u0418\u0437\u043C\u0435\u043D\u0438\u0442\u044C"] },
  "/qrcodes/generate": { title: "QR generatsiya", crumbs: ["Bosh", "Core", "QR \u043A\u043E\u0434\u044B", "\u0413\u0435\u043D\u0435\u0440\u0430\u0446\u0438\u044F"] },
  "/batches": { title: "\u041F\u0430\u0440\u0442\u0438\u0438", crumbs: ["Bosh", "Core", "QR \u043F\u0430\u0440\u0442\u0438\u0438"] },
  "/batches/add": { title: "\u041D\u043E\u0432\u0430\u044F \u043F\u0430\u0440\u0442\u0438\u044F", crumbs: ["Bosh", "Core", "QR \u043F\u0430\u0440\u0442\u0438\u0438", "\u0414\u043E\u0431\u0430\u0432\u0438\u0442\u044C"] },
  "/batches/edit": { title: "\u041F\u0430\u0440\u0442\u0438\u044F \xB7 S27-MAY-2026", crumbs: ["Bosh", "Core", "QR \u043F\u0430\u0440\u0442\u0438\u0438", "\u0418\u0437\u043C\u0435\u043D\u0438\u0442\u044C"] },
  "/stores": { title: "Do'konlar", crumbs: ["Bosh", "Core", "\u041C\u0430\u0433\u0430\u0437\u0438\u043D\u044B"] },
  "/stores/edit": { title: "Sadulla Jomiy 1", crumbs: ["Bosh", "Core", "\u041C\u0430\u0433\u0430\u0437\u0438\u043D\u044B", "\u0418\u0437\u043C\u0435\u043D\u0438\u0442\u044C"] },
  "/stores/add": { title: "Yangi do'kon", crumbs: ["Bosh", "Core", "\u041C\u0430\u0433\u0430\u0437\u0438\u043D\u044B", "\u0414\u043E\u0431\u0430\u0432\u0438\u0442\u044C"] },
  "/gifts": { title: "Sovg'alar", crumbs: ["Bosh", "Core", "\u041F\u043E\u0434\u0430\u0440\u043A\u0438"] },
  "/gifts/add": { title: "Yangi sovg'a", crumbs: ["Bosh", "Core", "\u041F\u043E\u0434\u0430\u0440\u043A\u0438", "\u0414\u043E\u0431\u0430\u0432\u0438\u0442\u044C"] },
  "/redemptions": { title: "Sovg'a so'rovlari", crumbs: ["Bosh", "Core", "\u0417\u0430\u044F\u0432\u043A\u0438 \u043D\u0430 \u043F\u043E\u0434\u0430\u0440\u043A\u0438"] },
  "/redemptions/edit": { title: "\u0417\u0430\u044F\u0432\u043A\u0430 #1009", crumbs: ["Bosh", "Core", "\u0417\u0430\u044F\u0432\u043A\u0438", "\u0418\u0437\u043C\u0435\u043D\u0438\u0442\u044C"] },
  "/transactions": { title: "Sotuvchi tranzaksiyalari", crumbs: ["Bosh", "Core", "\u0422\u0440\u0430\u043D\u0437\u0430\u043A\u0446\u0438\u0438"] },
  "/transactions/add": { title: "Yangi tranzaksiya", crumbs: ["Bosh", "Core", "\u0422\u0440\u0430\u043D\u0437\u0430\u043A\u0446\u0438\u0438", "\u0414\u043E\u0431\u0430\u0432\u0438\u0442\u044C"] },
  "/seller-codes": { title: "Sotuvchi ID lar", crumbs: ["Bosh", "Core", "\u041A\u043E\u0434\u044B \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438"] },
  "/activity": { title: "Faollik tarixi", crumbs: ["Bosh", "Core", "\u0416\u0443\u0440\u043D\u0430\u043B \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u0439"] },
  "/livestreams": { title: "Jonli efirlar", crumbs: ["Bosh", "Core", "LiveStream"] },
  "/livestreams/add": { title: "Yangi efir", crumbs: ["Bosh", "Core", "LiveStream", "\u0414\u043E\u0431\u0430\u0432\u0438\u0442\u044C"] },
  "/regionlog": { title: "Viloyat xabarlari logi", crumbs: ["Bosh", "Core", "\u041B\u043E\u0433\u0438 \u0440\u0430\u0441\u0441\u044B\u043B\u043E\u043A"] },
  "/videos": { title: "Video ko'rsatmalar", crumbs: ["Bosh", "Core", "\u0412\u0438\u0434\u0435\u043E\u0438\u043D\u0441\u0442\u0440\u0443\u043A\u0446\u0438\u0438"] },
  "/videos/add": { title: "Yangi video", crumbs: ["Bosh", "Core", "\u0412\u0438\u0434\u0435\u043E\u0438\u043D\u0441\u0442\u0440\u0443\u043A\u0446\u0438\u0438", "\u0414\u043E\u0431\u0430\u0432\u0438\u0442\u044C"] },
  "/monthly": { title: "Oylik eslatma sozlamalari", crumbs: ["Bosh", "Core", "\u041D\u0430\u043F\u043E\u043C\u0438\u043D\u0430\u043D\u0438\u044F"] },
  "/monthly-log": { title: "Eslatma logi", crumbs: ["Bosh", "Core", "\u041B\u043E\u0433\u0438 \u043D\u0430\u043F\u043E\u043C\u0438\u043D\u0430\u043D\u0438\u0439"] },
  "/contacts": { title: "Admin kontaktlari", crumbs: ["Bosh", "Core", "\u041A\u043E\u043D\u0442\u0430\u043A\u0442\u044B"] },
  "/privacy": { title: "Maxfiylik siyosati", crumbs: ["Bosh", "Core", "Privacy policy"] }
};
function Sidebar({ currentRoute, onNavigate }) {
  return /* @__PURE__ */ React.createElement("aside", { className: "sidebar" }, /* @__PURE__ */ React.createElement("div", { className: "sidebar-brand" }, /* @__PURE__ */ React.createElement("div", { className: "logo" }, "JIP"), /* @__PURE__ */ React.createElement("div", { className: "brand-text" }, /* @__PURE__ */ React.createElement("div", { className: "brand-name" }, "JIP GROUP"), /* @__PURE__ */ React.createElement("div", { className: "brand-sub" }, "Jahon Invest Plast"))), /* @__PURE__ */ React.createElement("nav", { className: "sidebar-nav" }, NAV_GROUPS.map((g, gi) => /* @__PURE__ */ React.createElement("div", { key: gi, style: { display: "contents" } }, /* @__PURE__ */ React.createElement("div", { className: "sidebar-section" }, g.label), g.items.map((it, ii) => {
    const active = currentRoute === it.route || it.route !== "/" && currentRoute.startsWith(it.route + "/");
    return /* @__PURE__ */ React.createElement(
      "button",
      {
        key: ii,
        className: "nav-item" + (active ? " active" : ""),
        onClick: () => onNavigate(it.route),
        title: it.label
      },
      /* @__PURE__ */ React.createElement("span", { className: "nav-icon" }, /* @__PURE__ */ React.createElement(Icon, { name: it.icon, size: 16 })),
      /* @__PURE__ */ React.createElement("span", { className: "nav-label" }, it.label),
      it.count != null && /* @__PURE__ */ React.createElement("span", { className: "nav-count" }, it.count.toLocaleString("ru"))
    );
  })))), /* @__PURE__ */ React.createElement("div", { className: "sidebar-footer" }, /* @__PURE__ */ React.createElement(Avatar, { name: window.DJANGO_USER ? window.DJANGO_USER.name : "\u0416\u0430\u0441\u0443\u0440 \u041A\u0430\u0440\u0438\u043C\u043E\u0432", size: 28 }), /* @__PURE__ */ React.createElement("div", { className: "user-info", style: { minWidth: 0, flex: 1 } }, /* @__PURE__ */ React.createElement("div", { style: { color: "var(--text-strong)", fontSize: 12.5, fontWeight: 500, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" } }, window.DJANGO_USER ? window.DJANGO_USER.username : "admin"), /* @__PURE__ */ React.createElement("div", { style: { fontSize: 11, color: "var(--text-dim)" } }, window.DJANGO_USER && window.DJANGO_USER.is_superuser ? "Superadmin" : "Admin")), /* @__PURE__ */ React.createElement(
    "a",
    {
      href: "/admin/logout/",
      title: "Chiqish",
      style: {
        color: "var(--text-dim)",
        display: "flex",
        alignItems: "center",
        padding: 4,
        borderRadius: 4,
        textDecoration: "none",
        transition: "color 0.15s"
      },
      onMouseEnter: (e) => e.currentTarget.style.color = "var(--danger)",
      onMouseLeave: (e) => e.currentTarget.style.color = "var(--text-dim)"
    },
    /* @__PURE__ */ React.createElement(Icon, { name: "log-out", size: 14 })
  )));
}
function Topbar({ route, onNavigate, tweaks, setTweak }) {
  const meta = PAGE_META[route] || PAGE_META["/dashboard"];
  const isDark = tweaks.theme === "dark";
  return /* @__PURE__ */ React.createElement("div", { className: "topbar" }, /* @__PURE__ */ React.createElement("button", { className: "icon-btn", onClick: () => setTweak("sidebar", tweaks.sidebar === "icon" ? "dark" : "icon"), title: "Toggle sidebar" }, /* @__PURE__ */ React.createElement(Icon, { name: "menu", size: 16 })), /* @__PURE__ */ React.createElement("div", { className: "topbar-title" }, /* @__PURE__ */ React.createElement("h1", null, meta.title), /* @__PURE__ */ React.createElement("div", { className: "crumb" }, meta.crumbs.map((c, i) => /* @__PURE__ */ React.createElement("span", { key: i, style: { display: "contents" } }, i > 0 && /* @__PURE__ */ React.createElement(Icon, { name: "chevron-right", size: 11 }), /* @__PURE__ */ React.createElement("span", { style: { color: i === meta.crumbs.length - 1 ? "var(--text)" : void 0 } }, c))))), /* @__PURE__ */ React.createElement("div", { className: "topbar-actions" }, /* @__PURE__ */ React.createElement("button", { className: "icon-btn", title: "\u041F\u043E\u0438\u0441\u043A" }, /* @__PURE__ */ React.createElement(Icon, { name: "search", size: 16 })), /* @__PURE__ */ React.createElement("button", { className: "icon-btn", title: "\u0423\u0432\u0435\u0434\u043E\u043C\u043B\u0435\u043D\u0438\u044F" }, /* @__PURE__ */ React.createElement(Icon, { name: "bell", size: 16 })), /* @__PURE__ */ React.createElement(
    "button",
    {
      className: "icon-btn",
      title: isDark ? "Kun rejimi" : "Tun rejimi",
      onClick: () => setTweak("theme", isDark ? "light" : "dark")
    },
    /* @__PURE__ */ React.createElement(Icon, { name: isDark ? "sun" : "moon", size: 16 })
  ), /* @__PURE__ */ React.createElement("div", { style: { width: 1, height: 22, background: "var(--border)", margin: "0 4px" } }), /* @__PURE__ */ React.createElement(Button, { variant: "primary", size: "sm", icon: "plus" }, "\u0414\u043E\u0431\u0430\u0432\u0438\u0442\u044C")));
}
Object.assign(window, { Sidebar, Topbar, NAV_GROUPS, PAGE_META });
const J = window.JIP;
function DashboardPage({ onNavigate }) {
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(
    PageHeader,
    {
      title: "Boshqaruv paneli",
      subtitle: "Loyihaning umumiy ko'rsatkichlari va so'nggi faoliyat",
      actions: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(Button, { variant: "secondary", icon: "download" }, "Eksport"), /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "plus" }, "Yangi yozuv"))
    }
  ), /* @__PURE__ */ React.createElement("div", { className: "kpi-grid" }, /* @__PURE__ */ React.createElement(KPI, { label: "Jami foydalanuvchilar", value: "23", icon: "users", delta: "+12%", hint: "Telegram reg.", color: "indigo", spark: [12, 14, 15, 18, 19, 21, 22, 23], onClick: () => onNavigate("/users") }), /* @__PURE__ */ React.createElement(KPI, { label: "Faol partiyalar", value: "17", icon: "box", delta: "+3", hint: "Hozirda faol", color: "emerald", spark: [10, 11, 12, 13, 14, 16, 16, 17], onClick: () => onNavigate("/batches") }), /* @__PURE__ */ React.createElement(KPI, { label: "Jami skanlar", value: "239", icon: "qrcode", delta: "+34", hint: "Ishlatilgan QR", color: "blue", spark: [120, 140, 155, 178, 200, 215, 225, 239], onClick: () => onNavigate("/qrcodes") }), /* @__PURE__ */ React.createElement(KPI, { label: "Kutilayotgan sovg'alar", value: "15", icon: "gift", delta: "+2", deltaDir: "up", hint: "\u041E\u0431\u0440\u0430\u0431\u043E\u0442\u0430\u0442\u044C", color: "amber", spark: [5, 8, 10, 11, 13, 12, 14, 15], onClick: () => onNavigate("/redemptions") })), /* @__PURE__ */ React.createElement("div", { className: "two-col" }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", flexDirection: "column", gap: 20 } }, /* @__PURE__ */ React.createElement(ModelGrid, { onNavigate }), /* @__PURE__ */ React.createElement(ActivityChart, null)), /* @__PURE__ */ React.createElement(RecentActions, { items: J.recentActions })));
}
function ModelGrid({ onNavigate }) {
  const sections = [
    {
      title: "Core",
      models: [
        { name: "Telegram \u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u0435\u043B\u0438", count: 23, route: "/users", icon: "users" },
        { name: "QR \u043A\u043E\u0434\u044B", count: 239, route: "/qrcodes", icon: "qrcode" },
        { name: "QR \u043F\u0430\u0440\u0442\u0438\u0438", count: 17, route: "/batches", icon: "box" },
        { name: "\u041C\u0430\u0433\u0430\u0437\u0438\u043D\u044B", count: 12, route: "/stores", icon: "store" },
        { name: "\u041F\u043E\u0434\u0430\u0440\u043A\u0438", count: 8, route: "/gifts", icon: "gift" },
        { name: "\u0417\u0430\u044F\u0432\u043A\u0438 \u043D\u0430 \u043F\u043E\u0434\u0430\u0440\u043A\u0438", count: 15, route: "/redemptions", icon: "gift-redeem" },
        { name: "\u0422\u0440\u0430\u043D\u0437\u0430\u043A\u0446\u0438\u0438", count: 1117, route: "/transactions", icon: "credit-card" },
        { name: "\u041A\u043E\u0434\u044B \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438", count: 25, route: "/seller-codes", icon: "id-card" },
        { name: "LiveStream", count: 4, route: "/livestreams", icon: "radio" },
        { name: "\u0412\u0438\u0434\u0435\u043E\u0438\u043D\u0441\u0442\u0440\u0443\u043A\u0446\u0438\u0438", count: 5, route: "/videos", icon: "video" },
        { name: "\u0416\u0443\u0440\u043D\u0430\u043B", count: 264, route: "/activity", icon: "history" },
        { name: "Politika", count: 2, route: "/privacy", icon: "file-text" }
      ]
    },
    {
      title: "Foydalanuvchilar va guruhlar",
      models: [
        { name: "Admin foydalanuvchilar", count: 4, route: "/auth/users", icon: "user" },
        { name: "Guruhlar", count: 4, route: "/auth/groups", icon: "shield" }
      ]
    }
  ];
  return /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "card-header" }, /* @__PURE__ */ React.createElement("h3", null, "Modellar"), /* @__PURE__ */ React.createElement("span", { className: "text-muted text-xs" }, "Bosib kerakli bo'limga o'tish")), /* @__PURE__ */ React.createElement("div", { style: { padding: 16, display: "flex", flexDirection: "column", gap: 24 } }, sections.map((s, si) => /* @__PURE__ */ React.createElement("div", { key: si }, /* @__PURE__ */ React.createElement("div", { style: {
    fontSize: 11,
    fontWeight: 600,
    color: "var(--text-dim)",
    letterSpacing: "0.06em",
    textTransform: "uppercase",
    marginBottom: 8,
    paddingLeft: 4
  } }, s.title), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))", gap: 8 } }, s.models.map((m, mi) => /* @__PURE__ */ React.createElement(
    "div",
    {
      key: mi,
      onClick: () => onNavigate(m.route),
      style: {
        display: "flex",
        alignItems: "center",
        gap: 12,
        padding: "10px 12px",
        borderRadius: 8,
        cursor: "pointer",
        border: "1px solid var(--border)",
        background: "var(--surface-2)",
        transition: "border 120ms, background 120ms"
      },
      onMouseEnter: (e) => {
        e.currentTarget.style.borderColor = "var(--border-strong)";
        e.currentTarget.style.background = "var(--surface-3)";
      },
      onMouseLeave: (e) => {
        e.currentTarget.style.borderColor = "var(--border)";
        e.currentTarget.style.background = "var(--surface-2)";
      }
    },
    /* @__PURE__ */ React.createElement("span", { style: {
      width: 32,
      height: 32,
      borderRadius: 6,
      background: "var(--primary-soft)",
      color: "var(--primary)",
      display: "grid",
      placeItems: "center",
      flexShrink: 0
    } }, /* @__PURE__ */ React.createElement(Icon, { name: m.icon, size: 15 })),
    /* @__PURE__ */ React.createElement("div", { style: { flex: 1, minWidth: 0 } }, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 13, color: "var(--text-strong)", fontWeight: 500, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" } }, m.name), /* @__PURE__ */ React.createElement("div", { style: { fontSize: 11.5, color: "var(--text-muted)", fontVariantNumeric: "tabular-nums" } }, m.count.toLocaleString("ru"), " yozuv")),
    /* @__PURE__ */ React.createElement("button", { className: "icon-btn", style: { width: 24, height: 24 }, title: "Yangi qo'shish", onClick: (e) => e.stopPropagation() }, /* @__PURE__ */ React.createElement(Icon, { name: "plus", size: 12 }))
  )))))));
}
function ActivityChart() {
  const days = ["18 \u043C\u0430\u0439", "19 \u043C\u0430\u0439", "20 \u043C\u0430\u0439", "21 \u043C\u0430\u0439", "22 \u043C\u0430\u0439", "23 \u043C\u0430\u0439", "24 \u043C\u0430\u0439", "25 \u043C\u0430\u0439", "26 \u043C\u0430\u0439"];
  const scans = [12, 18, 14, 22, 28, 24, 34, 30, 38];
  const regs = [1, 2, 1, 3, 2, 4, 3, 5, 2];
  const max = Math.max(...scans);
  return /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "card-header" }, /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("h3", null, "QR aktivlik \xB7 So'nggi 9 kun"), /* @__PURE__ */ React.createElement("div", { className: "sub" }, "Skanlar va yangi ro'yxatdan o'tishlar")), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 16, alignItems: "center" } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 6, fontSize: 12, color: "var(--text-muted)" } }, /* @__PURE__ */ React.createElement("span", { style: { width: 8, height: 8, borderRadius: 999, background: "var(--primary)" } }), "Skanlar"), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 6, fontSize: 12, color: "var(--text-muted)" } }, /* @__PURE__ */ React.createElement("span", { style: { width: 8, height: 8, borderRadius: 999, background: "var(--success)" } }), "Yangi"))), /* @__PURE__ */ React.createElement("div", { style: { padding: 24, height: 200, position: "relative" } }, /* @__PURE__ */ React.createElement("svg", { viewBox: "0 0 900 180", preserveAspectRatio: "none", style: { width: "100%", height: "100%", display: "block" } }, /* @__PURE__ */ React.createElement("defs", null, /* @__PURE__ */ React.createElement("linearGradient", { id: "chart-fill", x1: "0", x2: "0", y1: "0", y2: "1" }, /* @__PURE__ */ React.createElement("stop", { offset: "0%", stopColor: "#6366f1", stopOpacity: "0.3" }), /* @__PURE__ */ React.createElement("stop", { offset: "100%", stopColor: "#6366f1", stopOpacity: "0" }))), [0, 1, 2, 3, 4].map((i) => /* @__PURE__ */ React.createElement("line", { key: i, x1: "0", x2: "900", y1: i * 36 + 18, y2: i * 36 + 18, stroke: "rgba(255,255,255,0.04)", strokeDasharray: "2 4" })), days.map((d, i) => {
    const x = i / (days.length - 1) * 850 + 25;
    const h = scans[i] / max * 100;
    return /* @__PURE__ */ React.createElement("rect", { key: i, x: x - 8, y: 170 - h, width: "16", height: h, rx: "2", fill: "var(--success)", opacity: "0.18" });
  }), /* @__PURE__ */ React.createElement(
    "polyline",
    {
      fill: "url(#chart-fill)",
      stroke: "none",
      points: days.map((_, i) => `${i / (days.length - 1) * 850 + 25},${170 - scans[i] / max * 140} `).join("") + `${(days.length - 1) / (days.length - 1) * 850 + 25},170 25,170`
    }
  ), /* @__PURE__ */ React.createElement(
    "polyline",
    {
      fill: "none",
      stroke: "#6366f1",
      strokeWidth: "2",
      points: days.map((_, i) => `${i / (days.length - 1) * 850 + 25},${170 - scans[i] / max * 140}`).join(" ")
    }
  ), days.map((_, i) => /* @__PURE__ */ React.createElement("circle", { key: i, cx: i / (days.length - 1) * 850 + 25, cy: 170 - scans[i] / max * 140, r: "3.5", fill: "#6366f1", stroke: "var(--surface-1)", strokeWidth: "2" }))), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "space-between", padding: "8px 25px 0", fontSize: 11, color: "var(--text-dim)", fontVariantNumeric: "tabular-nums" } }, days.map((d, i) => /* @__PURE__ */ React.createElement("span", { key: i }, d)))));
}
function AnalyticsPage() {
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(
    PageHeader,
    {
      title: "\u0410\u043D\u0430\u043B\u0438\u0442\u0438\u043A\u0430",
      subtitle: "Loyiha bo'yicha to'liq ko'rsatkichlar",
      actions: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(Select, { style: { width: 140 } }, /* @__PURE__ */ React.createElement("option", null, "So'nggi 30 kun"), /* @__PURE__ */ React.createElement("option", null, "So'nggi 7 kun"), /* @__PURE__ */ React.createElement("option", null, "Bu oy"), /* @__PURE__ */ React.createElement("option", null, "O'tgan oy")), /* @__PURE__ */ React.createElement(Button, { variant: "secondary", icon: "download" }, "PDF eksport"))
    }
  ), /* @__PURE__ */ React.createElement("div", { className: "kpi-grid" }, /* @__PURE__ */ React.createElement(KPI, { label: "Aktivatsiya foizi", value: "19.7%", icon: "trending-up", delta: "+2.4%", color: "emerald", spark: [14, 15, 17, 18, 19, 20, 19, 20] }), /* @__PURE__ */ React.createElement(KPI, { label: "Yangi sotuvchilar", value: "21", icon: "users", delta: "+5", color: "indigo", spark: [2, 4, 6, 9, 12, 15, 18, 21] }), /* @__PURE__ */ React.createElement(KPI, { label: "Sovg'a so'rovlari", value: "15", icon: "gift", delta: "+8", color: "amber", spark: [3, 5, 6, 8, 10, 12, 14, 15] }), /* @__PURE__ */ React.createElement(KPI, { label: "Jami transaksiya", value: "1 117", icon: "credit-card", delta: "+82", color: "blue", spark: [800, 890, 940, 990, 1020, 1050, 1080, 1117] })), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: "2fr 1fr", gap: 20 } }, /* @__PURE__ */ React.createElement(ActivityChart, null), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "card-header" }, /* @__PURE__ */ React.createElement("h3", null, "Viloyatlar bo'yicha")), /* @__PURE__ */ React.createElement("div", { style: { padding: 20, display: "flex", flexDirection: "column", gap: 14 } }, [
    { name: "\u0413\u043E\u0440\u043E\u0434 \u0422\u0430\u0448\u043A\u0435\u043D\u0442", value: 8, pct: 35 },
    { name: "\u0421\u0430\u043C\u0430\u0440\u043A\u0430\u043D\u0434\u0441\u043A\u0430\u044F", value: 4, pct: 17 },
    { name: "\u0411\u0443\u0445\u0430\u0440\u0441\u043A\u0430\u044F", value: 3, pct: 13 },
    { name: "\u0424\u0435\u0440\u0433\u0430\u043D\u0441\u043A\u0430\u044F", value: 3, pct: 13 },
    { name: "\u0410\u043D\u0434\u0438\u0436\u0430\u043D\u0441\u043A\u0430\u044F", value: 2, pct: 9 },
    { name: "\u041F\u0440\u043E\u0447\u0438\u0435", value: 3, pct: 13 }
  ].map((r, i) => /* @__PURE__ */ React.createElement("div", { key: i }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "space-between", marginBottom: 4, fontSize: 12.5 } }, /* @__PURE__ */ React.createElement("span", { style: { color: "var(--text)" } }, r.name), /* @__PURE__ */ React.createElement("span", { className: "text-mono text-muted" }, r.value, " (", r.pct, "%)")), /* @__PURE__ */ React.createElement("div", { className: "progress" }, /* @__PURE__ */ React.createElement("div", { style: { width: r.pct + "%" } }))))))), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 } }, /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "card-header" }, /* @__PURE__ */ React.createElement("h3", null, "TOP sotuvchilar (ballar bo'yicha)")), /* @__PURE__ */ React.createElement("div", { className: "table-wrap" }, /* @__PURE__ */ React.createElement("table", { className: "table" }, /* @__PURE__ */ React.createElement("thead", null, /* @__PURE__ */ React.createElement("tr", null, /* @__PURE__ */ React.createElement("th", null, "Sotuvchi"), /* @__PURE__ */ React.createElement("th", null, "QR"), /* @__PURE__ */ React.createElement("th", { style: { textAlign: "right" } }, "Ball"))), /* @__PURE__ */ React.createElement("tbody", null, J.users.filter((u) => u.type === "sotuvchi").slice(0, 6).map((u) => /* @__PURE__ */ React.createElement("tr", { key: u.id }, /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("div", { className: "user-cell" }, /* @__PURE__ */ React.createElement(Avatar, { name: u.first_name + " " + u.last_name, size: 28 }), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { className: "user-name" }, u.first_name, " ", u.last_name), /* @__PURE__ */ React.createElement("div", { className: "user-meta" }, "@", u.username)))), /* @__PURE__ */ React.createElement("td", { className: "num" }, u.total_qr || 0), /* @__PURE__ */ React.createElement("td", { style: { textAlign: "right" } }, /* @__PURE__ */ React.createElement("span", { className: "text-mono", style: { color: "var(--primary)", fontWeight: 600 } }, u.points.toLocaleString("ru"))))))))), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "card-header" }, /* @__PURE__ */ React.createElement("h3", null, "Konversiya voronkasi")), /* @__PURE__ */ React.createElement("div", { style: { padding: 20, display: "flex", flexDirection: "column", gap: 12 } }, [
    { label: "Sotuvchilar ro'yxatdan o'tishi", v: 25, pct: 100, color: "var(--info)" },
    { label: "Tasdiqlanganlar", v: 21, pct: 84, color: "var(--primary)" },
    { label: "Partiya yaratganlar", v: 17, pct: 68, color: "#a855f7" },
    { label: "QR skanlandi (santenik)", v: 47, pct: 19.7, color: "var(--success)" },
    { label: "Sovg'a so'ragan", v: 15, pct: 6.3, color: "var(--warning)" }
  ].map((s, i) => /* @__PURE__ */ React.createElement("div", { key: i }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "space-between", fontSize: 12.5, marginBottom: 4 } }, /* @__PURE__ */ React.createElement("span", null, s.label), /* @__PURE__ */ React.createElement("span", { className: "text-mono" }, /* @__PURE__ */ React.createElement("strong", null, s.v), " ", /* @__PURE__ */ React.createElement("span", { className: "text-dim" }, "(", s.pct, "%)"))), /* @__PURE__ */ React.createElement("div", { style: { height: 10, background: "var(--surface-3)", borderRadius: 6, overflow: "hidden" } }, /* @__PURE__ */ React.createElement("div", { style: { height: "100%", width: s.pct + "%", background: s.color, borderRadius: 6 } }))))))));
}
function UsersListPage({ onNavigate }) {
  const [selected, setSelected] = useState([]);
  const allIds = J.users.map((u) => u.id);
  const allSelected = selected.length === allIds.length;
  const toggleAll = () => setSelected(allSelected ? [] : allIds);
  const toggleOne = (id) => setSelected((s) => s.includes(id) ? s.filter((x) => x !== id) : [...s, id]);
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(
    PageHeader,
    {
      title: "Telegram \u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u0435\u043B\u0438",
      subtitle: "Sistemada ro'yxatdan o'tgan barcha foydalanuvchilar",
      actions: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(Button, { variant: "secondary", icon: "message-circle", onClick: () => onNavigate("/users/send-single") }, "Xabar"), /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "send", onClick: () => onNavigate("/users/send-region") }, "\u041E\u0442\u043F\u0440\u0430\u0432\u0438\u0442\u044C \u043F\u043E \u043E\u0431\u043B\u0430\u0441\u0442\u0438"))
    }
  ), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement(DateHierarchy, { items: ["2026", "\u041C\u0430\u0439", "22", "23", "25", "26"], active: 5 }), /* @__PURE__ */ React.createElement("div", { className: "filter-bar" }, /* @__PURE__ */ React.createElement(SearchBar, { placeholder: "\u041F\u043E\u0438\u0441\u043A: ism, telefon, ID..." }), /* @__PURE__ */ React.createElement("div", { style: { flex: 1 } }), /* @__PURE__ */ React.createElement(FilterChip, { icon: "user" }, "\u0422\u0438\u043F"), /* @__PURE__ */ React.createElement(FilterChip, { icon: "check", active: true }, "Faollik: Faol"), /* @__PURE__ */ React.createElement(FilterChip, { icon: "flag" }, "Til"), /* @__PURE__ */ React.createElement(FilterChip, { icon: "map-pin" }, "Viloyat"), /* @__PURE__ */ React.createElement(FilterChip, { icon: "calendar" }, "Sana diapazoni")), selected.length > 0 && /* @__PURE__ */ React.createElement("div", { style: {
    padding: "10px 16px",
    background: "var(--primary-softer)",
    borderBottom: "1px solid var(--border)",
    display: "flex",
    alignItems: "center",
    gap: 10
  } }, /* @__PURE__ */ React.createElement("span", { className: "text-sm text-strong" }, selected.length, " ta tanlangan"), /* @__PURE__ */ React.createElement("div", { style: { flex: 1 } }), /* @__PURE__ */ React.createElement(Button, { size: "sm", variant: "success", icon: "check" }, "Tasdiqlash"), /* @__PURE__ */ React.createElement(Button, { size: "sm", variant: "danger", icon: "x" }, "Rad etish"), /* @__PURE__ */ React.createElement(Select, { style: { height: 28, fontSize: 12, width: 220 } }, /* @__PURE__ */ React.createElement("option", null, "Yana amallar..."), /* @__PURE__ */ React.createElement("option", null, "\u0422\u0438\u043F \u043D\u0430 Sotuvchi"), /* @__PURE__ */ React.createElement("option", null, "\u041E\u0431\u043D\u043E\u0432\u0438\u0442\u044C \u0432\u0438loyat (Nominatim)"), /* @__PURE__ */ React.createElement("option", null, "\u041F\u0435\u0440\u0441\u043E\u043D\u0430\u043B\u044C\u043D\u043E\u0435 \u0441\u043E\u043E\u0431\u0449\u0435\u043D\u0438\u0435"), /* @__PURE__ */ React.createElement("option", null, "O'chirish"))), /* @__PURE__ */ React.createElement("div", { className: "table-wrap" }, /* @__PURE__ */ React.createElement("table", { className: "table" }, /* @__PURE__ */ React.createElement("thead", null, /* @__PURE__ */ React.createElement("tr", null, /* @__PURE__ */ React.createElement("th", { className: "col-checkbox" }, /* @__PURE__ */ React.createElement("input", { type: "checkbox", className: "checkbox", checked: allSelected, onChange: toggleAll })), /* @__PURE__ */ React.createElement("th", null, "Foydalanuvchi"), /* @__PURE__ */ React.createElement("th", null, "Phone"), /* @__PURE__ */ React.createElement("th", null, "Viloyat / Tuman"), /* @__PURE__ */ React.createElement("th", null, "Tur"), /* @__PURE__ */ React.createElement("th", null, "Tasdiqlash"), /* @__PURE__ */ React.createElement("th", { style: { textAlign: "right" } }, "Ballar"), /* @__PURE__ */ React.createElement("th", null, "Til"), /* @__PURE__ */ React.createElement("th", null, "Status"), /* @__PURE__ */ React.createElement("th", { style: { textAlign: "right" } }))), /* @__PURE__ */ React.createElement("tbody", null, J.users.map((u) => /* @__PURE__ */ React.createElement("tr", { key: u.id }, /* @__PURE__ */ React.createElement("td", { className: "col-checkbox" }, /* @__PURE__ */ React.createElement("input", { type: "checkbox", className: "checkbox", checked: selected.includes(u.id), onChange: () => toggleOne(u.id) })), /* @__PURE__ */ React.createElement("td", { onClick: () => onNavigate(u.type === "santenik" ? "/users/santenik" : "/users/sotuvchi"), style: { cursor: "pointer" } }, /* @__PURE__ */ React.createElement("div", { className: "user-cell" }, /* @__PURE__ */ React.createElement(Avatar, { name: u.first_name + " " + u.last_name }), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { className: "user-name" }, u.type === "santenik" ? /* @__PURE__ */ React.createElement(Icon, { name: "wrench", size: 12, className: "text-muted" }) : /* @__PURE__ */ React.createElement(Icon, { name: "store", size: 12, className: "text-muted" }), u.first_name, " ", u.last_name, /* @__PURE__ */ React.createElement("span", { className: "text-muted text-xs" }, "@", u.username)), /* @__PURE__ */ React.createElement("div", { className: "user-meta" }, "ID: ", u.id)))), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("span", { className: "text-mono text-sm" }, u.phone)), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", flexDirection: "column", gap: 3 } }, /* @__PURE__ */ React.createElement(Badge, { variant: "info", icon: "map-pin" }, u.region.replace(" \u043E\u0431\u043B\u0430\u0441\u0442\u044C", "").replace("\u0413\u043E\u0440\u043E\u0434 ", "")), /* @__PURE__ */ React.createElement(Badge, { variant: "warning", outline: true, size: "sm", icon: "map-pin" }, u.district))), /* @__PURE__ */ React.createElement("td", null, u.type === "santenik" ? /* @__PURE__ */ React.createElement(StatusBadges.santenik, null) : /* @__PURE__ */ React.createElement(StatusBadges.sotuvchi, null)), /* @__PURE__ */ React.createElement("td", null, u.type === "sotuvchi" ? u.seller_approved ? /* @__PURE__ */ React.createElement(StatusBadges.approved, null) : /* @__PURE__ */ React.createElement(StatusBadges.pending, null) : /* @__PURE__ */ React.createElement("span", { className: "text-dim text-xs" }, "\u2014")), /* @__PURE__ */ React.createElement("td", { style: { textAlign: "right" } }, /* @__PURE__ */ React.createElement("span", { className: "text-mono", style: { color: "var(--primary)", fontWeight: 600 } }, u.points.toLocaleString("ru"))), /* @__PURE__ */ React.createElement("td", null, u.language === "uz" ? /* @__PURE__ */ React.createElement(StatusBadges.langUz, null) : /* @__PURE__ */ React.createElement(StatusBadges.langRu, null)), /* @__PURE__ */ React.createElement("td", null, u.is_active ? /* @__PURE__ */ React.createElement(StatusBadges.active, null) : /* @__PURE__ */ React.createElement(StatusBadges.inactive, null)), /* @__PURE__ */ React.createElement("td", { style: { textAlign: "right" } }, /* @__PURE__ */ React.createElement(Button, { size: "sm", variant: "ghost", icon: "message-square", onClick: () => onNavigate("/users/send-single") }, "\u041D\u0430\u043F\u0438\u0441\u0430\u0442\u044C"))))))), /* @__PURE__ */ React.createElement(Pagination, { total: 23, page: 1, perPage: 25 })));
}
function UserSantenikPage({ onNavigate }) {
  const u = J.users[0];
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(
    PageHeader,
    {
      title: /* @__PURE__ */ React.createElement("span", null, u.first_name, " ", u.last_name, " ", /* @__PURE__ */ React.createElement(Badge, { variant: "warning", icon: "wrench" }, "Santenik")),
      subtitle: "ID: " + u.id + " \xB7 @" + u.username + " \xB7 " + u.region,
      actions: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(Button, { variant: "ghost", icon: "history" }, "\u0418\u0441\u0442\u043E\u0440\u0438\u044F"), /* @__PURE__ */ React.createElement(Button, { variant: "secondary", icon: "trash" }, "O'chirish"), /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "check" }, "\u0421\u043E\u0445\u0440\u0430\u043D\u0438\u0442\u044C"))
    }
  ), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 } }, /* @__PURE__ */ React.createElement(FormBlock, { title: "\u041E\u0441\u043D\u043E\u0432\u043D\u0430\u044F \u0438\u043D\u0444\u043E\u0440\u043C\u0430\u0446\u0438\u044F", icon: "user" }, /* @__PURE__ */ React.createElement(Field, { label: "Telegram ID" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: u.id, readOnly: true })), /* @__PURE__ */ React.createElement(Field, { label: "Username" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: "@" + u.username, readOnly: true })), /* @__PURE__ */ React.createElement(Field, { label: "First name", required: true }, /* @__PURE__ */ React.createElement(Input, { defaultValue: u.first_name })), /* @__PURE__ */ React.createElement(Field, { label: "Last name" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: u.last_name })), /* @__PURE__ */ React.createElement(Field, { label: "Jami urinishlar", hint: "Faqat ko'rish" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: u.total_attempts, readOnly: true })), /* @__PURE__ */ React.createElement(Field, { label: "Muvaffaqiyatli", hint: "Faqat ko'rish" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: u.successful_attempts, readOnly: true })), /* @__PURE__ */ React.createElement(Field, { label: "Skanlangan urinishlar", hint: "Faqat ko'rish", span2: true }, /* @__PURE__ */ React.createElement(Input, { defaultValue: u.successful_attempts, readOnly: true }))), /* @__PURE__ */ React.createElement(FormBlock, { title: "\u041A\u043E\u043D\u0442\u0430\u043A\u0442\u043D\u044B\u0435 \u0434\u0430\u043D\u043D\u044B\u0435", icon: "map-pin" }, /* @__PURE__ */ React.createElement(Field, { label: "Phone number", required: true }, /* @__PURE__ */ React.createElement(Input, { defaultValue: u.phone })), /* @__PURE__ */ React.createElement(Field, { label: "Latitude" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: u.latitude.toFixed(6) })), /* @__PURE__ */ React.createElement(Field, { label: "Longitude" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: u.longitude.toFixed(6) })), /* @__PURE__ */ React.createElement(Field, { span2: true }, /* @__PURE__ */ React.createElement(Button, { variant: "secondary", icon: "map" }, "\u041E\u0442\u043A\u0440\u044B\u0442\u044C \u043D\u0430 \u042F\u043D\u0434\u0435\u043A\u0441.\u041A\u0430\u0440\u0442\u0430\u0445")), /* @__PURE__ */ React.createElement(Field, { label: "Viloyat (autocomplete)", required: true }, /* @__PURE__ */ React.createElement(Select, { defaultValue: u.region }, J.regions.map((r) => /* @__PURE__ */ React.createElement("option", { key: r }, r)))), /* @__PURE__ */ React.createElement(Field, { label: "Tuman" }, /* @__PURE__ */ React.createElement(Select, { defaultValue: u.district }, (J.districtsByRegion[u.region] || []).map((d) => /* @__PURE__ */ React.createElement("option", { key: d }, d))))), /* @__PURE__ */ React.createElement(FormBlock, { title: "\u0422\u0438\u043F \u0438 \u0431\u0430\u043B\u043B\u044B", icon: "coin", badge: /* @__PURE__ */ React.createElement(Badge, { variant: "primary" }, u.points.toLocaleString("ru"), " ball") }, /* @__PURE__ */ React.createElement(Field, { label: "User type" }, /* @__PURE__ */ React.createElement(Select, { defaultValue: "santenik" }, /* @__PURE__ */ React.createElement("option", { value: "santenik" }, "Santenik"), /* @__PURE__ */ React.createElement("option", { value: "sotuvchi" }, "Sotuvchi"))), /* @__PURE__ */ React.createElement(Field, { label: "\u0411\u0430\u043B\u043B\u044B (\u043F\u0440\u043E\u043C\u043E\u043A\u043E\u0434\u044B \u2212 \u0437\u0430\u043A\u0430\u0437\u044B)", hint: "Avtomatik hisoblanadi" }, /* @__PURE__ */ React.createElement("div", { className: "input", style: { color: "var(--primary)", fontWeight: 600 } }, u.points.toLocaleString("ru"))), /* @__PURE__ */ React.createElement(Field, { label: "Points", hint: "Faqat ko'rish", span2: true }, /* @__PURE__ */ React.createElement(Input, { defaultValue: u.points, readOnly: true })), /* @__PURE__ */ React.createElement("div", { className: "span-2", style: {
    padding: "10px 12px",
    background: "var(--surface-2)",
    borderRadius: 8,
    fontSize: 12.5,
    color: "var(--text-muted)",
    borderLeft: "3px solid var(--primary)"
  } }, /* @__PURE__ */ React.createElement("strong", { style: { color: "var(--text)" } }, "Santenik:"), " ballarni QR-skanlardan oladi. Har bir muvaffaqiyatli skan uchun 50 ball qo'shiladi.")), /* @__PURE__ */ React.createElement(FormBlock, { title: "\u041D\u0430\u0441\u0442\u0440\u043E\u0439\u043A\u0438 \u0438 \u0430\u043A\u0442\u0438\u0432\u043D\u043E\u0441\u0442\u044C", icon: "settings" }, /* @__PURE__ */ React.createElement(Field, { label: "Til" }, /* @__PURE__ */ React.createElement(Select, { defaultValue: u.language }, /* @__PURE__ */ React.createElement("option", { value: "uz" }, "\u{1F1FA}\u{1F1FF} O'zbek"), /* @__PURE__ */ React.createElement("option", { value: "ru" }, "\u{1F1F7}\u{1F1FA} \u0420\u0443\u0441\u0441\u043A\u0438\u0439"))), /* @__PURE__ */ React.createElement(Field, { label: "Faollik" }, /* @__PURE__ */ React.createElement("label", { style: { display: "flex", alignItems: "center", gap: 8 } }, /* @__PURE__ */ React.createElement("input", { type: "checkbox", className: "checkbox", defaultChecked: u.is_active }), /* @__PURE__ */ React.createElement("span", { className: "text-sm" }, "\u0410\u043A\u0442\u0438\u0432\u0435\u043D"))), /* @__PURE__ */ React.createElement(Field, { label: "Last message sent at" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: "2026-05-26 14:23", readOnly: true })), /* @__PURE__ */ React.createElement(Field, { label: "Blocked bot at" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: "\u2014", readOnly: true })), /* @__PURE__ */ React.createElement(Field, { label: "Promo failed attempts" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: "0" })), /* @__PURE__ */ React.createElement(Field, { label: "Promo block stage" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: "0" })), /* @__PURE__ */ React.createElement(Field, { label: "Promo blocked until", span2: true }, /* @__PURE__ */ React.createElement(Input, { defaultValue: "\u2014", readOnly: true }))), /* @__PURE__ */ React.createElement(FormBlock, { title: "Sotuvchi tasdiqlash", icon: "check", badge: /* @__PURE__ */ React.createElement(Badge, { variant: "neutral", outline: true }, "collapsed") }, /* @__PURE__ */ React.createElement(Field, { label: "Tasdiqlangan" }, /* @__PURE__ */ React.createElement("label", { style: { display: "flex", alignItems: "center", gap: 8 } }, /* @__PURE__ */ React.createElement("input", { type: "checkbox", className: "checkbox" }), /* @__PURE__ */ React.createElement("span", { className: "text-sm text-muted" }, "Faol"))), /* @__PURE__ */ React.createElement(Field, { label: "Tasdiqlangan vaqt" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: "\u2014", readOnly: true }))), /* @__PURE__ */ React.createElement(FormBlock, { title: "Sanalar", icon: "calendar" }, /* @__PURE__ */ React.createElement(Field, { label: "Yaratilgan" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: u.created_at + " 14:23:11", readOnly: true })), /* @__PURE__ */ React.createElement(Field, { label: "O'zgartirilgan" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: "2026-05-26 16:08:42", readOnly: true })))), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "card-header" }, /* @__PURE__ */ React.createElement("h3", null, "\u041E\u0442\u0441\u043A\u0430\u043D\u0438\u0440\u043E\u0432\u0430\u043D\u043D\u044B\u0435 \u043F\u0440\u043E\u043C\u043E\u043A\u043E\u0434\u044B"), /* @__PURE__ */ React.createElement(Badge, { variant: "neutral" }, u.successful_attempts, " ta")), /* @__PURE__ */ React.createElement("div", { className: "table-wrap" }, /* @__PURE__ */ React.createElement("table", { className: "table inline-table" }, /* @__PURE__ */ React.createElement("thead", null, /* @__PURE__ */ React.createElement("tr", null, /* @__PURE__ */ React.createElement("th", null, "Serial"), /* @__PURE__ */ React.createElement("th", null, "Store"), /* @__PURE__ */ React.createElement("th", null, "Batch"), /* @__PURE__ */ React.createElement("th", null, "Points"), /* @__PURE__ */ React.createElement("th", null, "Scanned at"))), /* @__PURE__ */ React.createElement("tbody", null, J.qrcodes.filter((q) => q.is_scanned).slice(0, 5).map((q) => /* @__PURE__ */ React.createElement("tr", { key: q.id }, /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("span", { className: "code-mask" }, "#", q.serial)), /* @__PURE__ */ React.createElement("td", null, q.store_name), /* @__PURE__ */ React.createElement("td", { className: "text-mono text-xs" }, q.batch_name), /* @__PURE__ */ React.createElement("td", { className: "num text-mono", style: { color: "var(--primary)" } }, "+", q.points), /* @__PURE__ */ React.createElement("td", { className: "text-mono text-xs text-muted" }, q.scanned_at))))))), /* @__PURE__ */ React.createElement("div", { className: "form-footer" }, /* @__PURE__ */ React.createElement("span", { className: "text-muted text-sm" }, "\u0418\u0437\u043C\u0435\u043D\u0435\u043D\u0438\u044F \u043D\u0435 \u0441\u043E\u0445\u0440\u0430\u043D\u0435\u043D\u044B"), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 8 } }, /* @__PURE__ */ React.createElement(Button, { variant: "ghost" }, "\u0421\u043E\u0445\u0440\u0430\u043D\u0438\u0442\u044C \u0438 \u0434\u043E\u0431\u0430\u0432\u0438\u0442\u044C \u0434\u0440\u0443\u0433\u043E\u0439"), /* @__PURE__ */ React.createElement(Button, { variant: "secondary" }, "\u0421\u043E\u0445\u0440\u0430\u043D\u0438\u0442\u044C \u0438 \u043F\u0440\u043E\u0434\u043E\u043B\u0436\u0438\u0442\u044C"), /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "check" }, "\u0421\u043E\u0445\u0440\u0430\u043D\u0438\u0442\u044C"))));
}
function UserSotuvchiPage({ onNavigate }) {
  const u = J.users.find((x) => x.type === "sotuvchi");
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(
    PageHeader,
    {
      title: /* @__PURE__ */ React.createElement("span", null, u.first_name, " ", u.last_name, " ", /* @__PURE__ */ React.createElement(Badge, { variant: "info", icon: "store" }, "Sotuvchi")),
      subtitle: /* @__PURE__ */ React.createElement("span", null, "ID: ", u.id, " \xB7 @", u.username, " \xB7 ", /* @__PURE__ */ React.createElement("span", { className: "code-mask" }, u.seller_code)),
      actions: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(Button, { variant: "ghost", icon: "history" }, "\u0418\u0441\u0442\u043E\u0440\u0438\u044F"), /* @__PURE__ */ React.createElement(Button, { variant: "secondary", icon: "download" }, "Excel eksport"), /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "check" }, "\u0421\u043E\u0445\u0440\u0430\u043D\u0438\u0442\u044C"))
    }
  ), /* @__PURE__ */ React.createElement(FormBlock, { title: "Asosiy ma'lumotlar", icon: "user", badge: /* @__PURE__ */ React.createElement(Badge, { variant: "primary" }, u.points.toLocaleString("ru"), " ball") }, /* @__PURE__ */ React.createElement(Field, { label: "First name", required: true }, /* @__PURE__ */ React.createElement(Input, { defaultValue: u.first_name })), /* @__PURE__ */ React.createElement(Field, { label: "Last name" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: u.last_name })), /* @__PURE__ */ React.createElement(Field, { label: "Username" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: "@" + u.username, readOnly: true })), /* @__PURE__ */ React.createElement(Field, { label: "Telegram ID" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: u.id, readOnly: true })), /* @__PURE__ */ React.createElement(Field, { label: "Phone number" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: u.phone })), /* @__PURE__ */ React.createElement(Field, { label: "User type" }, /* @__PURE__ */ React.createElement(Select, { defaultValue: "sotuvchi" }, /* @__PURE__ */ React.createElement("option", { value: "sotuvchi" }, "Sotuvchi"), /* @__PURE__ */ React.createElement("option", { value: "santenik" }, "Santenik"))), /* @__PURE__ */ React.createElement(Field, { label: "Language" }, /* @__PURE__ */ React.createElement(Select, { defaultValue: u.language }, /* @__PURE__ */ React.createElement("option", { value: "uz" }, "\u{1F1FA}\u{1F1FF} O'zbek"), /* @__PURE__ */ React.createElement("option", { value: "ru" }, "\u{1F1F7}\u{1F1FA} \u0420\u0443\u0441\u0441\u043A\u0438\u0439"))), /* @__PURE__ */ React.createElement(Field, { label: "Points", hint: "Faqat ko'rish" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: u.points, readOnly: true })), /* @__PURE__ */ React.createElement(Field, { label: "Seller code" }, /* @__PURE__ */ React.createElement("div", { className: "input" }, /* @__PURE__ */ React.createElement("span", { className: "code-mask" }, u.seller_code))), /* @__PURE__ */ React.createElement(Field, { label: "Store ID" }, /* @__PURE__ */ React.createElement("div", { className: "input", style: { display: "flex", alignItems: "center", gap: 8 } }, /* @__PURE__ */ React.createElement(Icon, { name: "store", size: 13, className: "text-muted" }), /* @__PURE__ */ React.createElement("a", { style: { color: "var(--primary)", cursor: "pointer" }, onClick: () => onNavigate("/stores") }, u.store_id, " \xB7 Sadulla Jomiy 1"))), /* @__PURE__ */ React.createElement(Field, { label: "is_active" }, /* @__PURE__ */ React.createElement("label", { style: { display: "flex", alignItems: "center", gap: 8 } }, /* @__PURE__ */ React.createElement("input", { type: "checkbox", className: "checkbox", defaultChecked: u.is_active }), " ", /* @__PURE__ */ React.createElement("span", { className: "text-sm" }, "\u0410\u043A\u0442\u0438\u0432\u0435\u043D"))), /* @__PURE__ */ React.createElement(Field, { label: "seller_approved" }, /* @__PURE__ */ React.createElement("label", { style: { display: "flex", alignItems: "center", gap: 8 } }, /* @__PURE__ */ React.createElement("input", { type: "checkbox", className: "checkbox", defaultChecked: u.seller_approved }), " ", /* @__PURE__ */ React.createElement("span", { className: "text-sm" }, "Tasdiqlangan"))), /* @__PURE__ */ React.createElement(Field, { label: "seller_approved_at", span2: true }, /* @__PURE__ */ React.createElement(Input, { defaultValue: u.seller_approved_at || "\u2014", readOnly: true }))), /* @__PURE__ */ React.createElement(FormBlock, { title: "Manzil va lokatsiya", icon: "map-pin" }, /* @__PURE__ */ React.createElement(Field, { label: "Viloyat (autocomplete)", required: true }, /* @__PURE__ */ React.createElement(Select, { defaultValue: u.region }, J.regions.map((r) => /* @__PURE__ */ React.createElement("option", { key: r }, r)))), /* @__PURE__ */ React.createElement(Field, { label: "Tuman" }, /* @__PURE__ */ React.createElement(Select, { defaultValue: u.district }, (J.districtsByRegion[u.region] || ["\u2014"]).map((d) => /* @__PURE__ */ React.createElement("option", { key: d }, d)))), /* @__PURE__ */ React.createElement(Field, { label: "Latitude" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: u.latitude.toFixed(6) })), /* @__PURE__ */ React.createElement(Field, { label: "Longitude" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: u.longitude.toFixed(6) })), /* @__PURE__ */ React.createElement(Field, { span2: true }, /* @__PURE__ */ React.createElement(Button, { variant: "secondary", icon: "map" }, "\u041E\u0442\u043A\u0440\u044B\u0442\u044C \u043D\u0430 \u042F\u043D\u0434\u0435\u043A\u0441.\u041A\u0430\u0440\u0442\u0430\u0445"))), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "card-header" }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 10 } }, /* @__PURE__ */ React.createElement("span", { style: { width: 24, height: 24, display: "grid", placeItems: "center", borderRadius: 6, background: "var(--primary-soft)", color: "var(--primary)" } }, /* @__PURE__ */ React.createElement(Icon, { name: "box", size: 13 })), /* @__PURE__ */ React.createElement("h3", null, "\u041F\u0430\u0440\u0442\u0438\u044F tarixi"), /* @__PURE__ */ React.createElement(Badge, { variant: "neutral" }, u.batches_count)), /* @__PURE__ */ React.createElement(Button, { size: "sm", variant: "success", icon: "download" }, "Barcha promo Excel eksport")), /* @__PURE__ */ React.createElement("div", { className: "table-wrap" }, /* @__PURE__ */ React.createElement("table", { className: "table inline-table" }, /* @__PURE__ */ React.createElement("thead", null, /* @__PURE__ */ React.createElement("tr", null, /* @__PURE__ */ React.createElement("th", null, "\u041F\u0430\u0440\u0442\u0438\u044F nomi"), /* @__PURE__ */ React.createElement("th", null, "Jami"), /* @__PURE__ */ React.createElement("th", null, "Ishlatilgan"), /* @__PURE__ */ React.createElement("th", null, "Sana"), /* @__PURE__ */ React.createElement("th", { style: { textAlign: "right" } }, "ZIP"))), /* @__PURE__ */ React.createElement("tbody", null, J.batches.filter((b) => b.seller_id === u.id).slice(0, 5).map((b) => /* @__PURE__ */ React.createElement("tr", { key: b.id }, /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("span", { className: "text-mono" }, b.name)), /* @__PURE__ */ React.createElement("td", { className: "num" }, b.quantity), /* @__PURE__ */ React.createElement("td", { className: "num" }, b.scanned, " ", /* @__PURE__ */ React.createElement("span", { className: "text-dim" }, "(", b.activation_pct.toFixed(1), "%)")), /* @__PURE__ */ React.createElement("td", { className: "text-mono text-xs text-muted" }, b.created_at), /* @__PURE__ */ React.createElement("td", { style: { textAlign: "right" } }, /* @__PURE__ */ React.createElement(Button, { size: "sm", variant: "ghost", icon: "download" }, "ZIP")))), J.batches.filter((b) => b.seller_id === u.id).length === 0 && /* @__PURE__ */ React.createElement("tr", null, /* @__PURE__ */ React.createElement("td", { colSpan: 5 }, /* @__PURE__ */ React.createElement("div", { className: "empty", style: { padding: 24 } }, /* @__PURE__ */ React.createElement("div", { className: "empty-icon" }, /* @__PURE__ */ React.createElement(Icon, { name: "box", size: 18 })), /* @__PURE__ */ React.createElement("h4", null, "\u041F\u0430\u0440\u0442\u0438\u044F yo'q"), /* @__PURE__ */ React.createElement("div", null, "Hali bu sotuvchi uchun partiya yaratilmagan")))))))), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "card-header" }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 10 } }, /* @__PURE__ */ React.createElement("span", { style: { width: 24, height: 24, display: "grid", placeItems: "center", borderRadius: 6, background: "var(--success-soft)", color: "var(--success)" } }, /* @__PURE__ */ React.createElement(Icon, { name: "bar-chart", size: 13 })), /* @__PURE__ */ React.createElement("h3", null, "Statistika"))), /* @__PURE__ */ React.createElement("div", { style: { padding: 20, display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16 } }, [
    { label: "Ro'yxatdan o'tgan", value: u.created_at, icon: "calendar" },
    { label: "Tasdiqlangan", value: u.seller_approved_at || "\u2014", icon: "check" },
    { label: "\u041F\u0430\u0440\u0442\u0438\u044F soni", value: u.batches_count, icon: "box" },
    { label: "Jami QR", value: u.total_qr, icon: "qrcode" },
    { label: "Skanlanganlar", value: u.scanned_qr, icon: "sparkles" },
    { label: "Aktivatsiya", value: (u.scanned_qr / u.total_qr * 100).toFixed(1) + "%", icon: "trending-up" },
    { label: "Joriy ballar", value: u.points.toLocaleString("ru"), icon: "coin" },
    { label: "Sovg'a so'rovlari", value: 0, icon: "gift" }
  ].map((s, i) => /* @__PURE__ */ React.createElement("div", { key: i, style: { padding: 12, background: "var(--surface-2)", borderRadius: 8, border: "1px solid var(--border)" } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 6, color: "var(--text-muted)", fontSize: 11.5, marginBottom: 4 } }, /* @__PURE__ */ React.createElement(Icon, { name: s.icon, size: 12 }), " ", s.label), /* @__PURE__ */ React.createElement("div", { style: { fontSize: 16, color: "var(--text-strong)", fontWeight: 600, fontVariantNumeric: "tabular-nums" } }, s.value))))), /* @__PURE__ */ React.createElement("div", { className: "form-footer" }, /* @__PURE__ */ React.createElement("span", { className: "text-muted text-sm" }, "\u0418\u0437\u043C\u0435\u043D\u0435\u043D\u0438\u044F \u043D\u0435 \u0441\u043E\u0445\u0440\u0430\u043D\u0435\u043D\u044B"), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 8 } }, /* @__PURE__ */ React.createElement(Button, { variant: "ghost" }, "\u0421\u043E\u0445\u0440\u0430\u043D\u0438\u0442\u044C \u0438 \u0434\u043E\u0431\u0430\u0432\u0438\u0442\u044C \u0434\u0440\u0443\u0433\u043E\u0439"), /* @__PURE__ */ React.createElement(Button, { variant: "secondary" }, "\u0421\u043E\u0445\u0440\u0430\u043D\u0438\u0442\u044C \u0438 \u043F\u0440\u043E\u0434\u043E\u043B\u0436\u0438\u0442\u044C"), /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "check" }, "\u0421\u043E\u0445\u0440\u0430\u043D\u0438\u0442\u044C"))));
}
function SendRegionMessagePage() {
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement("div", { className: "gradient-banner" }, /* @__PURE__ */ React.createElement("h2", null, /* @__PURE__ */ React.createElement(Icon, { name: "send", size: 20 }), " \xA0\u041E\u0442\u043F\u0440\u0430\u0432\u0438\u0442\u044C \u0441\u043E\u043E\u0431\u0449\u0435\u043D\u0438\u0435 \u043F\u043E \u043E\u0431\u043B\u0430\u0441\u0442\u0438"), /* @__PURE__ */ React.createElement("p", null, "\u0412\u044B\u0431\u0435\u0440\u0438\u0442\u0435 \u043E\u0431\u043B\u0430\u0441\u0442\u044C \u0423\u0437\u0431\u0435\u043A\u0438\u0441\u0442\u0430\u043D\u0430 \u0438 \u043E\u0442\u043F\u0440\u0430\u0432\u044C\u0442\u0435 \u0441\u043E\u043E\u0431\u0449\u0435\u043D\u0438\u0435 \u0432\u0441\u0435\u043C \u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u0435\u043B\u044F\u043C \u044D\u0442\u043E\u0433\u043E \u0440\u0435\u0433\u0438\u043E\u043D\u0430. \u041F\u043E\u0434\u0434\u0435\u0440\u0436\u0438\u0432\u0430\u0435\u0442\u0441\u044F \u0444\u043E\u0442\u043E, \u043E\u0442\u043B\u043E\u0436\u0435\u043D\u043D\u0430\u044F \u043E\u0442\u043F\u0440\u0430\u0432\u043A\u0430 \u0438 \u0442\u0435\u0441\u0442\u043E\u0432\u044B\u0439 \u0437\u0430\u043F\u0443\u0441\u043A."), /* @__PURE__ */ React.createElement("div", { className: "banner-badge" }, /* @__PURE__ */ React.createElement(Icon, { name: "map-pin", size: 11 }), " \xA014 \u043E\u0431\u043B\u0430\u0441\u0442\u0435\u0439 + \u0412\u0441\u0435 \u0440\u0435\u0433\u0438\u043E\u043D\u044B")), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: "1fr 320px", gap: 20, alignItems: "start" } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", flexDirection: "column", gap: 16 } }, /* @__PURE__ */ React.createElement(FormBlock, { title: "\u041F\u0430\u0440\u0430\u043C\u0435\u0442\u0440\u044B \u0440\u0430\u0441\u0441\u044B\u043B\u043A\u0438", icon: "settings" }, /* @__PURE__ */ React.createElement(Field, { label: "\u{1F5FA}\uFE0F \u041E\u0431\u043B\u0430\u0441\u0442\u044C", required: true }, /* @__PURE__ */ React.createElement(Select, null, /* @__PURE__ */ React.createElement("option", null, "\u2014 \u0412\u044B\u0431\u0435\u0440\u0438\u0442\u0435 \u043E\u0431\u043B\u0430\u0441\u0442\u044C \u2014"), /* @__PURE__ */ React.createElement("option", null, "\u0412\u0441\u0435 \u0440\u0435\u0433\u0438\u043E\u043D\u044B"), J.regions.map((r) => /* @__PURE__ */ React.createElement("option", { key: r }, r)))), /* @__PURE__ */ React.createElement(Field, { label: "\u{1F465} \u0422\u0438\u043F \u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u0435\u043B\u044F" }, /* @__PURE__ */ React.createElement(Select, null, /* @__PURE__ */ React.createElement("option", null, "\u0412\u0441\u0435"), /* @__PURE__ */ React.createElement("option", null, "\u0421\u0430\u043D\u0442\u0435\u0445\u043D\u0438\u043A\u0438"), /* @__PURE__ */ React.createElement("option", null, "\u041F\u0440\u043E\u0434\u0430\u0432\u0446\u044B"))), /* @__PURE__ */ React.createElement(Field, { label: "\u{1F310} \u042F\u0437\u044B\u043A \u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u0435\u043B\u044F" }, /* @__PURE__ */ React.createElement(Select, null, /* @__PURE__ */ React.createElement("option", null, "\u0412\u0441\u0435 \u044F\u0437\u044B\u043A\u0438"), /* @__PURE__ */ React.createElement("option", null, "\u{1F1FA}\u{1F1FF} O'zbek"), /* @__PURE__ */ React.createElement("option", null, "\u{1F1F7}\u{1F1FA} \u0420\u0443\u0441\u0441\u043A\u0438\u0439"))), /* @__PURE__ */ React.createElement(Field, { label: "\u{1F550} \u041E\u0442\u043B\u043E\u0436\u0435\u043D\u043D\u0430\u044F \u043E\u0442\u043F\u0440\u0430\u0432\u043A\u0430", hint: "\u0412\u0440\u0435\u043C\u044F \u0432 \u0447\u0430\u0441\u043E\u0432\u043E\u043C \u043F\u043E\u044F\u0441\u0435 \u0441\u0435\u0440\u0432\u0435\u0440\u0430 (Asia/Tashkent)" }, /* @__PURE__ */ React.createElement(Input, { type: "datetime-local" }))), /* @__PURE__ */ React.createElement(FormBlock, { title: "\u0421\u043E\u0434\u0435\u0440\u0436\u0438\u043C\u043E\u0435", icon: "message-square", single: true }, /* @__PURE__ */ React.createElement(Field, { label: "\u{1F4AC} \u0422\u0435\u043A\u0441\u0442 \u0441\u043E\u043E\u0431\u0449\u0435\u043D\u0438\u044F", required: true, hint: "\u0418\u0441\u043F\u043E\u043B\u044C\u0437\u0443\u0439\u0442\u0435 \u043A\u043D\u043E\u043F\u043A\u0438 \u0434\u043B\u044F \u0444\u043E\u0440\u043C\u0430\u0442\u0438\u0440\u043E\u0432\u0430\u043D\u0438\u044F: \u0436\u0438\u0440\u043D\u044B\u0439, \u043A\u0443\u0440\u0441\u0438\u0432, \u0441\u0441\u044B\u043B\u043A\u0430..." }, /* @__PURE__ */ React.createElement(Textarea, { rows: 8, placeholder: "\u0417\u0434\u0440\u0430\u0432\u0441\u0442\u0432\u0443\u0439\u0442\u0435! \u0421\u043E\u043E\u0431\u0449\u0430\u0435\u043C \u043E \u043D\u043E\u0432\u043E\u0439 \u0430\u043A\u0446\u0438\u0438..." }), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 4, marginTop: 6 } }, ["B", "I", "U", "S", "\u{1F517}"].map((t) => /* @__PURE__ */ React.createElement("button", { key: t, className: "btn btn-secondary btn-sm", style: { minWidth: 28, padding: 0 } }, t)))), /* @__PURE__ */ React.createElement(Field, { label: "\u{1F5BC}\uFE0F \u0424\u043E\u0442\u043E (\u043E\u043F\u0446\u0438\u043E\u043D\u0430\u043B\u044C\u043D\u043E)", hint: "\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u0435 \u0438\u0437\u043E\u0431\u0440\u0430\u0436\u0435\u043D\u0438\u0435 \u2014 \u0442\u0435\u043A\u0441\u0442 \u0431\u0443\u0434\u0435\u0442 \u043E\u0442\u043F\u0440\u0430\u0432\u043B\u0435\u043D \u043A\u0430\u043A \u043F\u043E\u0434\u043F\u0438\u0441\u044C" }, /* @__PURE__ */ React.createElement("div", { style: {
    border: "1.5px dashed var(--border-strong)",
    borderRadius: 8,
    padding: 24,
    textAlign: "center",
    cursor: "pointer",
    background: "var(--surface-2)",
    color: "var(--text-muted)"
  } }, /* @__PURE__ */ React.createElement(Icon, { name: "image", size: 20 }), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 6, fontSize: 12.5 } }, "Tashlang yoki ", /* @__PURE__ */ React.createElement("span", { style: { color: "var(--primary)" } }, "tanlang"))))), /* @__PURE__ */ React.createElement(FormBlock, { title: "\u0422\u0435\u0441\u0442\u043E\u0432\u0430\u044F \u043E\u0442\u043F\u0440\u0430\u0432\u043A\u0430", icon: "zap", single: true }, /* @__PURE__ */ React.createElement(Field, { label: "\u{1F464} Test \u044E\u0431\u043E\u0440\u0438\u0448", hint: "\u041E\u0442\u043F\u0440\u0430\u0432\u0438\u0442 \u0441\u043E\u043E\u0431\u0449\u0435\u043D\u0438\u0435 \u0442\u043E\u043B\u044C\u043A\u043E \u044D\u0442\u043E\u043C\u0443 \u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u0435\u043B\u044E \u0434\u043B\u044F \u043F\u0440\u043E\u0432\u0435\u0440\u043A\u0438" }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 8 } }, /* @__PURE__ */ React.createElement("div", { className: "input-group", style: { flex: 1 } }, /* @__PURE__ */ React.createElement("span", { className: "prefix" }, /* @__PURE__ */ React.createElement(Icon, { name: "search", size: 14 })), /* @__PURE__ */ React.createElement("input", { className: "input", placeholder: "\u041F\u043E\u0438\u0441\u043A \u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u0435\u043B\u044F..." })), /* @__PURE__ */ React.createElement(Button, { variant: "secondary", icon: "send" }, "\u0422\u0435\u0441\u0442")))), /* @__PURE__ */ React.createElement("div", { className: "form-footer" }, /* @__PURE__ */ React.createElement("span", { className: "text-muted text-sm" }, "\u0411\u0443\u0434\u0435\u0442 \u043E\u0442\u043F\u0440\u0430\u0432\u043B\u0435\u043D\u043E \u0432 ~23 \u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u0435\u043B\u0435\u0439"), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 8 } }, /* @__PURE__ */ React.createElement(Button, { variant: "secondary" }, "\u041E\u0442\u043C\u0435\u043D\u0430"), /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "send" }, "\u041E\u0442\u043F\u0440\u0430\u0432\u0438\u0442\u044C")))), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", flexDirection: "column", gap: 16, position: "sticky", top: 80 } }, /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "card-header" }, /* @__PURE__ */ React.createElement("h3", null, "\u041F\u0440\u0435\u0434\u0432\u0430\u0440\u0438\u0442\u0435\u043B\u044C\u043D\u044B\u0439 \u043F\u0440\u043E\u0441\u043C\u043E\u0442\u0440")), /* @__PURE__ */ React.createElement("div", { style: { padding: 16, background: "var(--surface-2)" } }, /* @__PURE__ */ React.createElement("div", { style: {
    background: "linear-gradient(135deg, #1a1f2b, #11151e)",
    borderRadius: 10,
    padding: 12,
    border: "1px solid var(--border)",
    maxWidth: "100%"
  } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 8, marginBottom: 8 } }, /* @__PURE__ */ React.createElement(Avatar, { name: "JIP GROUP", size: 28 }), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 12, color: "var(--text-strong)", fontWeight: 500 } }, "JIP GROUP Bot"), /* @__PURE__ */ React.createElement("div", { style: { fontSize: 10.5, color: "var(--text-dim)" } }, "\u0447\u0435\u0440\u0435\u0437 \u0431\u043E\u0442\u0430"))), /* @__PURE__ */ React.createElement("div", { style: {
    background: "rgba(99,102,241,0.12)",
    padding: 10,
    borderRadius: 8,
    fontSize: 12.5,
    color: "var(--text)",
    borderTopLeftRadius: 2
  } }, "\u0417\u0434\u0440\u0430\u0432\u0441\u0442\u0432\u0443\u0439\u0442\u0435! \u0421\u043E\u043E\u0431\u0449\u0430\u0435\u043C \u043E \u043D\u043E\u0432\u043E\u0439 \u0430\u043A\u0446\u0438\u0438 \u2014 \u043F\u043E\u0441\u0435\u0442\u0438\u0442\u0435 \u0431\u043B\u0438\u0436\u0430\u0439\u0448\u0438\u0439 \u043C\u0430\u0433\u0430\u0437\u0438\u043D JIP \u0438 \u043F\u043E\u043B\u0443\u0447\u0438\u0442\u0435 \u0441\u043A\u0438\u0434\u043A\u0443 15%."), /* @__PURE__ */ React.createElement("div", { style: { fontSize: 10, color: "var(--text-dim)", marginTop: 4, textAlign: "right" } }, "14:32")))), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "card-header" }, /* @__PURE__ */ React.createElement("h3", null, "\u0418\u0441\u0442\u043E\u0440\u0438\u044F \u0440\u0430\u0441\u0441\u044B\u043B\u043E\u043A")), /* @__PURE__ */ React.createElement("div", null, J.regionMessages.slice(0, 4).map((m) => /* @__PURE__ */ React.createElement("div", { key: m.id, style: { padding: "10px 16px", borderBottom: "1px solid var(--border)", fontSize: 12.5 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "space-between", alignItems: "center" } }, /* @__PURE__ */ React.createElement("span", { className: "text-strong" }, m.region), m.status === "done" && /* @__PURE__ */ React.createElement(Badge, { variant: "success", size: "sm", icon: "check" }, "Done"), m.status === "pending" && /* @__PURE__ */ React.createElement(Badge, { variant: "warning", size: "sm", icon: "clock" }, "Pending"), m.status === "error" && /* @__PURE__ */ React.createElement(Badge, { variant: "danger", size: "sm", icon: "x" }, "Error")), /* @__PURE__ */ React.createElement("div", { className: "text-dim text-xs text-mono", style: { marginTop: 2 } }, m.date, " \xB7 ", m.sent, "/", m.total))))))));
}
function SendSingleMessagePage() {
  const recipients = J.users.slice(0, 1);
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement("div", { className: "gradient-banner" }, /* @__PURE__ */ React.createElement("h2", null, /* @__PURE__ */ React.createElement(Icon, { name: "message-square", size: 20 }), " \xA0\u041E\u0442\u043F\u0440\u0430\u0432\u0438\u0442\u044C \u0441\u043E\u043E\u0431\u0449\u0435\u043D\u0438\u0435 \u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u0435\u043B\u044E"), /* @__PURE__ */ React.createElement("p", null, "\u041B\u0438\u0447\u043D\u043E\u0435 \u0441\u043E\u043E\u0431\u0449\u0435\u043D\u0438\u0435 \u0447\u0435\u0440\u0435\u0437 \u0431\u043E\u0442\u0430. \u041F\u043E\u0434\u0434\u0435\u0440\u0436\u0438\u0432\u0430\u0435\u0442\u0441\u044F HTML \u0438 Markdown \u0444\u043E\u0440\u043C\u0430\u0442\u0438\u0440\u043E\u0432\u0430\u043D\u0438\u0435."), /* @__PURE__ */ React.createElement("div", { className: "banner-badge" }, /* @__PURE__ */ React.createElement(Icon, { name: "users", size: 11 }), " \xA0\u0412\u044B\u0431\u0440\u0430\u043D\u043E \u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u0435\u043B\u0435\u0439: ", recipients.length)), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: "1fr 360px", gap: 20, alignItems: "start" } }, /* @__PURE__ */ React.createElement(FormBlock, { title: "\u0421\u043E\u043E\u0431\u0449\u0435\u043D\u0438\u0435", icon: "message-square", single: true }, /* @__PURE__ */ React.createElement(Field, { label: "\u{1F4AC} \u0422\u0435\u043A\u0441\u0442 \u0441\u043E\u043E\u0431\u0449\u0435\u043D\u0438\u044F", required: true }, /* @__PURE__ */ React.createElement(Textarea, { rows: 10, placeholder: "\u0417\u0434\u0440\u0430\u0432\u0441\u0442\u0432\u0443\u0439\u0442\u0435! \u0425\u043E\u0442\u0438\u043C \u0441\u043E\u043E\u0431\u0449\u0438\u0442\u044C..." })), /* @__PURE__ */ React.createElement(Field, { label: "\u0420\u0435\u0436\u0438\u043C \u043F\u0430\u0440\u0441\u0438\u043D\u0433\u0430" }, /* @__PURE__ */ React.createElement(Select, null, /* @__PURE__ */ React.createElement("option", null, "\u0411\u0435\u0437 \u0444\u043E\u0440\u043C\u0430\u0442\u0438\u0440\u043E\u0432\u0430\u043D\u0438\u044F"), /* @__PURE__ */ React.createElement("option", null, "HTML"), /* @__PURE__ */ React.createElement("option", null, "Markdown"))), /* @__PURE__ */ React.createElement("div", { className: "form-footer", style: { marginTop: 16, position: "static" } }, /* @__PURE__ */ React.createElement(Button, { variant: "secondary" }, "\u041E\u0442\u043C\u0435\u043D\u0430"), /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "send" }, "\u041E\u0442\u043F\u0440\u0430\u0432\u0438\u0442\u044C"))), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "card-header" }, /* @__PURE__ */ React.createElement("h3", null, "\u0421\u043F\u0438\u0441\u043E\u043A \u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u0435\u043B\u0435\u0439"), /* @__PURE__ */ React.createElement(Badge, { variant: "neutral" }, recipients.length)), /* @__PURE__ */ React.createElement("div", null, recipients.map((u) => /* @__PURE__ */ React.createElement("div", { key: u.id, style: { padding: "12px 16px", borderBottom: "1px solid var(--border)" } }, /* @__PURE__ */ React.createElement("div", { className: "user-cell" }, /* @__PURE__ */ React.createElement(Avatar, { name: u.first_name + " " + u.last_name }), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { className: "user-name" }, u.first_name, " ", u.last_name, " ", /* @__PURE__ */ React.createElement("span", { className: "text-muted text-xs" }, "@", u.username)), /* @__PURE__ */ React.createElement("div", { className: "user-meta" }, "ID: ", u.id, " \xB7 ", u.phone)))))))));
}
function AuthUsersPage({ onNavigate }) {
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(
    PageHeader,
    {
      title: "Admin foydalanuvchilar",
      subtitle: "Django auth \u2014 admin paneliga kira oladigan foydalanuvchilar",
      actions: /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "plus" }, "Foydalanuvchi qo'shish")
    }
  ), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "filter-bar" }, /* @__PURE__ */ React.createElement(SearchBar, { placeholder: "\u041F\u043E\u0438\u0441\u043A username, email..." }), /* @__PURE__ */ React.createElement("div", { style: { flex: 1 } }), /* @__PURE__ */ React.createElement(FilterChip, { icon: "shield" }, "Roli"), /* @__PURE__ */ React.createElement(FilterChip, { icon: "check" }, "Faolligi")), /* @__PURE__ */ React.createElement("div", { className: "table-wrap" }, /* @__PURE__ */ React.createElement("table", { className: "table" }, /* @__PURE__ */ React.createElement("thead", null, /* @__PURE__ */ React.createElement("tr", null, /* @__PURE__ */ React.createElement("th", { className: "col-checkbox" }, /* @__PURE__ */ React.createElement("input", { className: "checkbox", type: "checkbox" })), /* @__PURE__ */ React.createElement("th", null, "Username"), /* @__PURE__ */ React.createElement("th", null, "Ism"), /* @__PURE__ */ React.createElement("th", null, "Email"), /* @__PURE__ */ React.createElement("th", null, "Roli"), /* @__PURE__ */ React.createElement("th", null, "Active"), /* @__PURE__ */ React.createElement("th", null, "\u0422\u0430\u043A last login"))), /* @__PURE__ */ React.createElement("tbody", null, J.authUsers.map((u) => /* @__PURE__ */ React.createElement("tr", { key: u.id }, /* @__PURE__ */ React.createElement("td", { className: "col-checkbox" }, /* @__PURE__ */ React.createElement("input", { className: "checkbox", type: "checkbox" })), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("div", { className: "user-cell" }, /* @__PURE__ */ React.createElement(Avatar, { name: u.name }), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { className: "user-name" }, u.username), /* @__PURE__ */ React.createElement("div", { className: "user-meta" }, "#", u.id)))), /* @__PURE__ */ React.createElement("td", null, u.name), /* @__PURE__ */ React.createElement("td", { className: "text-mono text-sm text-muted" }, u.email), /* @__PURE__ */ React.createElement("td", null, u.is_superuser ? /* @__PURE__ */ React.createElement(Badge, { variant: "danger", icon: "shield" }, "Superuser") : /* @__PURE__ */ React.createElement(Badge, { variant: "info", icon: "user" }, "Staff")), /* @__PURE__ */ React.createElement("td", null, u.is_staff ? /* @__PURE__ */ React.createElement(StatusBadges.active, null) : /* @__PURE__ */ React.createElement(StatusBadges.inactive, null)), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("span", { className: "text-mono text-xs text-muted" }, u.last_login))))))), /* @__PURE__ */ React.createElement(Pagination, { total: 4, page: 1, perPage: 25 })));
}
function AuthGroupsPage() {
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(
    PageHeader,
    {
      title: "Guruhlar",
      subtitle: "Foydalanuvchilar guruhlari va ruxsatlari",
      actions: /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "plus" }, "Guruh qo'shish")
    }
  ), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "table-wrap" }, /* @__PURE__ */ React.createElement("table", { className: "table" }, /* @__PURE__ */ React.createElement("thead", null, /* @__PURE__ */ React.createElement("tr", null, /* @__PURE__ */ React.createElement("th", { className: "col-checkbox" }, /* @__PURE__ */ React.createElement("input", { className: "checkbox", type: "checkbox" })), /* @__PURE__ */ React.createElement("th", null, "Guruh nomi"), /* @__PURE__ */ React.createElement("th", null, "Foydalanuvchilar"), /* @__PURE__ */ React.createElement("th", null, "Ruxsatlar"), /* @__PURE__ */ React.createElement("th", null))), /* @__PURE__ */ React.createElement("tbody", null, J.authGroups.map((g) => /* @__PURE__ */ React.createElement("tr", { key: g.id }, /* @__PURE__ */ React.createElement("td", { className: "col-checkbox" }, /* @__PURE__ */ React.createElement("input", { className: "checkbox", type: "checkbox" })), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 10 } }, /* @__PURE__ */ React.createElement("span", { style: { width: 28, height: 28, borderRadius: 6, background: "var(--primary-soft)", color: "var(--primary)", display: "grid", placeItems: "center" } }, /* @__PURE__ */ React.createElement(Icon, { name: "shield", size: 14 })), /* @__PURE__ */ React.createElement("span", { className: "text-strong", style: { fontWeight: 500 } }, g.name))), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement(Badge, { variant: "neutral" }, g.users_count, " ta")), /* @__PURE__ */ React.createElement("td", { className: "text-muted" }, g.permissions), /* @__PURE__ */ React.createElement("td", { style: { textAlign: "right" } }, /* @__PURE__ */ React.createElement(Button, { size: "sm", variant: "ghost", icon: "edit" }, "O'zgartirish")))))))));
}
Object.assign(window, {
  DashboardPage,
  AnalyticsPage,
  UsersListPage,
  UserSantenikPage,
  UserSotuvchiPage,
  SendRegionMessagePage,
  SendSingleMessagePage,
  AuthUsersPage,
  AuthGroupsPage
});
const JQ = window.JIP;
function QRCodesPage({ onNavigate }) {
  const [filter, setFilter] = useState({ scanned: "all" });
  const filtered = JQ.qrcodes.filter((q) => {
    if (filter.scanned === "scanned") return q.is_scanned;
    if (filter.scanned === "unscanned") return !q.is_scanned;
    return true;
  });
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(
    PageHeader,
    {
      title: "QR kodlar",
      subtitle: "Barcha generatsiya qilingan QR kodlar va ularning ishlatilish holati",
      actions: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(Select, { style: { width: 160 } }, /* @__PURE__ */ React.createElement("option", null, "\u041C\u0430\u0439 2026"), /* @__PURE__ */ React.createElement("option", null, "\u0410\u043F\u0440\u0435\u043B\u044C 2026"), /* @__PURE__ */ React.createElement("option", null, "\u041C\u0430\u0440\u0442 2026")), /* @__PURE__ */ React.createElement(Button, { variant: "success", icon: "download" }, "\u042D\u043A\u0441port oylik (Excel)"), /* @__PURE__ */ React.createElement(Button, { variant: "secondary", icon: "download", disabled: filter.scanned !== "scanned" }, "\u042D\u043A\u0441port tarix"), /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "plus", onClick: () => onNavigate("/qrcodes/generate") }, "Generatsiya"))
    }
  ), /* @__PURE__ */ React.createElement("div", { className: "kpi-grid" }, /* @__PURE__ */ React.createElement(KPI, { label: "Jami QR kodlar", value: "239", icon: "qrcode", color: "indigo", hint: "Hammasi" }), /* @__PURE__ */ React.createElement(KPI, { label: "Ishlatilgan", value: "47", icon: "check", color: "emerald", hint: "19.7% aktivatsiya" }), /* @__PURE__ */ React.createElement(KPI, { label: "Kutilmoqda", value: "192", icon: "clock", color: "amber", hint: "Hali skanlanmagan" }), /* @__PURE__ */ React.createElement(KPI, { label: "O'chirilgan", value: "0", icon: "trash", color: "rose", hint: "Tizimdan" })), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "filter-bar" }, /* @__PURE__ */ React.createElement(SearchBar, { placeholder: "Serial yoki kod bo'yicha qidirish..." }), /* @__PURE__ */ React.createElement("div", { style: { flex: 1 } }), /* @__PURE__ */ React.createElement(FilterChip, { icon: "store" }, "\u041C\u0430\u0433\u0430\u0437\u0438\u043D"), /* @__PURE__ */ React.createElement(FilterChip, { icon: "box" }, "\u041F\u0430\u0440\u0442\u0438\u044F"), /* @__PURE__ */ React.createElement(FilterChip, { icon: "check", active: filter.scanned !== "all", onClick: () => setFilter((f) => __spreadProps(__spreadValues({}, f), { scanned: f.scanned === "scanned" ? "unscanned" : f.scanned === "unscanned" ? "all" : "scanned" })) }, filter.scanned === "scanned" ? "\u0418\u0441\u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u043D" : filter.scanned === "unscanned" ? "\u041D\u0435 \u0438\u0441\u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u043D" : "Holat: Hammasi"), /* @__PURE__ */ React.createElement(FilterChip, { icon: "trash" }, "\u0423\u0434\u0430\u043B\u0451\u043D")), /* @__PURE__ */ React.createElement("div", { className: "table-wrap" }, /* @__PURE__ */ React.createElement("table", { className: "table" }, /* @__PURE__ */ React.createElement("thead", null, /* @__PURE__ */ React.createElement("tr", null, /* @__PURE__ */ React.createElement("th", { className: "col-checkbox" }, /* @__PURE__ */ React.createElement("input", { className: "checkbox", type: "checkbox" })), /* @__PURE__ */ React.createElement("th", null, "QR-\u043A\u043E\u0434"), /* @__PURE__ */ React.createElement("th", null, "Do'kon"), /* @__PURE__ */ React.createElement("th", null, "\u041F\u0430\u0440\u0442\u0438\u044F"), /* @__PURE__ */ React.createElement("th", { style: { textAlign: "right" } }, "\u0411\u0430\u043B\u043B\u044B"), /* @__PURE__ */ React.createElement("th", null, "\u0421\u0442\u0430\u0442\u0443\u0441"), /* @__PURE__ */ React.createElement("th", null, "\u041F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u0435\u043B\u044C"), /* @__PURE__ */ React.createElement("th", null, "Generated at"))), /* @__PURE__ */ React.createElement("tbody", null, filtered.slice(0, 25).map((q) => /* @__PURE__ */ React.createElement("tr", { key: q.id, onClick: () => onNavigate("/qrcodes/edit"), style: { cursor: "pointer" } }, /* @__PURE__ */ React.createElement("td", { className: "col-checkbox", onClick: (e) => e.stopPropagation() }, /* @__PURE__ */ React.createElement("input", { className: "checkbox", type: "checkbox" })), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 10 } }, /* @__PURE__ */ React.createElement("span", { style: {
    width: 32,
    height: 32,
    borderRadius: 6,
    background: "var(--surface-2)",
    border: "1px solid var(--border)",
    display: "grid",
    placeItems: "center",
    color: q.is_scanned ? "var(--success)" : "var(--text-muted)"
  } }, /* @__PURE__ */ React.createElement(Icon, { name: "qrcode", size: 16 })), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 13, color: "var(--text-strong)", fontWeight: 500 } }, "#", q.serial), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("span", { className: "code-mask" }, q.is_scanned ? q.code : "JIP*****E"))))), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement(Badge, { variant: "info", icon: "store" }, q.store_name)), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("span", { className: "text-mono text-xs" }, q.batch_name)), /* @__PURE__ */ React.createElement("td", { style: { textAlign: "right" } }, /* @__PURE__ */ React.createElement("span", { className: "text-mono", style: { color: "var(--primary)", fontWeight: 600 } }, q.points)), /* @__PURE__ */ React.createElement("td", null, q.is_scanned ? /* @__PURE__ */ React.createElement(StatusBadges.scanned, null) : /* @__PURE__ */ React.createElement(StatusBadges.unscanned, null)), /* @__PURE__ */ React.createElement("td", null, q.scanned_by_name ? /* @__PURE__ */ React.createElement("div", { className: "user-cell" }, /* @__PURE__ */ React.createElement(Avatar, { name: q.scanned_by_name, size: 26 }), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { className: "user-name", style: { fontSize: 12.5 } }, q.scanned_by_name), /* @__PURE__ */ React.createElement("div", { className: "user-meta" }, "ID: ", q.scanned_by_id))) : /* @__PURE__ */ React.createElement("span", { className: "text-dim text-sm" }, "\u2014")), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("span", { className: "text-mono text-xs text-muted" }, q.scanned_at || q.generated_at))))))), /* @__PURE__ */ React.createElement(Pagination, { total: 239, page: 1, perPage: 25 })));
}
function QRCodeEditPage({ onNavigate }) {
  const q = JQ.qrcodes.find((x) => x.is_scanned) || JQ.qrcodes[0];
  const isScanned = q.is_scanned;
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(
    PageHeader,
    {
      title: /* @__PURE__ */ React.createElement("span", null, "QR \u043A\u043E\u0434 #", q.serial),
      subtitle: /* @__PURE__ */ React.createElement("span", null, "\u041F\u0430\u0440\u0442\u0438\u044F: ", /* @__PURE__ */ React.createElement("span", { className: "text-mono" }, q.batch_name), " \xB7 Magazin: ", q.store_name),
      actions: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(Button, { variant: "ghost", icon: "history" }, "\u0418\u0441\u0442\u043E\u0440\u0438\u044F"), isScanned && /* @__PURE__ */ React.createElement(Button, { variant: "secondary", icon: "zap", style: { color: "var(--warning)", borderColor: "var(--warning)" } }, "\u26A0 Cancel Scans"), /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "check" }, "\u0421\u043E\u0445\u0440\u0430\u043D\u0438\u0442\u044C"))
    }
  ), !isScanned && /* @__PURE__ */ React.createElement("div", { style: {
    background: "var(--warning-soft)",
    border: "1px solid rgba(245, 158, 11, 0.3)",
    borderRadius: 12,
    padding: 16,
    display: "flex",
    alignItems: "flex-start",
    gap: 12
  } }, /* @__PURE__ */ React.createElement(Icon, { name: "lock", size: 20, style: { color: "var(--warning)", flexShrink: 0, marginTop: 2 } }), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { color: "var(--warning-fg)", fontWeight: 600, marginBottom: 2 } }, "\u0418\u043D\u0444\u043E\u0440\u043C\u0430\u0446\u0438\u044F \u043E \u0431\u0435\u0437\u043E\u043F\u0430\u0441\u043D\u043E\u0441\u0442\u0438"), /* @__PURE__ */ React.createElement("div", { style: { color: "var(--text-muted)", fontSize: 13 } }, "\u041A\u043E\u0434 QR-\u043A\u043E\u0434\u0430 \u0441\u043A\u0440\u044B\u0442 \u0434\u043B\u044F \u0431\u0435\u0437\u043E\u043F\u0430\u0441\u043D\u043E\u0441\u0442\u0438 \u0434\u043E \u0442\u043E\u0433\u043E \u043A\u0430\u043A \u043E\u043D \u0431\u0443\u0434\u0435\u0442 \u043E\u0442\u0441\u043A\u0430\u043D\u0438\u0440\u043E\u0432\u0430\u043D \u0441\u0430\u043D\u0438\u0442\u0430\u0440\u043D\u044B\u043C \u0442\u0435\u0445\u043D\u0438\u043A\u043E\u043C. \u0421\u0435\u0440\u0438\u0439\u043D\u044B\u0439 \u043D\u043E\u043C\u0435\u0440: ", /* @__PURE__ */ React.createElement("span", { className: "text-mono text-strong" }, q.serial)))), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 } }, /* @__PURE__ */ React.createElement(FormBlock, { title: "QR \u043A\u043E\u0434 ma'lumotlari", icon: "qrcode" }, /* @__PURE__ */ React.createElement(Field, { label: "Serial number", required: true }, /* @__PURE__ */ React.createElement(Input, { defaultValue: q.serial, readOnly: true })), /* @__PURE__ */ React.createElement(Field, { label: "Code", hint: isScanned ? "Visible \u2014 kod ishlatilgan" : "\u0421\u043A\u0440\u044B\u0442" }, /* @__PURE__ */ React.createElement("div", { className: "input", style: { fontFamily: "var(--font-mono)" } }, isScanned ? q.code : "JIP*****E")), /* @__PURE__ */ React.createElement(Field, { label: "Hash code", span2: true, hint: isScanned ? "Salted SHA-256" : "\u0421\u043A\u0440\u044B\u0442" }, /* @__PURE__ */ React.createElement("div", { className: "input", style: { fontFamily: "var(--font-mono)", fontSize: 11.5 } }, isScanned ? q.hash_code : "\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022")), /* @__PURE__ */ React.createElement(Field, { label: "Points" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: q.points })), /* @__PURE__ */ React.createElement(Field, { label: "\u041C\u0430\u0433\u0430\u0437\u0438\u043D" }, /* @__PURE__ */ React.createElement(Select, { defaultValue: q.store_name }, JQ.stores.map((s) => /* @__PURE__ */ React.createElement("option", { key: s.id }, s.name)))), /* @__PURE__ */ React.createElement(Field, { label: "\u041F\u0430\u0440\u0442\u0438\u044F" }, /* @__PURE__ */ React.createElement(Select, { defaultValue: q.batch_name }, JQ.batches.map((b) => /* @__PURE__ */ React.createElement("option", { key: b.id }, b.name)))), /* @__PURE__ */ React.createElement(Field, { label: "is_deleted" }, /* @__PURE__ */ React.createElement("label", { style: { display: "flex", alignItems: "center", gap: 8 } }, /* @__PURE__ */ React.createElement("input", { type: "checkbox", className: "checkbox" }), " ", /* @__PURE__ */ React.createElement("span", { className: "text-sm" }, "O'chirilgan")))), /* @__PURE__ */ React.createElement(FormBlock, { title: "Skanlash ma'lumotlari", icon: "check", badge: isScanned ? /* @__PURE__ */ React.createElement(Badge, { variant: "success", icon: "check" }, "\u0418\u0441\u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u043D") : /* @__PURE__ */ React.createElement(Badge, { variant: "warning", icon: "clock" }, "\u041D\u0435 \u0438\u0441\u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u043D") }, /* @__PURE__ */ React.createElement(Field, { label: "is_scanned" }, /* @__PURE__ */ React.createElement("label", { style: { display: "flex", alignItems: "center", gap: 8 } }, /* @__PURE__ */ React.createElement("input", { type: "checkbox", className: "checkbox", defaultChecked: isScanned }), " ", /* @__PURE__ */ React.createElement("span", { className: "text-sm" }, "Skanlangan"))), /* @__PURE__ */ React.createElement(Field, { label: "Scanned at" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: q.scanned_at || "\u2014", readOnly: true })), /* @__PURE__ */ React.createElement(Field, { label: "Scanned by", span2: true }, q.scanned_by_name ? /* @__PURE__ */ React.createElement("div", { className: "input", style: { display: "flex", alignItems: "center", gap: 10 } }, /* @__PURE__ */ React.createElement(Avatar, { name: q.scanned_by_name, size: 22 }), /* @__PURE__ */ React.createElement("a", { style: { color: "var(--primary)", cursor: "pointer" }, onClick: () => onNavigate("/users/santenik") }, q.scanned_by_name, " \xB7 ID ", q.scanned_by_id)) : /* @__PURE__ */ React.createElement(Input, { defaultValue: "\u2014", readOnly: true })), /* @__PURE__ */ React.createElement(Field, { label: "Generated at", span2: true }, /* @__PURE__ */ React.createElement(Input, { defaultValue: q.generated_at, readOnly: true })))), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "card-header" }, /* @__PURE__ */ React.createElement("h3", null, "QR \u043A\u043E\u0434 urunishlari"), /* @__PURE__ */ React.createElement(Badge, { variant: "neutral" }, "3 ta")), /* @__PURE__ */ React.createElement("div", { className: "table-wrap" }, /* @__PURE__ */ React.createElement("table", { className: "table inline-table" }, /* @__PURE__ */ React.createElement("thead", null, /* @__PURE__ */ React.createElement("tr", null, /* @__PURE__ */ React.createElement("th", null, "Attempted at"), /* @__PURE__ */ React.createElement("th", null, "Raw code"), /* @__PURE__ */ React.createElement("th", null, "Status"), /* @__PURE__ */ React.createElement("th", null, "Source"))), /* @__PURE__ */ React.createElement("tbody", null, /* @__PURE__ */ React.createElement("tr", null, /* @__PURE__ */ React.createElement("td", { className: "text-mono text-xs text-muted" }, "2026-05-25 14:32:18"), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("span", { className: "code-mask" }, "jip", q.code.slice(3, 8).toLowerCase(), "e")), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement(Badge, { variant: "success", size: "sm" }, "success")), /* @__PURE__ */ React.createElement("td", null, "Telegram bot")), /* @__PURE__ */ React.createElement("tr", null, /* @__PURE__ */ React.createElement("td", { className: "text-mono text-xs text-muted" }, "2026-05-25 14:31:42"), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("span", { className: "code-mask" }, "jip0000e")), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement(Badge, { variant: "danger", size: "sm" }, "failed")), /* @__PURE__ */ React.createElement("td", null, "Telegram bot")), /* @__PURE__ */ React.createElement("tr", null, /* @__PURE__ */ React.createElement("td", { className: "text-mono text-xs text-muted" }, "2026-05-25 14:31:18"), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("span", { className: "code-mask" }, "jipxxxxe")), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement(Badge, { variant: "danger", size: "sm" }, "failed")), /* @__PURE__ */ React.createElement("td", null, "Telegram bot")))))));
}
function QRGeneratePage() {
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(PageHeader, { title: "QR generatsiya", subtitle: "Bir tanlovda \u043F\u0430\u0440\u0442\u0438\u044F uchun barcha QR kodlarini avtomatik generatsiya qilish" }), /* @__PURE__ */ React.createElement(FormBlock, { title: "Yangi QR partiyasini generatsiya qilish", icon: "sparkles" }, /* @__PURE__ */ React.createElement(Field, { label: "Partiya nomi", required: true }, /* @__PURE__ */ React.createElement(Input, { placeholder: "S27-MAY-2026" })), /* @__PURE__ */ React.createElement(Field, { label: "Sotuvchi (autocomplete)", required: true }, /* @__PURE__ */ React.createElement(Select, null, /* @__PURE__ */ React.createElement("option", null, "\u2014 Tanlang \u2014"), JQ.users.filter((u) => u.type === "sotuvchi").slice(0, 8).map((u) => /* @__PURE__ */ React.createElement("option", { key: u.id }, u.first_name, " ", u.last_name, " (@", u.username, ")")))), /* @__PURE__ */ React.createElement(Field, { label: "Magazin", required: true }, /* @__PURE__ */ React.createElement(Select, null, JQ.stores.map((s) => /* @__PURE__ */ React.createElement("option", { key: s.id }, s.name)))), /* @__PURE__ */ React.createElement(Field, { label: "Kartalar soni", required: true, hint: "Har karta 50 ball" }, /* @__PURE__ */ React.createElement(Input, { type: "number", defaultValue: 50, min: 1, max: 500 })), /* @__PURE__ */ React.createElement(Field, { label: "Har karta uchun ball" }, /* @__PURE__ */ React.createElement(Input, { type: "number", defaultValue: 50 })), /* @__PURE__ */ React.createElement(Field, { label: "Status" }, /* @__PURE__ */ React.createElement(Select, null, /* @__PURE__ */ React.createElement("option", null, "Faollashtirilmagan"), /* @__PURE__ */ React.createElement("option", null, "Faollashtirilgan"))), /* @__PURE__ */ React.createElement("div", { className: "span-2", style: {
    padding: 16,
    background: "var(--primary-soft)",
    borderRadius: 8,
    fontSize: 13,
    borderLeft: "3px solid var(--primary)",
    color: "var(--text)"
  } }, /* @__PURE__ */ React.createElement("strong", null, "50 \xD7 50 = 2,500 ball"), " sotuvchiga avtomatik qo'shiladi. Saqlangandan keyin QR kodlar generatsiya qilinadi va ZIP fayl yuklab olish uchun tayyor bo'ladi.")), /* @__PURE__ */ React.createElement("div", { className: "form-footer" }, /* @__PURE__ */ React.createElement("span", { className: "text-muted text-sm" }, "Generatsiya 5-15 soniya davom etadi"), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 8 } }, /* @__PURE__ */ React.createElement(Button, { variant: "secondary" }, "Bekor qilish"), /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "sparkles" }, "Generatsiya qilish"))));
}
function BatchesPage({ onNavigate }) {
  const colorFor = (pct) => pct >= 50 ? "success" : pct >= 20 ? "warning" : "danger";
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(
    PageHeader,
    {
      title: "\u041F\u0430\u0440\u0442\u0438\u0438",
      subtitle: "QR kodlar partiyalari \u2014 har biri 50-400 ta kartani o'z ichiga oladi",
      actions: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(Button, { variant: "secondary", icon: "download" }, "Eksport"), /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "plus", onClick: () => onNavigate("/batches/add") }, "Yangi \u043F\u0430\u0440\u0442\u0438\u044F"))
    }
  ), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "filter-bar" }, /* @__PURE__ */ React.createElement(SearchBar, { placeholder: "\u041F\u0430\u0440\u0442\u0438\u044F nomi yoki sotuvchi..." }), /* @__PURE__ */ React.createElement("div", { style: { flex: 1 } }), /* @__PURE__ */ React.createElement(FilterChip, { icon: "store" }, "\u041C\u0430\u0433\u0430\u0437\u0438\u043D"), /* @__PURE__ */ React.createElement(FilterChip, { icon: "users" }, "Sotuvchi"), /* @__PURE__ */ React.createElement(FilterChip, { icon: "check", active: true }, "Holat: Faol")), /* @__PURE__ */ React.createElement("div", { className: "table-wrap" }, /* @__PURE__ */ React.createElement("table", { className: "table" }, /* @__PURE__ */ React.createElement("thead", null, /* @__PURE__ */ React.createElement("tr", null, /* @__PURE__ */ React.createElement("th", { className: "col-checkbox" }, /* @__PURE__ */ React.createElement("input", { className: "checkbox", type: "checkbox" })), /* @__PURE__ */ React.createElement("th", null, "\u041F\u0430\u0440\u0442\u0438\u044F nomi"), /* @__PURE__ */ React.createElement("th", null, "Sotuvchi"), /* @__PURE__ */ React.createElement("th", { style: { textAlign: "right" } }, "Miqdor"), /* @__PURE__ */ React.createElement("th", { style: { textAlign: "right" } }, "Ball/karta"), /* @__PURE__ */ React.createElement("th", null, "Aktivatsiya"), /* @__PURE__ */ React.createElement("th", { style: { textAlign: "right" } }, "Skanlangan"), /* @__PURE__ */ React.createElement("th", null, "Holat"), /* @__PURE__ */ React.createElement("th", null, "Yetkazib berish"))), /* @__PURE__ */ React.createElement("tbody", null, JQ.batches.map((b) => /* @__PURE__ */ React.createElement("tr", { key: b.id, onClick: () => onNavigate("/batches/edit"), style: { cursor: "pointer" } }, /* @__PURE__ */ React.createElement("td", { className: "col-checkbox", onClick: (e) => e.stopPropagation() }, /* @__PURE__ */ React.createElement("input", { className: "checkbox", type: "checkbox" })), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 10 } }, /* @__PURE__ */ React.createElement("span", { style: { width: 32, height: 32, borderRadius: 6, background: "var(--primary-soft)", color: "var(--primary)", display: "grid", placeItems: "center" } }, /* @__PURE__ */ React.createElement(Icon, { name: "box", size: 14 })), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { className: "text-mono text-strong", style: { fontSize: 13, fontWeight: 500 } }, b.name), /* @__PURE__ */ React.createElement("div", { className: "text-xs text-muted" }, b.store_name)))), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("div", { className: "user-cell" }, /* @__PURE__ */ React.createElement(Avatar, { name: b.seller_name, size: 26 }), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { className: "user-name", style: { fontSize: 12.5 } }, b.seller_name), /* @__PURE__ */ React.createElement("div", { className: "user-meta" }, "ID: ", b.seller_id)))), /* @__PURE__ */ React.createElement("td", { className: "num", style: { textAlign: "right" } }, b.quantity), /* @__PURE__ */ React.createElement("td", { className: "num", style: { textAlign: "right", color: "var(--primary)" } }, b.points_per_card), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", flexDirection: "column", gap: 4, minWidth: 100 } }, /* @__PURE__ */ React.createElement("span", { className: "text-mono text-xs", style: { color: b.activation_pct >= 50 ? "var(--success-fg)" : b.activation_pct >= 20 ? "var(--warning-fg)" : "var(--danger-fg)" } }, b.activation_pct.toFixed(1), "%"), /* @__PURE__ */ React.createElement("div", { className: "progress " + colorFor(b.activation_pct) }, /* @__PURE__ */ React.createElement("div", { style: { width: Math.min(b.activation_pct, 100) + "%" } })))), /* @__PURE__ */ React.createElement("td", { className: "num", style: { textAlign: "right" } }, b.scanned, "/", b.quantity), /* @__PURE__ */ React.createElement("td", null, b.status === "active" ? /* @__PURE__ */ React.createElement(Badge, { variant: "success", dot: true }, "Faol") : b.status === "pending" ? /* @__PURE__ */ React.createElement(Badge, { variant: "warning", dot: true }, "Kutilmoqda") : /* @__PURE__ */ React.createElement(Badge, { variant: "neutral", dot: true }, "Arxiv")), /* @__PURE__ */ React.createElement("td", null, b.delivery === "delivered" ? /* @__PURE__ */ React.createElement(Badge, { variant: "success", icon: "check", size: "sm" }, "\u0414\u043E\u0441\u0442\u0430\u0432\u043B\u0435\u043D\u043E") : b.delivery === "in_transit" ? /* @__PURE__ */ React.createElement(Badge, { variant: "info", icon: "send", size: "sm" }, "\u0412 \u043F\u0443\u0442\u0438") : /* @__PURE__ */ React.createElement(Badge, { variant: "warning", icon: "clock", size: "sm" }, "\u041E\u0436\u0438\u0434\u0430\u0435\u0442"))))))), /* @__PURE__ */ React.createElement(Pagination, { total: 17, page: 1, perPage: 25 })));
}
function BatchAddPage() {
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(PageHeader, { title: "Yangi \u043F\u0430\u0440\u0442\u0438\u044F", subtitle: "Sotuvchi tanlang va miqdorni kiriting" }), /* @__PURE__ */ React.createElement(FormBlock, { title: "\u041F\u0430\u0440\u0442\u0438\u044F ma'lumotlari", icon: "box" }, /* @__PURE__ */ React.createElement(Field, { label: "Sotuvchi (autocomplete)", required: true, hint: "Ballar (50 \xD7 miqdor) sotuvchiga avtomatik qo'shiladi", span2: true }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 8 } }, /* @__PURE__ */ React.createElement(Select, { style: { flex: 1 } }, /* @__PURE__ */ React.createElement("option", null, "\u2014 Sotuvchini tanlang \u2014"), JQ.users.filter((u) => u.type === "sotuvchi").slice(0, 10).map((u) => /* @__PURE__ */ React.createElement("option", { key: u.id }, u.first_name, " ", u.last_name, " (@", u.username, ") \xB7 ", u.region))), /* @__PURE__ */ React.createElement(Button, { variant: "secondary", icon: "edit" }), /* @__PURE__ */ React.createElement(Button, { variant: "secondary", icon: "plus" }), /* @__PURE__ */ React.createElement(Button, { variant: "secondary", icon: "eye" }))), /* @__PURE__ */ React.createElement(Field, { label: "Miqdor (kartalar soni)", required: true, hint: "1 dan 500 gacha" }, /* @__PURE__ */ React.createElement(Input, { type: "number", defaultValue: 50, min: 1, max: 500 })), /* @__PURE__ */ React.createElement(Field, { label: "Magazin" }, /* @__PURE__ */ React.createElement(Select, null, JQ.stores.map((s) => /* @__PURE__ */ React.createElement("option", { key: s.id }, s.name)))), /* @__PURE__ */ React.createElement("div", { className: "span-2", style: {
    padding: 16,
    background: "var(--primary-soft)",
    borderRadius: 8,
    fontSize: 13,
    borderLeft: "3px solid var(--primary)",
    display: "flex",
    alignItems: "center",
    gap: 12
  } }, /* @__PURE__ */ React.createElement(Icon, { name: "sparkles", size: 18, style: { color: "var(--primary)", flexShrink: 0 } }), /* @__PURE__ */ React.createElement("span", null, /* @__PURE__ */ React.createElement("strong", null, "QR kodlar saqlangandan keyin avtomatik generatsiya qilinadi."), " Sotuvchiga 2 500 ball qo'shiladi."))), /* @__PURE__ */ React.createElement("div", { className: "form-footer" }, /* @__PURE__ */ React.createElement("span", { className: "text-muted text-sm" }, "Yangi yozuv"), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 8 } }, /* @__PURE__ */ React.createElement(Button, { variant: "ghost" }, "\u0421\u043E\u0445\u0440\u0430\u043D\u0438\u0442\u044C \u0438 \u0434\u043E\u0431\u0430\u0432\u0438\u0442\u044C"), /* @__PURE__ */ React.createElement(Button, { variant: "secondary" }, "\u0421\u043E\u0445\u0440\u0430\u043D\u0438\u0442\u044C \u0438 \u043F\u0440\u043E\u0434\u043E\u043B\u0436\u0438\u0442\u044C"), /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "check" }, "Saqlash"))));
}
function BatchEditPage({ onNavigate }) {
  const b = JQ.batches[0];
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(
    PageHeader,
    {
      title: /* @__PURE__ */ React.createElement("span", null, "\u041F\u0430\u0440\u0442\u0438\u044F ", /* @__PURE__ */ React.createElement("span", { className: "text-mono" }, b.name)),
      subtitle: /* @__PURE__ */ React.createElement("span", null, b.scanned, "/", b.quantity, " ishlatilgan \xB7 ", b.activation_pct.toFixed(1), "% aktivatsiya"),
      actions: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(Button, { variant: "secondary", icon: "download" }, "ZIP yuklab olish"), /* @__PURE__ */ React.createElement(Button, { variant: "ghost", icon: "history" }, "\u0418\u0441\u0442\u043E\u0440\u0438\u044F"), /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "check" }, "\u0421\u043E\u0445\u0440\u0430\u043D\u0438\u0442\u044C"))
    }
  ), /* @__PURE__ */ React.createElement("div", { className: "kpi-grid" }, /* @__PURE__ */ React.createElement(KPI, { label: "Jami QR", value: b.quantity, icon: "qrcode", color: "indigo" }), /* @__PURE__ */ React.createElement(KPI, { label: "Skanlangan", value: b.scanned, icon: "check", color: "emerald" }), /* @__PURE__ */ React.createElement(KPI, { label: "Aktivatsiya", value: b.activation_pct.toFixed(1) + "%", icon: "trending-up", color: b.activation_pct >= 50 ? "emerald" : b.activation_pct >= 20 ? "amber" : "rose" }), /* @__PURE__ */ React.createElement(KPI, { label: "Ball/karta", value: b.points_per_card, icon: "coin", color: "blue" })), /* @__PURE__ */ React.createElement(FormBlock, { title: "\u041F\u0430\u0440\u0442\u0438\u044F ma'lumotlari", icon: "box" }, /* @__PURE__ */ React.createElement(Field, { label: "\u041F\u0430\u0440\u0442\u0438\u044F nomi", required: true }, /* @__PURE__ */ React.createElement(Input, { defaultValue: b.name })), /* @__PURE__ */ React.createElement(Field, { label: "Status" }, /* @__PURE__ */ React.createElement(Select, { defaultValue: b.status }, /* @__PURE__ */ React.createElement("option", { value: "pending" }, "Faollashtirilmagan"), /* @__PURE__ */ React.createElement("option", { value: "active" }, "Faollashtirilgan"), /* @__PURE__ */ React.createElement("option", { value: "archived" }, "Arxivlangan"))), /* @__PURE__ */ React.createElement(Field, { label: "Sotuvchi", required: true }, /* @__PURE__ */ React.createElement("div", { className: "input", style: { display: "flex", alignItems: "center", gap: 10 } }, /* @__PURE__ */ React.createElement(Avatar, { name: b.seller_name, size: 22 }), /* @__PURE__ */ React.createElement("a", { style: { color: "var(--primary)", cursor: "pointer" }, onClick: () => onNavigate("/users/sotuvchi") }, b.seller_name))), /* @__PURE__ */ React.createElement(Field, { label: "Magazin" }, /* @__PURE__ */ React.createElement(Select, { defaultValue: b.store_name }, JQ.stores.map((s) => /* @__PURE__ */ React.createElement("option", { key: s.id }, s.name)))), /* @__PURE__ */ React.createElement(Field, { label: "Miqdor" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: b.quantity, readOnly: true })), /* @__PURE__ */ React.createElement(Field, { label: "Ball/karta" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: b.points_per_card })), /* @__PURE__ */ React.createElement(Field, { label: "Yetkazib berish holati" }, /* @__PURE__ */ React.createElement(Select, { defaultValue: b.delivery }, /* @__PURE__ */ React.createElement("option", { value: "pending" }, "\u041E\u0436\u0438\u0434\u0430\u0435\u0442"), /* @__PURE__ */ React.createElement("option", { value: "in_transit" }, "\u0412 \u043F\u0443\u0442\u0438"), /* @__PURE__ */ React.createElement("option", { value: "delivered" }, "\u0414\u043E\u0441\u0442\u0430\u0432\u043B\u0435\u043D\u043E"))), /* @__PURE__ */ React.createElement(Field, { label: "Yaratilgan" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: b.created_at + " 09:42", readOnly: true }))), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "card-header" }, /* @__PURE__ */ React.createElement("h3", null, "QR kodlar ro'yxati"), /* @__PURE__ */ React.createElement(Badge, { variant: "neutral" }, b.quantity, " ta")), /* @__PURE__ */ React.createElement("div", { className: "table-wrap", style: { maxHeight: 400 } }, /* @__PURE__ */ React.createElement("table", { className: "table inline-table" }, /* @__PURE__ */ React.createElement("thead", null, /* @__PURE__ */ React.createElement("tr", null, /* @__PURE__ */ React.createElement("th", null, "Serial"), /* @__PURE__ */ React.createElement("th", null, "Code"), /* @__PURE__ */ React.createElement("th", { style: { textAlign: "right" } }, "Ball"), /* @__PURE__ */ React.createElement("th", null, "Status"), /* @__PURE__ */ React.createElement("th", null, "Skanlangan"))), /* @__PURE__ */ React.createElement("tbody", null, JQ.qrcodes.filter((q) => q.batch_name === b.name).slice(0, 15).map((q) => /* @__PURE__ */ React.createElement("tr", { key: q.id }, /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("span", { className: "code-mask" }, "#", q.serial)), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("span", { className: "code-mask" }, q.is_scanned ? q.code : "JIP*****E")), /* @__PURE__ */ React.createElement("td", { className: "num text-mono", style: { textAlign: "right", color: "var(--primary)" } }, q.points), /* @__PURE__ */ React.createElement("td", null, q.is_scanned ? /* @__PURE__ */ React.createElement(StatusBadges.scanned, null) : /* @__PURE__ */ React.createElement(StatusBadges.unscanned, null)), /* @__PURE__ */ React.createElement("td", { className: "text-xs text-mono text-muted" }, q.scanned_by_name || "\u2014"))))))));
}
function StoresPage({ onNavigate }) {
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(
    PageHeader,
    {
      title: "Do'konlar",
      subtitle: "JIP partneri bo'lgan barcha do'konlar",
      actions: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(Button, { variant: "secondary", icon: "download" }, "Eksport"), /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "plus", onClick: () => onNavigate("/stores/add") }, "Yangi do'kon"))
    }
  ), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "filter-bar" }, /* @__PURE__ */ React.createElement(SearchBar, { placeholder: "Do'kon nomi, telefoni..." }), /* @__PURE__ */ React.createElement("div", { style: { flex: 1 } }), /* @__PURE__ */ React.createElement(FilterChip, { icon: "map-pin" }, "Viloyat"), /* @__PURE__ */ React.createElement(FilterChip, { icon: "check" }, "Faollik")), /* @__PURE__ */ React.createElement("div", { className: "table-wrap" }, /* @__PURE__ */ React.createElement("table", { className: "table" }, /* @__PURE__ */ React.createElement("thead", null, /* @__PURE__ */ React.createElement("tr", null, /* @__PURE__ */ React.createElement("th", null, "Do'kon"), /* @__PURE__ */ React.createElement("th", null, "Viloyat / Tuman"), /* @__PURE__ */ React.createElement("th", null, "Egasi"), /* @__PURE__ */ React.createElement("th", null, "Telefon"), /* @__PURE__ */ React.createElement("th", { style: { textAlign: "right" } }, "\u041F\u0430\u0440\u0442\u0438\u044F"), /* @__PURE__ */ React.createElement("th", null, "Aktivatsiya"), /* @__PURE__ */ React.createElement("th", { style: { textAlign: "right" } }, "Komissiya"), /* @__PURE__ */ React.createElement("th", null, "Holat"))), /* @__PURE__ */ React.createElement("tbody", null, JQ.stores.map((s) => {
    const pct = s.scanned_qr / s.total_qr * 100;
    const color = pct >= 50 ? "var(--success-fg)" : pct >= 20 ? "var(--warning-fg)" : "var(--danger-fg)";
    return /* @__PURE__ */ React.createElement("tr", { key: s.id, onClick: () => onNavigate("/stores/edit"), style: { cursor: "pointer" } }, /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 10 } }, /* @__PURE__ */ React.createElement("span", { style: { width: 32, height: 32, borderRadius: 6, background: "var(--info-soft)", color: "var(--info)", display: "grid", placeItems: "center" } }, /* @__PURE__ */ React.createElement(Icon, { name: "store", size: 15 })), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { className: "text-strong", style: { fontWeight: 500 } }, s.name), /* @__PURE__ */ React.createElement("div", { className: "text-xs text-muted" }, s.address)))), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", flexDirection: "column", gap: 3 } }, /* @__PURE__ */ React.createElement(Badge, { variant: "info", icon: "map-pin" }, s.region.replace(" \u043E\u0431\u043B\u0430\u0441\u0442\u044C", "").replace("\u0413\u043E\u0440\u043E\u0434 ", "")), /* @__PURE__ */ React.createElement(Badge, { variant: "warning", outline: true, size: "sm" }, s.district))), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("div", { className: "user-cell" }, /* @__PURE__ */ React.createElement(Avatar, { name: s.owner_name, size: 26 }), /* @__PURE__ */ React.createElement("span", { style: { fontSize: 12.5, color: "var(--text-strong)", fontWeight: 500 } }, s.owner_name))), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("span", { className: "text-mono text-sm" }, s.phone)), /* @__PURE__ */ React.createElement("td", { className: "num", style: { textAlign: "right" } }, s.batches_count), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", flexDirection: "column", gap: 4, minWidth: 110 } }, /* @__PURE__ */ React.createElement("span", { className: "text-mono text-xs", style: { color } }, pct.toFixed(1), "% (", s.scanned_qr, "/", s.total_qr, ")"), /* @__PURE__ */ React.createElement("div", { className: "progress" }, /* @__PURE__ */ React.createElement("div", { style: { width: Math.min(pct, 100) + "%", background: color } })))), /* @__PURE__ */ React.createElement("td", { className: "num", style: { textAlign: "right" } }, /* @__PURE__ */ React.createElement("span", { style: { color: "var(--primary)", fontWeight: 600 } }, s.commission_rate, "%")), /* @__PURE__ */ React.createElement("td", null, s.is_active ? /* @__PURE__ */ React.createElement(StatusBadges.active, null) : /* @__PURE__ */ React.createElement(StatusBadges.inactive, null)));
  })))), /* @__PURE__ */ React.createElement(Pagination, { total: 12, page: 1, perPage: 25 })));
}
function StoreEditPage({ onNavigate }) {
  const s = JQ.stores[0];
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(
    PageHeader,
    {
      title: s.name,
      subtitle: /* @__PURE__ */ React.createElement("span", null, s.region, " \xB7 ", s.district, " \xB7 ", s.batches_count, " ta \u043F\u0430\u0440\u0442\u0438\u044F"),
      actions: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(Button, { variant: "ghost", icon: "history" }, "\u0418\u0441\u0442\u043E\u0440\u0438\u044F"), /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "check" }, "\u0421\u043E\u0445\u0440\u0430\u043D\u0438\u0442\u044C"))
    }
  ), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 } }, /* @__PURE__ */ React.createElement(FormBlock, { title: "Asosiy ma'lumotlar", icon: "store" }, /* @__PURE__ */ React.createElement(Field, { label: "Do'kon nomi", required: true, span2: true }, /* @__PURE__ */ React.createElement(Input, { defaultValue: s.name })), /* @__PURE__ */ React.createElement(Field, { label: "Manzil", span2: true }, /* @__PURE__ */ React.createElement(Input, { defaultValue: s.address })), /* @__PURE__ */ React.createElement(Field, { label: "Viloyat (autocomplete)", required: true }, /* @__PURE__ */ React.createElement(Select, { defaultValue: s.region }, JQ.regions.map((r) => /* @__PURE__ */ React.createElement("option", { key: r }, r)))), /* @__PURE__ */ React.createElement(Field, { label: "Tuman", required: true }, /* @__PURE__ */ React.createElement(Select, { defaultValue: s.district }, (JQ.districtsByRegion[s.region] || ["\u2014"]).map((d) => /* @__PURE__ */ React.createElement("option", { key: d }, d)))), /* @__PURE__ */ React.createElement(Field, { label: "Egasi (autocomplete)", span2: true }, /* @__PURE__ */ React.createElement(Select, { defaultValue: s.owner_name }, JQ.users.filter((u) => u.type === "sotuvchi").slice(0, 12).map((u) => /* @__PURE__ */ React.createElement("option", { key: u.id }, u.first_name, " ", u.last_name)))), /* @__PURE__ */ React.createElement(Field, { label: "Telefon", required: true }, /* @__PURE__ */ React.createElement(Input, { defaultValue: s.phone })), /* @__PURE__ */ React.createElement(Field, { label: "Komissiya foizi", hint: "0-100%" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: s.commission_rate })), /* @__PURE__ */ React.createElement(Field, { label: "Faollik", span2: true }, /* @__PURE__ */ React.createElement("label", { style: { display: "flex", alignItems: "center", gap: 8 } }, /* @__PURE__ */ React.createElement("input", { type: "checkbox", className: "checkbox", defaultChecked: s.is_active }), " ", /* @__PURE__ */ React.createElement("span", { className: "text-sm" }, "Faol")))), /* @__PURE__ */ React.createElement(FormBlock, { title: "Aktivlik", icon: "bar-chart" }, /* @__PURE__ */ React.createElement("div", { className: "span-2", style: { display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 12 } }, /* @__PURE__ */ React.createElement("div", { style: { padding: 16, background: "var(--surface-2)", borderRadius: 8, border: "1px solid var(--border)" } }, /* @__PURE__ */ React.createElement("div", { className: "text-xs text-muted", style: { marginBottom: 4 } }, "Jami QR"), /* @__PURE__ */ React.createElement("div", { style: { fontSize: 24, fontWeight: 600, color: "var(--text-strong)" } }, s.total_qr)), /* @__PURE__ */ React.createElement("div", { style: { padding: 16, background: "var(--surface-2)", borderRadius: 8, border: "1px solid var(--border)" } }, /* @__PURE__ */ React.createElement("div", { className: "text-xs text-muted", style: { marginBottom: 4 } }, "Skanlangan"), /* @__PURE__ */ React.createElement("div", { style: { fontSize: 24, fontWeight: 600, color: "var(--success-fg)" } }, s.scanned_qr)), /* @__PURE__ */ React.createElement("div", { style: { padding: 16, background: "var(--surface-2)", borderRadius: 8, border: "1px solid var(--border)", gridColumn: "1/-1" } }, /* @__PURE__ */ React.createElement("div", { className: "text-xs text-muted", style: { marginBottom: 4 } }, "Aktivatsiya foizi"), /* @__PURE__ */ React.createElement("div", { style: { fontSize: 22, fontWeight: 600, color: "var(--primary)", marginBottom: 8 } }, (s.scanned_qr / s.total_qr * 100).toFixed(1), "%"), /* @__PURE__ */ React.createElement("div", { className: "progress" }, /* @__PURE__ */ React.createElement("div", { style: { width: Math.min(s.scanned_qr / s.total_qr * 100, 100) + "%" } })))))), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "card-header" }, /* @__PURE__ */ React.createElement("h3", null, "\u041F\u0430\u0440\u0442\u0438\u044F (do'konga biriktirilgan)"), /* @__PURE__ */ React.createElement(Badge, { variant: "neutral" }, s.batches_count, " ta")), /* @__PURE__ */ React.createElement("div", { className: "table-wrap" }, /* @__PURE__ */ React.createElement("table", { className: "table inline-table" }, /* @__PURE__ */ React.createElement("thead", null, /* @__PURE__ */ React.createElement("tr", null, /* @__PURE__ */ React.createElement("th", null, "\u041F\u0430\u0440\u0442\u0438\u044F"), /* @__PURE__ */ React.createElement("th", null, "Sotuvchi"), /* @__PURE__ */ React.createElement("th", { style: { textAlign: "right" } }, "Jami"), /* @__PURE__ */ React.createElement("th", null, "Aktivatsiya"), /* @__PURE__ */ React.createElement("th", null, "Holat"))), /* @__PURE__ */ React.createElement("tbody", null, JQ.batches.filter((b) => b.store_id === s.id).slice(0, 5).map((b) => /* @__PURE__ */ React.createElement("tr", { key: b.id }, /* @__PURE__ */ React.createElement("td", { className: "text-mono" }, b.name), /* @__PURE__ */ React.createElement("td", null, b.seller_name), /* @__PURE__ */ React.createElement("td", { className: "num", style: { textAlign: "right" } }, b.quantity), /* @__PURE__ */ React.createElement("td", { className: "text-mono text-xs" }, b.activation_pct.toFixed(1), "%"), /* @__PURE__ */ React.createElement("td", null, b.status === "active" ? /* @__PURE__ */ React.createElement(Badge, { variant: "success", dot: true }, "Faol") : /* @__PURE__ */ React.createElement(Badge, { variant: "neutral", dot: true }, "\u2014")))))))));
}
function StoreAddPage() {
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(PageHeader, { title: "Yangi do'kon", subtitle: "JIP partneri sifatida ro'yxatdan o'tkazish" }), /* @__PURE__ */ React.createElement(FormBlock, { title: "Asosiy ma'lumotlar", icon: "store" }, /* @__PURE__ */ React.createElement(Field, { label: "Do'kon nomi", required: true, span2: true }, /* @__PURE__ */ React.createElement(Input, { placeholder: "Sadulla Jomiy 2" })), /* @__PURE__ */ React.createElement(Field, { label: "Manzil", span2: true }, /* @__PURE__ */ React.createElement(Input, { placeholder: "\u0443\u043B. \u0410\u043C\u0438\u0440\u0430 \u0422\u0435\u043C\u0443\u0440\u0430, 25" })), /* @__PURE__ */ React.createElement(Field, { label: "Viloyat", required: true }, /* @__PURE__ */ React.createElement(Select, null, /* @__PURE__ */ React.createElement("option", null, "\u2014 Tanlang \u2014"), JQ.regions.map((r) => /* @__PURE__ */ React.createElement("option", { key: r }, r)))), /* @__PURE__ */ React.createElement(Field, { label: "Tuman", required: true }, /* @__PURE__ */ React.createElement(Select, null, /* @__PURE__ */ React.createElement("option", null, "\u2014 Avval viloyat \u2014"))), /* @__PURE__ */ React.createElement(Field, { label: "Egasi (sotuvchi)", span2: true }, /* @__PURE__ */ React.createElement(Select, null, /* @__PURE__ */ React.createElement("option", null, "\u2014 Tanlang \u2014"), JQ.users.filter((u) => u.type === "sotuvchi").slice(0, 10).map((u) => /* @__PURE__ */ React.createElement("option", { key: u.id }, u.first_name, " ", u.last_name)))), /* @__PURE__ */ React.createElement(Field, { label: "Telefon", required: true }, /* @__PURE__ */ React.createElement(Input, { placeholder: "+998 99 488 71 77" })), /* @__PURE__ */ React.createElement(Field, { label: "Komissiya foizi (%)" }, /* @__PURE__ */ React.createElement(Input, { type: "number", defaultValue: 7.43, step: 0.01 })), /* @__PURE__ */ React.createElement(Field, { label: "Faollik", span2: true }, /* @__PURE__ */ React.createElement("label", { style: { display: "flex", alignItems: "center", gap: 8 } }, /* @__PURE__ */ React.createElement("input", { type: "checkbox", className: "checkbox", defaultChecked: true }), " ", /* @__PURE__ */ React.createElement("span", { className: "text-sm" }, "Faol")))), /* @__PURE__ */ React.createElement("div", { className: "form-footer" }, /* @__PURE__ */ React.createElement("span", { className: "text-muted text-sm" }, "Yangi yozuv"), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 8 } }, /* @__PURE__ */ React.createElement(Button, { variant: "secondary" }, "Bekor qilish"), /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "check" }, "Saqlash"))));
}
Object.assign(window, {
  QRCodesPage,
  QRCodeEditPage,
  QRGeneratePage,
  BatchesPage,
  BatchAddPage,
  BatchEditPage,
  StoresPage,
  StoreEditPage,
  StoreAddPage
});
const JG = window.JIP;
function GiftsPage({ onNavigate }) {
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(
    PageHeader,
    {
      title: "Sovg'alar katalogi",
      subtitle: "Foydalanuvchilar tomonidan so'rashi mumkin bo'lgan sovg'alar",
      actions: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(Button, { variant: "secondary", icon: "archive" }, "Arxivga"), /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "plus", onClick: () => onNavigate("/gifts/add") }, "Yangi sovg'a"))
    }
  ), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "filter-bar" }, /* @__PURE__ */ React.createElement(SearchBar, { placeholder: "Nom yoki tur bo'yicha..." }), /* @__PURE__ */ React.createElement("div", { style: { flex: 1 } }), /* @__PURE__ */ React.createElement(FilterChip, { icon: "layers" }, "Tur"), /* @__PURE__ */ React.createElement(FilterChip, { icon: "check", active: true }, "Faol")), /* @__PURE__ */ React.createElement("div", { style: { padding: 16, display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))", gap: 12 } }, JG.gifts.map((g) => /* @__PURE__ */ React.createElement(
    "div",
    {
      key: g.id,
      style: {
        background: "var(--surface-2)",
        borderRadius: 12,
        padding: 16,
        border: "1px solid var(--border)",
        display: "flex",
        flexDirection: "column",
        gap: 10,
        cursor: "pointer",
        transition: "border 120ms"
      },
      onMouseEnter: (e) => e.currentTarget.style.borderColor = "var(--border-strong)",
      onMouseLeave: (e) => e.currentTarget.style.borderColor = "var(--border)"
    },
    /* @__PURE__ */ React.createElement("div", { style: {
      aspectRatio: "16/10",
      borderRadius: 8,
      background: "linear-gradient(135deg, rgba(99,102,241,0.18), rgba(139,92,246,0.18))",
      display: "grid",
      placeItems: "center",
      fontSize: 48
    } }, g.image),
    /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 6 } }, /* @__PURE__ */ React.createElement("div", { style: { minWidth: 0, flex: 1 } }, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 14, fontWeight: 500, color: "var(--text-strong)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" } }, g.name_ru), /* @__PURE__ */ React.createElement("div", { className: "text-xs text-muted" }, g.name_uz)), g.is_active ? /* @__PURE__ */ React.createElement(Badge, { variant: "success", size: "sm", dot: true }, "Faol") : /* @__PURE__ */ React.createElement(Badge, { variant: "neutral", size: "sm", dot: true }, "Arxiv")),
    /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", justifyContent: "space-between", borderTop: "1px solid var(--border)", paddingTop: 10 } }, /* @__PURE__ */ React.createElement("span", { style: {
      display: "flex",
      alignItems: "center",
      gap: 4,
      color: "var(--primary)",
      fontFamily: "var(--font-mono)",
      fontWeight: 600,
      fontSize: 14
    } }, /* @__PURE__ */ React.createElement(Icon, { name: "coin", size: 14 }), " ", g.price.toLocaleString("ru")), /* @__PURE__ */ React.createElement(Badge, { variant: "info", outline: true, size: "sm" }, g.type))
  )))));
}
function GiftAddPage() {
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(PageHeader, { title: "Yangi sovg'a", subtitle: "Katalogga yangi sovg'a qo'shish" }), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: "1fr 320px", gap: 16, alignItems: "start" } }, /* @__PURE__ */ React.createElement(FormBlock, { title: "Sovg'a ma'lumotlari", icon: "gift" }, /* @__PURE__ */ React.createElement(Field, { label: "Nomi (UZ)", required: true }, /* @__PURE__ */ React.createElement(Input, { placeholder: "AirPods 3-pokoleniya" })), /* @__PURE__ */ React.createElement(Field, { label: "Nomi (RU)", required: true }, /* @__PURE__ */ React.createElement(Input, { placeholder: "AirPods 3-\u0433\u043E \u043F\u043E\u043A\u043E\u043B\u0435\u043D\u0438\u044F" })), /* @__PURE__ */ React.createElement(Field, { label: "Tavsif (UZ)", span2: true }, /* @__PURE__ */ React.createElement(Textarea, { rows: 3, placeholder: "Apple AirPods 3-pokoleniya. Active Noise Cancellation..." })), /* @__PURE__ */ React.createElement(Field, { label: "Tavsif (RU)", span2: true }, /* @__PURE__ */ React.createElement(Textarea, { rows: 3, placeholder: "Apple AirPods 3-\u0433\u043E \u043F\u043E\u043A\u043E\u043B\u0435\u043D\u0438\u044F. \u0410\u043A\u0442\u0438\u0432\u043D\u043E\u0435 \u0448\u0443\u043C\u043E\u043F\u043E\u0434\u0430\u0432\u043B\u0435\u043D\u0438\u0435..." })), /* @__PURE__ */ React.createElement(Field, { label: "Ball narxi", required: true, hint: "50 000 ball ~ $50" }, /* @__PURE__ */ React.createElement(Input, { type: "number", defaultValue: 5e4, step: 1e3 })), /* @__PURE__ */ React.createElement(Field, { label: "Tur" }, /* @__PURE__ */ React.createElement(Select, null, /* @__PURE__ */ React.createElement("option", { value: "electronics" }, "Elektronika"), /* @__PURE__ */ React.createElement("option", { value: "clothing" }, "Kiyim"), /* @__PURE__ */ React.createElement("option", { value: "experience" }, "Tajriba"), /* @__PURE__ */ React.createElement("option", { value: "cash" }, "Naqd pul"))), /* @__PURE__ */ React.createElement(Field, { label: "Faollik", span2: true }, /* @__PURE__ */ React.createElement("label", { style: { display: "flex", alignItems: "center", gap: 8 } }, /* @__PURE__ */ React.createElement("input", { type: "checkbox", className: "checkbox", defaultChecked: true }), /* @__PURE__ */ React.createElement("span", { className: "text-sm" }, "Sovg'a katalogda ko'rinadi")))), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "card-header" }, /* @__PURE__ */ React.createElement("h3", null, "Tasvir")), /* @__PURE__ */ React.createElement("div", { style: { padding: 20 } }, /* @__PURE__ */ React.createElement("div", { style: {
    aspectRatio: "1",
    border: "1.5px dashed var(--border-strong)",
    borderRadius: 12,
    display: "grid",
    placeItems: "center",
    color: "var(--text-muted)",
    cursor: "pointer",
    background: "var(--surface-2)"
  } }, /* @__PURE__ */ React.createElement("div", { style: { textAlign: "center" } }, /* @__PURE__ */ React.createElement(Icon, { name: "image", size: 32 }), /* @__PURE__ */ React.createElement("div", { className: "text-sm", style: { marginTop: 6 } }, "Tashlang yoki ", /* @__PURE__ */ React.createElement("span", { style: { color: "var(--primary)" } }, "tanlang")), /* @__PURE__ */ React.createElement("div", { className: "text-xs text-dim", style: { marginTop: 4 } }, "PNG, JPG, max 2MB")))))), /* @__PURE__ */ React.createElement("div", { className: "form-footer" }, /* @__PURE__ */ React.createElement("span", { className: "text-muted text-sm" }, "Yangi yozuv"), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 8 } }, /* @__PURE__ */ React.createElement(Button, { variant: "secondary" }, "Bekor qilish"), /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "check" }, "Saqlash"))));
}
function RedemptionsPage({ onNavigate }) {
  const statusBadge = (s) => {
    if (s === "pending") return /* @__PURE__ */ React.createElement(Badge, { variant: "warning", icon: "clock" }, "\u0417\u0430\u043F\u0440\u043E\u0441 \u043F\u0440\u0438\u043D\u044F\u0442");
    if (s === "confirmed") return /* @__PURE__ */ React.createElement(Badge, { variant: "info", icon: "check" }, "\u041F\u043E\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043D\u0438\u0435 \u043F\u043E\u043B\u0443\u0447.");
    if (s === "cancelled") return /* @__PURE__ */ React.createElement(Badge, { variant: "danger", icon: "x" }, "\u0417\u0430\u043F\u0440\u043E\u0441 \u043E\u0442\u043C\u0435\u043D\u0451\u043D");
    return /* @__PURE__ */ React.createElement(Badge, { variant: "neutral" }, s);
  };
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(
    PageHeader,
    {
      title: "Sovg'a so'rovlari",
      subtitle: "Foydalanuvchilar tomonidan so'ralgan sovg'alar",
      actions: /* @__PURE__ */ React.createElement(Button, { variant: "secondary", icon: "download" }, "Eksport")
    }
  ), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement(DateHierarchy, { items: ["2026", "\u041C\u0430\u0439", "\u0412\u0441\u0435"], active: 2 }), /* @__PURE__ */ React.createElement("div", { className: "filter-bar" }, /* @__PURE__ */ React.createElement(SearchBar, { placeholder: "Foydalanuvchi yoki sovg'a..." }), /* @__PURE__ */ React.createElement("div", { style: { flex: 1 } }), /* @__PURE__ */ React.createElement(FilterChip, { icon: "clock" }, "Holat"), /* @__PURE__ */ React.createElement(FilterChip, { icon: "check" }, "Tasdiqlash"), /* @__PURE__ */ React.createElement(FilterChip, { icon: "calendar" }, "Sana")), /* @__PURE__ */ React.createElement("div", { className: "table-wrap" }, /* @__PURE__ */ React.createElement("table", { className: "table" }, /* @__PURE__ */ React.createElement("thead", null, /* @__PURE__ */ React.createElement("tr", null, /* @__PURE__ */ React.createElement("th", null, "Zakaz"), /* @__PURE__ */ React.createElement("th", null, "Foydalanuvchi"), /* @__PURE__ */ React.createElement("th", null, "Telefon"), /* @__PURE__ */ React.createElement("th", null, "\u0420\u0435\u0433\u0438\u043E\u043D"), /* @__PURE__ */ React.createElement("th", null, "Sovg'a"), /* @__PURE__ */ React.createElement("th", null, "Status"), /* @__PURE__ */ React.createElement("th", null, "Tasdiqlash"), /* @__PURE__ */ React.createElement("th", null, "So'ralgan vaqt"))), /* @__PURE__ */ React.createElement("tbody", null, JG.redemptions.map((r) => {
    var _a;
    return /* @__PURE__ */ React.createElement("tr", { key: r.id, onClick: () => onNavigate("/redemptions/edit"), style: { cursor: "pointer" } }, /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("span", { className: "code-mask" }, "#", r.id)), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("div", { className: "user-cell" }, /* @__PURE__ */ React.createElement(Avatar, { name: r.user_name, size: 28 }), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { className: "user-name", style: { fontSize: 12.5 } }, r.user_name), /* @__PURE__ */ React.createElement("div", { className: "user-meta" }, "ID: ", r.user_id)))), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("span", { className: "text-mono text-sm" }, r.phone)), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement(Badge, { variant: "info", icon: "map-pin" }, r.region.replace(" \u043E\u0431\u043B\u0430\u0441\u0442\u044C", "").replace("\u0413\u043E\u0440\u043E\u0434 ", ""))), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 8 } }, /* @__PURE__ */ React.createElement("span", { style: {
      width: 28,
      height: 28,
      borderRadius: 6,
      display: "grid",
      placeItems: "center",
      background: "linear-gradient(135deg, rgba(99,102,241,0.18), rgba(139,92,246,0.18))",
      fontSize: 14
    } }, ((_a = JG.gifts.find((g) => g.id === r.gift_id)) == null ? void 0 : _a.image) || "\u{1F381}"), /* @__PURE__ */ React.createElement("span", { className: "text-strong", style: { fontSize: 12.5, fontWeight: 500 } }, r.gift_name))), /* @__PURE__ */ React.createElement("td", null, statusBadge(r.status)), /* @__PURE__ */ React.createElement("td", null, r.is_confirmed ? /* @__PURE__ */ React.createElement(Badge, { variant: "success", icon: "check" }, "\u041F\u043E\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043D\u043E") : /* @__PURE__ */ React.createElement(Badge, { variant: "warning", icon: "clock" }, "\u041D\u0435 \u043F\u043E\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043D\u043E")), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("span", { className: "text-mono text-xs text-muted" }, r.created_at)));
  })))), /* @__PURE__ */ React.createElement(Pagination, { total: 15, page: 1, perPage: 25 })));
}
function RedemptionEditPage({ onNavigate }) {
  const r = JG.redemptions[0];
  const g = JG.gifts.find((x) => x.id === r.gift_id);
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(
    PageHeader,
    {
      title: /* @__PURE__ */ React.createElement("span", null, "\u0417\u0430\u044F\u0432\u043A\u0430 ", /* @__PURE__ */ React.createElement("span", { className: "code-mask" }, "#", r.id)),
      subtitle: /* @__PURE__ */ React.createElement("span", null, r.user_name, " \xB7 ", r.created_at),
      actions: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(Button, { variant: "ghost", icon: "history" }, "\u0418\u0441\u0442\u043E\u0440\u0438\u044F"), /* @__PURE__ */ React.createElement(Button, { variant: "danger", icon: "x" }, "\u041E\u0442\u043C\u0435\u043D\u0438\u0442\u044C"), /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "check" }, "\u0421\u043E\u0445\u0440\u0430\u043D\u0438\u0442\u044C"))
    }
  ), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 } }, /* @__PURE__ */ React.createElement(FormBlock, { title: "\u0418\u043D\u0444\u043E\u0440\u043C\u0430\u0446\u0438\u044F \u043E \u0437\u0430\u043F\u0440\u043E\u0441\u0435", icon: "gift-redeem" }, /* @__PURE__ */ React.createElement(Field, { label: "\u0423\u0447\u0430\u0441\u0442\u043D\u0438\u043A", span2: true }, /* @__PURE__ */ React.createElement("div", { className: "input", style: { display: "flex", alignItems: "center", gap: 10 } }, /* @__PURE__ */ React.createElement(Avatar, { name: r.user_name, size: 26 }), /* @__PURE__ */ React.createElement("a", { style: { color: "var(--primary)", cursor: "pointer" }, onClick: () => onNavigate("/users/santenik") }, r.user_name, " \xB7 ID ", r.user_id))), /* @__PURE__ */ React.createElement(Field, { label: "Sovg'a", span2: true }, /* @__PURE__ */ React.createElement("div", { className: "input", style: { display: "flex", alignItems: "center", gap: 10 } }, /* @__PURE__ */ React.createElement("span", { style: { fontSize: 18 } }, g == null ? void 0 : g.image), /* @__PURE__ */ React.createElement("a", { style: { color: "var(--primary)", cursor: "pointer" }, onClick: () => onNavigate("/gifts") }, r.gift_name), /* @__PURE__ */ React.createElement("span", { className: "text-mono", style: { marginLeft: "auto", color: "var(--primary)", fontWeight: 600 } }, g == null ? void 0 : g.price.toLocaleString("ru"), " ball"))), /* @__PURE__ */ React.createElement(Field, { label: "\u0420\u0435\u0433\u0438\u043E\u043D" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: r.region, readOnly: true })), /* @__PURE__ */ React.createElement(Field, { label: "\u0422\u0435\u043B\u0435\u0444\u043E\u043D" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: r.phone, readOnly: true })), /* @__PURE__ */ React.createElement(Field, { label: "So'ralgan vaqt", span2: true }, /* @__PURE__ */ React.createElement(Input, { defaultValue: r.created_at, readOnly: true }))), /* @__PURE__ */ React.createElement(FormBlock, { title: "\u041E\u0431\u0440\u0430\u0431\u043E\u0442\u043A\u0430", icon: "settings" }, /* @__PURE__ */ React.createElement(Field, { label: "Holat", required: true, span2: true }, /* @__PURE__ */ React.createElement(Select, { defaultValue: r.status }, /* @__PURE__ */ React.createElement("option", { value: "pending" }, "\u{1F3C6} \u0417\u0430\u043F\u0440\u043E\u0441 \u043F\u0440\u0438\u043D\u044F\u0442 \u043A \u043E\u0431\u0440\u0430\u0431\u043E\u0442\u043A\u0435"), /* @__PURE__ */ React.createElement("option", { value: "confirmed" }, "\u2705 \u041F\u043E\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043D\u0438\u0435 \u043F\u043E\u043B\u0443\u0447\u0435\u043D\u0438\u044F \u043F\u0440\u043E\u0434\u0443\u043A\u0442\u0430"), /* @__PURE__ */ React.createElement("option", { value: "cancelled" }, "\u274C \u0417\u0430\u043F\u0440\u043E\u0441 \u043E\u0442\u043C\u0435\u043D\u0451\u043D"))), /* @__PURE__ */ React.createElement(Field, { label: "is_confirmed", span2: true }, /* @__PURE__ */ React.createElement("label", { style: { display: "flex", alignItems: "center", gap: 8 } }, /* @__PURE__ */ React.createElement("input", { type: "checkbox", className: "checkbox", defaultChecked: r.is_confirmed }), /* @__PURE__ */ React.createElement("span", { className: "text-sm" }, "Foydalanuvchi sovg'ani oldi"))), /* @__PURE__ */ React.createElement(Field, { label: "Admin izoh", span2: true }, /* @__PURE__ */ React.createElement(Textarea, { rows: 5, placeholder: "Sovg'a yetkazib berildi. Doimiy mijoz..." })))), /* @__PURE__ */ React.createElement("div", { className: "form-footer" }, /* @__PURE__ */ React.createElement("span", { className: "text-muted text-sm" }, "Sa'lash + Telegram xabari yuboriladi"), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 8 } }, /* @__PURE__ */ React.createElement(Button, { variant: "secondary" }, "Bekor qilish"), /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "check" }, "\u0421\u043E\u0445\u0440\u0430\u043D\u0438\u0442\u044C"))));
}
function TransactionsPage({ onNavigate }) {
  const typeBadge = (t) => {
    if (t === "sale_bonus") return /* @__PURE__ */ React.createElement(Badge, { variant: "success", icon: "trending-up" }, "Sotuv bonusi");
    if (t === "admin_add") return /* @__PURE__ */ React.createElement(Badge, { variant: "info", icon: "plus" }, "Admin qo'shdi");
    if (t === "correction") return /* @__PURE__ */ React.createElement(Badge, { variant: "warning", icon: "sliders" }, "Tuzatish");
    return /* @__PURE__ */ React.createElement(Badge, null, t);
  };
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(
    PageHeader,
    {
      title: "Sotuvchi tranzaksiyalari",
      subtitle: "Sotuvchilar uchun ball harakatlari tarixi",
      actions: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(Button, { variant: "secondary", icon: "download" }, "Eksport"), /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "plus", onClick: () => onNavigate("/transactions/add") }, "Yangi"))
    }
  ), /* @__PURE__ */ React.createElement("div", { className: "kpi-grid" }, /* @__PURE__ */ React.createElement(KPI, { label: "Jami tranzaksiyalar", value: "1 117", icon: "credit-card", color: "indigo" }), /* @__PURE__ */ React.createElement(KPI, { label: "Sotuv bonusi", value: "893", icon: "trending-up", color: "emerald", hint: "79.9%" }), /* @__PURE__ */ React.createElement(KPI, { label: "Admin qo'shdi", value: "178", icon: "plus", color: "blue", hint: "15.9%" }), /* @__PURE__ */ React.createElement(KPI, { label: "Tuzatish", value: "46", icon: "sliders", color: "amber", hint: "4.1%" })), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "filter-bar" }, /* @__PURE__ */ React.createElement(SearchBar, { placeholder: "Sotuvchi nomi..." }), /* @__PURE__ */ React.createElement("div", { style: { flex: 1 } }), /* @__PURE__ */ React.createElement(FilterChip, { icon: "users" }, "Sotuvchi"), /* @__PURE__ */ React.createElement(FilterChip, { icon: "layers" }, "Tur"), /* @__PURE__ */ React.createElement(FilterChip, { icon: "calendar" }, "Sana")), /* @__PURE__ */ React.createElement("div", { className: "table-wrap" }, /* @__PURE__ */ React.createElement("table", { className: "table" }, /* @__PURE__ */ React.createElement("thead", null, /* @__PURE__ */ React.createElement("tr", null, /* @__PURE__ */ React.createElement("th", null, "Vaqt"), /* @__PURE__ */ React.createElement("th", null, "Sotuvchi"), /* @__PURE__ */ React.createElement("th", null, "Tur"), /* @__PURE__ */ React.createElement("th", { style: { textAlign: "right" } }, "Ballar"), /* @__PURE__ */ React.createElement("th", { style: { textAlign: "right" } }, "Sotuv ($)"), /* @__PURE__ */ React.createElement("th", null, "Kim qo'shgan"))), /* @__PURE__ */ React.createElement("tbody", null, JG.txns.map((t) => /* @__PURE__ */ React.createElement("tr", { key: t.id }, /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("span", { className: "text-mono text-xs text-muted" }, t.created_at)), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("div", { className: "user-cell" }, /* @__PURE__ */ React.createElement(Avatar, { name: t.seller_name, size: 26 }), /* @__PURE__ */ React.createElement("span", { style: { fontSize: 12.5, color: "var(--text-strong)", fontWeight: 500 } }, t.seller_name))), /* @__PURE__ */ React.createElement("td", null, typeBadge(t.type)), /* @__PURE__ */ React.createElement("td", { style: { textAlign: "right" } }, /* @__PURE__ */ React.createElement("span", { className: "text-mono", style: {
    fontWeight: 600,
    color: t.points >= 0 ? "var(--success-fg)" : "var(--danger-fg)"
  } }, t.points >= 0 ? "+" : "", t.points.toLocaleString("ru"))), /* @__PURE__ */ React.createElement("td", { className: "num", style: { textAlign: "right" } }, t.sale_amount ? "$" + t.sale_amount : "\u2014"), /* @__PURE__ */ React.createElement("td", null, t.added_by === "Bot" ? /* @__PURE__ */ React.createElement(Badge, { variant: "primary", icon: "zap" }, "Bot") : /* @__PURE__ */ React.createElement("span", { className: "text-mono text-sm text-muted" }, t.added_by))))))), /* @__PURE__ */ React.createElement(Pagination, { total: 1117, page: 1, perPage: 25 })));
}
function TransactionAddPage() {
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(PageHeader, { title: "Yangi tranzaksiya", subtitle: "Sotuvchiga ball qo'shish yoki tuzatish" }), /* @__PURE__ */ React.createElement(FormBlock, { title: "Tranzaksiya ma'lumotlari", icon: "credit-card" }, /* @__PURE__ */ React.createElement(Field, { label: "Sotuvchi", required: true, span2: true }, /* @__PURE__ */ React.createElement(Select, null, /* @__PURE__ */ React.createElement("option", null, "\u2014 Sotuvchini tanlang \u2014"), JG.users.filter((u) => u.type === "sotuvchi").map((u) => /* @__PURE__ */ React.createElement("option", { key: u.id }, u.first_name, " ", u.last_name, " (@", u.username, ") \xB7 Joriy: ", u.points.toLocaleString("ru"), " ball")))), /* @__PURE__ */ React.createElement(Field, { label: "Tur", required: true }, /* @__PURE__ */ React.createElement(Select, null, /* @__PURE__ */ React.createElement("option", { value: "sale_bonus" }, "Sotuv bonusi"), /* @__PURE__ */ React.createElement("option", { value: "admin_add" }, "Admin qo'shdi"), /* @__PURE__ */ React.createElement("option", { value: "correction" }, "Tuzatish"))), /* @__PURE__ */ React.createElement(Field, { label: "Ballar", required: true, hint: "Manfiy raqam \u2014 kamaytirish" }, /* @__PURE__ */ React.createElement(Input, { type: "number", placeholder: "+1000" })), /* @__PURE__ */ React.createElement(Field, { label: "Sotuv summasi ($)", hint: "Sotuv bonusi uchun" }, /* @__PURE__ */ React.createElement(Input, { type: "number", placeholder: "50.00", step: 0.01 })), /* @__PURE__ */ React.createElement(Field, { label: "Izoh", span2: true }, /* @__PURE__ */ React.createElement(Textarea, { rows: 3, placeholder: "Iyul oyi premiyasi..." }))), /* @__PURE__ */ React.createElement("div", { className: "form-footer" }, /* @__PURE__ */ React.createElement("span", { className: "text-muted text-sm" }, "Yangi yozuv"), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 8 } }, /* @__PURE__ */ React.createElement(Button, { variant: "secondary" }, "Bekor qilish"), /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "check" }, "Saqlash"))));
}
function SellerCodesPage() {
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(
    PageHeader,
    {
      title: "Sotuvchi ID lari",
      subtitle: "Sotuvchilar uchun ro'yxatdan o'tish kodlari",
      actions: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(Button, { variant: "secondary", icon: "download" }, "Excel eksport"), /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "sparkles" }, "Yangi kodlar generatsiya"))
    }
  ), /* @__PURE__ */ React.createElement("div", { className: "kpi-grid" }, /* @__PURE__ */ React.createElement(KPI, { label: "Jami kodlar", value: "25", icon: "id-card", color: "indigo" }), /* @__PURE__ */ React.createElement(KPI, { label: "Ishlatilgan", value: "14", icon: "check", color: "emerald", hint: "56%" }), /* @__PURE__ */ React.createElement(KPI, { label: "Kutilmoqda", value: "11", icon: "clock", color: "amber", hint: "44%" }), /* @__PURE__ */ React.createElement(KPI, { label: "Bu hafta yaratilgan", value: "5", icon: "sparkles", color: "blue" })), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "filter-bar" }, /* @__PURE__ */ React.createElement(SearchBar, { placeholder: "Kod yoki label..." }), /* @__PURE__ */ React.createElement("div", { style: { flex: 1 } }), /* @__PURE__ */ React.createElement(FilterChip, { icon: "check" }, "Ishlatilgan"), /* @__PURE__ */ React.createElement(FilterChip, { icon: "calendar" }, "Yaratilgan sana")), /* @__PURE__ */ React.createElement("div", { className: "table-wrap" }, /* @__PURE__ */ React.createElement("table", { className: "table" }, /* @__PURE__ */ React.createElement("thead", null, /* @__PURE__ */ React.createElement("tr", null, /* @__PURE__ */ React.createElement("th", { className: "col-checkbox" }, /* @__PURE__ */ React.createElement("input", { className: "checkbox", type: "checkbox" })), /* @__PURE__ */ React.createElement("th", null, "Kod"), /* @__PURE__ */ React.createElement("th", null, "Label"), /* @__PURE__ */ React.createElement("th", null, "Egasi"), /* @__PURE__ */ React.createElement("th", null, "Holat"), /* @__PURE__ */ React.createElement("th", null, "Yaratilgan"))), /* @__PURE__ */ React.createElement("tbody", null, JG.sellerCodes.map((c) => /* @__PURE__ */ React.createElement("tr", { key: c.id }, /* @__PURE__ */ React.createElement("td", { className: "col-checkbox" }, /* @__PURE__ */ React.createElement("input", { className: "checkbox", type: "checkbox" })), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("span", { className: "code-mask" }, c.code)), /* @__PURE__ */ React.createElement("td", null, c.label), /* @__PURE__ */ React.createElement("td", null, c.owner_name !== "\u2014" ? /* @__PURE__ */ React.createElement("div", { className: "user-cell" }, /* @__PURE__ */ React.createElement(Avatar, { name: c.owner_name, size: 24 }), /* @__PURE__ */ React.createElement("span", { style: { fontSize: 12.5, fontWeight: 500, color: "var(--text-strong)" } }, c.owner_name)) : /* @__PURE__ */ React.createElement("span", { className: "text-dim text-sm" }, "\u2014 hali ishlatilmagan \u2014")), /* @__PURE__ */ React.createElement("td", null, c.is_used ? /* @__PURE__ */ React.createElement(StatusBadges.approved, null) : /* @__PURE__ */ React.createElement(StatusBadges.pending, null)), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("span", { className: "text-mono text-xs text-muted" }, c.created_at))))))), /* @__PURE__ */ React.createElement(Pagination, { total: 25, page: 1, perPage: 25 })));
}
Object.assign(window, {
  GiftsPage,
  GiftAddPage,
  RedemptionsPage,
  RedemptionEditPage,
  TransactionsPage,
  TransactionAddPage,
  SellerCodesPage
});
const JM = window.JIP;
function ActivityLogPage() {
  const actionBadge = (a) => {
    const map = {
      create: { variant: "success", icon: "plus", label: "Yaratildi" },
      update: { variant: "info", icon: "edit", label: "O'zgartirildi" },
      delete: { variant: "danger", icon: "trash", label: "O'chirildi" }
    };
    const m = map[a.code] || map.update;
    return /* @__PURE__ */ React.createElement(Badge, { variant: m.variant, icon: m.icon }, m.label);
  };
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(
    PageHeader,
    {
      title: "Faollik tarixi",
      subtitle: "Tizimda sodir bo'lgan barcha o'zgarishlar audit logi",
      actions: /* @__PURE__ */ React.createElement(Button, { variant: "secondary", icon: "download" }, "Eksport")
    }
  ), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement(DateHierarchy, { items: ["2026", "\u041C\u0430\u0439", "24", "25", "26"], active: 4 }), /* @__PURE__ */ React.createElement("div", { className: "filter-bar" }, /* @__PURE__ */ React.createElement(SearchBar, { placeholder: "Kim, qaysi obyekt..." }), /* @__PURE__ */ React.createElement("div", { style: { flex: 1 } }), /* @__PURE__ */ React.createElement(FilterChip, { icon: "user" }, "Kim"), /* @__PURE__ */ React.createElement(FilterChip, { icon: "sparkles" }, "Amal"), /* @__PURE__ */ React.createElement(FilterChip, { icon: "box" }, "Obyekt turi"), /* @__PURE__ */ React.createElement(FilterChip, { icon: "calendar" }, "Sana")), /* @__PURE__ */ React.createElement("div", { className: "table-wrap" }, /* @__PURE__ */ React.createElement("table", { className: "table" }, /* @__PURE__ */ React.createElement("thead", null, /* @__PURE__ */ React.createElement("tr", null, /* @__PURE__ */ React.createElement("th", { className: "col-checkbox" }, /* @__PURE__ */ React.createElement("input", { className: "checkbox", type: "checkbox" })), /* @__PURE__ */ React.createElement("th", null, "Vaqt"), /* @__PURE__ */ React.createElement("th", null, "Kim"), /* @__PURE__ */ React.createElement("th", null, "Amal"), /* @__PURE__ */ React.createElement("th", null, "Obyekt"), /* @__PURE__ */ React.createElement("th", null, "Tavsif"), /* @__PURE__ */ React.createElement("th", null, "IP"))), /* @__PURE__ */ React.createElement("tbody", null, JM.log.map((l) => /* @__PURE__ */ React.createElement("tr", { key: l.id }, /* @__PURE__ */ React.createElement("td", { className: "col-checkbox" }, /* @__PURE__ */ React.createElement("input", { className: "checkbox", type: "checkbox" })), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("span", { className: "text-mono text-xs text-muted" }, l.timestamp)), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("div", { className: "user-cell" }, /* @__PURE__ */ React.createElement(Avatar, { name: l.who, size: 24 }), /* @__PURE__ */ React.createElement("span", { className: "text-mono text-sm", style: { color: "var(--text-strong)", fontWeight: 500 } }, l.who))), /* @__PURE__ */ React.createElement("td", null, actionBadge(l.action)), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", flexDirection: "column", gap: 2 } }, /* @__PURE__ */ React.createElement("span", { style: { fontSize: 12.5, color: "var(--text-strong)", fontWeight: 500 } }, l.object_type), /* @__PURE__ */ React.createElement("span", { className: "text-mono text-xs text-muted" }, l.object_label))), /* @__PURE__ */ React.createElement("td", { className: "text-sm" }, l.description), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("span", { className: "text-mono text-xs text-muted" }, l.ip))))))), /* @__PURE__ */ React.createElement(Pagination, { total: 264, page: 1, perPage: 40 })));
}
function LivestreamsPage({ onNavigate }) {
  const statusBadge = (s) => {
    if (s === "scheduled") return /* @__PURE__ */ React.createElement(Badge, { variant: "info", icon: "clock" }, "Rejalashtirilgan");
    if (s === "active") return /* @__PURE__ */ React.createElement(Badge, { variant: "success", icon: "radio" }, "Faol");
    if (s === "completed") return /* @__PURE__ */ React.createElement(Badge, { variant: "neutral", icon: "check" }, "Tugagan");
    return /* @__PURE__ */ React.createElement(Badge, null, s);
  };
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(
    PageHeader,
    {
      title: "Jonli efirlar",
      subtitle: "LiveStream sessiyalari va g'oliblar ro'yxati",
      actions: /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "plus", onClick: () => onNavigate("/livestreams/add") }, "Yangi efir")
    }
  ), /* @__PURE__ */ React.createElement("div", { className: "kpi-grid" }, /* @__PURE__ */ React.createElement(KPI, { label: "Jami efirlar", value: "4", icon: "radio", color: "indigo" }), /* @__PURE__ */ React.createElement(KPI, { label: "Tugagan", value: "2", icon: "check", color: "emerald" }), /* @__PURE__ */ React.createElement(KPI, { label: "Faol", value: "1", icon: "zap", color: "amber" }), /* @__PURE__ */ React.createElement(KPI, { label: "Rejalashtirilgan", value: "1", icon: "clock", color: "blue" })), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "filter-bar" }, /* @__PURE__ */ React.createElement(SearchBar, { placeholder: "Sarlavha bo'yicha..." }), /* @__PURE__ */ React.createElement("div", { style: { flex: 1 } }), /* @__PURE__ */ React.createElement(FilterChip, { icon: "check" }, "Holat")), /* @__PURE__ */ React.createElement("div", { className: "table-wrap" }, /* @__PURE__ */ React.createElement("table", { className: "table" }, /* @__PURE__ */ React.createElement("thead", null, /* @__PURE__ */ React.createElement("tr", null, /* @__PURE__ */ React.createElement("th", null, "Sarlavha"), /* @__PURE__ */ React.createElement("th", null, "Holat"), /* @__PURE__ */ React.createElement("th", null, "Boshlanish vaqti"), /* @__PURE__ */ React.createElement("th", { style: { textAlign: "right" } }, "G'oliblar soni"), /* @__PURE__ */ React.createElement("th", null))), /* @__PURE__ */ React.createElement("tbody", null, JM.livestreams.map((ls) => /* @__PURE__ */ React.createElement("tr", { key: ls.id }, /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 10 } }, /* @__PURE__ */ React.createElement("span", { style: { width: 32, height: 32, borderRadius: 6, background: "var(--danger-soft)", color: "var(--danger)", display: "grid", placeItems: "center" } }, /* @__PURE__ */ React.createElement(Icon, { name: "radio", size: 14 })), /* @__PURE__ */ React.createElement("span", { className: "text-strong", style: { fontWeight: 500 } }, ls.title))), /* @__PURE__ */ React.createElement("td", null, statusBadge(ls.status)), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("span", { className: "text-mono text-sm text-muted" }, ls.start_at)), /* @__PURE__ */ React.createElement("td", { className: "num", style: { textAlign: "right" } }, ls.winners_count), /* @__PURE__ */ React.createElement("td", { style: { textAlign: "right" } }, /* @__PURE__ */ React.createElement(Button, { size: "sm", variant: "ghost", icon: "edit" }, "Tahrirlash")))))))));
}
function LivestreamAddPage() {
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(PageHeader, { title: "Yangi jonli efir", subtitle: "LiveStream sessiyasini rejalashtirish" }), /* @__PURE__ */ React.createElement(FormBlock, { title: "Asosiy ma'lumotlar", icon: "radio" }, /* @__PURE__ */ React.createElement(Field, { label: "Sarlavha", required: true, span2: true }, /* @__PURE__ */ React.createElement(Input, { placeholder: "Yangi mahsulot taqdimoti" })), /* @__PURE__ */ React.createElement(Field, { label: "Tavsif (HTML)", span2: true }, /* @__PURE__ */ React.createElement(Textarea, { rows: 5, placeholder: "<p>Iyun oyida bo'lib o'tadigan...</p>" })), /* @__PURE__ */ React.createElement(Field, { label: "Boshlanish vaqti", required: true }, /* @__PURE__ */ React.createElement(Input, { type: "datetime-local" })), /* @__PURE__ */ React.createElement(Field, { label: "G'oliblar soni" }, /* @__PURE__ */ React.createElement(Input, { type: "number", defaultValue: 5, min: 1 })), /* @__PURE__ */ React.createElement(Field, { label: "Faollik", span2: true }, /* @__PURE__ */ React.createElement("label", { style: { display: "flex", alignItems: "center", gap: 8 } }, /* @__PURE__ */ React.createElement("input", { type: "checkbox", className: "checkbox", defaultChecked: true }), " ", /* @__PURE__ */ React.createElement("span", { className: "text-sm" }, "Faol")))), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "card-header" }, /* @__PURE__ */ React.createElement("h3", null, "G'oliblar ro'yxati (inline)"), /* @__PURE__ */ React.createElement(Button, { size: "sm", variant: "secondary", icon: "plus" }, "Qo'shish")), /* @__PURE__ */ React.createElement("div", { className: "table-wrap" }, /* @__PURE__ */ React.createElement("table", { className: "table inline-table" }, /* @__PURE__ */ React.createElement("thead", null, /* @__PURE__ */ React.createElement("tr", null, /* @__PURE__ */ React.createElement("th", null, "O'rin"), /* @__PURE__ */ React.createElement("th", null, "Foydalanuvchi"), /* @__PURE__ */ React.createElement("th", null, "Sovg'a"), /* @__PURE__ */ React.createElement("th", null))), /* @__PURE__ */ React.createElement("tbody", null, [1, 2, 3].map((i) => /* @__PURE__ */ React.createElement("tr", { key: i }, /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement(Badge, { variant: i === 1 ? "warning" : "neutral", outline: true }, i, "-o'rin")), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement(Select, null, /* @__PURE__ */ React.createElement("option", null, "\u2014 Tanlang \u2014"), JM.users.slice(0, 6).map((u) => /* @__PURE__ */ React.createElement("option", { key: u.id }, u.first_name, " ", u.last_name)))), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement(Select, null, /* @__PURE__ */ React.createElement("option", null, "\u2014 Tanlang \u2014"), JM.gifts.slice(0, 4).map((g) => /* @__PURE__ */ React.createElement("option", { key: g.id }, g.name_ru)))), /* @__PURE__ */ React.createElement("td", { style: { textAlign: "right" } }, /* @__PURE__ */ React.createElement(Button, { size: "sm", variant: "ghost", icon: "x" })))))))), /* @__PURE__ */ React.createElement("div", { className: "form-footer" }, /* @__PURE__ */ React.createElement("span", { className: "text-muted text-sm" }, "Yangi yozuv"), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 8 } }, /* @__PURE__ */ React.createElement(Button, { variant: "secondary" }, "Bekor qilish"), /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "check" }, "Saqlash"))));
}
function RegionLogPage() {
  const statusBadge = (s) => {
    const map = {
      pending: { v: "warning", i: "clock", l: "Kutilmoqda" },
      sending: { v: "info", i: "send", l: "Yuborilmoqda" },
      done: { v: "success", i: "check", l: "Bajarildi" },
      error: { v: "danger", i: "x", l: "Xato" }
    };
    const m = map[s] || map.pending;
    return /* @__PURE__ */ React.createElement(Badge, { variant: m.v, icon: m.i }, m.l);
  };
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(PageHeader, { title: "Viloyat xabarlari logi", subtitle: "Viloyatlar bo'yicha yuborilgan ommaviy xabarlar tarixi" }), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "filter-bar" }, /* @__PURE__ */ React.createElement(SearchBar, { placeholder: "Viloyat yoki yuboruvchi..." }), /* @__PURE__ */ React.createElement("div", { style: { flex: 1 } }), /* @__PURE__ */ React.createElement(FilterChip, { icon: "check" }, "Holat"), /* @__PURE__ */ React.createElement(FilterChip, { icon: "calendar" }, "Sana")), /* @__PURE__ */ React.createElement("div", { className: "table-wrap" }, /* @__PURE__ */ React.createElement("table", { className: "table" }, /* @__PURE__ */ React.createElement("thead", null, /* @__PURE__ */ React.createElement("tr", null, /* @__PURE__ */ React.createElement("th", null, "Sana"), /* @__PURE__ */ React.createElement("th", null, "Viloyat"), /* @__PURE__ */ React.createElement("th", { style: { textAlign: "right" } }, "Jami"), /* @__PURE__ */ React.createElement("th", { style: { textAlign: "right" } }, "Yuborildi"), /* @__PURE__ */ React.createElement("th", { style: { textAlign: "right" } }, "Xato"), /* @__PURE__ */ React.createElement("th", null, "Holat"), /* @__PURE__ */ React.createElement("th", null, "Kim yubordi"))), /* @__PURE__ */ React.createElement("tbody", null, JM.regionMessages.map((m) => /* @__PURE__ */ React.createElement("tr", { key: m.id }, /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("span", { className: "text-mono text-xs text-muted" }, m.date)), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement(Badge, { variant: "info", icon: "map-pin" }, m.region)), /* @__PURE__ */ React.createElement("td", { className: "num", style: { textAlign: "right" } }, m.total), /* @__PURE__ */ React.createElement("td", { className: "num", style: { textAlign: "right", color: "var(--success-fg)" } }, m.sent), /* @__PURE__ */ React.createElement("td", { className: "num", style: { textAlign: "right", color: m.errors > 0 ? "var(--danger-fg)" : "var(--text-dim)" } }, m.errors), /* @__PURE__ */ React.createElement("td", null, statusBadge(m.status)), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("span", { className: "text-mono text-sm text-muted" }, m.who)))))))));
}
function VideosPage({ onNavigate }) {
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(
    PageHeader,
    {
      title: "Video ko'rsatmalar",
      subtitle: "Foydalanuvchilar uchun video instruktsiyalar",
      actions: /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "plus", onClick: () => onNavigate("/videos/add") }, "Yangi video")
    }
  ), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "filter-bar" }, /* @__PURE__ */ React.createElement(SearchBar, { placeholder: "Sarlavha..." }), /* @__PURE__ */ React.createElement("div", { style: { flex: 1 } }), /* @__PURE__ */ React.createElement(FilterChip, { icon: "users" }, "Tur (santenik/sotuvchi)"), /* @__PURE__ */ React.createElement(FilterChip, { icon: "check" }, "Faolligi")), /* @__PURE__ */ React.createElement("div", { className: "table-wrap" }, /* @__PURE__ */ React.createElement("table", { className: "table" }, /* @__PURE__ */ React.createElement("thead", null, /* @__PURE__ */ React.createElement("tr", null, /* @__PURE__ */ React.createElement("th", null, "Video"), /* @__PURE__ */ React.createElement("th", null, "Tur"), /* @__PURE__ */ React.createElement("th", { style: { textAlign: "right" } }, "Tartib"), /* @__PURE__ */ React.createElement("th", null, "Faollik"), /* @__PURE__ */ React.createElement("th", null))), /* @__PURE__ */ React.createElement("tbody", null, JM.videos.map((v) => /* @__PURE__ */ React.createElement("tr", { key: v.id }, /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 10 } }, /* @__PURE__ */ React.createElement("span", { style: { width: 48, height: 32, borderRadius: 6, background: "#000", display: "grid", placeItems: "center", color: "white" } }, /* @__PURE__ */ React.createElement(Icon, { name: "play", size: 14 })), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { className: "text-strong", style: { fontWeight: 500 } }, v.title), /* @__PURE__ */ React.createElement("div", { className: "text-xs text-muted text-mono" }, v.url)))), /* @__PURE__ */ React.createElement("td", null, v.type === "santenik" ? /* @__PURE__ */ React.createElement(Badge, { variant: "warning", icon: "wrench" }, "Santenik") : /* @__PURE__ */ React.createElement(Badge, { variant: "info", icon: "store" }, "Sotuvchi")), /* @__PURE__ */ React.createElement("td", { className: "num", style: { textAlign: "right" } }, v.order), /* @__PURE__ */ React.createElement("td", null, v.is_active ? /* @__PURE__ */ React.createElement(StatusBadges.active, null) : /* @__PURE__ */ React.createElement(StatusBadges.inactive, null)), /* @__PURE__ */ React.createElement("td", { style: { textAlign: "right" } }, /* @__PURE__ */ React.createElement(Button, { size: "sm", variant: "ghost", icon: "edit" })))))))));
}
function VideoAddPage() {
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(PageHeader, { title: "Yangi video qo'shish" }), /* @__PURE__ */ React.createElement(FormBlock, { title: "Video ma'lumotlari", icon: "video" }, /* @__PURE__ */ React.createElement(Field, { label: "Sarlavha (UZ)", required: true }, /* @__PURE__ */ React.createElement(Input, { placeholder: "QR kod skanlash" })), /* @__PURE__ */ React.createElement(Field, { label: "Sarlavha (RU)", required: true }, /* @__PURE__ */ React.createElement(Input, { placeholder: "\u0421\u043A\u0430\u043D\u0438\u0440\u043E\u0432\u0430\u043D\u0438\u0435 QR-\u043A\u043E\u0434\u0430" })), /* @__PURE__ */ React.createElement(Field, { label: "Video URL (YouTube)", required: true, span2: true, hint: "Faqat YouTube URL formatida" }, /* @__PURE__ */ React.createElement("div", { className: "input-group" }, /* @__PURE__ */ React.createElement("span", { className: "prefix" }, /* @__PURE__ */ React.createElement(Icon, { name: "video", size: 14 })), /* @__PURE__ */ React.createElement("input", { className: "input", placeholder: "https://youtu.be/abc123" }))), /* @__PURE__ */ React.createElement(Field, { label: "Tartib raqami" }, /* @__PURE__ */ React.createElement(Input, { type: "number", defaultValue: 1, min: 1 })), /* @__PURE__ */ React.createElement(Field, { label: "Tur", required: true }, /* @__PURE__ */ React.createElement(Select, null, /* @__PURE__ */ React.createElement("option", { value: "santenik" }, "Santenik uchun"), /* @__PURE__ */ React.createElement("option", { value: "sotuvchi" }, "Sotuvchi uchun"))), /* @__PURE__ */ React.createElement(Field, { label: "Faollik", span2: true }, /* @__PURE__ */ React.createElement("label", { style: { display: "flex", alignItems: "center", gap: 8 } }, /* @__PURE__ */ React.createElement("input", { type: "checkbox", className: "checkbox", defaultChecked: true }), " ", /* @__PURE__ */ React.createElement("span", { className: "text-sm" }, "Botda ko'rsatilsin")))), /* @__PURE__ */ React.createElement("div", { className: "form-footer" }, /* @__PURE__ */ React.createElement(Button, { variant: "secondary" }, "Bekor qilish"), /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "check" }, "Saqlash")));
}
function MonthlySettingsPage() {
  const [on, setOn] = useState(true);
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(PageHeader, { title: "Oylik eslatma sozlamalari", subtitle: "Har oyning birinchi sanasida sotuvchilarga avtomatik xabar yuboriladi" }), /* @__PURE__ */ React.createElement(FormBlock, { title: "Avtomatik eslatma", icon: "bell", badge: on ? /* @__PURE__ */ React.createElement(Badge, { variant: "success", dot: true }, "YOQILGAN") : /* @__PURE__ */ React.createElement(Badge, { variant: "neutral", dot: true }, "O'CHIRILGAN") }, /* @__PURE__ */ React.createElement("div", { className: "span-2", style: {
    padding: 16,
    background: on ? "var(--success-soft)" : "var(--surface-2)",
    borderRadius: 8,
    display: "flex",
    alignItems: "center",
    gap: 14,
    border: "1px solid " + (on ? "rgba(16, 185, 129, 0.3)" : "var(--border)")
  } }, /* @__PURE__ */ React.createElement(Toggle, { on, onChange: setOn }), /* @__PURE__ */ React.createElement("div", { style: { flex: 1 } }, /* @__PURE__ */ React.createElement("div", { style: { color: "var(--text-strong)", fontWeight: 500, fontSize: 13.5 } }, on ? "Avtomatik eslatma yoqilgan" : "Avtomatik eslatma o'chirilgan"), /* @__PURE__ */ React.createElement("div", { className: "text-xs text-muted", style: { marginTop: 2 } }, on ? "Har oyning 1-sanasida belgilangan vaqtda bot xabar yuboradi" : "Hech qanday avtomatik xabar yuborilmaydi"))), /* @__PURE__ */ React.createElement(Field, { label: "\u{1F550} Yuborish vaqti (HH:MM)", hint: "Asia/Tashkent vaqti" }, /* @__PURE__ */ React.createElement(Input, { type: "time", defaultValue: "09:00" })), /* @__PURE__ */ React.createElement(Field, { label: "Maksimal urinish" }, /* @__PURE__ */ React.createElement(Input, { type: "number", defaultValue: 3, min: 1, max: 10 })), /* @__PURE__ */ React.createElement(Field, { label: "Xabar matni (UZ)", span2: true }, /* @__PURE__ */ React.createElement(Textarea, { rows: 4, defaultValue: "Assalomu alaykum! Yangi oy boshlandi. Bu oyda JIP partnyorlar uchun maxsus aksiyalar bor \u2014 botga kirib batafsil ma'lumot oling." })), /* @__PURE__ */ React.createElement(Field, { label: "Xabar matni (RU)", span2: true }, /* @__PURE__ */ React.createElement(Textarea, { rows: 4, defaultValue: "\u0417\u0434\u0440\u0430\u0432\u0441\u0442\u0432\u0443\u0439\u0442\u0435! \u041D\u0430\u0447\u0430\u043B\u0441\u044F \u043D\u043E\u0432\u044B\u0439 \u043C\u0435\u0441\u044F\u0446. \u0412 \u044D\u0442\u043E\u043C \u043C\u0435\u0441\u044F\u0446\u0435 \u0434\u043B\u044F \u043F\u0430\u0440\u0442\u043D\u0451\u0440\u043E\u0432 JIP \u2014 \u0441\u043F\u0435\u0446\u0438\u0430\u043B\u044C\u043D\u044B\u0435 \u0430\u043A\u0446\u0438\u0438. \u0417\u0430\u0439\u0434\u0438\u0442\u0435 \u0432 \u0431\u043E\u0442 \u0437\u0430 \u043F\u043E\u0434\u0440\u043E\u0431\u043D\u043E\u0441\u0442\u044F\u043C\u0438." }))), /* @__PURE__ */ React.createElement("div", { className: "form-footer" }, /* @__PURE__ */ React.createElement("span", { className: "text-muted text-sm" }, "Sozlamalar avtomatik tatbiq etiladi"), /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "check" }, "Sozlamalarni saqlash")));
}
function MonthlyLogPage() {
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(PageHeader, { title: "Oylik eslatma logi", subtitle: "Har oylik avtomatik eslatma jo'natilishlari tarixi" }), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "table-wrap" }, /* @__PURE__ */ React.createElement("table", { className: "table" }, /* @__PURE__ */ React.createElement("thead", null, /* @__PURE__ */ React.createElement("tr", null, /* @__PURE__ */ React.createElement("th", null, "Sana"), /* @__PURE__ */ React.createElement("th", null, "Holat"), /* @__PURE__ */ React.createElement("th", { style: { textAlign: "right" } }, "Yuborilganlar"), /* @__PURE__ */ React.createElement("th", { style: { textAlign: "right" } }, "Xatolar"), /* @__PURE__ */ React.createElement("th", null, "Vaqt"))), /* @__PURE__ */ React.createElement("tbody", null, JM.reminderLogs.map((r) => /* @__PURE__ */ React.createElement("tr", { key: r.id }, /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("span", { className: "text-mono text-sm text-muted" }, r.date)), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement(Badge, { variant: r.status === "done" ? "success" : "danger", icon: r.status === "done" ? "check" : "x" }, r.status === "done" ? "Bajarildi" : "Xato")), /* @__PURE__ */ React.createElement("td", { className: "num", style: { textAlign: "right", color: "var(--success-fg)" } }, r.sent), /* @__PURE__ */ React.createElement("td", { className: "num", style: { textAlign: "right", color: r.errors > 0 ? "var(--danger-fg)" : "var(--text-dim)" } }, r.errors), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("span", { className: "text-mono text-xs text-muted" }, r.duration)))))))));
}
function AdminContactsPage() {
  const iconFor = (t) => t === "Telegram" ? "send" : t === "Telefon" ? "phone" : "message-circle";
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(
    PageHeader,
    {
      title: "Admin kontaktlari",
      subtitle: "Botda \xABYordam\xBB bo'limida foydalanuvchilarga ko'rsatiladigan kontaktlar",
      actions: /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "plus" }, "Kontakt qo'shish")
    }
  ), /* @__PURE__ */ React.createElement("div", { className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "table-wrap" }, /* @__PURE__ */ React.createElement("table", { className: "table" }, /* @__PURE__ */ React.createElement("thead", null, /* @__PURE__ */ React.createElement("tr", null, /* @__PURE__ */ React.createElement("th", null, "Tur"), /* @__PURE__ */ React.createElement("th", null, "Qiymat"), /* @__PURE__ */ React.createElement("th", null, "Faollik"), /* @__PURE__ */ React.createElement("th", null))), /* @__PURE__ */ React.createElement("tbody", null, JM.adminContacts.map((c) => /* @__PURE__ */ React.createElement("tr", { key: c.id }, /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 10 } }, /* @__PURE__ */ React.createElement("span", { style: { width: 32, height: 32, borderRadius: 6, background: "var(--primary-soft)", color: "var(--primary)", display: "grid", placeItems: "center" } }, /* @__PURE__ */ React.createElement(Icon, { name: iconFor(c.type), size: 14 })), /* @__PURE__ */ React.createElement("span", { className: "text-strong", style: { fontWeight: 500 } }, c.type))), /* @__PURE__ */ React.createElement("td", null, /* @__PURE__ */ React.createElement("span", { className: "text-mono" }, c.value)), /* @__PURE__ */ React.createElement("td", null, c.is_active ? /* @__PURE__ */ React.createElement(StatusBadges.active, null) : /* @__PURE__ */ React.createElement(StatusBadges.inactive, null)), /* @__PURE__ */ React.createElement("td", { style: { textAlign: "right" } }, /* @__PURE__ */ React.createElement(Button, { size: "sm", variant: "ghost", icon: "edit" }), /* @__PURE__ */ React.createElement(Button, { size: "sm", variant: "ghost", icon: "trash" })))))))));
}
function PrivacyPolicyPage() {
  return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(
    PageHeader,
    {
      title: "Maxfiylik siyosati",
      subtitle: "Botda foydalanuvchilarga ko'rsatiladigan privacy hujjat",
      actions: /* @__PURE__ */ React.createElement(Button, { variant: "primary", icon: "plus" }, "Yangi hujjat")
    }
  ), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 } }, JM.policies.map((p) => /* @__PURE__ */ React.createElement("div", { key: p.id, className: "card" }, /* @__PURE__ */ React.createElement("div", { className: "card-header" }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 10 } }, /* @__PURE__ */ React.createElement("span", { style: { width: 32, height: 32, borderRadius: 6, background: "var(--primary-soft)", color: "var(--primary)", display: "grid", placeItems: "center" } }, /* @__PURE__ */ React.createElement(Icon, { name: "file-text", size: 14 })), /* @__PURE__ */ React.createElement("h3", null, p.title_ru)), p.is_active ? /* @__PURE__ */ React.createElement(StatusBadges.active, null) : /* @__PURE__ */ React.createElement(StatusBadges.inactive, null)), /* @__PURE__ */ React.createElement("div", { style: { padding: 16 } }, /* @__PURE__ */ React.createElement("div", { className: "text-sm text-muted", style: { marginBottom: 4 } }, "UZ nomi"), /* @__PURE__ */ React.createElement("div", { className: "text-strong", style: { marginBottom: 12 } }, p.title_uz), /* @__PURE__ */ React.createElement("div", { className: "text-sm text-muted", style: { marginBottom: 4 } }, "Yaratilgan"), /* @__PURE__ */ React.createElement("div", { className: "text-mono text-sm", style: { marginBottom: 12 } }, p.created), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 8, marginTop: 16 } }, /* @__PURE__ */ React.createElement(Button, { size: "sm", variant: "secondary", icon: "edit" }, "Tahrirlash"), /* @__PURE__ */ React.createElement(Button, { size: "sm", variant: "ghost", icon: "eye" }, "Ko'rish")))))), /* @__PURE__ */ React.createElement(FormBlock, { title: "HTML editor", icon: "code", single: true }, /* @__PURE__ */ React.createElement(Field, { label: "Sarlavha (UZ)" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: "Maxfiylik siyosati" })), /* @__PURE__ */ React.createElement(Field, { label: "Sarlavha (RU)" }, /* @__PURE__ */ React.createElement(Input, { defaultValue: "\u041F\u043E\u043B\u0438\u0442\u0438\u043A\u0430 \u043A\u043E\u043D\u0444\u0438\u0434\u0435\u043D\u0446\u0438\u0430\u043B\u044C\u043D\u043E\u0441\u0442\u0438" })), /* @__PURE__ */ React.createElement(Field, { label: "Matn (UZ) \u2014 HTML" }, /* @__PURE__ */ React.createElement(Textarea, { rows: 8, defaultValue: "<h2>Ma'lumotlarni yig'ish</h2>\n<p>JIP GROUP foydalanuvchilarning shaxsiy ma'lumotlarini...</p>" })), /* @__PURE__ */ React.createElement(Field, { label: "Matn (RU) \u2014 HTML" }, /* @__PURE__ */ React.createElement(Textarea, { rows: 8, defaultValue: "<h2>\u0421\u0431\u043E\u0440 \u0434\u0430\u043D\u043D\u044B\u0445</h2>\n<p>JIP GROUP \u0441\u043E\u0431\u0438\u0440\u0430\u0435\u0442 \u0441\u043B\u0435\u0434\u0443\u044E\u0449\u0438\u0435 \u043F\u0435\u0440\u0441\u043E\u043D\u0430\u043B\u044C\u043D\u044B\u0435 \u0434\u0430\u043D\u043D\u044B\u0435 \u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u0435\u043B\u0435\u0439...</p>" })), /* @__PURE__ */ React.createElement(Field, { label: "Faollik" }, /* @__PURE__ */ React.createElement("label", { style: { display: "flex", alignItems: "center", gap: 8 } }, /* @__PURE__ */ React.createElement("input", { type: "checkbox", className: "checkbox", defaultChecked: true }), " ", /* @__PURE__ */ React.createElement("span", { className: "text-sm" }, "Faol")))));
}
Object.assign(window, {
  ActivityLogPage,
  LivestreamsPage,
  LivestreamAddPage,
  RegionLogPage,
  VideosPage,
  VideoAddPage,
  MonthlySettingsPage,
  MonthlyLogPage,
  AdminContactsPage,
  PrivacyPolicyPage
});
const { useState: useStateApp, useEffect: useEffectApp } = React;
const TWEAK_DEFAULTS = {
  "sidebar": "dark",
  "density": "comfortable",
  "theme": "dark"
};
(function patchRealData() {
  const s = window.DJANGO_STATS;
  if (!s) return;
  if (window.JIP && window.JIP.stats) {
    if (s.users_total) window.JIP.stats.users_total = s.users_total;
    if (s.batches_active) window.JIP.stats.batches_active = s.batches_active;
    if (s.qr_total) window.JIP.stats.qr_total = s.qr_total;
    if (s.qr_scanned) window.JIP.stats.qr_scanned = s.qr_scanned;
    if (s.gifts_pending) window.JIP.stats.gifts_pending = s.gifts_pending;
    if (s.txns_total) window.JIP.stats.txns_total = s.txns_total;
    if (s.audit_total) window.JIP.stats.audit_total = s.audit_total;
  }
})();
function djAdmin(path) {
  return (window.DJANGO_ADMIN_BASE || "/admin/") + path;
}
const DJANGO_REDIRECT = {
  // These routes open Django admin instead of SPA pages
  "/users/santenik": () => djAdmin("core/telegramuser/"),
  "/users/sotuvchi": () => djAdmin("core/telegramuser/"),
  "/qrcodes/edit": () => djAdmin("core/qrcode/"),
  "/batches/add": () => djAdmin("core/qrcodebatch/add/"),
  "/batches/edit": () => djAdmin("core/qrcodebatch/"),
  "/stores/add": () => djAdmin("core/store/add/"),
  "/stores/edit": () => djAdmin("core/store/"),
  "/gifts/add": () => djAdmin("core/gift/add/"),
  "/redemptions/edit": () => djAdmin("core/giftredemption/"),
  "/transactions/add": () => djAdmin("core/sellerpointstransaction/add/"),
  "/livestreams/add": () => djAdmin("core/livestream/add/"),
  "/videos/add": () => djAdmin("core/videoinstruction/add/")
};
function useHashRoute() {
  const [route, setRoute] = useStateApp(() => {
    const h = window.location.hash.slice(1) || "/dashboard";
    return h.startsWith("/") ? h : "/" + h;
  });
  useEffectApp(() => {
    const onHash = () => {
      const h = window.location.hash.slice(1) || "/dashboard";
      const r = h.startsWith("/") ? h : "/" + h;
      setRoute(r);
    };
    window.addEventListener("hashchange", onHash);
    return () => window.removeEventListener("hashchange", onHash);
  }, []);
  const navigate = (r) => {
    const djUrl = DJANGO_REDIRECT[r];
    if (djUrl) {
      window.location.href = djUrl();
      return;
    }
    window.location.hash = r;
  };
  return [route, navigate];
}
function PageRouter({ route, onNavigate }) {
  switch (route) {
    case "/":
    case "/dashboard":
      return /* @__PURE__ */ React.createElement(DashboardPage, { onNavigate });
    case "/analytics":
      return /* @__PURE__ */ React.createElement(AnalyticsPage, null);
    case "/users":
      return /* @__PURE__ */ React.createElement(UsersListPage, { onNavigate });
    case "/users/santenik":
      return /* @__PURE__ */ React.createElement(UserSantenikPage, { onNavigate });
    case "/users/sotuvchi":
      return /* @__PURE__ */ React.createElement(UserSotuvchiPage, { onNavigate });
    case "/users/send-region":
      return /* @__PURE__ */ React.createElement(SendRegionMessagePage, null);
    case "/users/send-single":
      return /* @__PURE__ */ React.createElement(SendSingleMessagePage, null);
    case "/auth/users":
      return /* @__PURE__ */ React.createElement(AuthUsersPage, { onNavigate });
    case "/auth/groups":
      return /* @__PURE__ */ React.createElement(AuthGroupsPage, null);
    case "/qrcodes":
      return /* @__PURE__ */ React.createElement(QRCodesPage, { onNavigate });
    case "/qrcodes/edit":
      return /* @__PURE__ */ React.createElement(QRCodeEditPage, { onNavigate });
    case "/qrcodes/generate":
      return /* @__PURE__ */ React.createElement(QRGeneratePage, null);
    case "/batches":
      return /* @__PURE__ */ React.createElement(BatchesPage, { onNavigate });
    case "/batches/add":
      return /* @__PURE__ */ React.createElement(BatchAddPage, null);
    case "/batches/edit":
      return /* @__PURE__ */ React.createElement(BatchEditPage, { onNavigate });
    case "/stores":
      return /* @__PURE__ */ React.createElement(StoresPage, { onNavigate });
    case "/stores/edit":
      return /* @__PURE__ */ React.createElement(StoreEditPage, { onNavigate });
    case "/stores/add":
      return /* @__PURE__ */ React.createElement(StoreAddPage, null);
    case "/gifts":
      return /* @__PURE__ */ React.createElement(GiftsPage, { onNavigate });
    case "/gifts/add":
      return /* @__PURE__ */ React.createElement(GiftAddPage, null);
    case "/redemptions":
      return /* @__PURE__ */ React.createElement(RedemptionsPage, { onNavigate });
    case "/redemptions/edit":
      return /* @__PURE__ */ React.createElement(RedemptionEditPage, { onNavigate });
    case "/transactions":
      return /* @__PURE__ */ React.createElement(TransactionsPage, { onNavigate });
    case "/transactions/add":
      return /* @__PURE__ */ React.createElement(TransactionAddPage, null);
    case "/seller-codes":
      return /* @__PURE__ */ React.createElement(SellerCodesPage, null);
    case "/activity":
      return /* @__PURE__ */ React.createElement(ActivityLogPage, null);
    case "/livestreams":
      return /* @__PURE__ */ React.createElement(LivestreamsPage, { onNavigate });
    case "/livestreams/add":
      return /* @__PURE__ */ React.createElement(LivestreamAddPage, null);
    case "/regionlog":
      return /* @__PURE__ */ React.createElement(RegionLogPage, null);
    case "/videos":
      return /* @__PURE__ */ React.createElement(VideosPage, { onNavigate });
    case "/videos/add":
      return /* @__PURE__ */ React.createElement(VideoAddPage, null);
    case "/monthly":
      return /* @__PURE__ */ React.createElement(MonthlySettingsPage, null);
    case "/monthly-log":
      return /* @__PURE__ */ React.createElement(MonthlyLogPage, null);
    case "/contacts":
      return /* @__PURE__ */ React.createElement(AdminContactsPage, null);
    case "/privacy":
      return /* @__PURE__ */ React.createElement(PrivacyPolicyPage, null);
    default:
      return /* @__PURE__ */ React.createElement("div", { className: "page" }, /* @__PURE__ */ React.createElement(PageHeader, { title: "Sahifa topilmadi", subtitle: "Route: " + route }), /* @__PURE__ */ React.createElement(EmptyState, { icon: "help-circle", title: "404 \u2014 yo'q sahifa", hint: "Chap menyudan boshqa sahifani tanlang" }));
  }
}
function App() {
  const [route, navigate] = useHashRoute();
  const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);
  useEffectApp(() => {
    document.documentElement.setAttribute("data-sidebar", t.sidebar);
    document.documentElement.setAttribute("data-density", t.density);
    document.documentElement.setAttribute("data-theme", t.theme);
  }, [t.sidebar, t.density, t.theme]);
  useEffectApp(() => {
    const main = document.querySelector(".main");
    if (main) main.scrollTop = 0;
    window.scrollTo(0, 0);
  }, [route]);
  return /* @__PURE__ */ React.createElement("div", { className: "app", "data-screen-label": "route:" + route }, /* @__PURE__ */ React.createElement(Sidebar, { currentRoute: route, onNavigate: navigate }), /* @__PURE__ */ React.createElement("div", { className: "main" }, /* @__PURE__ */ React.createElement(Topbar, { route, onNavigate: navigate, tweaks: t, setTweak }), /* @__PURE__ */ React.createElement(PageRouter, { route, onNavigate: navigate })), /* @__PURE__ */ React.createElement(TweaksPanel, null, /* @__PURE__ */ React.createElement(TweakSection, { label: "Tema" }), /* @__PURE__ */ React.createElement(
    TweakRadio,
    {
      label: "Theme",
      value: t.theme,
      options: [
        { value: "dark", label: "\u{1F319} Tun" },
        { value: "light", label: "\u2600\uFE0F Kun" }
      ],
      onChange: (v) => setTweak("theme", v)
    }
  ), /* @__PURE__ */ React.createElement(TweakSection, { label: "Layout" }), /* @__PURE__ */ React.createElement(
    TweakRadio,
    {
      label: "Sidebar",
      value: t.sidebar,
      options: [
        { value: "dark", label: "Dark" },
        { value: "light", label: "Light" },
        { value: "icon", label: "Icons" }
      ],
      onChange: (v) => setTweak("sidebar", v)
    }
  ), /* @__PURE__ */ React.createElement(
    TweakRadio,
    {
      label: "Density",
      value: t.density,
      options: [
        { value: "comfortable", label: "Comfy" },
        { value: "compact", label: "Compact" }
      ],
      onChange: (v) => setTweak("density", v)
    }
  ), /* @__PURE__ */ React.createElement(TweakSection, { label: "Navigation" }), /* @__PURE__ */ React.createElement("div", { style: { padding: "8px 16px" } }, /* @__PURE__ */ React.createElement("a", { href: "/admin/", target: "_blank", style: {
    display: "flex",
    alignItems: "center",
    gap: 8,
    fontSize: 12,
    color: "var(--primary)",
    textDecoration: "none",
    padding: "6px 8px",
    borderRadius: 6,
    background: "var(--primary-soft)"
  } }, /* @__PURE__ */ React.createElement("svg", { width: "14", height: "14", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2" }, /* @__PURE__ */ React.createElement("path", { d: "M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" })), "Django Admin \u2192"))));
}
ReactDOM.createRoot(document.getElementById("root")).render(/* @__PURE__ */ React.createElement(App, null));
