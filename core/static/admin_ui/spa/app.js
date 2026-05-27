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
