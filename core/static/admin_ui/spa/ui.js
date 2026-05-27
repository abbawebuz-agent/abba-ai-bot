var __defProp = Object.defineProperty;
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
