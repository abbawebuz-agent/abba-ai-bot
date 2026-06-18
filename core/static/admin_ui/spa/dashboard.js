/* ============================================================================
 * JIP Admin Dashboard — "Modern Apple style UI" (Claude Design handoff)
 * Build-free port: plain React.createElement (no JSX / no esbuild step).
 * Reads REAL data from /jip-admin/api/<section>/ (read-only). Same look as the
 * approved prototype; data source swapped from mock -> Django JSON API.
 * ==========================================================================*/
(function () {
  "use strict";
  var React = window.React, ReactDOM = window.ReactDOM;
  if (!React || !ReactDOM) { console.error("React not loaded"); return; }

  var API_BASE = (window.DJANGO_SPA_BASE || "/jip-admin/") + "api/";
  var ADMIN_BASE = window.DJANGO_ADMIN_BASE || "/admin/";

  // Region centroids for the Leaflet map (codes from build_promo_table_rows)
  var REGION_COORDS = {
    tashkent_city: [41.31, 69.28], tashkent_region: [41.05, 69.78], tashkent: [41.31, 69.28],
    samarkand: [39.65, 66.96], samarqand: [39.65, 66.96],
    bukhara: [39.77, 64.42], buxoro: [39.77, 64.42],
    andijan: [40.78, 72.34], andijon: [40.78, 72.34],
    fergana: [40.39, 71.78], fargona: [40.39, 71.78],
    namangan: [41.0, 71.67],
    kashkadarya: [38.86, 65.79], qashqadaryo: [38.86, 65.79],
    surkhandarya: [37.23, 67.28], surxondaryo: [37.23, 67.28],
    khorezm: [41.55, 60.63], xorazm: [41.55, 60.63],
    navoi: [40.08, 65.38], navoiy: [40.08, 65.38],
    jizzakh: [40.12, 67.84], jizzax: [40.12, 67.84],
    syrdarya: [40.49, 68.78], sirdaryo: [40.49, 68.78],
    karakalpakstan: [42.9, 59.62], qoraqalpogiston: [42.9, 59.62]
  };

  class Dashboard extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        page: "overview", theme: "light", lang: "uz", range: "30d",
        collapsed: false, tabs: {}, filters: {}, detail: null, cache: {}
      };
      this._loading = null;
      this.h = function (t, p) { return React.createElement.apply(React, arguments); };
      this.ICONS = {
        overview: "M4 4h6v6H4z M14 4h6v6h-6z M4 14h6v6H4z M14 14h6v6h-6z",
        users: "M8.5 11a3 3 0 100-6 3 3 0 000 6z M3 20a5.5 5.5 0 0111 0 M16 11a3 3 0 100-6 M21.5 20a5.5 5.5 0 00-4-5.3",
        promo: "M4 7h16a1 1 0 011 1v2a2 2 0 000 4v2a1 1 0 01-1 1H4a1 1 0 01-1-1v-2a2 2 0 000-4V8a1 1 0 011-1z M15 7v12",
        gift: "M5 12h14v8H5z M3 8h18v4H3z M12 8v12 M12 8C9.5 8 8 4.5 10 4.5S12 8 12 8z M12 8c2.5 0 4-3.5 2-3.5S12 8 12 8z",
        seller: "M4 9l1.2-4.5h13.6L20 9 M5 9v10h14V9 M5 9a2.2 2.2 0 003.5 0 2.2 2.2 0 003.5 0 2.2 2.2 0 003.5 0 2.2 2.2 0 003 0 M10 19v-5h4v5",
        geo: "M12 21s-6.5-5.6-6.5-10.5a6.5 6.5 0 1113 0C18.5 15.4 12 21 12 21z M12 12.5a2.5 2.5 0 100-5 2.5 2.5 0 000 5z",
        fraud: "M12 3l7.5 2.8v5.7c0 4.6-3.4 7.6-7.5 8.7-4.1-1.1-7.5-4.1-7.5-8.7V5.8z M9 11.5l2 2 4-4",
        broadcast: "M3.5 10.5v3a1 1 0 001 1H7l4.5 4V5.5L7 9.5H4.5a1 1 0 00-1 1z M15 8.5a4.5 4.5 0 010 7 M17.5 5.5a8 8 0 010 13",
        lottery: "M8 4h8v3.5a4 4 0 01-8 0z M8 5.5H5.5A2 2 0 007.5 10 M16 5.5h2.5A2 2 0 0116.5 10 M10.5 12.5v3.5 M13.5 12.5v3.5 M8.5 20h7 M9.5 16h5",
        photos: "M4 5.5h16v13H4z M8.5 11a2 2 0 100-4 2 2 0 000 4z M4 16l4.5-4.5 4 4 3.5-3.5 4 4",
        audit: "M7 3.5h7l4 4v13H7z M14 3.5v4h4 M9.5 12.5h6 M9.5 16h6 M9.5 9h2.5",
        admin: "M12 15.2a3.2 3.2 0 100-6.4 3.2 3.2 0 000 6.4z M19.4 12c0-.5 0-.9-.1-1.4l2-1.5-2-3.4-2.3 1a7 7 0 00-2.4-1.4L14.2 3h-4.4l-.4 2.3a7 7 0 00-2.4 1.4l-2.3-1-2 3.4 2 1.5c-.1.5-.1.9-.1 1.4s0 .9.1 1.4l-2 1.5 2 3.4 2.3-1a7 7 0 002.4 1.4l.4 2.3h4.4l.4-2.3a7 7 0 002.4-1.4l2.3 1 2-3.4-2-1.5c.1-.5.1-.9.1-1.4z",
        logout: "M15.5 17l5-5-5-5 M20.5 12H10 M12 3.5H6a2 2 0 00-2 2v13a2 2 0 002 2h6",
        refresh: "M20.5 12a8.5 8.5 0 11-2.8-6.3L20.5 8 M20.5 3.5V8h-4.5",
        export: "M12 3.5v11 M8 10.5l4 4 4-4 M4.5 17v2a2 2 0 002 2h11a2 2 0 002-2v-2",
        sun: "M12 16.5a4.5 4.5 0 100-9 4.5 4.5 0 000 9z M12 2.5v2 M12 19.5v2 M4.5 12h-2 M21.5 12h-2 M5.6 5.6L7 7 M17 17l1.4 1.4 M18.4 5.6L17 7 M7 17l-1.4 1.4",
        moon: "M20.5 13A8.5 8.5 0 1111 2.5a6.6 6.6 0 009.5 10.5z",
        menu: "M4 7h16 M4 12h16 M4 17h16",
        search: "M11 17a6 6 0 100-12 6 6 0 000 12z M20 20l-3.6-3.6",
        chevron: "M9.5 6l6 6-6 6",
        clock: "M12 21a9 9 0 100-18 9 9 0 000 18z M12 7.5V12l3 2",
        close: "M6 6l12 12 M18 6L6 18",
        arrow: "M5 12h14 M13 6l6 6-6 6"
      };
      this.makeComponents();
    }

    // ----------------------------- data loading ----------------------------
    cacheKey(section) { return section + "::" + this.state.range + "::" + this.state.lang; }
    cur() { return this.state.cache[this.cacheKey(this.state.page)]; }
    ensure() {
      var key = this.cacheKey(this.state.page);
      if (this.state.cache[key] || this._loading === key) return;
      this._loading = key;
      var self = this, section = this.state.page;
      fetch(API_BASE + section + "/?range=" + this.state.range + "&lang=" + this.state.lang,
        { credentials: "same-origin", headers: { "X-Requested-With": "XMLHttpRequest" } })
        .then(function (r) { return r.json(); })
        .then(function (j) {
          self._loading = null;
          var val = (j && j.ok) ? j.data : { __error: (j && j.error) || "error" };
          self.setState(function (s) { var c = Object.assign({}, s.cache); c[key] = val; return { cache: c }; });
        })
        .catch(function (e) {
          self._loading = null;
          self.setState(function (s) { var c = Object.assign({}, s.cache); c[key] = { __error: String(e) }; return { cache: c }; });
        });
    }
    componentDidMount() { this.ensure(); }
    componentDidUpdate() { this.ensure(); }
    reloadCurrent() {
      var key = this.cacheKey(this.state.page);
      this.setState(function (s) { var c = Object.assign({}, s.cache); delete c[key]; return { cache: c }; });
    }

    // ----------------------------- formatting ------------------------------
    L(o) { if (o && typeof o === "object" && !Array.isArray(o) && (("uz" in o) || ("ru" in o))) return o[this.state.lang] != null ? o[this.state.lang] : o.uz; return o; }
    fmt(n) { return Math.round(n || 0).toLocaleString("ru-RU").replace(/ /g, " "); }
    pct(n) { return (Math.round((n || 0) * 10) / 10).toString().replace(".", ",") + "%"; }

    pal() {
      if (this.state.theme === "dark") return {
        bg: "#0B0C0F", bg2: "#101116", panel: "rgba(16,17,22,0.82)", card: "#14151A", card2: "#1A1C22", cardHi: "#1F2128",
        text: "#EDEEF1", text2: "#9094A0", text3: "#626775", sep: "#22242B", sepHi: "#2E313A",
        accent: "#7C82F2", accentText: "#A2A7F8", accentSoft: "rgba(124,130,242,0.16)", accentSoft2: "rgba(124,130,242,0.09)",
        green: "#3DBE79", greenSoft: "rgba(61,190,121,0.15)", red: "#E8675E", redSoft: "rgba(232,103,94,0.15)",
        orange: "#D6A05A", orangeSoft: "rgba(214,160,90,0.15)", purple: "#9D8CF0", purpleSoft: "rgba(157,140,240,0.15)",
        teal: "#5FB1C4", pink: "#D58CA6", yellow: "#D4BE68",
        chart: ["#7C82F2", "#A6ABF7", "#C9CCFA", "#7B8294", "#464A57"], iconBg: "#1E2027",
        shadow: "0 1px 2px rgba(0,0,0,0.4), 0 6px 20px rgba(0,0,0,0.38)", shadowHi: "0 12px 32px rgba(0,0,0,0.5)",
        input: "#1A1C22", inputBorder: "#2E313A", track: "#22242B"
      };
      return {
        bg: "#F6F7F9", bg2: "#FCFCFD", panel: "rgba(252,252,253,0.82)", card: "#FFFFFF", card2: "#F8F9FB", cardHi: "#FFFFFF",
        text: "#11131A", text2: "#596072", text3: "#9298A6", sep: "#ECEEF1", sepHi: "#E0E2E8",
        accent: "#4F46E5", accentText: "#4339D6", accentSoft: "rgba(79,70,229,0.08)", accentSoft2: "rgba(79,70,229,0.05)",
        green: "#177D4D", greenSoft: "rgba(23,125,77,0.10)", red: "#C2362E", redSoft: "rgba(194,54,46,0.09)",
        orange: "#A56911", orangeSoft: "rgba(165,105,17,0.10)", purple: "#6D52C9", purpleSoft: "rgba(109,82,201,0.10)",
        teal: "#1A7E91", pink: "#B53E68", yellow: "#977916",
        chart: ["#4F46E5", "#838AEF", "#B4B9F5", "#8990A0", "#C6CBD4"], iconBg: "#F1F2F5",
        shadow: "0 1px 2px rgba(17,19,26,0.04), 0 4px 14px rgba(17,19,26,0.05)", shadowHi: "0 10px 28px rgba(17,19,26,0.10)",
        input: "#FFFFFF", inputBorder: "#E1E3E9", track: "#EEEFF2"
      };
    }

    icon(name, size, sw, color) {
      var h = this.h;
      return h("svg", { width: size || 20, height: size || 20, viewBox: "0 0 24 24", fill: "none", stroke: color || "currentColor", "strokeWidth": sw || 1.7, "strokeLinecap": "round", "strokeLinejoin": "round", style: { display: "block", flex: "none" } }, h("path", { d: this.ICONS[name] || "" }));
    }

    // hover helper (replaces DC style-hover)
    hov(base, hover) {
      return {
        onMouseEnter: function (e) { for (var k in hover) e.currentTarget.style[k] = hover[k]; },
        onMouseLeave: function (e) { for (var k in hover) e.currentTarget.style[k] = (base && base[k] != null) ? base[k] : ""; }
      };
    }

    // --------------------------- reusable components -----------------------
    makeComponents() {
      var self = this; var h = this.h;
      this.Count = function Count(props) { var value = props.value, format = props.format; return (format || (function (x) { return self.fmt(x); }))(value); };

      this.DataTable = function DataTable(props) {
        var columns = props.columns, rows = props.rows, P = props.P, pageSize = props.pageSize, onRow = props.onRow, toolbar = props.toolbar, dense = props.dense;
        var ps = pageSize || 9;
        var qS = React.useState(""); var q = qS[0], setQ = qS[1];
        var sortS = React.useState({ key: null, dir: 1 }); var sort = sortS[0], setSort = sortS[1];
        var pgS = React.useState(0); var pg = pgS[0], setPg = pgS[1];
        var data = rows || [];
        if (q) { var s = q.toLowerCase(); data = data.filter(function (r) { return columns.some(function (c) { try { return String(c.get ? c.get(r) : "").toLowerCase().includes(s); } catch (e) { return false; } }); }); }
        if (sort.key) { var col = columns.find(function (c) { return c.key === sort.key; }); if (col && col.get) { data = data.slice().sort(function (a, b) { var av = col.get(a), bv = col.get(b); var an = typeof av === "number", bn = typeof bv === "number"; var r; if (an && bn) r = av - bv; else r = String(av).localeCompare(String(bv)); return r * sort.dir; }); } }
        var pages = Math.max(1, Math.ceil(data.length / ps));
        var cur = Math.min(pg, pages - 1);
        var slice = data.slice(cur * ps, (cur + 1) * ps);
        var thBase = { padding: "0 16px 12px", textAlign: "left", font: "600 11px/1 inherit", letterSpacing: ".04em", textTransform: "uppercase", color: P.text3, whiteSpace: "nowrap", userSelect: "none" };
        return h("div", { style: { display: "flex", flexDirection: "column", gap: 0 } },
          h("div", { style: { display: "flex", alignItems: "center", gap: 12, marginBottom: 14, flexWrap: "wrap" } },
            h("div", { style: { position: "relative", flex: "0 0 auto" } },
              h("span", { style: { position: "absolute", left: 11, top: "50%", transform: "translateY(-50%)", color: P.text3, pointerEvents: "none" } }, self.icon("search", 16, 1.7)),
              h("input", { value: q, onChange: function (e) { setQ(e.target.value); setPg(0); }, placeholder: self.L({ uz: "Qidirish…", ru: "Поиск…" }), style: { width: 240, height: 38, padding: "0 12px 0 34px", borderRadius: 11, border: "1px solid " + P.inputBorder, background: P.input, color: P.text, outline: "none", font: "500 13.5px inherit", transition: "border-color .2s, box-shadow .2s" }, onFocus: function (e) { e.target.style.borderColor = P.accent; e.target.style.boxShadow = "0 0 0 4px " + P.accentSoft; }, onBlur: function (e) { e.target.style.borderColor = P.inputBorder; e.target.style.boxShadow = "none"; } })
            ),
            toolbar || null,
            h("div", { style: { marginLeft: "auto", font: "500 12.5px inherit", color: P.text3 } }, self.fmt(data.length) + " " + self.L({ uz: "ta yozuv", ru: "записей" }))
          ),
          h("div", { style: { background: P.card, borderRadius: 14, border: "1px solid " + P.sep, boxShadow: P.shadow, overflow: "hidden" } },
            h("div", { style: { overflowX: "auto" } },
              h("table", { style: { width: "100%", borderCollapse: "collapse", minWidth: Math.max(640, columns.length * 120) } },
                h("thead", null, h("tr", { style: { borderBottom: "1px solid " + P.sep } }, columns.map(function (c, i) {
                  return h("th", { key: i, onClick: c.get ? function () { setSort(function (st) { return { key: c.key, dir: st.key === c.key ? -st.dir : 1 }; }); } : undefined, style: Object.assign({}, thBase, { paddingTop: 16, cursor: c.get ? "pointer" : "default", textAlign: c.align || "left" }) },
                    h("span", { style: { display: "inline-flex", alignItems: "center", gap: 5, justifyContent: c.align === "right" ? "flex-end" : "flex-start" } }, self.L(c.label), sort.key === c.key ? h("span", { style: { color: P.accent, fontSize: 9 } }, sort.dir > 0 ? "▲" : "▼") : null));
                }))),
                h("tbody", null, slice.length ? slice.map(function (r, ri) {
                  return h("tr", { key: ri, onClick: onRow ? function () { onRow(r); } : undefined, style: { borderTop: ri ? "1px solid " + P.sep : "none", cursor: onRow ? "pointer" : "default", transition: "background .15s", animation: "fadeIn .4s ease both", animationDelay: (ri * 24) + "ms" }, onMouseEnter: function (e) { e.currentTarget.style.background = P.accentSoft2; }, onMouseLeave: function (e) { e.currentTarget.style.background = "transparent"; } },
                    columns.map(function (c, ci) { return h("td", { key: ci, style: { padding: (dense ? "11px 16px" : "14px 16px"), font: "500 13.5px inherit", color: P.text, textAlign: c.align || "left", verticalAlign: "middle", whiteSpace: c.wrap ? "normal" : "nowrap" } }, c.render ? c.render(r, P) : (c.get ? c.get(r) : "")); }));
                }) : h("tr", null, h("td", { colSpan: columns.length, style: { padding: "48px 16px", textAlign: "center", color: P.text3, font: "500 14px inherit" } }, self.L({ uz: "Ma'lumot topilmadi", ru: "Данные не найдены" }))))
              )
            )
          ),
          pages > 1 ? h("div", { style: { display: "flex", alignItems: "center", justifyContent: "space-between", marginTop: 14 } },
            h("div", { style: { font: "500 12.5px inherit", color: P.text3 } }, (cur * ps + 1) + "–" + Math.min((cur + 1) * ps, data.length) + " / " + self.fmt(data.length)),
            h("div", { style: { display: "flex", gap: 8 } },
              self.pageBtn(P, "‹", function () { setPg(Math.max(0, cur - 1)); }, cur === 0),
              h("div", { style: { display: "flex", alignItems: "center", padding: "0 14px", borderRadius: 10, background: P.card, border: "1px solid " + P.sep, font: "600 13px inherit", color: P.text } }, (cur + 1) + " / " + pages),
              self.pageBtn(P, "›", function () { setPg(Math.min(pages - 1, cur + 1)); }, cur === pages - 1)
            )
          ) : null
        );
      };

      this.UzMap = function UzMap(props) {
        var P = props.P, regions = props.regions, theme = props.theme, lang = props.lang, onSelect = props.onSelect;
        var ref = React.useRef();
        React.useEffect(function () {
          var cancelled = false;
          self.loadLeaflet().then(function () {
            if (cancelled || !ref.current) return;
            var Lf = window.L; var el = ref.current; el.innerHTML = "";
            var map = Lf.map(el, { zoomControl: true, attributionControl: false, minZoom: 4, maxZoom: 12, scrollWheelZoom: true, zoomAnimation: false, fadeAnimation: false, markerZoomAnimation: false, zoomSnap: 0.5, wheelPxPerZoomLevel: 80 }).setView([41.5, 63.9], 5.5);
            ref._map = map;
            var url = theme === "dark" ? "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png" : "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png";
            Lf.tileLayer(url, { maxZoom: 19, subdomains: "abcd" }).addTo(map);
            var maxV = Math.max.apply(null, regions.map(function (r) { return r.v; }).concat([1]));
            var markers = [];
            regions.forEach(function (rg) {
              if (rg.lat == null) return;
              var rad = 7 + (rg.v / maxV) * 20;
              var cm = Lf.circleMarker([rg.lat, rg.lng], { radius: rad, color: P.accent, weight: 2, opacity: .95, fillColor: P.accent, fillOpacity: .32 });
              cm.addTo(map);
              cm.on("click", function () { if (onSelect) onSelect(rg); });
              cm.on("mouseover", function () { this.setStyle({ fillOpacity: .6 }); });
              cm.on("mouseout", function () { this.setStyle({ fillOpacity: .32 }); });
              var html = '<div style="font-weight:700">' + self.L(rg.label) + '</div><div style="opacity:.85;margin-top:1px">' + self.fmt(rg.v) + ' ' + self.L({ uz: "foydalanuvchi", ru: "польз." }) + '</div>';
              markers.push({ cm: cm, html: html });
            });
            function updateTips() { var z = map.getZoom(); markers.forEach(function (o) { if (z >= 6) { if (!o.cm.getTooltip()) o.cm.bindTooltip(o.html, { permanent: true, direction: "top", offset: [0, -3], className: "uz-tip" }); o.cm.openTooltip(); } else if (o.cm.getTooltip()) { o.cm.unbindTooltip(); } }); }
            map.on("zoomend", updateTips); updateTips();
            [120, 450, 800].forEach(function (t) { setTimeout(function () { try { map.invalidateSize(); } catch (e) { } }, t); });
          }).catch(function () { if (ref.current) ref.current.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:' + P.text3 + ';font:500 14px inherit">Xarita yuklanmadi (internet kerak)</div>'; });
          return function () { cancelled = true; try { if (ref._map) { ref._map.remove(); ref._map = null; } } catch (e) { } };
        }, [theme, lang, regions]);
        return React.createElement("div", { ref: ref, style: { height: 480, width: "100%", background: P.card2 } });
      };
    }

    loadLeaflet() {
      if (window.L) return Promise.resolve();
      if (this._leafletP) return this._leafletP;
      this._leafletP = new Promise(function (res, rej) {
        var css = document.createElement("link"); css.rel = "stylesheet"; css.href = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"; document.head.appendChild(css);
        var st = document.createElement("style"); st.textContent = ".leaflet-container{background:transparent;font-family:inherit;} .leaflet-tooltip.uz-tip{background:rgba(17,19,26,.92);color:#fff;border:none;box-shadow:0 4px 14px rgba(0,0,0,.3);border-radius:8px;padding:5px 9px;font-size:12px;line-height:1.25;white-space:nowrap;} .leaflet-tooltip.uz-tip:before{display:none;} .leaflet-bar a{border-radius:8px!important;}"; document.head.appendChild(st);
        var sc = document.createElement("script"); sc.src = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"; sc.onload = function () { res(); }; sc.onerror = rej; document.head.appendChild(sc);
      });
      return this._leafletP;
    }

    pageBtn(P, label, onClick, disabled) {
      var h = this.h;
      return h("button", { onClick: disabled ? undefined : onClick, disabled: disabled, style: { width: 36, height: 36, borderRadius: 10, border: "1px solid " + P.sep, background: P.card, color: disabled ? P.text3 : P.text, cursor: disabled ? "default" : "pointer", font: "600 16px inherit", opacity: disabled ? 0.5 : 1, transition: "all .15s", display: "flex", alignItems: "center", justifyContent: "center" }, onMouseEnter: function (e) { if (!disabled) { e.currentTarget.style.background = P.accentSoft; e.currentTarget.style.borderColor = P.accent; e.currentTarget.style.color = P.accent; } }, onMouseLeave: function (e) { e.currentTarget.style.background = P.card; e.currentTarget.style.borderColor = P.sep; e.currentTarget.style.color = disabled ? P.text3 : P.text; } }, label);
    }

    // ----------------------------- chart helpers ---------------------------
    lineArea(P, series, color, opts) {
      var h = this.h; opts = opts || {};
      var W = opts.w || 520, H = opts.h || 170, pad = 8;
      var flat = Array.isArray(series[0]) ? series.reduce(function (a, b) { return a.concat(b); }, []) : series;
      var max = Math.max.apply(null, flat.concat([1])) * 1.12 || 1;
      var gid = "g" + Math.floor(Math.random() * 1e6);
      function mk(arr, col) {
        var n = arr.length || 1; var step = (W - pad * 2) / Math.max(1, n - 1);
        var pts = arr.map(function (v, i) { return [pad + i * step, H - pad - (v / max) * (H - pad * 2)]; });
        if (!pts.length) pts = [[pad, H - pad]];
        var d = pts.map(function (p, i) { return (i ? "L" : "M") + p[0].toFixed(1) + " " + p[1].toFixed(1); }).join(" ");
        var area = d + " L" + pts[pts.length - 1][0].toFixed(1) + " " + (H - pad) + " L" + pts[0][0].toFixed(1) + " " + (H - pad) + " Z";
        return { d: d, area: area, pts: pts, col: col };
      }
      var lines = Array.isArray(series[0]) ? series.map(function (s, i) { return mk(s, opts.colors[i]); }) : [mk(series, color)];
      return h("svg", { viewBox: "0 0 " + W + " " + H, width: "100%", height: H, preserveAspectRatio: "none", style: { display: "block", overflow: "visible" } },
        h("defs", null, lines.map(function (ln, i) { return h("linearGradient", { key: i, id: gid + i, x1: "0", y1: "0", x2: "0", y2: "1" }, h("stop", { offset: "0", stopColor: ln.col, stopOpacity: 0.26 }), h("stop", { offset: "1", stopColor: ln.col, stopOpacity: 0 })); })),
        [0.25, 0.5, 0.75, 1].map(function (g, i) { return h("line", { key: "gl" + i, x1: pad, x2: W - pad, y1: H - pad - g * (H - pad * 2), y2: H - pad - g * (H - pad * 2), stroke: P.sep, strokeWidth: 1, strokeDasharray: "1 5" }); }),
        lines.map(function (ln, i) {
          return h("g", { key: i },
            h("path", { d: ln.area, fill: "url(#" + gid + i + ")", style: { animation: "fadeIn 1s ease both", animationDelay: "0.3s" } }),
            h("path", { d: ln.d, fill: "none", stroke: ln.col, strokeWidth: 2.4, strokeLinecap: "round", strokeLinejoin: "round", pathLength: "1", style: { strokeDasharray: 1, strokeDashoffset: 1, animation: "dash 1.3s cubic-bezier(.16,1,.3,1) both", animationDelay: (i * 0.15) + "s" } }),
            h("circle", { cx: ln.pts[ln.pts.length - 1][0], cy: ln.pts[ln.pts.length - 1][1], r: 3.5, fill: ln.col, style: { animation: "pop .4s ease both", animationDelay: "1.2s" } })
          );
        })
      );
    }

    donut(P, segs, opts) {
      var h = this.h; opts = opts || {}; var self = this;
      var size = opts.size || 180, sw = opts.sw || 26, r = (size - sw) / 2, C = 2 * Math.PI * r, cx = size / 2;
      var total = segs.reduce(function (a, s) { return a + s.v; }, 0) || 1;
      var acc = 0;
      return h("div", { style: { display: "flex", alignItems: "center", gap: 24, flexWrap: "wrap" } },
        h("div", { style: { position: "relative", width: size, height: size, flex: "none" } },
          h("svg", { width: size, height: size, viewBox: "0 0 " + size + " " + size, style: { transform: "rotate(-90deg)", animation: "pop .6s cubic-bezier(.16,1,.3,1) both" } },
            h("circle", { cx: cx, cy: cx, r: r, fill: "none", stroke: P.track, strokeWidth: sw }),
            segs.map(function (s, i) { var len = (s.v / total) * C; var off = -acc; acc += len; return h("circle", { key: i, cx: cx, cy: cx, r: r, fill: "none", stroke: s.c, strokeWidth: sw, strokeDasharray: len + " " + (C - len), strokeDashoffset: off, strokeLinecap: "butt" }); })
          ),
          h("div", { style: { position: "absolute", inset: 0, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 2 } },
            h("div", { style: { font: "700 26px inherit", letterSpacing: "-.02em", color: P.text } }, h(this.Count, { value: total })),
            h("div", { style: { font: "500 11.5px inherit", color: P.text3 } }, opts.label ? this.L(opts.label) : this.L({ uz: "Jami", ru: "Всего" }))
          )
        ),
        h("div", { style: { display: "flex", flexDirection: "column", gap: 9, minWidth: 150 } }, segs.map(function (s, i) {
          return h("div", { key: i, style: { display: "flex", alignItems: "center", gap: 10, animation: "fadeIn .5s ease both", animationDelay: (i * 60 + 200) + "ms" } },
            h("span", { style: { width: 10, height: 10, borderRadius: 3, background: s.c, flex: "none" } }),
            h("span", { style: { font: "500 13px inherit", color: P.text2, flex: 1 } }, self.L(s.label)),
            h("span", { style: { font: "600 13px inherit", color: P.text } }, self.fmt(s.v)),
            h("span", { style: { font: "500 12px inherit", color: P.text3, width: 42, textAlign: "right" } }, self.pct(s.v / total * 100))
          );
        }))
      );
    }

    vbars(P, items, color) {
      var h = this.h; var self = this;
      var max = Math.max.apply(null, items.map(function (i) { return i.v; }).concat([1]));
      return h("div", { style: { display: "flex", alignItems: "flex-end", gap: 10, height: 150, paddingTop: 10 } }, items.map(function (it, i) {
        return h("div", { key: i, style: { flex: 1, display: "flex", flexDirection: "column", alignItems: "center", gap: 8, height: "100%", justifyContent: "flex-end" } },
          h("div", { style: { font: "600 11px inherit", color: P.text2 } }, it.v),
          h("div", { style: { width: "100%", maxWidth: 34, height: (it.v / max * 100) + "%", minHeight: 4, borderRadius: "7px 7px 3px 3px", background: it.c || color || P.accent, transformOrigin: "bottom", animation: "barGrowY .9s cubic-bezier(.16,1,.3,1) both", animationDelay: (i * 50) + "ms" } }),
          h("div", { style: { font: "500 11px inherit", color: P.text3, whiteSpace: "nowrap" } }, self.L(it.label))
        );
      }));
    }

    // ------------------------------- ui atoms ------------------------------
    badge(P, text, kind) {
      var map = { green: [P.green, P.greenSoft], red: [P.red, P.redSoft], orange: [P.orange, P.orangeSoft], accent: [P.accent, P.accentSoft], purple: [P.purple, P.purpleSoft], teal: [P.teal, P.accentSoft], gray: [P.text2, P.track] };
      var pair = map[kind] || map.gray;
      return this.h("span", { style: { display: "inline-flex", alignItems: "center", gap: 5, padding: "3px 10px", borderRadius: 8, background: pair[1], color: pair[0], font: "600 12px inherit", whiteSpace: "nowrap" } }, text);
    }
    card(P, children, extra, i) {
      return this.h("div", { style: Object.assign({ background: P.card, borderRadius: 16, border: "1px solid " + P.sep, boxShadow: P.shadow, padding: 22, animation: "cardIn .55s cubic-bezier(.16,1,.3,1) both", animationDelay: ((i || 0) * 45) + "ms" }, (extra || {})) }, children);
    }
    sectionTitle(P, text, right) {
      return this.h("div", { style: { display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 4 } },
        this.h("h2", { style: { margin: 0, font: "600 17px inherit", letterSpacing: "-.01em", color: P.text } }, this.L(text)), right || null);
    }
    chartCard(P, title, node, i, sub) {
      var h = this.h;
      return this.card(P, h("div", null,
        h("div", { style: { display: "flex", alignItems: "baseline", justifyContent: "space-between", marginBottom: 18 } },
          h("div", null, h("div", { style: { font: "600 15px inherit", color: P.text, letterSpacing: "-.01em" } }, this.L(title)), sub ? h("div", { style: { font: "500 12.5px inherit", color: P.text3, marginTop: 3 } }, this.L(sub)) : null)
        ), node
      ), null, i);
    }
    kpi(P, item, i) {
      var h = this.h;
      var trendUp = item.trend != null && item.trend >= 0;
      return h("div", { onClick: item.onClick, style: { background: P.card, borderRadius: 14, border: "1px solid " + P.sep, boxShadow: P.shadow, padding: "18px 18px 16px", cursor: item.onClick ? "pointer" : "default", transition: "transform .25s cubic-bezier(.16,1,.3,1), box-shadow .25s", animation: "cardIn .55s cubic-bezier(.16,1,.3,1) both", animationDelay: ((i || 0) * 45) + "ms", position: "relative", overflow: "hidden" }, onMouseEnter: function (e) { if (item.onClick) { e.currentTarget.style.transform = "translateY(-3px)"; e.currentTarget.style.boxShadow = P.shadowHi; } }, onMouseLeave: function (e) { e.currentTarget.style.transform = "none"; e.currentTarget.style.boxShadow = P.shadow; } },
        h("div", { style: { display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 8, marginBottom: 14 } },
          h("div", { style: { font: "600 12.5px inherit", color: P.text2, lineHeight: 1.3 } }, this.L(item.label)),
          item.icon ? h("div", { style: { width: 34, height: 34, borderRadius: 9, background: P.iconBg, color: P.text2, display: "flex", alignItems: "center", justifyContent: "center", flex: "none" } }, this.icon(item.icon, 18, 1.7)) : null
        ),
        h("div", { style: { font: "700 28px inherit", letterSpacing: "-.03em", color: P.text, lineHeight: 1 } }, h(this.Count, { value: item.value, format: item.format })),
        h("div", { style: { display: "flex", alignItems: "center", gap: 8, marginTop: 12, minHeight: 18 } },
          item.trend != null ? h("span", { style: { display: "inline-flex", alignItems: "center", gap: 3, padding: "2px 7px", borderRadius: 7, background: trendUp ? P.greenSoft : P.redSoft, color: trendUp ? P.green : P.red, font: "700 11.5px inherit" } }, (trendUp ? "▲" : "▼") + " " + Math.abs(item.trend) + "%") : null,
          item.sub ? h("span", { style: { font: "500 12px inherit", color: P.text3 } }, this.L(item.sub)) : null
        )
      );
    }
    kpiGrid(P, items, cols) {
      var self = this;
      return this.h("div", { style: { display: "grid", gridTemplateColumns: "repeat(" + (cols || 4) + ", minmax(0,1fr))", gap: 16 } }, items.map(function (it, i) { return self.kpi(P, it, i); }));
    }
    segmented(P, tabs, active, onChange) {
      var h = this.h; var self = this;
      return h("div", { style: { display: "inline-flex", padding: 4, borderRadius: 12, background: P.track, gap: 3 } }, tabs.map(function (t, i) { var on = t.key === active; return h("button", { key: i, onClick: function () { onChange(t.key); }, style: { padding: "7px 16px", borderRadius: 9, border: "none", background: on ? P.card : "transparent", color: on ? P.text : P.text2, font: "600 13px inherit", cursor: "pointer", boxShadow: on ? P.shadow : "none", transition: "all .2s", whiteSpace: "nowrap" } }, self.L(t.label)); }));
    }
    pageWrap(P, children) {
      return this.h("div", { key: this.state.page, style: { display: "flex", flexDirection: "column", gap: 24, animation: "slideContent .5s cubic-bezier(.16,1,.3,1) both", maxWidth: 1320, margin: "0 auto" } }, children);
    }
    loadingBlock(P) {
      var h = this.h;
      return h("div", { key: "load", style: { display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 16, padding: "120px 0", color: P.text3 } },
        h("div", { style: { width: 38, height: 38, borderRadius: "50%", border: "3px solid " + P.track, borderTopColor: P.accent, animation: "spin .8s linear infinite" } }),
        h("div", { style: { font: "500 13.5px inherit" } }, this.L({ uz: "Yuklanmoqda…", ru: "Загрузка…" }))
      );
    }
    errorBlock(P, msg) {
      var h = this.h;
      return h("div", { key: "err", style: { padding: "60px 24px", textAlign: "center", color: P.red, font: "500 14px inherit" } },
        h("div", { style: { marginBottom: 8, fontSize: 28 } }, "⚠"),
        this.L({ uz: "Ma'lumot yuklab bo'lmadi", ru: "Не удалось загрузить данные" }),
        msg ? h("div", { style: { marginTop: 8, font: "500 12px ui-monospace,monospace", color: P.text3 } }, String(msg).slice(0, 200)) : null
      );
    }

    // --------------------------- state actions -----------------------------
    setPage(k) { this.setState({ page: k, detail: null }); var sc = document.querySelector("[data-scroll]"); if (sc) sc.scrollTop = 0; }
    getTab(page, def) { return this.state.tabs[page] || def; }
    setTab(page, key) { this.setState(function (s) { var t = Object.assign({}, s.tabs); t[page] = key; return { tabs: t }; }); }
    getFilter(key, def) { return this.state.filters[key] != null ? this.state.filters[key] : def; }
    setFilter(key, val) { this.setState(function (s) { var f = Object.assign({}, s.filters); f[key] = val; return { filters: f }; }); }

    rstatusInfo(st) {
      var m = { pending: ["orange", { uz: "Kutilmoqda", ru: "Ожидает" }], approved: ["accent", { uz: "Tasdiqlangan", ru: "Одобрено" }], sent: ["teal", { uz: "Yuborilgan", ru: "Отправлено" }], completed: ["green", { uz: "Yakunlangan", ru: "Завершено" }], rejected: ["red", { uz: "Rad etilgan", ru: "Отклонено" }], cancelled: ["gray", { uz: "Bekor qilingan", ru: "Отменено" }], not_received: ["purple", { uz: "Olinmagan", ru: "Не получено" }] };
      return m[st] || ["gray", st];
    }
    typeInfo(t) {
      var m = { santenik: ["accent", { uz: "Santexnik", ru: "Сантехник" }], sotuvchi: ["purple", { uz: "Sotuvchi", ru: "Продавец" }], none: ["gray", { uz: "Tanlanmagan", ru: "Не выбран" }] };
      return m[t] || ["gray", t];
    }

    initials(name) { return (name || "").split(" ").map(function (x) { return x[0]; }).filter(Boolean).slice(0, 2).join(""); }

    // ------------------------------- PAGES ---------------------------------
    renderPage(P) {
      var d = this.cur();
      if (!d) return this.pageWrap(P, [this.loadingBlock(P)]);
      if (d.__error) return this.pageWrap(P, [this.errorBlock(P, d.__error)]);
      switch (this.state.page) {
        case "overview": return this.pgOverview(P, d);
        case "users": return this.pgUsers(P, d);
        case "promo": return this.pgPromo(P, d);
        case "gift": return this.pgGift(P, d);
        case "seller": return this.pgSeller(P, d);
        case "geo": return this.pgGeo(P, d);
        case "fraud": return this.pgFraud(P, d);
        case "broadcast": return this.pgBroadcast(P, d);
        case "lottery": return this.pgLottery(P, d);
        case "photos": return this.pgPhotos(P, d);
        case "audit": return this.pgAudit(P, d);
        default: return this.pgOverview(P, d);
      }
    }

    pgOverview(P, d) {
      var h = this.h; var head = d.head || {}; var c = d.charts || {}; var tr = d.trends || {};
      var actPct = head.qrTotal ? Math.round(head.qrScan / head.qrTotal * 1000) / 10 : 0;
      var self = this;
      var kpis = [
        { label: { uz: "Jami foydalanuvchi", ru: "Всего пользователей" }, value: head.uTotal, trend: tr.users, sub: { uz: "davr o'sishi", ru: "за период" }, icon: "users", onClick: function () { self.setPage("users"); } },
        { label: { uz: "Santexniklar", ru: "Сантехники" }, value: head.uSan, sub: { uz: "usta", ru: "мастера" }, icon: "users", onClick: function () { self.setFilter("userType", "santenik"); self.setPage("users"); } },
        { label: { uz: "Sotuvchilar", ru: "Продавцы" }, value: head.uSel, sub: { uz: "hamkor", ru: "партнёры" }, icon: "seller", onClick: function () { self.setFilter("userType", "sotuvchi"); self.setPage("users"); } },
        { label: { uz: "Rol tanlamagan", ru: "Без роли" }, value: head.uUns, icon: "users" },
        { label: { uz: "Jami promokod", ru: "Всего промокодов" }, value: head.qrTotal, icon: "promo", onClick: function () { self.setPage("promo"); } },
        { label: { uz: "Skanlangan", ru: "Сканировано" }, value: head.qrScan, sub: { uz: "aktivatsiya " + this.pct(actPct), ru: "активация " + this.pct(actPct) }, icon: "promo" },
        { label: { uz: "Tarqatilgan ball", ru: "Начислено баллов" }, value: head.ptsTotal, trend: tr.points, icon: "lottery" },
        { label: { uz: "Kutilayotgan so'rov", ru: "Ожидающие заявки" }, value: head.giftsPending, icon: "gift", onClick: function () { self.setTab("gift", "requests"); self.setPage("gift"); } }
      ];
      var rs = d.redStats || {};
      var redSegs = [
        { label: { uz: "Yakunlangan", ru: "Завершено" }, v: rs.completed || 0, c: P.chart[0] },
        { label: { uz: "Yuborilgan", ru: "Отправлено" }, v: rs.sent || 0, c: P.chart[1] },
        { label: { uz: "Tasdiqlangan", ru: "Одобрено" }, v: rs.approved || 0, c: P.chart[2] },
        { label: { uz: "Kutilmoqda", ru: "Ожидает" }, v: rs.pending || 0, c: P.chart[3] },
        { label: { uz: "Rad/Bekor", ru: "Откл/Отмена" }, v: (rs.rejected || 0) + (rs.cancelled || 0) + (rs.not_received || 0), c: P.chart[4] }
      ];
      var sg = d.segments || {};
      var segSegs = [
        { label: { uz: "Toza", ru: "Чистые" }, v: sg.clean || 0, c: P.chart[1] },
        { label: { uz: "Ogohlantirish", ru: "Внимание" }, v: sg.warning || 0, c: P.chart[3] },
        { label: { uz: "Shubhali", ru: "Подозрит." }, v: sg.suspicious || 0, c: P.orange },
        { label: { uz: "Bloklangan", ru: "Заблок." }, v: sg.blocked || 0, c: P.red }
      ];
      return this.pageWrap(P, [
        h("div", { key: "k", style: { display: "grid", gridTemplateColumns: "repeat(4,minmax(0,1fr))", gap: 16 } }, kpis.map(function (it, i) { return self.kpi(P, it, i); })),
        h("div", { key: "ch", style: { display: "grid", gridTemplateColumns: "repeat(3,minmax(0,1fr))", gap: 16 } }, [
          this.chartCard(P, { uz: "Ro'yxatdan o'tishlar", ru: "Регистрации" }, this.lineArea(P, c.reg || [], P.accent, { h: 150 }), 8, { uz: "kunlik yangi foydalanuvchilar", ru: "новые пользователи / день" }),
          this.chartCard(P, { uz: "Promokod aktivatsiyasi", ru: "Активация промокодов" }, this.lineArea(P, c.act || [], P.green, { h: 150 }), 9, { uz: "kunlik skanlar", ru: "сканирования / день" }),
          this.chartCard(P, { uz: "Sovg'a so'rovlari", ru: "Заявки на подарки" }, this.lineArea(P, c.red || [], P.orange, { h: 150 }), 10, { uz: "kunlik so'rovlar", ru: "заявки / день" })
        ]),
        h("div", { key: "d", style: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 } }, [
          this.chartCard(P, { uz: "Sovg'a so'rovlari taqsimoti", ru: "Распределение заявок" }, this.donut(P, redSegs, { label: { uz: "so'rov", ru: "заявок" } }), 11),
          this.chartCard(P, { uz: "Foydalanuvchi integriteti", ru: "Целостность пользователей" }, this.donut(P, segSegs, { label: { uz: "user", ru: "польз." } }), 12)
        ])
      ]);
    }

    pgUsers(P, d) {
      var h = this.h; var self = this; var k = d.kpis || {};
      var ft = this.getFilter("userType", "all");
      var rows = d.rows || []; if (ft !== "all") rows = rows.filter(function (u) { return u.type === ft; });
      var kpis = [
        { label: { uz: "Jami foydalanuvchi", ru: "Всего" }, value: k.total, icon: "users" },
        { label: { uz: "Santexniklar", ru: "Сантехники" }, value: k.san, icon: "users" },
        { label: { uz: "Sotuvchilar", ru: "Продавцы" }, value: k.sel, icon: "seller" },
        { label: { uz: "Bugun qo'shilgan", ru: "Сегодня добавлено" }, value: k.today, icon: "users" }
      ];
      var filters = [["all", { uz: "Hammasi", ru: "Все" }], ["santenik", { uz: "Santexnik", ru: "Сантехники" }], ["sotuvchi", { uz: "Sotuvchi", ru: "Продавцы" }], ["none", { uz: "Rol yo'q", ru: "Без роли" }]];
      var toolbar = h("div", { style: { display: "flex", gap: 6, flexWrap: "wrap" } }, filters.map(function (f, i) { var on = ft === f[0]; return h("button", { key: i, onClick: function () { self.setFilter("userType", f[0]); }, style: { padding: "8px 14px", borderRadius: 10, border: "1px solid " + (on ? P.accent : P.sep), background: on ? P.accentSoft : P.card, color: on ? P.accent : P.text2, font: "600 12.5px inherit", cursor: "pointer", transition: "all .15s" } }, self.L(f[1])); }));
      var cols = [
        { key: "name", label: { uz: "Foydalanuvchi", ru: "Пользователь" }, get: function (u) { return u.name; }, render: function (u, P) { return h("div", { style: { display: "flex", alignItems: "center", gap: 11 } }, h("div", { style: { width: 34, height: 34, borderRadius: "50%", background: P.accentSoft, color: P.accent, display: "flex", alignItems: "center", justifyContent: "center", font: "700 13px inherit", flex: "none" } }, self.initials(u.name)), h("div", null, h("div", { style: { font: "600 13.5px inherit", color: P.text } }, u.name), h("div", { style: { font: "500 12px inherit", color: P.text3 } }, u.username))); } },
        { key: "phone", label: { uz: "Telefon", ru: "Телефон" }, get: function (u) { return u.phone; } },
        { key: "type", label: { uz: "Rol", ru: "Роль" }, get: function (u) { return u.type; }, render: function (u, P) { var ci = self.typeInfo(u.type); return self.badge(P, self.L(ci[1]), ci[0]); } },
        { key: "region", label: { uz: "Viloyat", ru: "Регион" }, get: function (u) { return u.region || ""; }, render: function (u, P) { return u.region ? u.region : h("span", { style: { color: P.text3 } }, "—"); } },
        { key: "points", label: { uz: "Ball", ru: "Баллы" }, align: "right", get: function (u) { return u.points; }, render: function (u, P) { return h("span", { style: { font: "600 13.5px inherit", color: u.points > 0 ? P.text : P.text3 } }, self.fmt(u.points)); } },
        { key: "complete", label: { uz: "Ro'yxat", ru: "Регистр." }, align: "center", get: function (u) { return u.complete ? 1 : 0; }, render: function (u, P) { return u.complete ? self.badge(P, "✓", "green") : self.badge(P, "⏳", "orange"); } },
        { key: "status", label: { uz: "Holat", ru: "Статус" }, get: function (u) { return u.blocked ? 2 : (u.active ? 0 : 1); }, render: function (u, P) { return u.blocked ? self.badge(P, self.L({ uz: "Bloklangan", ru: "Заблок." }), "red") : (u.active ? self.badge(P, self.L({ uz: "Faol", ru: "Активен" }), "green") : self.badge(P, self.L({ uz: "Nofaol", ru: "Неактивен" }), "gray")); } },
        { key: "created", label: { uz: "Qo'shilgan", ru: "Добавлен" }, align: "right", get: function (u) { return u.created; } }
      ];
      return this.pageWrap(P, [
        h("div", { key: "k" }, this.kpiGrid(P, kpis, 4)),
        h("div", { key: "t" }, h(this.DataTable, { columns: cols, rows: rows, P: P, pageSize: 10, toolbar: toolbar, onRow: function (u) { self.setState({ detail: { type: "user", row: u } }); } }))
      ]);
    }

    pgPromo(P, d) {
      var h = this.h; var self = this; var k = d.kpis || {};
      var kpis = [
        { label: { uz: "Jami promokod", ru: "Всего" }, value: k.total, icon: "promo" },
        { label: { uz: "Skanlangan", ru: "Сканировано" }, value: k.scanned, icon: "promo" },
        { label: { uz: "Skanlanmagan", ru: "Не сканир." }, value: k.unscanned, icon: "promo" },
        { label: { uz: "Aktivatsiya %", ru: "Активация %" }, value: k.activation, format: function (x) { return self.pct(x); }, icon: "lottery" },
        { label: { uz: "Ball pool", ru: "Пул баллов" }, value: k.points, icon: "lottery" }
      ];
      var cols = [
        { key: "seq", label: { uz: "№", ru: "№" }, get: function (p) { return p.seq; } },
        { key: "code", label: { uz: "Kod", ru: "Код" }, get: function (p) { return p.code; }, render: function (p, P) { return h("span", { style: { font: "600 13px ui-monospace,SFMono-Regular,Menlo,monospace", color: P.text } }, p.code); } },
        { key: "serial", label: { uz: "Serial", ru: "Серийный" }, get: function (p) { return p.serial; } },
        { key: "points", label: { uz: "Ball", ru: "Баллы" }, align: "right", get: function (p) { return p.points; } },
        { key: "scanned", label: { uz: "Holat", ru: "Статус" }, get: function (p) { return p.scanned ? 1 : 0; }, render: function (p, P) { return p.scanned ? self.badge(P, self.L({ uz: "Skanlangan", ru: "Сканир." }), "green") : self.badge(P, self.L({ uz: "Yangi", ru: "Новый" }), "gray"); } },
        { key: "by", label: { uz: "Kim skanladi", ru: "Кто сканировал" }, get: function (p) { return p.by ? p.by.name : ""; }, render: function (p, P) { return p.by ? h("div", null, h("div", { style: { font: "600 13px inherit", color: P.text } }, p.by.name), h("div", { style: { font: "500 11.5px inherit", color: P.text3 } }, p.by.phone)) : h("span", { style: { color: P.text3 } }, "—"); } },
        { key: "at", label: { uz: "Sana", ru: "Дата" }, align: "right", get: function (p) { return p.at; }, render: function (p, P) { return p.at ? p.at : h("span", { style: { color: P.text3 } }, "—"); } },
        { key: "batch", label: { uz: "Partiya", ru: "Партия" }, get: function (p) { return p.batch; } }
      ];
      return this.pageWrap(P, [
        h("div", { key: "k" }, this.kpiGrid(P, kpis, 5)),
        h("div", { key: "t" }, h(this.DataTable, { columns: cols, rows: d.rows || [], P: P, pageSize: 9 }))
      ]);
    }

    pgGift(P, d) {
      var h = this.h; var self = this;
      var tab = this.getTab("gift", "catalog");
      var tabs = [{ key: "catalog", label: { uz: "Katalog", ru: "Каталог" } }, { key: "requests", label: { uz: "So'rovlar", ru: "Заявки" } }];
      var body;
      if (tab === "catalog") {
        var gifts = d.catalog || [];
        var kpis = [
          { label: { uz: "Jami sovg'a", ru: "Всего подарков" }, value: gifts.length, icon: "gift" },
          { label: { uz: "Faol", ru: "Активные" }, value: gifts.filter(function (g) { return g.active; }).length, icon: "gift" },
          { label: { uz: "Jami so'rovlar", ru: "Всего заявок" }, value: gifts.reduce(function (a, g) { return a + (g.req || 0); }, 0), icon: "gift" }
        ];
        var grid = h("div", { style: { display: "grid", gridTemplateColumns: "repeat(4,minmax(0,1fr))", gap: 16 } }, gifts.map(function (g, i) {
          return h("div", { key: i, style: { background: P.card, borderRadius: 18, border: "1px solid " + P.sep, boxShadow: P.shadow, overflow: "hidden", animation: "cardIn .5s cubic-bezier(.16,1,.3,1) both", animationDelay: (i * 40) + "ms", transition: "transform .25s, box-shadow .25s", opacity: g.active ? 1 : 0.6 }, onMouseEnter: function (e) { e.currentTarget.style.transform = "translateY(-3px)"; e.currentTarget.style.boxShadow = P.shadowHi; }, onMouseLeave: function (e) { e.currentTarget.style.transform = "none"; e.currentTarget.style.boxShadow = P.shadow; } },
            h("div", { style: { height: 120, background: P.card2, borderBottom: "1px solid " + P.sep, display: "flex", alignItems: "center", justifyContent: "center", position: "relative" } },
              h("div", { style: { width: 50, height: 50, borderRadius: 13, background: P.iconBg, color: P.text2, display: "flex", alignItems: "center", justifyContent: "center" } }, self.icon("gift", 24, 1.7)),
              !g.active ? h("span", { style: { position: "absolute", top: 10, right: 10, padding: "3px 9px", borderRadius: 7, background: P.track, color: P.text2, font: "600 11px inherit" } }, self.L({ uz: "Nofaol", ru: "Неактивен" })) : null
            ),
            h("div", { style: { padding: 16 } },
              h("div", { style: { font: "600 14px inherit", color: P.text, marginBottom: 6, minHeight: 36 } }, g.name),
              h("div", { style: { display: "flex", alignItems: "center", justifyContent: "space-between" } },
                h("div", { style: { display: "flex", alignItems: "center", gap: 5, color: P.accent, font: "700 15px inherit" } }, self.fmt(g.cost), h("span", { style: { font: "500 11px inherit", color: P.text3 } }, self.L({ uz: "ball", ru: "балл" }))),
                h("span", { style: { font: "500 12px inherit", color: P.text3 } }, self.L({ uz: "zaxira", ru: "остаток" }) + ": " + (g.stock === "∞" ? "∞" : g.stock))
              ),
              h("div", { style: { marginTop: 12, paddingTop: 12, borderTop: "1px solid " + P.sep, font: "500 12px inherit", color: P.text2, display: "flex", alignItems: "center", gap: 6 } }, self.icon("users", 14, 1.7, P.text3), self.fmt(g.req) + " " + self.L({ uz: "marta so'ralgan", ru: "раз запрошено" }))
            )
          );
        }));
        body = [h("div", { key: "k" }, this.kpiGrid(P, kpis, 3)), h("div", { key: "g" }, grid)];
      } else {
        var rs = d.redStats || {};
        var totalReq = Object.keys(rs).reduce(function (a, kk) { return a + (rs[kk] || 0); }, 0);
        var kpis2 = [
          { label: { uz: "Jami so'rov", ru: "Всего заявок" }, value: totalReq, icon: "gift" },
          { label: { uz: "Kutilmoqda", ru: "Ожидает" }, value: rs.pending || 0, icon: "clock" },
          { label: { uz: "Yakunlangan", ru: "Завершено" }, value: rs.completed || 0, icon: "gift" },
          { label: { uz: "Sarflangan ball", ru: "Потрачено баллов" }, value: (rs.completed || 0) * 820, icon: "lottery" }
        ];
        var cols = [
          { key: "user", label: { uz: "Foydalanuvchi", ru: "Пользователь" }, get: function (r) { return r.user.name; }, render: function (r, P) { return h("div", null, h("div", { style: { font: "600 13.5px inherit", color: P.text } }, r.user.name), h("div", { style: { font: "500 11.5px inherit", color: P.text3 } }, r.user.phone)); } },
          { key: "gift", label: { uz: "Sovg'a", ru: "Подарок" }, get: function (r) { return r.gift; }, render: function (r, P) { return h("div", { style: { display: "flex", alignItems: "center", gap: 9 } }, h("span", { style: { width: 8, height: 8, borderRadius: 3, background: r.giftColor } }), r.gift); } },
          { key: "cost", label: { uz: "Narx", ru: "Цена" }, align: "right", get: function (r) { return r.cost; }, render: function (r) { return self.fmt(r.cost); } },
          { key: "status", label: { uz: "Holat", ru: "Статус" }, get: function (r) { return r.status; }, render: function (r, P) { var ci = self.rstatusInfo(r.status); return self.badge(P, self.L(ci[1]), ci[0]); } },
          { key: "at", label: { uz: "So'ralgan", ru: "Запрошено" }, align: "right", get: function (r) { return r.at; } }
        ];
        var donutSegs = [
          { label: { uz: "Yakunlangan", ru: "Завершено" }, v: rs.completed || 0, c: P.chart[0] }, { label: { uz: "Yuborilgan", ru: "Отправлено" }, v: rs.sent || 0, c: P.chart[1] },
          { label: { uz: "Tasdiqlangan", ru: "Одобрено" }, v: rs.approved || 0, c: P.chart[2] }, { label: { uz: "Kutilmoqda", ru: "Ожидает" }, v: rs.pending || 0, c: P.chart[3] },
          { label: { uz: "Boshqa", ru: "Прочее" }, v: (rs.rejected || 0) + (rs.cancelled || 0) + (rs.not_received || 0), c: P.chart[4] }
        ];
        body = [h("div", { key: "k" }, this.kpiGrid(P, kpis2, 4)), h("div", { key: "d" }, this.chartCard(P, { uz: "Status taqsimoti", ru: "Распределение статусов" }, this.donut(P, donutSegs), 4)), h("div", { key: "t" }, h(this.DataTable, { columns: cols, rows: d.requests || [], P: P, pageSize: 9, onRow: function (r) { self.setState({ detail: { type: "redemption", row: r } }); } }))];
      }
      return this.pageWrap(P, [h("div", { key: "seg" }, this.segmented(P, tabs, tab, function (kk) { self.setTab("gift", kk); }))].concat(body));
    }

    pgSeller(P, d) {
      var h = this.h; var self = this; var k = d.kpis || {};
      var tab = this.getTab("seller", "list");
      var tabs = [{ key: "list", label: { uz: "Sotuvchilar", ru: "Продавцы" } }, { key: "pending", label: { uz: "Tasdiqlanmagan", ru: "Не одобрены" } }];
      if (tab === "pending") {
        var pend = d.pending || [];
        var cols0 = [
          { key: "name", label: { uz: "Foydalanuvchi", ru: "Пользователь" }, get: function (u) { return u.name; }, render: function (u, P) { return h("div", null, h("div", { style: { font: "600 13.5px inherit", color: P.text } }, u.name), h("div", { style: { font: "500 11.5px inherit", color: P.text3 } }, u.username)); } },
          { key: "phone", label: { uz: "Telefon", ru: "Телефон" }, get: function (u) { return u.phone; } },
          { key: "region", label: { uz: "Viloyat", ru: "Регион" }, get: function (u) { return u.region || "—"; } },
          { key: "created", label: { uz: "So'rov sanasi", ru: "Дата заявки" }, align: "right", get: function (u) { return u.created; } },
          { key: "st", label: { uz: "Holat", ru: "Статус" }, align: "right", get: function () { return 0; }, render: function (u, P) { return self.badge(P, self.L({ uz: "Kutilmoqda", ru: "Ожидает" }), "orange"); } }
        ];
        return this.pageWrap(P, [
          h("div", { key: "seg" }, this.segmented(P, tabs, tab, function (kk) { self.setTab("seller", kk); })),
          h("div", { key: "info", style: { padding: "14px 18px", borderRadius: 14, background: P.orangeSoft, color: P.orange, font: "500 13px inherit", display: "flex", alignItems: "center", gap: 10 } }, this.icon("fraud", 18, 1.8), this.L({ uz: "Tasdiqlash faqat admin panelda bajariladi — bu yerda faqat ko'rish.", ru: "Одобрение выполняется только в админ-панели — здесь только просмотр." })),
          h("div", { key: "t" }, h(this.DataTable, { columns: cols0, rows: pend, P: P, pageSize: 8 }))
        ]);
      }
      var kpis = [
        { label: { uz: "Jami sotuvchi", ru: "Всего продавцов" }, value: k.total, icon: "seller" },
        { label: { uz: "Tasdiqlangan", ru: "Одобрено" }, value: k.approved, icon: "seller" },
        { label: { uz: "Tasdiqlanmagan", ru: "Не одобрено" }, value: k.pending, icon: "clock" },
        { label: { uz: "Berilgan promokod", ru: "Выдано промокодов" }, value: k.qrIssued, icon: "promo" },
        { label: { uz: "O'rtacha aktivatsiya", ru: "Сред. активация" }, value: k.avgAct, format: function (x) { return self.pct(x); }, icon: "lottery" }
      ];
      var cols = [
        { key: "name", label: { uz: "Sotuvchi", ru: "Продавец" }, get: function (s) { return s.name; }, render: function (s, P) { return h("div", { style: { display: "flex", alignItems: "center", gap: 11 } }, h("div", { style: { width: 34, height: 34, borderRadius: 10, background: P.purpleSoft, color: P.purple, display: "flex", alignItems: "center", justifyContent: "center", flex: "none" } }, self.icon("seller", 18, 1.8)), h("div", null, h("div", { style: { font: "600 13.5px inherit", color: P.text } }, s.name), h("div", { style: { font: "500 11.5px inherit", color: P.text3 } }, s.owner || s.region))); } },
        { key: "region", label: { uz: "Viloyat", ru: "Регион" }, get: function (s) { return s.region; } },
        { key: "batches", label: { uz: "Partiyalar", ru: "Партии" }, align: "right", get: function (s) { return s.batches; } },
        { key: "total", label: { uz: "Promokod", ru: "Промокоды" }, align: "right", get: function (s) { return s.total; }, render: function (s) { return self.fmt(s.total); } },
        { key: "act", label: { uz: "Aktiv", ru: "Активир." }, align: "right", get: function (s) { return s.act; }, render: function (s) { return self.fmt(s.act); } },
        { key: "pct", label: { uz: "Aktivatsiya %", ru: "Активация %" }, align: "right", get: function (s) { return s.pct; }, render: function (s, P) { return h("span", { style: { display: "inline-flex", alignItems: "center", gap: 8, justifyContent: "flex-end" } }, h("span", { style: { width: 54, height: 7, borderRadius: 5, background: P.track, overflow: "hidden" } }, h("span", { style: { display: "block", height: "100%", width: s.pct + "%", background: s.pct > 60 ? P.green : s.pct > 40 ? P.orange : P.red } })), h("span", { style: { font: "600 13px inherit", color: P.text, width: 42, textAlign: "right" } }, self.pct(s.pct))); } },
        { key: "points", label: { uz: "Ball", ru: "Баллы" }, align: "right", get: function (s) { return s.points; }, render: function (s) { return self.fmt(s.points); } }
      ];
      return this.pageWrap(P, [
        h("div", { key: "seg" }, this.segmented(P, tabs, tab, function (kk) { self.setTab("seller", kk); })),
        h("div", { key: "k" }, this.kpiGrid(P, kpis, 5)),
        h("div", { key: "t" }, h(this.DataTable, { columns: cols, rows: d.rows || [], P: P, pageSize: 9, onRow: function (s) { self.setState({ detail: { type: "seller", row: s } }); } }))
      ]);
    }

    pgGeo(P, d) {
      var h = this.h; var self = this;
      var items = (d.regions || []).map(function (r) {
        var c = REGION_COORDS[r.code] || null;
        return { label: r.name, code: r.code, v: r.v, scan: r.scan, pts: r.pts, lat: c ? c[0] : null, lng: c ? c[1] : null };
      });
      var cols = [
        { key: "region", label: { uz: "Viloyat", ru: "Регион" }, get: function (r) { return r.label; }, render: function (r, P) { return h("div", { style: { display: "flex", alignItems: "center", gap: 10 } }, h("span", { style: { color: P.accent } }, self.icon("geo", 16, 1.8)), h("span", { style: { font: "600 13.5px inherit", color: P.text } }, r.label)); } },
        { key: "users", label: { uz: "Foydalanuvchi", ru: "Пользователи" }, align: "right", get: function (r) { return r.v; }, render: function (r) { return self.fmt(r.v); } },
        { key: "scan", label: { uz: "Skanlar", ru: "Сканирования" }, align: "right", get: function (r) { return r.scan; }, render: function (r) { return self.fmt(r.scan); } },
        { key: "points", label: { uz: "Ball", ru: "Баллы" }, align: "right", get: function (r) { return r.pts; }, render: function (r) { return self.fmt(r.pts); } },
        { key: "d", label: { uz: "", ru: "" }, align: "right", get: null, render: function (r, P) { return h("span", { style: { color: P.text3 } }, self.icon("chevron", 16, 1.8)); } }
      ];
      return this.pageWrap(P, [
        h("div", { key: "bc", style: { display: "flex", alignItems: "center", gap: 8, font: "500 13px inherit", color: P.text2 } }, h("span", { style: { color: P.accent, fontWeight: 600 } }, "O'zbekiston"), h("span", { style: { color: P.text3 } }, "›"), this.L({ uz: "Barcha viloyatlar", ru: "Все регионы" })),
        h("div", { key: "map" }, this.card(P, h("div", null,
          h("div", { style: { display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 12, marginBottom: 16, flexWrap: "wrap" } },
            h("div", null, h("div", { style: { font: "600 15px inherit", color: P.text } }, this.L({ uz: "O'zbekiston xaritasi", ru: "Карта Узбекистана" })), h("div", { style: { font: "500 12.5px inherit", color: P.text3, marginTop: 3, maxWidth: 520 } }, this.L({ uz: "Nuqtalar — viloyatlar faolligi. Yaqinlashtirsangiz raqamlar va shaharlar ko'rinadi.", ru: "Точки — активность регионов. При приближении появляются цифры и города." }))),
            h("div", { style: { display: "flex", alignItems: "center", gap: 7, padding: "7px 12px", borderRadius: 9, background: P.accentSoft, color: P.accent, font: "600 12px inherit", whiteSpace: "nowrap" } }, this.icon("search", 14, 1.9), this.L({ uz: "Yaqinlashtiring", ru: "Приблизьте" }))
          ),
          h("div", { style: { borderRadius: 12, overflow: "hidden", border: "1px solid " + P.sep } }, h(this.UzMap, { P: P, regions: items, theme: this.state.theme, lang: this.state.lang, onSelect: function (rg) { self.setState({ detail: { type: "region", row: rg } }); } }))
        ), null, 2)),
        h("div", { key: "t" }, h(this.DataTable, { columns: cols, rows: items, P: P, pageSize: 14, onRow: function (r) { self.setState({ detail: { type: "region", row: r } }); } }))
      ]);
    }

    pgFraud(P, d) {
      var h = this.h; var self = this; var k = d.kpis || {};
      var kpis = [
        { label: { uz: "Jami urinish", ru: "Всего попыток" }, value: k.total, icon: "fraud" },
        { label: { uz: "Muvaffaqiyatli", ru: "Успешных" }, value: k.success, icon: "fraud" },
        { label: { uz: "Xato", ru: "Ошибочных" }, value: k.failed, icon: "fraud" },
        { label: { uz: "Muvaffaqiyat %", ru: "Успех %" }, value: k.successRate, format: function (x) { return self.pct(x); }, icon: "lottery" },
        { label: { uz: "Bloklangan user", ru: "Заблок. польз." }, value: k.blocked, icon: "fraud" }
      ];
      var sg = d.segments || {};
      var segSegs = [{ label: { uz: "Toza", ru: "Чистые" }, v: sg.clean || 0, c: P.chart[1] }, { label: { uz: "Ogohlantirish", ru: "Внимание" }, v: sg.warning || 0, c: P.chart[3] }, { label: { uz: "Shubhali", ru: "Подозрит." }, v: sg.suspicious || 0, c: P.red }, { label: { uz: "Bloklangan", ru: "Заблок." }, v: sg.blocked || 0, c: P.purple }];
      var src = d.sources || {};
      var srcSegs = [{ label: { uz: "Bot", ru: "Бот" }, v: src.bot || 0, c: P.chart[0] }, { label: { uz: "Webapp", ru: "Webapp" }, v: src.webapp || 0, c: P.chart[2] }, { label: { uz: "Noma'lum", ru: "Неизвестно" }, v: src.unknown || 0, c: P.chart[4] }];
      var lbCols = [
        { key: "r", label: { uz: "#", ru: "#" }, get: function (r) { return r._i; }, render: function (r, P) { return h("span", { style: { font: "700 14px inherit", color: r._i <= 3 ? P.red : P.text3 } }, r._i); } },
        { key: "name", label: { uz: "Foydalanuvchi", ru: "Пользователь" }, get: function (u) { return u.name; }, render: function (u, P) { return h("div", null, h("div", { style: { font: "600 13.5px inherit", color: P.text } }, u.name), h("div", { style: { font: "500 11.5px inherit", color: P.text3 } }, u.phone)); } },
        { key: "region", label: { uz: "Viloyat", ru: "Регион" }, get: function (u) { return u.region || "—"; } },
        { key: "fails", label: { uz: "Ketma-ket xato", ru: "Подряд ошибок" }, align: "right", get: function (u) { return u.fails; }, render: function (u, P) { return self.badge(P, u.fails + "", u.fails >= 7 ? "red" : "orange"); } }
      ];
      var lb = (d.leaderboard || []).map(function (u, i) { return Object.assign({}, u, { _i: i + 1 }); });
      var atCols = [
        { key: "user", label: { uz: "Foydalanuvchi", ru: "Пользователь" }, get: function (a) { return a.user.name; }, render: function (a, P) { return h("div", null, h("div", { style: { font: "600 13px inherit", color: P.text } }, a.user.name), h("div", { style: { font: "500 11.5px inherit", color: P.text3 } }, a.user.phone)); } },
        { key: "raw", label: { uz: "Kiritilgan kod", ru: "Введённый код" }, get: function (a) { return a.raw; }, render: function (a, P) { return h("span", { style: { font: "600 13px ui-monospace,monospace", color: P.text } }, a.raw); } },
        { key: "ok", label: { uz: "Natija", ru: "Результат" }, get: function (a) { return a.ok ? 1 : 0; }, render: function (a, P) { return a.ok ? self.badge(P, self.L({ uz: "Muvaffaqiyatli", ru: "Успешно" }), "green") : self.badge(P, self.L({ uz: "Xato", ru: "Ошибка" }), "red"); } },
        { key: "src", label: { uz: "Manba", ru: "Источник" }, get: function (a) { return a.src; }, render: function (a, P) { return self.badge(P, a.src, a.src === "bot" ? "accent" : a.src === "webapp" ? "teal" : "gray"); } },
        { key: "at", label: { uz: "Sana", ru: "Дата" }, align: "right", get: function (a) { return a.at; } }
      ];
      return this.pageWrap(P, [
        h("div", { key: "k" }, this.kpiGrid(P, kpis, 5)),
        h("div", { key: "d", style: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 } }, [this.chartCard(P, { uz: "Integritet segmentlari", ru: "Сегменты целостности" }, this.donut(P, segSegs), 5), this.chartCard(P, { uz: "Urinish manbalari", ru: "Источники попыток" }, this.donut(P, srcSegs), 6)]),
        h("div", { key: "lb" }, this.card(P, h("div", null, this.sectionTitle(P, { uz: "🚩 Shubhali faollik — Top 10", ru: "🚩 Подозрительная активность — Топ 10" }), h("div", { style: { marginTop: 16 } }, h(this.DataTable, { columns: lbCols, rows: lb, P: P, pageSize: 10 }))), null, 4)),
        h("div", { key: "at" }, this.chartCard(P, { uz: "Promokod urinishlari", ru: "Попытки промокодов" }, h(this.DataTable, { columns: atCols, rows: d.attempts || [], P: P, pageSize: 8 }), 7))
      ]);
    }

    pgBroadcast(P, d) {
      var h = this.h; var self = this; var k = d.kpis || {};
      var tab = this.getTab("broadcast", "general");
      var tabs = [{ key: "general", label: { uz: "Umumiy", ru: "Общие" } }, { key: "region", label: { uz: "Viloyat bo'yicha", ru: "По регионам" } }, { key: "monthly", label: { uz: "Oylik eslatma", ru: "Ежемес. напоминание" } }];
      var stInfo = function (s) { var m = { completed: ["green", { uz: "Yakunlangan", ru: "Завершено" }], sending: ["accent", { uz: "Yuborilmoqda", ru: "Отправка" }], pending: ["orange", { uz: "Kutilmoqda", ru: "Ожидает" }], failed: ["red", { uz: "Xato", ru: "Ошибка" }], scheduled: ["purple", { uz: "Rejalashtirilgan", ru: "Запланир." }] }; return m[s] || ["gray", s]; };
      var body;
      if (tab === "general") {
        var kpis = [{ label: { uz: "Jami rassilka", ru: "Всего рассылок" }, value: k.total, icon: "broadcast" }, { label: { uz: "Yuborilgan xabar", ru: "Отправлено сообщений" }, value: k.sent, icon: "broadcast" }, { label: { uz: "Muvaffaqiyat %", ru: "Успех %" }, value: k.successRate, format: function (x) { return self.pct(x); }, icon: "lottery" }];
        var cols = [{ key: "title", label: { uz: "Sarlavha", ru: "Заголовок" }, get: function (b) { return b.title; }, render: function (b, P) { return h("div", { style: { font: "600 13.5px inherit", color: P.text } }, b.title); } }, { key: "filter", label: { uz: "Filtr", ru: "Фильтр" }, get: function (b) { return b.filter; }, render: function (b, P) { return self.badge(P, b.filter, "gray"); } }, { key: "total", label: { uz: "Jami", ru: "Всего" }, align: "right", get: function (b) { return b.total; }, render: function (b) { return self.fmt(b.total); } }, { key: "sent", label: { uz: "Yuborildi", ru: "Отправлено" }, align: "right", get: function (b) { return b.sent; }, render: function (b, P) { return h("span", { style: { color: P.green, fontWeight: 600 } }, self.fmt(b.sent)); } }, { key: "failed", label: { uz: "Xato", ru: "Ошибка" }, align: "right", get: function (b) { return b.failed; }, render: function (b, P) { return h("span", { style: { color: b.failed ? P.red : P.text3, fontWeight: 600 } }, self.fmt(b.failed)); } }, { key: "status", label: { uz: "Holat", ru: "Статус" }, get: function (b) { return b.status; }, render: function (b, P) { var ci = stInfo(b.status); return self.badge(P, self.L(ci[1]), ci[0]); } }, { key: "at", label: { uz: "Sana", ru: "Дата" }, align: "right", get: function (b) { return b.at; } }];
        body = [h("div", { key: "k" }, this.kpiGrid(P, kpis, 3)), h("div", { key: "t" }, h(this.DataTable, { columns: cols, rows: d.general || [], P: P, pageSize: 9 }))];
      } else if (tab === "region") {
        var cols2 = [{ key: "region", label: { uz: "Viloyat", ru: "Регион" }, get: function (r) { return r.region; }, render: function (r, P) { return h("div", { style: { display: "flex", alignItems: "center", gap: 9 } }, h("span", { style: { color: P.accent } }, self.icon("geo", 15, 1.8)), r.region); } }, { key: "total", label: { uz: "Jami", ru: "Всего" }, align: "right", get: function (r) { return r.total; }, render: function (r) { return self.fmt(r.total); } }, { key: "sent", label: { uz: "Yuborildi", ru: "Отправлено" }, align: "right", get: function (r) { return r.sent; }, render: function (r, P) { return h("span", { style: { color: P.green, fontWeight: 600 } }, self.fmt(r.sent)); } }, { key: "failed", label: { uz: "Xato", ru: "Ошибка" }, align: "right", get: function (r) { return r.failed; }, render: function (r) { return self.fmt(r.failed); } }, { key: "status", label: { uz: "Holat", ru: "Статус" }, get: function (r) { return r.status; }, render: function (r, P) { var ci = stInfo(r.status); return self.badge(P, self.L(ci[1]), ci[0]); } }, { key: "at", label: { uz: "Sana", ru: "Дата" }, align: "right", get: function (r) { return r.at; } }];
        body = [h("div", { key: "t" }, h(this.DataTable, { columns: cols2, rows: d.region || [], P: P, pageSize: 10 }))];
      } else {
        var cols3 = [{ key: "month", label: { uz: "Oy", ru: "Месяц" }, get: function (r) { return r.month; }, render: function (r, P) { return h("span", { style: { font: "600 13.5px inherit", color: P.text } }, r.month); } }, { key: "total", label: { uz: "Jami", ru: "Всего" }, align: "right", get: function (r) { return r.total; }, render: function (r) { return self.fmt(r.total); } }, { key: "sent", label: { uz: "Yuborildi", ru: "Отправлено" }, align: "right", get: function (r) { return r.sent; }, render: function (r, P) { return h("span", { style: { color: P.green, fontWeight: 600 } }, self.fmt(r.sent)); } }, { key: "failed", label: { uz: "Xato", ru: "Ошибка" }, align: "right", get: function (r) { return r.failed; }, render: function (r) { return self.fmt(r.failed); } }, { key: "status", label: { uz: "Holat", ru: "Статус" }, get: function (r) { return r.status; }, render: function (r, P) { var ci = stInfo(r.status); return self.badge(P, self.L(ci[1]), ci[0]); } }];
        body = [h("div", { key: "info", style: { padding: "16px 18px", borderRadius: 14, background: P.greenSoft, color: P.green, font: "500 13px inherit", display: "flex", alignItems: "center", gap: 10 } }, this.icon("clock", 18, 1.8), this.L({ uz: "Oylik eslatma — har oy 1-sanasida avtomatik yuboriladi.", ru: "Ежемесячное напоминание — 1-го числа каждого месяца." })), h("div", { key: "t" }, h(this.DataTable, { columns: cols3, rows: d.monthly || [], P: P, pageSize: 8 }))];
      }
      return this.pageWrap(P, [h("div", { key: "seg" }, this.segmented(P, tabs, tab, function (kk) { self.setTab("broadcast", kk); }))].concat(body));
    }

    pgLottery(P, d) {
      var h = this.h; var self = this; var k = d.kpis || {};
      var tab = this.getTab("lottery", "tickets");
      var tabs = [{ key: "tickets", label: { uz: "Lotereya biletlari", ru: "Лотерейные билеты" } }, { key: "streams", label: { uz: "Jonli efirlar", ru: "Прямые эфиры" } }];
      if (tab === "streams") {
        var cards = h("div", { style: { display: "grid", gridTemplateColumns: "repeat(2,minmax(0,1fr))", gap: 16 } }, (d.streams || []).map(function (s, i) {
          return h("div", { key: i, style: { background: P.card, borderRadius: 20, border: "1px solid " + P.sep, boxShadow: P.shadow, padding: 22, animation: "cardIn .5s cubic-bezier(.16,1,.3,1) both", animationDelay: (i * 50) + "ms" } },
            h("div", { style: { display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 12, marginBottom: 14 } },
              h("div", { style: { display: "flex", alignItems: "center", gap: 12 } }, h("div", { style: { width: 46, height: 46, borderRadius: 13, background: s.status === "upcoming" ? P.accentSoft : P.greenSoft, color: s.status === "upcoming" ? P.accent : P.green, display: "flex", alignItems: "center", justifyContent: "center", flex: "none" } }, self.icon("lottery", 24, 1.8)), h("div", null, h("div", { style: { font: "600 15px inherit", color: P.text } }, s.title), h("div", { style: { font: "500 12.5px inherit", color: P.text3, marginTop: 3 } }, s.at))),
              self.badge(P, s.status === "upcoming" ? self.L({ uz: "Kelgusi", ru: "Предстоит" }) : self.L({ uz: "O'tgan", ru: "Прошёл" }), s.status === "upcoming" ? "accent" : "gray")
            ),
            h("div", { style: { display: "flex", gap: 20, padding: "12px 0", borderTop: "1px solid " + P.sep, borderBottom: s.winners.length ? "1px solid " + P.sep : "none", marginBottom: s.winners.length ? 14 : 0 } }, h("div", null, h("div", { style: { font: "700 19px inherit", color: P.text } }, self.fmt(s.part)), h("div", { style: { font: "500 11.5px inherit", color: P.text3 } }, self.L({ uz: "ishtirokchi", ru: "участников" }))), h("div", null, h("div", { style: { font: "700 19px inherit", color: P.text } }, s.winners.length), h("div", { style: { font: "500 11.5px inherit", color: P.text3 } }, self.L({ uz: "g'olib", ru: "победителей" })))),
            s.winners.length ? h("div", { style: { display: "flex", flexDirection: "column", gap: 8 } }, s.winners.map(function (w, wi) { return h("div", { key: wi, style: { display: "flex", alignItems: "center", gap: 11 } }, h("div", { style: { width: 24, height: 24, borderRadius: 7, background: w.pos === 1 ? P.accentSoft : P.iconBg, color: w.pos === 1 ? P.accent : P.text2, display: "flex", alignItems: "center", justifyContent: "center", font: "700 12px inherit", flex: "none" } }, w.pos), h("span", { style: { font: "600 13px inherit", color: P.text, flex: 1 } }, w.u), h("span", { style: { font: "500 12.5px inherit", color: P.accent } }, w.prize)); })) : null
          );
        }));
        return this.pageWrap(P, [h("div", { key: "seg" }, this.segmented(P, tabs, tab, function (kk) { self.setTab("lottery", kk); })), h("div", { key: "c" }, cards)]);
      }
      var kpis = [{ label: { uz: "Joriy oy biletlari", ru: "Билеты тек. месяца" }, value: k.current, icon: "lottery" }, { label: { uz: "Jami biletlar", ru: "Всего билетов" }, value: k.total, icon: "lottery" }, { label: { uz: "Ishtirokchilar", ru: "Участники" }, value: k.participants, icon: "users" }];
      var cols = [{ key: "no", label: { uz: "Bilet №", ru: "Билет №" }, get: function (t) { return t.no; }, render: function (t, P) { return h("span", { style: { font: "700 13.5px inherit", color: P.accent } }, t.no); } }, { key: "user", label: { uz: "Foydalanuvchi", ru: "Пользователь" }, get: function (t) { return t.user.name; }, render: function (t, P) { return h("div", null, h("div", { style: { font: "600 13px inherit", color: P.text } }, t.user.name), h("div", { style: { font: "500 11.5px inherit", color: P.text3 } }, t.user.phone)); } }, { key: "type", label: { uz: "Rol", ru: "Роль" }, get: function (t) { return t.type; }, render: function (t, P) { var ci = self.typeInfo(t.type); return self.badge(P, self.L(ci[1]), ci[0]); } }, { key: "qr", label: { uz: "QR kod", ru: "QR код" }, get: function (t) { return t.qr; }, render: function (t, P) { return h("span", { style: { font: "600 13px ui-monospace,monospace", color: P.text2 } }, t.qr); } }, { key: "month", label: { uz: "Oy", ru: "Месяц" }, get: function (t) { return t.month; } }, { key: "at", label: { uz: "Sana", ru: "Дата" }, align: "right", get: function (t) { return t.at; } }];
      return this.pageWrap(P, [h("div", { key: "seg" }, this.segmented(P, tabs, tab, function (kk) { self.setTab("lottery", kk); })), h("div", { key: "k" }, this.kpiGrid(P, kpis, 3)), h("div", { key: "t" }, h(this.DataTable, { columns: cols, rows: d.tickets || [], P: P, pageSize: 9 }))]);
    }

    pgPhotos(P, d) {
      var h = this.h; var self = this; var k = d.kpis || {};
      var kpis = [{ label: { uz: "Jami rasm", ru: "Всего фото" }, value: k.total, icon: "photos" }, { label: { uz: "Faol", ru: "Активные" }, value: k.active, icon: "photos" }, { label: { uz: "Usta o'chirgan", ru: "Удалено" }, value: k.deleted, icon: "photos" }, { label: { uz: "Bugun yuklangan", ru: "Сегодня загружено" }, value: k.today, icon: "photos" }];
      var grid = h("div", { style: { display: "grid", gridTemplateColumns: "repeat(4,minmax(0,1fr))", gap: 16 } }, (d.rows || []).map(function (p, i) {
        return h("div", { key: i, style: { background: P.card, borderRadius: 16, border: "1px solid " + P.sep, boxShadow: P.shadow, overflow: "hidden", animation: "cardIn .5s cubic-bezier(.16,1,.3,1) both", animationDelay: (i * 30) + "ms", cursor: "pointer", transition: "transform .25s, box-shadow .25s", opacity: p.active ? 1 : 0.55 }, onMouseEnter: function (e) { e.currentTarget.style.transform = "translateY(-3px)"; e.currentTarget.style.boxShadow = P.shadowHi; }, onMouseLeave: function (e) { e.currentTarget.style.transform = "none"; e.currentTarget.style.boxShadow = P.shadow; } },
          h("div", { style: { height: 140, background: P.card2, borderBottom: "1px solid " + P.sep, display: "flex", alignItems: "center", justifyContent: "center", position: "relative", backgroundImage: p.img ? ("url(" + p.img + ")") : "none", backgroundSize: "cover", backgroundPosition: "center" } }, !p.img ? h("div", { style: { color: P.text3, opacity: 0.7 } }, self.icon("photos", 36, 1.4)) : null, !p.active ? h("span", { style: { position: "absolute", top: 10, right: 10, padding: "3px 9px", borderRadius: 7, background: P.redSoft, color: P.red, font: "600 11px inherit" } }, self.L({ uz: "O'chirilgan", ru: "Удалено" })) : null),
          h("div", { style: { padding: 14 } }, h("div", { style: { font: "600 13.5px inherit", color: P.text, marginBottom: 6 } }, p.caption || self.L({ uz: "Izohsiz", ru: "Без подписи" })), h("div", { style: { display: "flex", alignItems: "center", justifyContent: "space-between" } }, h("span", { style: { font: "500 12px inherit", color: P.text2 } }, (p.user.name || "").split(" ")[0]), h("span", { style: { font: "500 11.5px inherit", color: P.text3 } }, p.at)))
        );
      }));
      return this.pageWrap(P, [h("div", { key: "k" }, this.kpiGrid(P, kpis, 4)), h("div", { key: "info", style: { padding: "12px 16px", borderRadius: 12, background: P.orangeSoft, color: P.orange, font: "500 12.5px inherit", display: "flex", alignItems: "center", gap: 9 } }, this.icon("photos", 16, 1.8), this.L({ uz: "Ba'zi rasm fayllari serverda mavjud bo'lmasligi mumkin — bunday holatda zaxira ikonka ko'rsatiladi.", ru: "Некоторые файлы могут отсутствовать на сервере — тогда показывается запасная иконка." })), h("div", { key: "g" }, grid)]);
    }

    pgAudit(P, d) {
      var h = this.h; var self = this; var k = d.kpis || {};
      var kpis = [{ label: { uz: "Jami log", ru: "Всего логов" }, value: k.total, icon: "audit" }, { label: { uz: "Bugungi amallar", ru: "Действий сегодня" }, value: k.today, icon: "audit" }, { label: { uz: "Kirish urinishlari", ru: "Входы" }, value: k.logins, icon: "audit" }, { label: { uz: "Xatolar", ru: "Ошибки" }, value: k.errors, icon: "fraud" }];
      var aInfo = function (a) { var m = { login: [P.accent, "🔑"], logout: [P.text2, "🚪"], login_failed: [P.red, "✖"], create: [P.green, "➕"], update: [P.orange, "✎"], delete: [P.red, "🗑"], export: [P.purple, "⤓"], webhook: [P.teal, "⚡"], admin_action: [P.accent, "⚙"], error: [P.red, "⚠"], backup: [P.text2, "💾"], custom: [P.text2, "•"] }; return m[a] || [P.text2, "•"]; };
      var cols = [{ key: "at", label: { uz: "Vaqt", ru: "Время" }, get: function (a) { return a.at; }, render: function (a, P) { return h("span", { style: { font: "500 12.5px inherit", color: P.text2 } }, a.at); } }, { key: "who", label: { uz: "Kim", ru: "Кто" }, get: function (a) { return a.who; }, render: function (a, P) { return h("span", { style: { font: "600 13px inherit", color: P.text } }, a.who); } }, { key: "action", label: { uz: "Amal", ru: "Действие" }, get: function (a) { return a.action; }, render: function (a, P) { var ci = aInfo(a.action); return h("span", { style: { display: "inline-flex", alignItems: "center", gap: 6, padding: "3px 10px", borderRadius: 8, background: ci[0] + "1a", color: ci[0], font: "600 12px inherit" } }, ci[1], a.action); } }, { key: "target", label: { uz: "Obyekt", ru: "Объект" }, get: function (a) { return a.target; }, render: function (a, P) { return h("span", { style: { font: "500 12.5px ui-monospace,monospace", color: P.text2 } }, a.target); } }, { key: "desc", label: { uz: "Tavsif", ru: "Описание" }, get: function (a) { return a.desc; }, wrap: true }, { key: "ip", label: { uz: "IP", ru: "IP" }, align: "right", get: function (a) { return a.ip; }, render: function (a, P) { return h("span", { style: { font: "500 12px ui-monospace,monospace", color: P.text3 } }, a.ip); } }];
      return this.pageWrap(P, [h("div", { key: "k" }, this.kpiGrid(P, kpis, 4)), h("div", { key: "t" }, h(this.DataTable, { columns: cols, rows: d.rows || [], P: P, pageSize: 10, dense: true }))]);
    }

    // ------------------------------- drawer --------------------------------
    renderDrawer(P) {
      var det = this.state.detail; if (!det) return null;
      var h = this.h; var self = this; var close = function () { self.setState({ detail: null }); };
      var row = function (k, v) { return h("div", { key: typeof k === "object" ? (k.uz || k.ru) : k, style: { display: "flex", justifyContent: "space-between", gap: 16, padding: "11px 0", borderBottom: "1px solid " + P.sep } }, h("span", { style: { font: "500 13px inherit", color: P.text3 } }, self.L(k)), h("span", { style: { font: "600 13px inherit", color: P.text, textAlign: "right" } }, v)); };
      var title = "", icon = "users", body = [];
      if (det.type === "user") {
        var u = det.row; title = u.name; icon = "users";
        var ci = this.typeInfo(u.type);
        body = [row({ uz: "Telegram ID", ru: "Telegram ID" }, u.id), row({ uz: "Username", ru: "Username" }, u.username || "—"), row({ uz: "Telefon", ru: "Телефон" }, u.phone), row({ uz: "Rol", ru: "Роль" }, this.L(ci[1])), row({ uz: "Viloyat", ru: "Регион" }, u.region || "—"), row({ uz: "Til", ru: "Язык" }, (u.lang || "").toUpperCase()), row({ uz: "Ball balansi", ru: "Баланс баллов" }, this.fmt(u.points)), row({ uz: "Ro'yxat", ru: "Регистрация" }, u.complete ? this.L({ uz: "Tugallangan", ru: "Завершена" }) : this.L({ uz: "Tugallanmagan", ru: "Не завершена" })), row({ uz: "Holat", ru: "Статус" }, u.blocked ? this.L({ uz: "Bloklangan", ru: "Заблокирован" }) : this.L({ uz: "Faol", ru: "Активен" })), row({ uz: "Qo'shilgan", ru: "Добавлен" }, u.created)];
      } else if (det.type === "seller") {
        var s = det.row; title = s.name; icon = "seller";
        body = [row({ uz: "Egasi", ru: "Владелец" }, s.owner || "—"), row({ uz: "Viloyat", ru: "Регион" }, s.region || "—"), row({ uz: "Partiyalar", ru: "Партии" }, s.batches), row({ uz: "Jami promokod", ru: "Всего промокодов" }, this.fmt(s.total)), row({ uz: "Aktivlashtirilgan", ru: "Активировано" }, this.fmt(s.act)), row({ uz: "Aktivatsiya %", ru: "Активация %" }, this.pct(s.pct)), row({ uz: "Jami ball", ru: "Всего баллов" }, this.fmt(s.points))];
      } else if (det.type === "redemption") {
        var r = det.row; title = r.user.name; icon = "gift"; var ci2 = this.rstatusInfo(r.status);
        body = [row({ uz: "Telefon", ru: "Телефон" }, r.user.phone), row({ uz: "Sovg'a", ru: "Подарок" }, r.gift), row({ uz: "Narx", ru: "Цена" }, this.fmt(r.cost) + " " + this.L({ uz: "ball", ru: "балл" })), row({ uz: "Status", ru: "Статус" }, this.L(ci2[1])), row({ uz: "So'ralgan", ru: "Запрошено" }, r.at)];
      } else if (det.type === "region") {
        var rg = det.row; title = this.L(rg.label); icon = "geo";
        body = [row({ uz: "Foydalanuvchilar", ru: "Пользователи" }, this.fmt(rg.v)), row({ uz: "Skanlar", ru: "Сканирования" }, this.fmt(rg.scan)), row({ uz: "Tarqatilgan ball", ru: "Начислено баллов" }, this.fmt(rg.pts))];
      }
      return h("div", { style: { position: "fixed", inset: 0, zIndex: 60, display: "flex", justifyContent: "flex-end" } },
        h("div", { onClick: close, style: { position: "absolute", inset: 0, background: "rgba(0,0,0,0.32)", backdropFilter: "blur(2px)", animation: "overlayIn .25s ease both" } }),
        h("div", { style: { position: "relative", width: 420, maxWidth: "90vw", height: "100%", background: P.bg2, borderLeft: "1px solid " + P.sep, boxShadow: "-20px 0 60px rgba(0,0,0,0.18)", animation: "drawerIn .4s cubic-bezier(.16,1,.3,1) both", display: "flex", flexDirection: "column", overflow: "hidden" } },
          h("div", { style: { padding: "22px 24px", borderBottom: "1px solid " + P.sep, display: "flex", alignItems: "center", gap: 14 } },
            h("div", { style: { width: 48, height: 48, borderRadius: 14, background: P.accentSoft, color: P.accent, display: "flex", alignItems: "center", justifyContent: "center", flex: "none" } }, this.icon(icon, 24, 1.8)),
            h("div", { style: { flex: 1, minWidth: 0 } }, h("div", { style: { font: "700 18px inherit", letterSpacing: "-.01em", color: P.text, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" } }, title), h("div", { style: { font: "500 12.5px inherit", color: P.text3, marginTop: 2 } }, this.L({ uz: "Tafsilotlar", ru: "Детали" }))),
            h("button", { onClick: close, style: { width: 34, height: 34, borderRadius: 10, border: "1px solid " + P.sep, background: P.card, color: P.text2, cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center", flex: "none" } }, this.icon("close", 18, 1.9))
          ),
          h("div", { style: { flex: 1, overflowY: "auto", padding: "8px 24px 24px" } }, body),
          h("div", { style: { padding: "16px 24px", borderTop: "1px solid " + P.sep } }, h("button", { onClick: function () { window.open(ADMIN_BASE, "_blank"); }, style: { width: "100%", height: 46, borderRadius: 13, border: "none", background: P.accent, color: "#fff", font: "600 14px inherit", cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center", gap: 8, transition: "transform .15s, filter .15s" }, onMouseEnter: function (e) { e.currentTarget.style.filter = "brightness(1.08)"; e.currentTarget.style.transform = "translateY(-1px)"; }, onMouseLeave: function (e) { e.currentTarget.style.filter = "none"; e.currentTarget.style.transform = "none"; } }, this.L({ uz: "Admin panelda ochish", ru: "Открыть в админ-панели" }), this.icon("arrow", 18, 1.9, "#fff")))
        )
      );
    }

    // ------------------------------- shell ---------------------------------
    render() {
      var P = this.pal(); var h = this.h; var self = this; var lang = this.state.lang;
      var collapsed = this.state.collapsed; var expanded = !collapsed;
      var page = this.state.page;
      document.body.style.background = P.bg;

      var navDefs = [
        { key: "overview", icon: "overview", label: { uz: "Umumiy ko'rinish", ru: "Обзор" } },
        { key: "users", icon: "users", label: { uz: "Foydalanuvchilar", ru: "Пользователи" } },
        { key: "promo", icon: "promo", label: { uz: "Promokodlar", ru: "Промокоды" } },
        { key: "gift", icon: "gift", label: { uz: "Sovg'alar", ru: "Подарки" } },
        { key: "seller", icon: "seller", label: { uz: "Sotuvchilar", ru: "Продавцы" } },
        { key: "geo", icon: "geo", label: { uz: "Geografiya", ru: "География" } },
        { key: "fraud", icon: "fraud", label: { uz: "Xavfsizlik", ru: "Безопасность" } },
        { key: "broadcast", icon: "broadcast", label: { uz: "Rassilkalar", ru: "Рассылки" } },
        { key: "lottery", icon: "lottery", label: { uz: "Lotereya / Efir", ru: "Лотерея / Эфир" } },
        { key: "photos", icon: "photos", label: { uz: "Loyiha rasmlari", ru: "Фото проектов" } },
        { key: "audit", icon: "audit", label: { uz: "Audit log", ru: "Аудит лог" } }
      ];
      var titles = { overview: { uz: "Umumiy ko'rinish", ru: "Обзор" }, users: { uz: "Foydalanuvchilar", ru: "Пользователи" }, promo: { uz: "Promokodlar", ru: "Промокоды" }, gift: { uz: "Sovg'alar va so'rovlar", ru: "Подарки и заявки" }, seller: { uz: "Sotuvchilar", ru: "Продавцы" }, geo: { uz: "Geografiya", ru: "География" }, fraud: { uz: "Xavfsizlik / Fraud", ru: "Безопасность / Fraud" }, broadcast: { uz: "Rassilkalar", ru: "Рассылки" }, lottery: { uz: "Lotereya / Jonli efir", ru: "Лотерея / Эфир" }, photos: { uz: "Loyiha rasmlari", ru: "Фото проектов" }, audit: { uz: "Audit log", ru: "Аудит лог" } };
      var subs = { overview: { uz: "Tizimning umumiy holati bir qarashda", ru: "Состояние системы с одного взгляда" }, users: { uz: "Barcha foydalanuvchilarni ko'rish va filtrlash", ru: "Просмотр и фильтрация пользователей" }, promo: { uz: "QR / skretch kartalar tahlili", ru: "Анализ QR / скретч-карт" }, gift: { uz: "Sovg'a katalogi va so'rovlar oqimi", ru: "Каталог подарков и поток заявок" }, seller: { uz: "Sotuvchilar, partiyalar va balans", ru: "Продавцы, партии и баланс" }, geo: { uz: "Viloyat va tuman bo'yicha tahlil", ru: "Анализ по регионам и районам" }, fraud: { uz: "Firibgarlik aniqlash va bloklar", ru: "Обнаружение мошенничества" }, broadcast: { uz: "Yuborilgan xabarlar tarixi", ru: "История отправленных сообщений" }, lottery: { uz: "Oylik biletlar va efir g'oliblari", ru: "Билеты месяца и победители" }, photos: { uz: "Ustalar yuklagan ish rasmlari", ru: "Фото работ мастеров" }, audit: { uz: "Tizimdagi barcha amallar jurnali", ru: "Журнал всех действий" } };
      var dateOpts = [["7d", { uz: "7 kun", ru: "7 дней" }], ["30d", { uz: "30 kun", ru: "30 дней" }], ["prev", { uz: "O'tgan oy", ru: "Прош. месяц" }], ["all", { uz: "Hammasi", ru: "Всё время" }]];

      var iconBtn = { width: 38, height: 38, borderRadius: 11, border: "1px solid " + P.sep, background: P.card, color: P.text2, cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center", transition: "all .18s", flex: "none" };
      var iconBtnHover = { background: P.accentSoft, borderColor: P.accent, color: P.accent };

      // sidebar nav buttons
      var navButtons = navDefs.map(function (n) {
        var on = page === n.key;
        var base = { display: "flex", alignItems: "center", gap: 12, width: "100%", padding: collapsed ? "10px" : "9px 12px", justifyContent: collapsed ? "center" : "flex-start", borderRadius: 12, border: "none", background: on ? P.accentSoft : "transparent", color: on ? P.accent : P.text2, font: (on ? "600" : "500") + " 13.5px inherit", cursor: "pointer", transition: "background .18s, color .18s", textAlign: "left", position: "relative" };
        var hover = { background: on ? P.accentSoft : P.track, color: on ? P.accent : P.text };
        var hh = self.hov(base, hover);
        return h("button", { key: n.key, style: base, onMouseEnter: hh.onMouseEnter, onMouseLeave: hh.onMouseLeave, onClick: function () { self.setPage(n.key); }, title: self.L(n.label) },
          h("span", { style: { display: "flex", alignItems: "center", justifyContent: "center", flex: "none", color: on ? P.accent : P.text2 } }, self.icon(n.icon, 20, 1.8)),
          expanded ? h("span", { style: { flex: 1, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" } }, self.L(n.label)) : null
        );
      });
      var footDefs = [
        { key: "admin", icon: "admin", label: { uz: "Admin panel", ru: "Админ-панель" }, onClick: function () { window.open(ADMIN_BASE, "_blank"); }, danger: false },
        { key: "logout", icon: "logout", label: { uz: "Chiqish", ru: "Выйти" }, onClick: function () { window.location.href = ADMIN_BASE + "logout/"; }, danger: true }
      ];
      var footButtons = footDefs.map(function (n) {
        var base = { display: "flex", alignItems: "center", gap: 12, width: "100%", padding: collapsed ? "10px" : "9px 12px", justifyContent: collapsed ? "center" : "flex-start", borderRadius: 12, border: "none", background: "transparent", color: n.danger ? P.red : P.text2, font: "500 13.5px inherit", cursor: "pointer", transition: "background .18s", textAlign: "left" };
        var hover = { background: n.danger ? P.redSoft : P.track };
        var hh = self.hov(base, hover);
        return h("button", { key: n.key, style: base, onMouseEnter: hh.onMouseEnter, onMouseLeave: hh.onMouseLeave, onClick: n.onClick, title: self.L(n.label) },
          h("span", { style: { display: "flex", alignItems: "center", justifyContent: "center", flex: "none" } }, self.icon(n.icon, 20, 1.8)),
          expanded ? h("span", { style: { flex: 1, whiteSpace: "nowrap" } }, self.L(n.label)) : null
        );
      });

      var dateChips = dateOpts.map(function (o) {
        var on = self.state.range === o[0];
        return h("button", { key: o[0], onClick: function () { self.setState({ range: o[0] }); }, style: { padding: "7px 13px", borderRadius: 9, border: "none", background: on ? P.card : "transparent", color: on ? P.text : P.text2, font: (on ? "600" : "500") + " 12.5px inherit", cursor: "pointer", boxShadow: on ? P.shadow : "none", transition: "all .2s", whiteSpace: "nowrap" } }, self.L(o[1]));
      });

      function iconButton(name, onClick, title) {
        var hh = self.hov(iconBtn, iconBtnHover);
        return h("button", { style: iconBtn, onMouseEnter: hh.onMouseEnter, onMouseLeave: hh.onMouseLeave, onClick: onClick, title: title }, self.icon(name, 18, 1.9));
      }
      var menuHov = self.hov(iconBtn, iconBtnHover);
      var langHov = self.hov(undefined, iconBtnHover);

      var du = window.DJANGO_USER || {};
      var userName = du.name || du.username || "Admin";

      return h("div", { style: { display: "flex", height: "100vh", width: "100%", background: P.bg, color: P.text, overflow: "hidden" } },
        // sidebar
        h("aside", { style: { width: collapsed ? 72 : 248, flex: "none", display: "flex", flexDirection: "column", background: P.panel, backdropFilter: "blur(24px) saturate(180%)", WebkitBackdropFilter: "blur(24px) saturate(180%)", borderRight: "1px solid " + P.sep, transition: "width .3s cubic-bezier(.16,1,.3,1)", zIndex: 20 } },
          h("div", { style: { display: "flex", alignItems: "center", gap: 12, padding: collapsed ? "20px 0" : "20px 22px", justifyContent: collapsed ? "center" : "flex-start" } },
            h("div", { style: { width: 38, height: 38, borderRadius: 10, background: P.accent, color: "#fff", display: "flex", alignItems: "center", justifyContent: "center", font: "800 19px inherit", flex: "none", boxShadow: "0 4px 12px " + P.accentSoft } }, "J"),
            expanded ? h("div", { style: { display: "flex", flexDirection: "column", lineHeight: 1.1 } }, h("div", { style: { font: "800 17px inherit", letterSpacing: "-.02em", color: P.text } }, "JIP"), h("div", { style: { font: "600 11px inherit", color: P.text3, letterSpacing: ".04em", textTransform: "uppercase" } }, "Dashboard")) : null
          ),
          h("nav", { style: { display: "flex", flexDirection: "column", gap: 3, padding: collapsed ? "6px 12px" : "6px 14px", flex: 1, overflowY: "auto" } }, navButtons),
          h("div", { style: { display: "flex", flexDirection: "column", gap: 3, padding: collapsed ? "10px 12px 16px" : "10px 14px 16px", borderTop: "1px solid " + P.sep } }, footButtons)
        ),
        // main
        h("main", { style: { flex: 1, display: "flex", flexDirection: "column", minWidth: 0, overflow: "hidden" } },
          h("header", { style: { display: "flex", alignItems: "center", justifyContent: "space-between", gap: 16, padding: "0 28px", height: 72, flex: "none", background: P.panel, backdropFilter: "blur(24px) saturate(180%)", WebkitBackdropFilter: "blur(24px) saturate(180%)", borderBottom: "1px solid " + P.sep, zIndex: 15 } },
            h("div", { style: { display: "flex", alignItems: "center", gap: 14, minWidth: 0 } },
              h("button", { style: iconBtn, onMouseEnter: menuHov.onMouseEnter, onMouseLeave: menuHov.onMouseLeave, onClick: function () { self.setState(function (s) { return { collapsed: !s.collapsed }; }); }, title: "Menu" }, self.icon("menu", 20, 1.9)),
              h("div", null, h("div", { style: { font: "700 20px inherit", letterSpacing: "-.02em", color: P.text, lineHeight: 1.1, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" } }, self.L(titles[page])), h("div", { style: { font: "500 12.5px inherit", color: P.text3, marginTop: 2, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" } }, self.L(subs[page])))
            ),
            h("div", { style: { display: "flex", alignItems: "center", gap: 10 } },
              h("div", { style: { display: "flex", alignItems: "center", gap: 2, padding: 4, borderRadius: 12, background: P.track } }, dateChips),
              iconButton("refresh", function () { self.reloadCurrent(); }, self.L({ uz: "Yangilash", ru: "Обновить" })),
              h("button", { style: { height: 38, padding: "0 14px", borderRadius: 11, border: "1px solid " + P.sep, background: P.card, color: P.text, cursor: "pointer", font: "700 12.5px inherit", letterSpacing: ".02em", transition: "all .18s", flex: "none" }, onMouseEnter: langHov.onMouseEnter, onMouseLeave: function (e) { e.currentTarget.style.background = P.card; e.currentTarget.style.borderColor = P.sep; e.currentTarget.style.color = P.text; }, onClick: function () { self.setState(function (s) { return { lang: s.lang === "uz" ? "ru" : "uz" }; }); } }, lang === "uz" ? "UZ" : "RU"),
              iconButton(this.state.theme === "dark" ? "sun" : "moon", function () { self.setState(function (s) { return { theme: s.theme === "dark" ? "light" : "dark" }; }); }, "Theme"),
              h("div", { style: { display: "flex", alignItems: "center", gap: 10, paddingLeft: 6, marginLeft: 2 } }, h("div", { style: { width: 38, height: 38, borderRadius: "50%", background: P.iconBg, color: P.text2, display: "flex", alignItems: "center", justifyContent: "center", font: "700 14px inherit", flex: "none" } }, (self.initials(userName) || "AD").toUpperCase()), expanded ? h("div", { style: { lineHeight: 1.2 } }, h("div", { style: { font: "600 13px inherit", color: P.text, whiteSpace: "nowrap" } }, userName), h("div", { style: { font: "500 11.5px inherit", color: P.text3 } }, self.L({ uz: "Administrator", ru: "Администратор" }))) : null)
            )
          ),
          h("div", { "data-scroll": true, style: { flex: 1, overflowY: "auto", padding: "28px", position: "relative" } }, this.renderPage(P))
        ),
        this.renderDrawer(P)
      );
    }
  }

  var root = document.getElementById("root");
  if (ReactDOM.createRoot) { ReactDOM.createRoot(root).render(React.createElement(Dashboard)); }
  else { ReactDOM.render(React.createElement(Dashboard), root); }
})();
