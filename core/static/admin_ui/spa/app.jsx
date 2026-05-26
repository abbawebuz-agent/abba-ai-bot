// JIP Admin SPA — app.jsx
// Modified from Claude Design: real Django stats + user + navigation to Django admin
const { useState: useStateApp, useEffect: useEffectApp } = React;

const TWEAK_DEFAULTS = {
  "sidebar": "dark",
  "density": "comfortable",
  "theme": "dark"
};

// Inject real Django stats into the mock data if available
(function patchRealData() {
  const s = window.DJANGO_STATS;
  if (!s) return;
  // Override stats in the JIP mock store
  if (window.JIP && window.JIP.stats) {
    if (s.users_total)    window.JIP.stats.users_total   = s.users_total;
    if (s.batches_active) window.JIP.stats.batches_active = s.batches_active;
    if (s.qr_total)       window.JIP.stats.qr_total      = s.qr_total;
    if (s.qr_scanned)     window.JIP.stats.qr_scanned    = s.qr_scanned;
    if (s.gifts_pending)  window.JIP.stats.gifts_pending  = s.gifts_pending;
    if (s.txns_total)     window.JIP.stats.txns_total    = s.txns_total;
    if (s.audit_total)    window.JIP.stats.audit_total   = s.audit_total;
  }
})();

// Build Django admin URL for a model
function djAdmin(path) {
  return (window.DJANGO_ADMIN_BASE || '/admin/') + path;
}

// Navigation: some routes go to Django admin directly (CRUD pages)
// Others stay as SPA overview pages
const DJANGO_REDIRECT = {
  // These routes open Django admin instead of SPA pages
  '/users/santenik':       () => djAdmin('core/telegramuser/'),
  '/users/sotuvchi':       () => djAdmin('core/telegramuser/'),
  '/qrcodes/edit':         () => djAdmin('core/qrcode/'),
  '/batches/add':          () => djAdmin('core/qrcodebatch/add/'),
  '/batches/edit':         () => djAdmin('core/qrcodebatch/'),
  '/stores/add':           () => djAdmin('core/store/add/'),
  '/stores/edit':          () => djAdmin('core/store/'),
  '/gifts/add':            () => djAdmin('core/gift/add/'),
  '/redemptions/edit':     () => djAdmin('core/giftredemption/'),
  '/transactions/add':     () => djAdmin('core/sellerpointstransaction/add/'),
  '/livestreams/add':      () => djAdmin('core/livestream/add/'),
  '/videos/add':           () => djAdmin('core/videoinstruction/add/'),
};

function useHashRoute() {
  const [route, setRoute] = useStateApp(() => {
    const h = window.location.hash.slice(1) || '/dashboard';
    return h.startsWith('/') ? h : '/' + h;
  });
  useEffectApp(() => {
    const onHash = () => {
      const h = window.location.hash.slice(1) || '/dashboard';
      const r = h.startsWith('/') ? h : '/' + h;
      setRoute(r);
    };
    window.addEventListener('hashchange', onHash);
    return () => window.removeEventListener('hashchange', onHash);
  }, []);
  const navigate = (r) => {
    // Check if this route should go to Django admin
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
    case '/':
    case '/dashboard':         return <DashboardPage onNavigate={onNavigate}/>;
    case '/analytics':         return <AnalyticsPage/>;
    case '/users':             return <UsersListPage onNavigate={onNavigate}/>;
    case '/users/santenik':    return <UserSantenikPage onNavigate={onNavigate}/>;
    case '/users/sotuvchi':    return <UserSotuvchiPage onNavigate={onNavigate}/>;
    case '/users/send-region': return <SendRegionMessagePage/>;
    case '/users/send-single': return <SendSingleMessagePage/>;
    case '/auth/users':        return <AuthUsersPage onNavigate={onNavigate}/>;
    case '/auth/groups':       return <AuthGroupsPage/>;
    case '/qrcodes':           return <QRCodesPage onNavigate={onNavigate}/>;
    case '/qrcodes/edit':      return <QRCodeEditPage onNavigate={onNavigate}/>;
    case '/qrcodes/generate':  return <QRGeneratePage/>;
    case '/batches':           return <BatchesPage onNavigate={onNavigate}/>;
    case '/batches/add':       return <BatchAddPage/>;
    case '/batches/edit':      return <BatchEditPage onNavigate={onNavigate}/>;
    case '/stores':            return <StoresPage onNavigate={onNavigate}/>;
    case '/stores/edit':       return <StoreEditPage onNavigate={onNavigate}/>;
    case '/stores/add':        return <StoreAddPage/>;
    case '/gifts':             return <GiftsPage onNavigate={onNavigate}/>;
    case '/gifts/add':         return <GiftAddPage/>;
    case '/redemptions':       return <RedemptionsPage onNavigate={onNavigate}/>;
    case '/redemptions/edit':  return <RedemptionEditPage onNavigate={onNavigate}/>;
    case '/transactions':      return <TransactionsPage onNavigate={onNavigate}/>;
    case '/transactions/add':  return <TransactionAddPage/>;
    case '/seller-codes':      return <SellerCodesPage/>;
    case '/activity':          return <ActivityLogPage/>;
    case '/livestreams':       return <LivestreamsPage onNavigate={onNavigate}/>;
    case '/livestreams/add':   return <LivestreamAddPage/>;
    case '/regionlog':         return <RegionLogPage/>;
    case '/videos':            return <VideosPage onNavigate={onNavigate}/>;
    case '/videos/add':        return <VideoAddPage/>;
    case '/monthly':           return <MonthlySettingsPage/>;
    case '/monthly-log':       return <MonthlyLogPage/>;
    case '/contacts':          return <AdminContactsPage/>;
    case '/privacy':           return <PrivacyPolicyPage/>;
    default:
      return (
        <div className="page">
          <PageHeader title="Sahifa topilmadi" subtitle={'Route: ' + route}/>
          <EmptyState icon="help-circle" title="404 — yo'q sahifa" hint="Chap menyudan boshqa sahifani tanlang"/>
        </div>
      );
  }
}

function App() {
  const [route, navigate] = useHashRoute();
  const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);

  // Apply tweaks to root
  useEffectApp(() => {
    document.documentElement.setAttribute('data-sidebar', t.sidebar);
    document.documentElement.setAttribute('data-density', t.density);
    document.documentElement.setAttribute('data-theme', t.theme);
  }, [t.sidebar, t.density, t.theme]);

  // Scroll to top on route change
  useEffectApp(() => {
    const main = document.querySelector('.main');
    if (main) main.scrollTop = 0;
    window.scrollTo(0, 0);
  }, [route]);

  return (
    <div className="app" data-screen-label={'route:' + route}>
      <Sidebar currentRoute={route} onNavigate={navigate}/>
      <div className="main">
        <Topbar route={route} onNavigate={navigate} tweaks={t} setTweak={setTweak}/>
        <PageRouter route={route} onNavigate={navigate}/>
      </div>

      <TweaksPanel>
        <TweakSection label="Tema"/>
        <TweakRadio label="Theme" value={t.theme}
          options={[
            { value: 'dark',  label: '🌙 Tun' },
            { value: 'light', label: '☀️ Kun' },
          ]}
          onChange={(v) => setTweak('theme', v)}/>
        <TweakSection label="Layout"/>
        <TweakRadio label="Sidebar" value={t.sidebar}
          options={[
            { value: 'dark',  label: 'Dark' },
            { value: 'light', label: 'Light' },
            { value: 'icon',  label: 'Icons' },
          ]}
          onChange={(v) => setTweak('sidebar', v)}/>
        <TweakRadio label="Density" value={t.density}
          options={[
            { value: 'comfortable', label: 'Comfy' },
            { value: 'compact',     label: 'Compact' },
          ]}
          onChange={(v) => setTweak('density', v)}/>
        <TweakSection label="Navigation"/>
        <div style={{padding: '8px 16px'}}>
          <a href="/admin/" target="_blank" style={{
            display: 'flex', alignItems: 'center', gap: 8,
            fontSize: 12, color: 'var(--primary)', textDecoration: 'none',
            padding: '6px 8px', borderRadius: 6,
            background: 'var(--primary-soft)',
          }}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
            </svg>
            Django Admin →
          </a>
        </div>
      </TweaksPanel>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App/>);
