// Shell: Sidebar (with all 35 routes) + Topbar + Layout
// Reads currentRoute from props, calls onNavigate when user clicks.

const NAV_GROUPS = [
  {
    label: 'Boshqaruv',
    items: [
      { route: '/dashboard',  label: 'Dashboard',  icon: 'home',       count: null },
      { route: '/analytics',  label: 'Аналитика',  icon: 'bar-chart',  count: null },
    ],
  },
  {
    label: 'Foydalanuvchilar',
    items: [
      { route: '/users',           label: 'Telegram users', icon: 'users',          count: 23 },
      { route: '/users/send-region', label: 'Xabar (viloyat)', icon: 'send',         count: null },
      { route: '/users/send-single', label: 'Xabar (single)',  icon: 'message-circle', count: null },
      { route: '/auth/users',      label: 'Admin users',    icon: 'user',           count: 4 },
      { route: '/auth/groups',     label: 'Guruhlar',       icon: 'shield',         count: 4 },
    ],
  },
  {
    label: 'QR & Партии',
    items: [
      { route: '/qrcodes',         label: 'QR kodlar',      icon: 'qrcode',  count: 239 },
      { route: '/qrcodes/generate', label: 'QR generatsiya', icon: 'plus',    count: null },
      { route: '/batches',         label: 'Партии',         icon: 'box',     count: 17 },
      { route: '/batches/add',     label: 'Yangi партия',   icon: 'plus',    count: null },
      { route: '/stores',          label: 'Do\'konlar',     icon: 'store',   count: 12 },
    ],
  },
  {
    label: 'Sovg\'alar',
    items: [
      { route: '/gifts',         label: 'Sovg\'alar katalogi', icon: 'gift',         count: 8 },
      { route: '/redemptions',   label: 'Sovg\'a so\'rovlari', icon: 'gift-redeem',  count: 15 },
    ],
  },
  {
    label: 'Sotuvchilar',
    items: [
      { route: '/transactions', label: 'Tranzaksiyalar',  icon: 'credit-card', count: 1117 },
      { route: '/seller-codes', label: 'Sotuvchi ID lar', icon: 'id-card',     count: 25 },
    ],
  },
  {
    label: 'Kontent',
    items: [
      { route: '/livestreams', label: 'Jonli efirlar',  icon: 'radio', count: 4 },
      { route: '/videos',      label: 'Videolar',       icon: 'video', count: 5 },
      { route: '/privacy',     label: 'Maxfiylik',      icon: 'file-text', count: null },
    ],
  },
  {
    label: 'Tizim',
    items: [
      { route: '/activity',     label: 'Faollik tarixi', icon: 'history', count: 264 },
      { route: '/regionlog',    label: 'Viloyat logi',   icon: 'map',     count: null },
      { route: '/monthly',      label: 'Oylik eslatma',  icon: 'bell',    count: null },
      { route: '/monthly-log',  label: 'Eslatma logi',   icon: 'clock',   count: null },
      { route: '/contacts',     label: 'Admin kontakt',  icon: 'phone',   count: null },
    ],
  },
];

// Topbar config per route (title + breadcrumb)
const PAGE_META = {
  '/dashboard':            { title: 'Dashboard', crumbs: ['Bosh', 'Dashboard'] },
  '/analytics':            { title: 'Аналитика', crumbs: ['Bosh', 'Аналитика'] },
  '/users':                { title: 'Пользователи Telegram', crumbs: ['Bosh', 'Core', 'Telegram пользователи'] },
  '/users/santenik':       { title: 'Сантехник', crumbs: ['Bosh', 'Core', 'Telegram пользователи', 'Изменить'] },
  '/users/sotuvchi':       { title: 'Продавец', crumbs: ['Bosh', 'Core', 'Telegram пользователи', 'Изменить'] },
  '/users/send-region':    { title: 'Отправить по области', crumbs: ['Bosh', 'Telegram пользователи', 'Рассылка'] },
  '/users/send-single':    { title: 'Отправить пользователю', crumbs: ['Bosh', 'Telegram пользователи', 'Сообщение'] },
  '/auth/users':           { title: 'Admin foydalanuvchilar', crumbs: ['Bosh', 'Auth', 'Users'] },
  '/auth/groups':          { title: 'Guruhlar', crumbs: ['Bosh', 'Auth', 'Groups'] },
  '/qrcodes':              { title: 'QR kodlar', crumbs: ['Bosh', 'Core', 'QR коды'] },
  '/qrcodes/edit':         { title: 'QR код · #001', crumbs: ['Bosh', 'Core', 'QR коды', 'Изменить'] },
  '/qrcodes/generate':     { title: 'QR generatsiya', crumbs: ['Bosh', 'Core', 'QR коды', 'Генерация'] },
  '/batches':              { title: 'Партии', crumbs: ['Bosh', 'Core', 'QR партии'] },
  '/batches/add':          { title: 'Новая партия', crumbs: ['Bosh', 'Core', 'QR партии', 'Добавить'] },
  '/batches/edit':         { title: 'Партия · S27-MAY-2026', crumbs: ['Bosh', 'Core', 'QR партии', 'Изменить'] },
  '/stores':               { title: 'Do\'konlar', crumbs: ['Bosh', 'Core', 'Магазины'] },
  '/stores/edit':          { title: 'Sadulla Jomiy 1', crumbs: ['Bosh', 'Core', 'Магазины', 'Изменить'] },
  '/stores/add':           { title: 'Yangi do\'kon', crumbs: ['Bosh', 'Core', 'Магазины', 'Добавить'] },
  '/gifts':                { title: 'Sovg\'alar', crumbs: ['Bosh', 'Core', 'Подарки'] },
  '/gifts/add':            { title: 'Yangi sovg\'a', crumbs: ['Bosh', 'Core', 'Подарки', 'Добавить'] },
  '/redemptions':          { title: 'Sovg\'a so\'rovlari', crumbs: ['Bosh', 'Core', 'Заявки на подарки'] },
  '/redemptions/edit':     { title: 'Заявка #1009', crumbs: ['Bosh', 'Core', 'Заявки', 'Изменить'] },
  '/transactions':         { title: 'Sotuvchi tranzaksiyalari', crumbs: ['Bosh', 'Core', 'Транзакции'] },
  '/transactions/add':     { title: 'Yangi tranzaksiya', crumbs: ['Bosh', 'Core', 'Транзакции', 'Добавить'] },
  '/seller-codes':         { title: 'Sotuvchi ID lar', crumbs: ['Bosh', 'Core', 'Коды регистрации'] },
  '/activity':             { title: 'Faollik tarixi', crumbs: ['Bosh', 'Core', 'Журнал действий'] },
  '/livestreams':          { title: 'Jonli efirlar', crumbs: ['Bosh', 'Core', 'LiveStream'] },
  '/livestreams/add':      { title: 'Yangi efir', crumbs: ['Bosh', 'Core', 'LiveStream', 'Добавить'] },
  '/regionlog':            { title: 'Viloyat xabarlari logi', crumbs: ['Bosh', 'Core', 'Логи рассылок'] },
  '/videos':               { title: 'Video ko\'rsatmalar', crumbs: ['Bosh', 'Core', 'Видеоинструкции'] },
  '/videos/add':           { title: 'Yangi video', crumbs: ['Bosh', 'Core', 'Видеоинструкции', 'Добавить'] },
  '/monthly':              { title: 'Oylik eslatma sozlamalari', crumbs: ['Bosh', 'Core', 'Напоминания'] },
  '/monthly-log':          { title: 'Eslatma logi', crumbs: ['Bosh', 'Core', 'Логи напоминаний'] },
  '/contacts':             { title: 'Admin kontaktlari', crumbs: ['Bosh', 'Core', 'Контакты'] },
  '/privacy':              { title: 'Maxfiylik siyosati', crumbs: ['Bosh', 'Core', 'Privacy policy'] },
};

function Sidebar({ currentRoute, onNavigate }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="logo">JIP</div>
        <div className="brand-text">
          <div className="brand-name">JIP GROUP</div>
          <div className="brand-sub">Jahon Invest Plast</div>
        </div>
      </div>
      <nav className="sidebar-nav">
        {NAV_GROUPS.map((g, gi) => (
          <div key={gi} style={{display: 'contents'}}>
            <div className="sidebar-section">{g.label}</div>
            {g.items.map((it, ii) => {
              const active = currentRoute === it.route || (it.route !== '/' && currentRoute.startsWith(it.route + '/'));
              return (
                <button
                  key={ii}
                  className={'nav-item' + (active ? ' active' : '')}
                  onClick={() => onNavigate(it.route)}
                  title={it.label}
                >
                  <span className="nav-icon"><Icon name={it.icon} size={16}/></span>
                  <span className="nav-label">{it.label}</span>
                  {it.count != null && <span className="nav-count">{it.count.toLocaleString('ru')}</span>}
                </button>
              );
            })}
          </div>
        ))}
      </nav>
      <div className="sidebar-footer">
        <Avatar name={window.DJANGO_USER ? window.DJANGO_USER.name : 'Жасур Каримов'} size={28}/>
        <div className="user-info" style={{minWidth: 0, flex: 1}}>
          <div style={{color: 'var(--text-strong)', fontSize: 12.5, fontWeight: 500, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap'}}>
            {window.DJANGO_USER ? window.DJANGO_USER.username : 'admin'}
          </div>
          <div style={{fontSize: 11, color: 'var(--text-dim)'}}>
            {window.DJANGO_USER && window.DJANGO_USER.is_superuser ? 'Superadmin' : 'Admin'}
          </div>
        </div>
        <a href="/admin/logout/" title="Chiqish" style={{
          color: 'var(--text-dim)', display: 'flex', alignItems: 'center',
          padding: 4, borderRadius: 4, textDecoration: 'none',
          transition: 'color 0.15s',
        }} onMouseEnter={e => e.currentTarget.style.color='var(--danger)'}
           onMouseLeave={e => e.currentTarget.style.color='var(--text-dim)'}>
          <Icon name="log-out" size={14}/>
        </a>
      </div>
    </aside>
  );
}

function Topbar({ route, onNavigate, tweaks, setTweak }) {
  const meta = PAGE_META[route] || PAGE_META['/dashboard'];
  const isDark = tweaks.theme === 'dark';
  return (
    <div className="topbar">
      <button className="icon-btn" onClick={() => setTweak('sidebar', tweaks.sidebar === 'icon' ? 'dark' : 'icon')} title="Toggle sidebar">
        <Icon name="menu" size={16}/>
      </button>
      <div className="topbar-title">
        <h1>{meta.title}</h1>
        <div className="crumb">
          {meta.crumbs.map((c, i) => (
            <span key={i} style={{display: 'contents'}}>
              {i > 0 && <Icon name="chevron-right" size={11}/>}
              <span style={{color: i === meta.crumbs.length - 1 ? 'var(--text)' : undefined}}>{c}</span>
            </span>
          ))}
        </div>
      </div>
      <div className="topbar-actions">
        <button className="icon-btn" title="Поиск"><Icon name="search" size={16}/></button>
        <button className="icon-btn" title="Уведомления"><Icon name="bell" size={16}/></button>
        <button
          className="icon-btn"
          title={isDark ? 'Kun rejimi' : 'Tun rejimi'}
          onClick={() => setTweak('theme', isDark ? 'light' : 'dark')}
        >
          <Icon name={isDark ? 'sun' : 'moon'} size={16}/>
        </button>
        <div style={{width: 1, height: 22, background: 'var(--border)', margin: '0 4px'}}/>
        <Button variant="primary" size="sm" icon="plus">Добавить</Button>
      </div>
    </div>
  );
}

Object.assign(window, { Sidebar, Topbar, NAV_GROUPS, PAGE_META });
