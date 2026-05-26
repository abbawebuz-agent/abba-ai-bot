// UI primitives + icons for JIP Admin
// Components attach to window for sharing across babel script files.

const { useState, useEffect, useRef, useMemo, Fragment } = React;

// ============================================================
// Icons (Lucide-style minimal stroke SVGs, 16x16)
// ============================================================
function Icon({ name, size = 16, className = '', strokeWidth = 1.75 }) {
  const paths = {
    // navigation
    home: <><path d="M3 9.5L12 3l9 6.5V20a1 1 0 01-1 1h-5v-7H9v7H4a1 1 0 01-1-1V9.5z"/></>,
    users: <><circle cx="9" cy="8" r="3.5"/><path d="M15 11a3 3 0 100-6"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><path d="M16 14c2.5.4 5 2.3 5 6"/></>,
    user: <><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-8 8-8s8 3.6 8 8"/></>,
    qrcode: <><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><path d="M14 14h3v3h-3zM20 14v3M14 20h3M20 20h1"/></>,
    box: <><path d="M21 8l-9-5-9 5 9 5 9-5z"/><path d="M3 8v8l9 5 9-5V8"/><path d="M12 13v8"/></>,
    store: <><path d="M3 9l1.5-5h15L21 9"/><path d="M3 9v11h18V9"/><path d="M3 9h18"/><path d="M9 21v-6h6v6"/></>,
    gift: <><rect x="3" y="8" width="18" height="4" rx="1"/><path d="M5 12v9h14v-9"/><path d="M12 8v13"/><path d="M12 8c-3-1-5-3-3-5s4 1 3 5z"/><path d="M12 8c3-1 5-3 3-5s-4 1-3 5z"/></>,
    'gift-redeem': <><path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2v-7"/><rect x="2" y="7" width="20" height="5" rx="1"/><path d="M12 22V7"/><path d="M12 7c-3 0-6-2-6-4s3-2 6 4z"/><path d="M12 7c3 0 6-2 6-4s-3-2-6 4z"/></>,
    coin: <><circle cx="12" cy="12" r="9"/><path d="M9 9.5C9 8 10 7 12 7s3 1 3 2.5-1.2 2-3 2.5-3 1-3 2.5S10 17 12 17s3-1 3-2.5"/></>,
    'credit-card': <><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/><path d="M6 15h4"/></>,
    'id-card': <><rect x="2" y="5" width="20" height="14" rx="2"/><circle cx="9" cy="12" r="2.5"/><path d="M14 10h5M14 13h5M14 16h3"/></>,
    video: <><rect x="3" y="6" width="14" height="12" rx="2"/><path d="M17 10l5-3v10l-5-3"/></>,
    bell: <><path d="M12 3a6 6 0 016 6v4l2 3H4l2-3V9a6 6 0 016-6z"/><path d="M10 21a2 2 0 004 0"/></>,
    activity: <><path d="M3 12h4l3-8 4 16 3-8h4"/></>,
    radio: <><circle cx="12" cy="12" r="2"/><path d="M16.24 7.76a6 6 0 010 8.49M7.76 7.76a6 6 0 000 8.49"/><path d="M19.07 4.93a10 10 0 010 14.14M4.93 4.93a10 10 0 000 14.14"/></>,
    send: <><path d="M22 2L11 13"/><path d="M22 2l-7 20-4-9-9-4z"/></>,
    phone: <><path d="M22 16.92v3a2 2 0 01-2.18 2 19.86 19.86 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.86 19.86 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72c.13.96.37 1.9.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.91.33 1.85.57 2.81.7A2 2 0 0122 16.92z"/></>,
    lock: <><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 018 0v4"/></>,
    shield: <><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></>,
    settings: <><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 11-2.83 2.83l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 11-4 0v-.09a1.65 1.65 0 00-1-1.51 1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 11-2.83-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 110-4h.09a1.65 1.65 0 001.51-1 1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 112.83-2.83l.06.06a1.65 1.65 0 001.82.33h0a1.65 1.65 0 001-1.51V3a2 2 0 114 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 112.83 2.83l-.06.06a1.65 1.65 0 00-.33 1.82v0a1.65 1.65 0 001.51 1H21a2 2 0 110 4h-.09a1.65 1.65 0 00-1.51 1z"/></>,
    'bar-chart': <><path d="M3 21V3"/><path d="M3 21h18"/><rect x="7" y="13" width="3" height="5"/><rect x="12" y="9" width="3" height="9"/><rect x="17" y="5" width="3" height="13"/></>,
    // ui
    search: <><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></>,
    filter: <><path d="M3 4h18l-7 9v6l-4 2v-8z"/></>,
    plus: <><path d="M12 5v14M5 12h14"/></>,
    download: <><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><path d="M7 10l5 5 5-5"/><path d="M12 15V3"/></>,
    upload: <><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><path d="M17 8l-5-5-5 5"/><path d="M12 3v12"/></>,
    edit: <><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.12 2.12 0 113 3L12 15l-4 1 1-4 9.5-9.5z"/></>,
    eye: <><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></>,
    'eye-off': <><path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19"/><path d="M14.12 14.12a3 3 0 11-4.24-4.24"/><path d="M1 1l22 22"/></>,
    check: <><path d="M20 6L9 17l-5-5"/></>,
    x: <><path d="M18 6L6 18M6 6l12 12"/></>,
    chevron: <><path d="M9 18l6-6-6-6"/></>,
    'chevron-down': <><path d="M6 9l6 6 6-6"/></>,
    'chevron-up': <><path d="M18 15l-6-6-6 6"/></>,
    'chevron-left': <><path d="M15 18l-6-6 6-6"/></>,
    'chevron-right': <><path d="M9 18l6-6-6-6"/></>,
    menu: <><path d="M3 6h18M3 12h18M3 18h18"/></>,
    plug: <><path d="M9 2v6M15 2v6M6 8h12v3a6 6 0 11-12 0z"/><path d="M12 17v5"/></>,
    history: <><path d="M3 12a9 9 0 109-9 9.74 9.74 0 00-7 3.16L3 8"/><path d="M3 3v5h5"/><path d="M12 7v5l4 2"/></>,
    clock: <><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></>,
    map: <><path d="M3 6v15l6-3 6 3 6-3V3l-6 3-6-3-6 3z"/><path d="M9 3v15M15 6v15"/></>,
    'map-pin': <><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></>,
    layers: <><path d="M12 2l10 6-10 6L2 8z"/><path d="M2 14l10 6 10-6"/><path d="M2 18l10 6 10-6"/></>,
    sparkles: <><path d="M12 3l2 5 5 2-5 2-2 5-2-5-5-2 5-2z"/><path d="M19 17l1 2 2 1-2 1-1 2-1-2-2-1 2-1z"/></>,
    'message-circle': <><path d="M21 12a9 9 0 11-3.94-7.43L21 3l-1.43 3.94A8.96 8.96 0 0121 12z"/></>,
    'message-square': <><path d="M21 11.5a8.38 8.38 0 01-9 8.5 8.5 8.5 0 01-4-1l-5 1 1-5a8.5 8.5 0 014-9 8.38 8.38 0 019-1 8.5 8.5 0 014 9z"/></>,
    sliders: <><path d="M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3"/><path d="M1 14h6M9 8h6M17 16h6"/></>,
    'trending-up': <><path d="M22 7l-9.5 9.5-5-5L1 18"/><path d="M16 7h6v6"/></>,
    'trending-down': <><path d="M22 17l-9.5-9.5-5 5L1 6"/><path d="M16 17h6v-6"/></>,
    zap: <><path d="M13 2L3 14h7l-1 8 10-12h-7z"/></>,
    flame: <><path d="M14 7c-3 5-7 6-7 10a5 5 0 0010 0c0-3-2-4-3-7zM10 14a3 3 0 003 3"/></>,
    'arrow-right': <><path d="M5 12h14M12 5l7 7-7 7"/></>,
    'arrow-up-right': <><path d="M7 17L17 7M7 7h10v10"/></>,
    'more-horizontal': <><circle cx="5" cy="12" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/></>,
    trash: <><path d="M3 6h18M8 6V4a1 1 0 011-1h6a1 1 0 011 1v2M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6"/></>,
    'file-text': <><path d="M14 3H6a2 2 0 00-2 2v14a2 2 0 002 2h12a2 2 0 002-2V9z"/><path d="M14 3v6h6"/><path d="M8 13h8M8 17h8M8 9h2"/></>,
    archive: <><rect x="2" y="3" width="20" height="5" rx="1"/><path d="M4 8v11a2 2 0 002 2h12a2 2 0 002-2V8"/><path d="M10 12h4"/></>,
    image: <><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="M21 15l-5-5L5 21"/></>,
    calendar: <><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></>,
    'log-out': <><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><path d="M16 17l5-5-5-5M21 12H9"/></>,
    'help-circle': <><circle cx="12" cy="12" r="9"/><path d="M9.1 9a3 3 0 015.8 1c0 2-3 2-3 4"/><circle cx="12" cy="17" r="0.5"/></>,
    flag: <><path d="M4 22V4M4 4l14 4-6 5 6 4H4"/></>,
    'flag-uz': <><rect x="2" y="6" width="20" height="12" rx="1" fill="#0099b5" stroke="none"/><rect x="2" y="9.7" width="20" height="4.6" fill="#fff" stroke="none"/><rect x="2" y="11" width="20" height="2" fill="#1eb53a" stroke="none"/></>,
    'flag-ru': <><rect x="2" y="6" width="20" height="4" fill="#fff" stroke="none"/><rect x="2" y="10" width="20" height="4" fill="#0039a6" stroke="none"/><rect x="2" y="14" width="20" height="4" fill="#d52b1e" stroke="none"/></>,
    play: <><path d="M5 3l14 9-14 9z"/></>,
    code: <><path d="M16 18l6-6-6-6M8 6l-6 6 6 6"/></>,
    'shopping-cart': <><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.7 13.4a2 2 0 002 1.6h9.7a2 2 0 002-1.6L23 6H6"/></>,
    wrench: <><path d="M14.7 6.3a4 4 0 00-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 005.4-5.4l-2.7 2.7-2.6-2.6z"/></>,
    sun: <><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></>,
    moon: <><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/></>,
  };
  const path = paths[name];
  if (!path) return <span style={{display:'inline-block',width:size,height:size}}/>;
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={strokeWidth}
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      style={{flexShrink: 0}}
    >
      {path}
    </svg>
  );
}

// ============================================================
// Badge — full system with semantic variants
// ============================================================
function Badge({ children, variant = 'neutral', icon, dot, outline, size = 'md' }) {
  const cls = ['badge', `badge-${variant}`, outline ? 'badge-outline' : '', size === 'sm' ? 'badge-sm' : ''].join(' ');
  return (
    <span className={cls}>
      {dot && <span className="badge-dot"/>}
      {icon && <Icon name={icon} size={11}/>}
      {children}
    </span>
  );
}

// Status helpers (commonly used patterns)
const StatusBadges = {
  active: () => <Badge variant="success" dot>Активен</Badge>,
  inactive: () => <Badge variant="neutral" dot>Неактивен</Badge>,
  approved: () => <Badge variant="success" icon="check">Tasdiqlangan</Badge>,
  pending: () => <Badge variant="warning" icon="clock">Kutilmoqda</Badge>,
  cancelled: () => <Badge variant="danger" icon="x">Bekor qilindi</Badge>,
  santenik: () => <Badge variant="warning" icon="wrench">Santenik</Badge>,
  sotuvchi: () => <Badge variant="info" icon="store">Sotuvchi</Badge>,
  scanned: () => <Badge variant="success" icon="check">Использован</Badge>,
  unscanned: () => <Badge variant="warning" icon="clock">Не использован</Badge>,
  langUz: () => <Badge variant="neutral"><Icon name="flag-uz" size={11}/>O'zbek</Badge>,
  langRu: () => <Badge variant="neutral"><Icon name="flag-ru" size={11}/>Русский</Badge>,
};

// ============================================================
// Button
// ============================================================
function Button({ variant = 'secondary', size = 'md', icon, children, onClick, type = 'button', disabled }) {
  const cls = ['btn', `btn-${variant}`, size === 'sm' ? 'btn-sm' : (size === 'lg' ? 'btn-lg' : '')].join(' ');
  return (
    <button type={type} className={cls} onClick={onClick} disabled={disabled}>
      {icon && <Icon name={icon} size={14}/>}
      {children}
    </button>
  );
}

// ============================================================
// KPI Card
// ============================================================
function Sparkline({ values = [], color = '#6366f1' }) {
  if (!values.length) return null;
  const max = Math.max(...values);
  const min = Math.min(...values);
  const w = 100;
  const h = 30;
  const points = values.map((v, i) => {
    const x = (i / (values.length - 1)) * w;
    const y = h - ((v - min) / Math.max(max - min, 1)) * h;
    return `${x},${y}`;
  }).join(' ');
  return (
    <svg viewBox={`0 0 ${w} ${h}`} preserveAspectRatio="none" className="sparkline-svg">
      <defs>
        <linearGradient id={`spark-${color.replace('#','')}`} x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stopColor={color} stopOpacity="0.5"/>
          <stop offset="100%" stopColor={color} stopOpacity="0"/>
        </linearGradient>
      </defs>
      <polyline points={points} fill="none" stroke={color} strokeWidth="1.5" vectorEffect="non-scaling-stroke"/>
      <polygon points={`0,${h} ${points} ${w},${h}`} fill={`url(#spark-${color.replace('#','')})`}/>
    </svg>
  );
}

function KPI({ label, value, icon, delta, deltaDir = 'up', hint, color = 'indigo', spark, onClick }) {
  const colors = {
    indigo: { bg: 'var(--primary-soft)', fg: 'var(--primary)' },
    emerald: { bg: 'var(--success-soft)', fg: 'var(--success)' },
    amber:   { bg: 'var(--warning-soft)', fg: 'var(--warning)' },
    rose:    { bg: 'var(--danger-soft)', fg: 'var(--danger)' },
    blue:    { bg: 'var(--info-soft)', fg: 'var(--info)' },
  };
  const c = colors[color];
  return (
    <div className="kpi" onClick={onClick} role={onClick ? 'button' : undefined}>
      <div className="kpi-head">
        <span className="kpi-label">{label}</span>
        <span className="kpi-icon" style={{background: c.bg, color: c.fg}}>
          <Icon name={icon} size={16}/>
        </span>
      </div>
      <div className="kpi-value">{value}</div>
      <div className="kpi-meta">
        {delta && (
          <span className={deltaDir === 'up' ? 'delta-up' : 'delta-down'}>
            <Icon name={deltaDir === 'up' ? 'trending-up' : 'trending-down'} size={12}/> {delta}
          </span>
        )}
        {hint && <span>{hint}</span>}
      </div>
      {spark && <div className="kpi-spark"><Sparkline values={spark} color={c.fg.startsWith('var(') ? '#6366f1' : c.fg}/></div>}
    </div>
  );
}

// ============================================================
// Avatar
// ============================================================
function Avatar({ name, size = 32, color }) {
  const initials = (name || '?').split(' ').map(s => s[0]).slice(0, 2).join('').toUpperCase();
  const hash = (name || '').split('').reduce((a, c) => a + c.charCodeAt(0), 0);
  const gradients = [
    'linear-gradient(135deg, #6366f1, #4338ca)',
    'linear-gradient(135deg, #10b981, #047857)',
    'linear-gradient(135deg, #f59e0b, #d97706)',
    'linear-gradient(135deg, #ec4899, #9333ea)',
    'linear-gradient(135deg, #3b82f6, #1e40af)',
    'linear-gradient(135deg, #14b8a6, #0f766e)',
  ];
  return (
    <div style={{
      width: size, height: size, borderRadius: 999,
      background: color || gradients[hash % gradients.length],
      display: 'grid', placeItems: 'center', color: 'white',
      fontSize: size * 0.36, fontWeight: 600,
      flexShrink: 0,
    }}>{initials}</div>
  );
}

// ============================================================
// Page wrapper helpers
// ============================================================
function PageHeader({ title, subtitle, actions }) {
  return (
    <div className="page-header">
      <div>
        <h2>{title}</h2>
        {subtitle && <div className="subtitle">{subtitle}</div>}
      </div>
      {actions && <div className="page-actions">{actions}</div>}
    </div>
  );
}

function FormBlock({ title, badge, children, single, icon }) {
  return (
    <div className="form-block">
      <div className="form-block-header">
        {icon && <span style={{
          width: 24, height: 24, display: 'grid', placeItems: 'center',
          borderRadius: 6, background: 'var(--primary-soft)', color: 'var(--primary)'
        }}><Icon name={icon} size={13}/></span>}
        <h3>{title}</h3>
        {badge}
      </div>
      <div className={'form-block-body' + (single ? ' single' : '')}>{children}</div>
    </div>
  );
}

function Field({ label, hint, required, children, span2 }) {
  return (
    <div className={'field' + (span2 ? ' span-2' : '')}>
      {label && <label className="field-label">{label}{required && <span className="req">*</span>}</label>}
      {children}
      {hint && <span className="field-hint">{hint}</span>}
    </div>
  );
}

function Input(props) { return <input className="input" {...props}/>; }
function Textarea(props) { return <textarea className="textarea" {...props}/>; }
function Select({ children, ...props }) { return <select className="select" {...props}>{children}</select>; }
function Toggle({ on, onChange }) {
  return <button type="button" className={'toggle' + (on ? ' on' : '')} onClick={() => onChange(!on)}/>;
}

// ============================================================
// Filter bar + search
// ============================================================
function SearchBar({ placeholder = 'Поиск...', value, onChange }) {
  return (
    <div className="input-group" style={{minWidth: 260, height: 32}}>
      <span className="prefix"><Icon name="search" size={14}/></span>
      <input className="input" placeholder={placeholder} value={value || ''} onChange={e => onChange?.(e.target.value)} style={{height: 30, fontSize: 13}}/>
    </div>
  );
}

function FilterChip({ active, onClick, children, icon }) {
  return (
    <button className={'filter-chip' + (active ? ' active' : '')} onClick={onClick}>
      {icon && <Icon name={icon} size={12}/>}
      {children}
      <Icon name="chevron-down" size={11}/>
    </button>
  );
}

// ============================================================
// Empty state
// ============================================================
function EmptyState({ icon = 'box', title, hint }) {
  return (
    <div className="empty">
      <div className="empty-icon"><Icon name={icon} size={20}/></div>
      <h4>{title}</h4>
      {hint && <div>{hint}</div>}
    </div>
  );
}

// ============================================================
// Pagination
// ============================================================
function Pagination({ total, page = 1, perPage = 25, onChange }) {
  const pages = Math.ceil(total / perPage);
  const start = (page - 1) * perPage + 1;
  const end = Math.min(page * perPage, total);
  return (
    <div className="pagination">
      <span>Показано <strong>{start}–{end}</strong> из <strong>{total.toLocaleString('ru')}</strong></span>
      <div className="pager">
        <button className="page-btn" onClick={() => onChange?.(Math.max(1, page-1))}><Icon name="chevron-left" size={14}/></button>
        {Array.from({length: Math.min(5, pages)}, (_, i) => i + 1).map(p => (
          <button key={p} className={'page-btn' + (p === page ? ' active' : '')} onClick={() => onChange?.(p)}>{p}</button>
        ))}
        {pages > 5 && <span style={{padding: '0 6px', color: 'var(--text-dim)'}}>…</span>}
        {pages > 5 && <button className="page-btn" onClick={() => onChange?.(pages)}>{pages}</button>}
        <button className="page-btn" onClick={() => onChange?.(Math.min(pages, page+1))}><Icon name="chevron-right" size={14}/></button>
      </div>
    </div>
  );
}

// ============================================================
// Date hierarchy
// ============================================================
function DateHierarchy({ items = ['2026', 'Май', '22', '23', '25', '26'], active = 0 }) {
  return (
    <div className="date-strip">
      <span style={{marginRight: 8, color: 'var(--text-dim)'}}><Icon name="calendar" size={12}/></span>
      {items.map((d, i) => (
        <span key={i} className={'crumb-item' + (i === active ? ' active' : '')}>{d}</span>
      ))}
    </div>
  );
}

// ============================================================
// Recent actions panel
// ============================================================
function RecentActions({ items }) {
  return (
    <div className="card">
      <div className="card-header">
        <h3>Последние действия</h3>
        <Icon name="activity" size={14} className="text-muted"/>
      </div>
      <div style={{padding: '4px 0'}}>
        {items.map((a, i) => (
          <div key={i} style={{
            padding: '10px 20px',
            borderBottom: i < items.length - 1 ? '1px solid var(--border)' : 0,
            display: 'flex',
            flexDirection: 'column',
            gap: 2,
            cursor: 'pointer',
            transition: 'background 100ms',
          }} onMouseEnter={e => e.currentTarget.style.background = 'rgba(255,255,255,0.02)'}
             onMouseLeave={e => e.currentTarget.style.background = 'transparent'}>
            <div style={{fontSize: 13, color: 'var(--text-strong)', fontWeight: 500}}>{a.object}</div>
            <div style={{display:'flex', justifyContent:'space-between', alignItems:'center', gap: 8}}>
              <span style={{fontSize: 12, color: 'var(--text-muted)'}}>{a.action}</span>
              <span style={{fontSize: 11, color: 'var(--text-dim)', fontFamily: 'var(--font-mono)'}}>{a.time}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ============================================================
// Modal
// ============================================================
function Modal({ open, title, onClose, children, footer, icon }) {
  if (!open) return null;
  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          {icon && <Icon name={icon} size={16} className="text-muted"/>}
          <h3 style={{margin: 0, fontSize: 14, fontWeight: 600, color: 'var(--text-strong)'}}>{title}</h3>
          <button className="icon-btn" style={{marginLeft: 'auto', width: 28, height: 28}} onClick={onClose}>
            <Icon name="x" size={14}/>
          </button>
        </div>
        <div className="modal-body">{children}</div>
        {footer && <div className="modal-footer">{footer}</div>}
      </div>
    </div>
  );
}

// Export to window for cross-file sharing
Object.assign(window, {
  Icon, Badge, StatusBadges, Button, KPI, Sparkline, Avatar,
  PageHeader, FormBlock, Field, Input, Textarea, Select, Toggle,
  SearchBar, FilterChip, EmptyState, Pagination, DateHierarchy,
  RecentActions, Modal,
});
