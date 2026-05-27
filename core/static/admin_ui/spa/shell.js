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
