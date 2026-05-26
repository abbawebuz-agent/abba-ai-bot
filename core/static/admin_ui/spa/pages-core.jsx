// Core pages: Dashboard, Analytics, Users list, User edit (Santenik + Sotuvchi),
// Send-region message, Send-single message, Admin auth users/groups

const J = window.JIP;

// ============================================================
// 1. DASHBOARD
// ============================================================
function DashboardPage({ onNavigate }) {
  return (
    <div className="page">
      <PageHeader
        title="Boshqaruv paneli"
        subtitle="Loyihaning umumiy ko'rsatkichlari va so'nggi faoliyat"
        actions={<>
          <Button variant="secondary" icon="download">Eksport</Button>
          <Button variant="primary" icon="plus">Yangi yozuv</Button>
        </>}
      />

      <div className="kpi-grid">
        <KPI label="Jami foydalanuvchilar" value="23" icon="users" delta="+12%" hint="Telegram reg." color="indigo" spark={[12,14,15,18,19,21,22,23]} onClick={() => onNavigate('/users')}/>
        <KPI label="Faol partiyalar" value="17" icon="box" delta="+3" hint="Hozirda faol" color="emerald" spark={[10,11,12,13,14,16,16,17]} onClick={() => onNavigate('/batches')}/>
        <KPI label="Jami skanlar" value="239" icon="qrcode" delta="+34" hint="Ishlatilgan QR" color="blue" spark={[120,140,155,178,200,215,225,239]} onClick={() => onNavigate('/qrcodes')}/>
        <KPI label="Kutilayotgan sovg'alar" value="15" icon="gift" delta="+2" deltaDir="up" hint="Обработать" color="amber" spark={[5,8,10,11,13,12,14,15]} onClick={() => onNavigate('/redemptions')}/>
      </div>

      <div className="two-col">
        <div style={{display: 'flex', flexDirection: 'column', gap: 20}}>
          <ModelGrid onNavigate={onNavigate}/>
          <ActivityChart/>
        </div>
        <RecentActions items={J.recentActions}/>
      </div>
    </div>
  );
}

function ModelGrid({ onNavigate }) {
  const sections = [
    {
      title: 'Core',
      models: [
        { name: 'Telegram пользователи', count: 23, route: '/users', icon: 'users' },
        { name: 'QR коды', count: 239, route: '/qrcodes', icon: 'qrcode' },
        { name: 'QR партии', count: 17, route: '/batches', icon: 'box' },
        { name: 'Магазины', count: 12, route: '/stores', icon: 'store' },
        { name: 'Подарки', count: 8, route: '/gifts', icon: 'gift' },
        { name: 'Заявки на подарки', count: 15, route: '/redemptions', icon: 'gift-redeem' },
        { name: 'Транзакции', count: 1117, route: '/transactions', icon: 'credit-card' },
        { name: 'Коды регистрации', count: 25, route: '/seller-codes', icon: 'id-card' },
        { name: 'LiveStream', count: 4, route: '/livestreams', icon: 'radio' },
        { name: 'Видеоинструкции', count: 5, route: '/videos', icon: 'video' },
        { name: 'Журнал', count: 264, route: '/activity', icon: 'history' },
        { name: 'Politika', count: 2, route: '/privacy', icon: 'file-text' },
      ],
    },
    {
      title: 'Foydalanuvchilar va guruhlar',
      models: [
        { name: 'Admin foydalanuvchilar', count: 4, route: '/auth/users', icon: 'user' },
        { name: 'Guruhlar', count: 4, route: '/auth/groups', icon: 'shield' },
      ],
    },
  ];

  return (
    <div className="card">
      <div className="card-header">
        <h3>Modellar</h3>
        <span className="text-muted text-xs">Bosib kerakli bo'limga o'tish</span>
      </div>
      <div style={{padding: 16, display: 'flex', flexDirection: 'column', gap: 24}}>
        {sections.map((s, si) => (
          <div key={si}>
            <div style={{
              fontSize: 11, fontWeight: 600, color: 'var(--text-dim)',
              letterSpacing: '0.06em', textTransform: 'uppercase', marginBottom: 8, paddingLeft: 4,
            }}>{s.title}</div>
            <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: 8}}>
              {s.models.map((m, mi) => (
                <div key={mi} onClick={() => onNavigate(m.route)} style={{
                  display: 'flex', alignItems: 'center', gap: 12, padding: '10px 12px',
                  borderRadius: 8, cursor: 'pointer', border: '1px solid var(--border)',
                  background: 'var(--surface-2)', transition: 'border 120ms, background 120ms',
                }}
                onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--border-strong)'; e.currentTarget.style.background = 'var(--surface-3)'; }}
                onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.background = 'var(--surface-2)'; }}>
                  <span style={{
                    width: 32, height: 32, borderRadius: 6,
                    background: 'var(--primary-soft)', color: 'var(--primary)',
                    display: 'grid', placeItems: 'center', flexShrink: 0,
                  }}><Icon name={m.icon} size={15}/></span>
                  <div style={{flex: 1, minWidth: 0}}>
                    <div style={{fontSize: 13, color: 'var(--text-strong)', fontWeight: 500, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap'}}>{m.name}</div>
                    <div style={{fontSize: 11.5, color: 'var(--text-muted)', fontVariantNumeric: 'tabular-nums'}}>{m.count.toLocaleString('ru')} yozuv</div>
                  </div>
                  <button className="icon-btn" style={{width: 24, height: 24}} title="Yangi qo'shish" onClick={e => e.stopPropagation()}>
                    <Icon name="plus" size={12}/>
                  </button>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function ActivityChart() {
  // Decorative line + bar chart card
  const days = ['18 май','19 май','20 май','21 май','22 май','23 май','24 май','25 май','26 май'];
  const scans = [12, 18, 14, 22, 28, 24, 34, 30, 38];
  const regs = [1, 2, 1, 3, 2, 4, 3, 5, 2];
  const max = Math.max(...scans);
  return (
    <div className="card">
      <div className="card-header">
        <div>
          <h3>QR aktivlik · So'nggi 9 kun</h3>
          <div className="sub">Skanlar va yangi ro'yxatdan o'tishlar</div>
        </div>
        <div style={{display:'flex', gap: 16, alignItems: 'center'}}>
          <div style={{display:'flex', alignItems:'center', gap: 6, fontSize: 12, color: 'var(--text-muted)'}}>
            <span style={{width: 8, height: 8, borderRadius: 999, background: 'var(--primary)'}}/>
            Skanlar
          </div>
          <div style={{display:'flex', alignItems:'center', gap: 6, fontSize: 12, color: 'var(--text-muted)'}}>
            <span style={{width: 8, height: 8, borderRadius: 999, background: 'var(--success)'}}/>
            Yangi
          </div>
        </div>
      </div>
      <div style={{padding: 24, height: 200, position: 'relative'}}>
        <svg viewBox="0 0 900 180" preserveAspectRatio="none" style={{width: '100%', height: '100%', display: 'block'}}>
          <defs>
            <linearGradient id="chart-fill" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0%" stopColor="#6366f1" stopOpacity="0.3"/>
              <stop offset="100%" stopColor="#6366f1" stopOpacity="0"/>
            </linearGradient>
          </defs>
          {[0,1,2,3,4].map(i => (
            <line key={i} x1="0" x2="900" y1={i * 36 + 18} y2={i * 36 + 18} stroke="rgba(255,255,255,0.04)" strokeDasharray="2 4"/>
          ))}
          {days.map((d, i) => {
            const x = (i / (days.length - 1)) * 850 + 25;
            const h = (scans[i] / max) * 100;
            return (
              <rect key={i} x={x - 8} y={170 - h} width="16" height={h} rx="2" fill="var(--success)" opacity="0.18"/>
            );
          })}
          <polyline
            fill="url(#chart-fill)"
            stroke="none"
            points={days.map((_, i) => `${(i / (days.length - 1)) * 850 + 25},${170 - (scans[i] / max) * 140} ` ).join('') + `${(days.length-1)/(days.length-1)*850+25},170 25,170`}
          />
          <polyline
            fill="none"
            stroke="#6366f1"
            strokeWidth="2"
            points={days.map((_, i) => `${(i / (days.length - 1)) * 850 + 25},${170 - (scans[i] / max) * 140}` ).join(' ')}
          />
          {days.map((_, i) => (
            <circle key={i} cx={(i / (days.length - 1)) * 850 + 25} cy={170 - (scans[i] / max) * 140} r="3.5" fill="#6366f1" stroke="var(--surface-1)" strokeWidth="2"/>
          ))}
        </svg>
        <div style={{display: 'flex', justifyContent: 'space-between', padding: '8px 25px 0', fontSize: 11, color: 'var(--text-dim)', fontVariantNumeric: 'tabular-nums'}}>
          {days.map((d, i) => <span key={i}>{d}</span>)}
        </div>
      </div>
    </div>
  );
}

// ============================================================
// 34. ANALYTICS PAGE
// ============================================================
function AnalyticsPage() {
  return (
    <div className="page">
      <PageHeader
        title="Аналитика"
        subtitle="Loyiha bo'yicha to'liq ko'rsatkichlar"
        actions={<>
          <Select style={{width: 140}}>
            <option>So'nggi 30 kun</option>
            <option>So'nggi 7 kun</option>
            <option>Bu oy</option>
            <option>O'tgan oy</option>
          </Select>
          <Button variant="secondary" icon="download">PDF eksport</Button>
        </>}
      />

      <div className="kpi-grid">
        <KPI label="Aktivatsiya foizi" value="19.7%" icon="trending-up" delta="+2.4%" color="emerald" spark={[14,15,17,18,19,20,19,20]}/>
        <KPI label="Yangi sotuvchilar" value="21" icon="users" delta="+5" color="indigo" spark={[2,4,6,9,12,15,18,21]}/>
        <KPI label="Sovg'a so'rovlari" value="15" icon="gift" delta="+8" color="amber" spark={[3,5,6,8,10,12,14,15]}/>
        <KPI label="Jami transaksiya" value="1 117" icon="credit-card" delta="+82" color="blue" spark={[800,890,940,990,1020,1050,1080,1117]}/>
      </div>

      <div style={{display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 20}}>
        <ActivityChart/>
        <div className="card">
          <div className="card-header">
            <h3>Viloyatlar bo'yicha</h3>
          </div>
          <div style={{padding: 20, display: 'flex', flexDirection: 'column', gap: 14}}>
            {[
              { name: 'Город Ташкент', value: 8, pct: 35 },
              { name: 'Самаркандская', value: 4, pct: 17 },
              { name: 'Бухарская', value: 3, pct: 13 },
              { name: 'Ферганская', value: 3, pct: 13 },
              { name: 'Андижанская', value: 2, pct: 9 },
              { name: 'Прочие', value: 3, pct: 13 },
            ].map((r, i) => (
              <div key={i}>
                <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: 4, fontSize: 12.5}}>
                  <span style={{color: 'var(--text)'}}>{r.name}</span>
                  <span className="text-mono text-muted">{r.value} ({r.pct}%)</span>
                </div>
                <div className="progress"><div style={{width: r.pct + '%'}}/></div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20}}>
        <div className="card">
          <div className="card-header"><h3>TOP sotuvchilar (ballar bo'yicha)</h3></div>
          <div className="table-wrap">
            <table className="table">
              <thead><tr><th>Sotuvchi</th><th>QR</th><th style={{textAlign: 'right'}}>Ball</th></tr></thead>
              <tbody>
                {J.users.filter(u => u.type === 'sotuvchi').slice(0, 6).map(u => (
                  <tr key={u.id}>
                    <td>
                      <div className="user-cell">
                        <Avatar name={u.first_name + ' ' + u.last_name} size={28}/>
                        <div>
                          <div className="user-name">{u.first_name} {u.last_name}</div>
                          <div className="user-meta">@{u.username}</div>
                        </div>
                      </div>
                    </td>
                    <td className="num">{u.total_qr || 0}</td>
                    <td style={{textAlign: 'right'}}><span className="text-mono" style={{color: 'var(--primary)', fontWeight: 600}}>{u.points.toLocaleString('ru')}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="card">
          <div className="card-header"><h3>Konversiya voronkasi</h3></div>
          <div style={{padding: 20, display: 'flex', flexDirection: 'column', gap: 12}}>
            {[
              { label: 'Sotuvchilar ro\'yxatdan o\'tishi', v: 25, pct: 100, color: 'var(--info)' },
              { label: 'Tasdiqlanganlar', v: 21, pct: 84, color: 'var(--primary)' },
              { label: 'Partiya yaratganlar', v: 17, pct: 68, color: '#a855f7' },
              { label: 'QR skanlandi (santenik)', v: 47, pct: 19.7, color: 'var(--success)' },
              { label: 'Sovg\'a so\'ragan', v: 15, pct: 6.3, color: 'var(--warning)' },
            ].map((s, i) => (
              <div key={i}>
                <div style={{display: 'flex', justifyContent: 'space-between', fontSize: 12.5, marginBottom: 4}}>
                  <span>{s.label}</span>
                  <span className="text-mono"><strong>{s.v}</strong> <span className="text-dim">({s.pct}%)</span></span>
                </div>
                <div style={{height: 10, background: 'var(--surface-3)', borderRadius: 6, overflow: 'hidden'}}>
                  <div style={{height: '100%', width: s.pct + '%', background: s.color, borderRadius: 6}}/>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// ============================================================
// 2. USERS LIST
// ============================================================
function UsersListPage({ onNavigate }) {
  const [selected, setSelected] = useState([]);
  const allIds = J.users.map(u => u.id);
  const allSelected = selected.length === allIds.length;

  const toggleAll = () => setSelected(allSelected ? [] : allIds);
  const toggleOne = (id) => setSelected(s => s.includes(id) ? s.filter(x => x !== id) : [...s, id]);

  return (
    <div className="page">
      <PageHeader
        title="Telegram пользователи"
        subtitle="Sistemada ro'yxatdan o'tgan barcha foydalanuvchilar"
        actions={<>
          <Button variant="secondary" icon="message-circle" onClick={() => onNavigate('/users/send-single')}>Xabar</Button>
          <Button variant="primary" icon="send" onClick={() => onNavigate('/users/send-region')}>Отправить по области</Button>
        </>}
      />

      <div className="card">
        <DateHierarchy items={['2026', 'Май', '22', '23', '25', '26']} active={5}/>
        <div className="filter-bar">
          <SearchBar placeholder="Поиск: ism, telefon, ID..." />
          <div style={{flex: 1}}/>
          <FilterChip icon="user">Тип</FilterChip>
          <FilterChip icon="check" active>Faollik: Faol</FilterChip>
          <FilterChip icon="flag">Til</FilterChip>
          <FilterChip icon="map-pin">Viloyat</FilterChip>
          <FilterChip icon="calendar">Sana diapazoni</FilterChip>
        </div>

        {selected.length > 0 && (
          <div style={{
            padding: '10px 16px', background: 'var(--primary-softer)',
            borderBottom: '1px solid var(--border)', display: 'flex', alignItems: 'center', gap: 10
          }}>
            <span className="text-sm text-strong">{selected.length} ta tanlangan</span>
            <div style={{flex: 1}}/>
            <Button size="sm" variant="success" icon="check">Tasdiqlash</Button>
            <Button size="sm" variant="danger" icon="x">Rad etish</Button>
            <Select style={{height: 28, fontSize: 12, width: 220}}>
              <option>Yana amallar...</option>
              <option>Тип на Sotuvchi</option>
              <option>Обновить виloyat (Nominatim)</option>
              <option>Персональное сообщение</option>
              <option>O'chirish</option>
            </Select>
          </div>
        )}

        <div className="table-wrap">
          <table className="table">
            <thead>
              <tr>
                <th className="col-checkbox"><input type="checkbox" className="checkbox" checked={allSelected} onChange={toggleAll}/></th>
                <th>Foydalanuvchi</th>
                <th>Phone</th>
                <th>Viloyat / Tuman</th>
                <th>Tur</th>
                <th>Tasdiqlash</th>
                <th style={{textAlign: 'right'}}>Ballar</th>
                <th>Til</th>
                <th>Status</th>
                <th style={{textAlign: 'right'}}></th>
              </tr>
            </thead>
            <tbody>
              {J.users.map(u => (
                <tr key={u.id}>
                  <td className="col-checkbox"><input type="checkbox" className="checkbox" checked={selected.includes(u.id)} onChange={() => toggleOne(u.id)}/></td>
                  <td onClick={() => onNavigate(u.type === 'santenik' ? '/users/santenik' : '/users/sotuvchi')} style={{cursor:'pointer'}}>
                    <div className="user-cell">
                      <Avatar name={u.first_name + ' ' + u.last_name}/>
                      <div>
                        <div className="user-name">
                          {u.type === 'santenik' ? <Icon name="wrench" size={12} className="text-muted"/> : <Icon name="store" size={12} className="text-muted"/>}
                          {u.first_name} {u.last_name}
                          <span className="text-muted text-xs">@{u.username}</span>
                        </div>
                        <div className="user-meta">ID: {u.id}</div>
                      </div>
                    </div>
                  </td>
                  <td><span className="text-mono text-sm">{u.phone}</span></td>
                  <td>
                    <div style={{display:'flex', flexDirection:'column', gap: 3}}>
                      <Badge variant="info" icon="map-pin">{u.region.replace(' область', '').replace('Город ', '')}</Badge>
                      <Badge variant="warning" outline size="sm" icon="map-pin">{u.district}</Badge>
                    </div>
                  </td>
                  <td>{u.type === 'santenik' ? <StatusBadges.santenik/> : <StatusBadges.sotuvchi/>}</td>
                  <td>{u.type === 'sotuvchi' ? (u.seller_approved ? <StatusBadges.approved/> : <StatusBadges.pending/>) : <span className="text-dim text-xs">—</span>}</td>
                  <td style={{textAlign: 'right'}}><span className="text-mono" style={{color:'var(--primary)', fontWeight: 600}}>{u.points.toLocaleString('ru')}</span></td>
                  <td>{u.language === 'uz' ? <StatusBadges.langUz/> : <StatusBadges.langRu/>}</td>
                  <td>{u.is_active ? <StatusBadges.active/> : <StatusBadges.inactive/>}</td>
                  <td style={{textAlign: 'right'}}>
                    <Button size="sm" variant="ghost" icon="message-square" onClick={() => onNavigate('/users/send-single')}>Написать</Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <Pagination total={23} page={1} perPage={25}/>
      </div>
    </div>
  );
}

// ============================================================
// 2b-1. SANTENIK EDIT
// ============================================================
function UserSantenikPage({ onNavigate }) {
  const u = J.users[0];
  return (
    <div className="page">
      <PageHeader
        title={<span>{u.first_name} {u.last_name} <Badge variant="warning" icon="wrench">Santenik</Badge></span>}
        subtitle={'ID: ' + u.id + ' · @' + u.username + ' · ' + u.region}
        actions={<>
          <Button variant="ghost" icon="history">История</Button>
          <Button variant="secondary" icon="trash">O'chirish</Button>
          <Button variant="primary" icon="check">Сохранить</Button>
        </>}
      />

      <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16}}>
        <FormBlock title="Основная информация" icon="user">
          <Field label="Telegram ID"><Input defaultValue={u.id} readOnly/></Field>
          <Field label="Username"><Input defaultValue={'@' + u.username} readOnly/></Field>
          <Field label="First name" required><Input defaultValue={u.first_name}/></Field>
          <Field label="Last name"><Input defaultValue={u.last_name}/></Field>
          <Field label="Jami urinishlar" hint="Faqat ko'rish"><Input defaultValue={u.total_attempts} readOnly/></Field>
          <Field label="Muvaffaqiyatli" hint="Faqat ko'rish"><Input defaultValue={u.successful_attempts} readOnly/></Field>
          <Field label="Skanlangan urinishlar" hint="Faqat ko'rish" span2><Input defaultValue={u.successful_attempts} readOnly/></Field>
        </FormBlock>

        <FormBlock title="Контактные данные" icon="map-pin">
          <Field label="Phone number" required><Input defaultValue={u.phone}/></Field>
          <Field label="Latitude"><Input defaultValue={u.latitude.toFixed(6)}/></Field>
          <Field label="Longitude"><Input defaultValue={u.longitude.toFixed(6)}/></Field>
          <Field span2>
            <Button variant="secondary" icon="map">Открыть на Яндекс.Картах</Button>
          </Field>
          <Field label="Viloyat (autocomplete)" required>
            <Select defaultValue={u.region}>{J.regions.map(r => <option key={r}>{r}</option>)}</Select>
          </Field>
          <Field label="Tuman">
            <Select defaultValue={u.district}>
              {(J.districtsByRegion[u.region] || []).map(d => <option key={d}>{d}</option>)}
            </Select>
          </Field>
        </FormBlock>

        <FormBlock title="Тип и баллы" icon="coin" badge={<Badge variant="primary">{u.points.toLocaleString('ru')} ball</Badge>}>
          <Field label="User type">
            <Select defaultValue="santenik">
              <option value="santenik">Santenik</option>
              <option value="sotuvchi">Sotuvchi</option>
            </Select>
          </Field>
          <Field label="Баллы (промокоды − заказы)" hint="Avtomatik hisoblanadi">
            <div className="input" style={{color:'var(--primary)', fontWeight: 600}}>{u.points.toLocaleString('ru')}</div>
          </Field>
          <Field label="Points" hint="Faqat ko'rish" span2>
            <Input defaultValue={u.points} readOnly/>
          </Field>
          <div className="span-2" style={{
            padding: '10px 12px', background: 'var(--surface-2)', borderRadius: 8,
            fontSize: 12.5, color: 'var(--text-muted)', borderLeft: '3px solid var(--primary)'
          }}>
            <strong style={{color:'var(--text)'}}>Santenik:</strong> ballarni QR-skanlardan oladi.
            Har bir muvaffaqiyatli skan uchun 50 ball qo'shiladi.
          </div>
        </FormBlock>

        <FormBlock title="Настройки и активность" icon="settings">
          <Field label="Til">
            <Select defaultValue={u.language}>
              <option value="uz">🇺🇿 O'zbek</option>
              <option value="ru">🇷🇺 Русский</option>
            </Select>
          </Field>
          <Field label="Faollik">
            <label style={{display:'flex', alignItems:'center', gap: 8}}>
              <input type="checkbox" className="checkbox" defaultChecked={u.is_active}/>
              <span className="text-sm">Активен</span>
            </label>
          </Field>
          <Field label="Last message sent at"><Input defaultValue="2026-05-26 14:23" readOnly/></Field>
          <Field label="Blocked bot at"><Input defaultValue="—" readOnly/></Field>
          <Field label="Promo failed attempts"><Input defaultValue="0"/></Field>
          <Field label="Promo block stage"><Input defaultValue="0"/></Field>
          <Field label="Promo blocked until" span2><Input defaultValue="—" readOnly/></Field>
        </FormBlock>

        <FormBlock title="Sotuvchi tasdiqlash" icon="check" badge={<Badge variant="neutral" outline>collapsed</Badge>}>
          <Field label="Tasdiqlangan">
            <label style={{display:'flex', alignItems:'center', gap: 8}}>
              <input type="checkbox" className="checkbox"/>
              <span className="text-sm text-muted">Faol</span>
            </label>
          </Field>
          <Field label="Tasdiqlangan vaqt"><Input defaultValue="—" readOnly/></Field>
        </FormBlock>

        <FormBlock title="Sanalar" icon="calendar">
          <Field label="Yaratilgan"><Input defaultValue={u.created_at + ' 14:23:11'} readOnly/></Field>
          <Field label="O'zgartirilgan"><Input defaultValue="2026-05-26 16:08:42" readOnly/></Field>
        </FormBlock>
      </div>

      <div className="card">
        <div className="card-header">
          <h3>Отсканированные промокоды</h3>
          <Badge variant="neutral">{u.successful_attempts} ta</Badge>
        </div>
        <div className="table-wrap">
          <table className="table inline-table">
            <thead><tr><th>Serial</th><th>Store</th><th>Batch</th><th>Points</th><th>Scanned at</th></tr></thead>
            <tbody>
              {J.qrcodes.filter(q => q.is_scanned).slice(0, 5).map(q => (
                <tr key={q.id}>
                  <td><span className="code-mask">#{q.serial}</span></td>
                  <td>{q.store_name}</td>
                  <td className="text-mono text-xs">{q.batch_name}</td>
                  <td className="num text-mono" style={{color:'var(--primary)'}}>+{q.points}</td>
                  <td className="text-mono text-xs text-muted">{q.scanned_at}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="form-footer">
        <span className="text-muted text-sm">Изменения не сохранены</span>
        <div style={{display: 'flex', gap: 8}}>
          <Button variant="ghost">Сохранить и добавить другой</Button>
          <Button variant="secondary">Сохранить и продолжить</Button>
          <Button variant="primary" icon="check">Сохранить</Button>
        </div>
      </div>
    </div>
  );
}

// ============================================================
// 2b-2. SOTUVCHI EDIT (4 blocks)
// ============================================================
function UserSotuvchiPage({ onNavigate }) {
  const u = J.users.find(x => x.type === 'sotuvchi');
  return (
    <div className="page">
      <PageHeader
        title={<span>{u.first_name} {u.last_name} <Badge variant="info" icon="store">Sotuvchi</Badge></span>}
        subtitle={<span>ID: {u.id} · @{u.username} · <span className="code-mask">{u.seller_code}</span></span>}
        actions={<>
          <Button variant="ghost" icon="history">История</Button>
          <Button variant="secondary" icon="download">Excel eksport</Button>
          <Button variant="primary" icon="check">Сохранить</Button>
        </>}
      />

      <FormBlock title="Asosiy ma'lumotlar" icon="user" badge={<Badge variant="primary">{u.points.toLocaleString('ru')} ball</Badge>}>
        <Field label="First name" required><Input defaultValue={u.first_name}/></Field>
        <Field label="Last name"><Input defaultValue={u.last_name}/></Field>
        <Field label="Username"><Input defaultValue={'@' + u.username} readOnly/></Field>
        <Field label="Telegram ID"><Input defaultValue={u.id} readOnly/></Field>
        <Field label="Phone number"><Input defaultValue={u.phone}/></Field>
        <Field label="User type">
          <Select defaultValue="sotuvchi"><option value="sotuvchi">Sotuvchi</option><option value="santenik">Santenik</option></Select>
        </Field>
        <Field label="Language">
          <Select defaultValue={u.language}><option value="uz">🇺🇿 O'zbek</option><option value="ru">🇷🇺 Русский</option></Select>
        </Field>
        <Field label="Points" hint="Faqat ko'rish"><Input defaultValue={u.points} readOnly/></Field>
        <Field label="Seller code"><div className="input"><span className="code-mask">{u.seller_code}</span></div></Field>
        <Field label="Store ID">
          <div className="input" style={{display:'flex', alignItems:'center', gap: 8}}>
            <Icon name="store" size={13} className="text-muted"/>
            <a style={{color: 'var(--primary)', cursor:'pointer'}} onClick={() => onNavigate('/stores')}>{u.store_id} · Sadulla Jomiy 1</a>
          </div>
        </Field>
        <Field label="is_active">
          <label style={{display:'flex', alignItems:'center', gap: 8}}><input type="checkbox" className="checkbox" defaultChecked={u.is_active}/> <span className="text-sm">Активен</span></label>
        </Field>
        <Field label="seller_approved">
          <label style={{display:'flex', alignItems:'center', gap: 8}}><input type="checkbox" className="checkbox" defaultChecked={u.seller_approved}/> <span className="text-sm">Tasdiqlangan</span></label>
        </Field>
        <Field label="seller_approved_at" span2><Input defaultValue={u.seller_approved_at || '—'} readOnly/></Field>
      </FormBlock>

      <FormBlock title="Manzil va lokatsiya" icon="map-pin">
        <Field label="Viloyat (autocomplete)" required>
          <Select defaultValue={u.region}>{J.regions.map(r => <option key={r}>{r}</option>)}</Select>
        </Field>
        <Field label="Tuman">
          <Select defaultValue={u.district}>
            {(J.districtsByRegion[u.region] || ['—']).map(d => <option key={d}>{d}</option>)}
          </Select>
        </Field>
        <Field label="Latitude"><Input defaultValue={u.latitude.toFixed(6)}/></Field>
        <Field label="Longitude"><Input defaultValue={u.longitude.toFixed(6)}/></Field>
        <Field span2>
          <Button variant="secondary" icon="map">Открыть на Яндекс.Картах</Button>
        </Field>
      </FormBlock>

      <div className="card">
        <div className="card-header">
          <div style={{display: 'flex', alignItems: 'center', gap: 10}}>
            <span style={{width: 24, height: 24, display: 'grid', placeItems: 'center', borderRadius: 6, background: 'var(--primary-soft)', color: 'var(--primary)'}}><Icon name="box" size={13}/></span>
            <h3>Партия tarixi</h3>
            <Badge variant="neutral">{u.batches_count}</Badge>
          </div>
          <Button size="sm" variant="success" icon="download">Barcha promo Excel eksport</Button>
        </div>
        <div className="table-wrap">
          <table className="table inline-table">
            <thead>
              <tr><th>Партия nomi</th><th>Jami</th><th>Ishlatilgan</th><th>Sana</th><th style={{textAlign: 'right'}}>ZIP</th></tr>
            </thead>
            <tbody>
              {J.batches.filter(b => b.seller_id === u.id).slice(0, 5).map(b => (
                <tr key={b.id}>
                  <td><span className="text-mono">{b.name}</span></td>
                  <td className="num">{b.quantity}</td>
                  <td className="num">{b.scanned} <span className="text-dim">({b.activation_pct.toFixed(1)}%)</span></td>
                  <td className="text-mono text-xs text-muted">{b.created_at}</td>
                  <td style={{textAlign: 'right'}}>
                    <Button size="sm" variant="ghost" icon="download">ZIP</Button>
                  </td>
                </tr>
              ))}
              {J.batches.filter(b => b.seller_id === u.id).length === 0 && (
                <tr><td colSpan={5}><div className="empty" style={{padding: 24}}><div className="empty-icon"><Icon name="box" size={18}/></div><h4>Партия yo'q</h4><div>Hali bu sotuvchi uchun partiya yaratilmagan</div></div></td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <div style={{display: 'flex', alignItems: 'center', gap: 10}}>
            <span style={{width: 24, height: 24, display: 'grid', placeItems: 'center', borderRadius: 6, background: 'var(--success-soft)', color: 'var(--success)'}}><Icon name="bar-chart" size={13}/></span>
            <h3>Statistika</h3>
          </div>
        </div>
        <div style={{padding: 20, display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16}}>
          {[
            { label: 'Ro\'yxatdan o\'tgan', value: u.created_at, icon: 'calendar' },
            { label: 'Tasdiqlangan', value: u.seller_approved_at || '—', icon: 'check' },
            { label: 'Партия soni', value: u.batches_count, icon: 'box' },
            { label: 'Jami QR', value: u.total_qr, icon: 'qrcode' },
            { label: 'Skanlanganlar', value: u.scanned_qr, icon: 'sparkles' },
            { label: 'Aktivatsiya', value: ((u.scanned_qr / u.total_qr) * 100).toFixed(1) + '%', icon: 'trending-up' },
            { label: 'Joriy ballar', value: u.points.toLocaleString('ru'), icon: 'coin' },
            { label: 'Sovg\'a so\'rovlari', value: 0, icon: 'gift' },
          ].map((s, i) => (
            <div key={i} style={{padding: 12, background: 'var(--surface-2)', borderRadius: 8, border: '1px solid var(--border)'}}>
              <div style={{display:'flex', alignItems:'center', gap: 6, color: 'var(--text-muted)', fontSize: 11.5, marginBottom: 4}}>
                <Icon name={s.icon} size={12}/> {s.label}
              </div>
              <div style={{fontSize: 16, color: 'var(--text-strong)', fontWeight: 600, fontVariantNumeric: 'tabular-nums'}}>{s.value}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="form-footer">
        <span className="text-muted text-sm">Изменения не сохранены</span>
        <div style={{display: 'flex', gap: 8}}>
          <Button variant="ghost">Сохранить и добавить другой</Button>
          <Button variant="secondary">Сохранить и продолжить</Button>
          <Button variant="primary" icon="check">Сохранить</Button>
        </div>
      </div>
    </div>
  );
}

// ============================================================
// 2d. SEND REGION MESSAGE
// ============================================================
function SendRegionMessagePage() {
  return (
    <div className="page">
      <div className="gradient-banner">
        <h2><Icon name="send" size={20}/> &nbsp;Отправить сообщение по области</h2>
        <p>Выберите область Узбекистана и отправьте сообщение всем пользователям этого региона. Поддерживается фото, отложенная отправка и тестовый запуск.</p>
        <div className="banner-badge"><Icon name="map-pin" size={11}/> &nbsp;14 областей + Все регионы</div>
      </div>

      <div style={{display: 'grid', gridTemplateColumns: '1fr 320px', gap: 20, alignItems: 'start'}}>
        <div style={{display: 'flex', flexDirection: 'column', gap: 16}}>
          <FormBlock title="Параметры рассылки" icon="settings">
            <Field label="🗺️ Область" required>
              <Select>
                <option>— Выберите область —</option>
                <option>Все регионы</option>
                {J.regions.map(r => <option key={r}>{r}</option>)}
              </Select>
            </Field>
            <Field label="👥 Тип пользователя">
              <Select><option>Все</option><option>Сантехники</option><option>Продавцы</option></Select>
            </Field>
            <Field label="🌐 Язык пользователя">
              <Select><option>Все языки</option><option>🇺🇿 O'zbek</option><option>🇷🇺 Русский</option></Select>
            </Field>
            <Field label="🕐 Отложенная отправка" hint="Время в часовом поясе сервера (Asia/Tashkent)">
              <Input type="datetime-local"/>
            </Field>
          </FormBlock>

          <FormBlock title="Содержимое" icon="message-square" single>
            <Field label="💬 Текст сообщения" required hint="Используйте кнопки для форматирования: жирный, курсив, ссылка...">
              <Textarea rows={8} placeholder="Здравствуйте! Сообщаем о новой акции..." />
              <div style={{display: 'flex', gap: 4, marginTop: 6}}>
                {['B','I','U','S','🔗'].map(t => (
                  <button key={t} className="btn btn-secondary btn-sm" style={{minWidth: 28, padding: 0}}>{t}</button>
                ))}
              </div>
            </Field>
            <Field label="🖼️ Фото (опционально)" hint="Загрузите изображение — текст будет отправлен как подпись">
              <div style={{
                border: '1.5px dashed var(--border-strong)', borderRadius: 8,
                padding: 24, textAlign: 'center', cursor: 'pointer',
                background: 'var(--surface-2)', color: 'var(--text-muted)',
              }}>
                <Icon name="image" size={20}/>
                <div style={{marginTop: 6, fontSize: 12.5}}>Tashlang yoki <span style={{color: 'var(--primary)'}}>tanlang</span></div>
              </div>
            </Field>
          </FormBlock>

          <FormBlock title="Тестовая отправка" icon="zap" single>
            <Field label="👤 Test юбориш" hint="Отправит сообщение только этому пользователю для проверки">
              <div style={{display: 'flex', gap: 8}}>
                <div className="input-group" style={{flex: 1}}>
                  <span className="prefix"><Icon name="search" size={14}/></span>
                  <input className="input" placeholder="Поиск пользователя..."/>
                </div>
                <Button variant="secondary" icon="send">Тест</Button>
              </div>
            </Field>
          </FormBlock>

          <div className="form-footer">
            <span className="text-muted text-sm">Будет отправлено в ~23 пользователей</span>
            <div style={{display: 'flex', gap: 8}}>
              <Button variant="secondary">Отмена</Button>
              <Button variant="primary" icon="send">Отправить</Button>
            </div>
          </div>
        </div>

        <div style={{display: 'flex', flexDirection: 'column', gap: 16, position: 'sticky', top: 80}}>
          <div className="card">
            <div className="card-header"><h3>Предварительный просмотр</h3></div>
            <div style={{padding: 16, background: 'var(--surface-2)'}}>
              <div style={{
                background: 'linear-gradient(135deg, #1a1f2b, #11151e)',
                borderRadius: 10, padding: 12, border: '1px solid var(--border)',
                maxWidth: '100%',
              }}>
                <div style={{display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8}}>
                  <Avatar name="JIP GROUP" size={28}/>
                  <div>
                    <div style={{fontSize: 12, color: 'var(--text-strong)', fontWeight: 500}}>JIP GROUP Bot</div>
                    <div style={{fontSize: 10.5, color: 'var(--text-dim)'}}>через бота</div>
                  </div>
                </div>
                <div style={{
                  background: 'rgba(99,102,241,0.12)', padding: 10,
                  borderRadius: 8, fontSize: 12.5, color: 'var(--text)',
                  borderTopLeftRadius: 2,
                }}>
                  Здравствуйте! Сообщаем о новой акции — посетите ближайший магазин JIP и получите скидку 15%.
                </div>
                <div style={{fontSize: 10, color: 'var(--text-dim)', marginTop: 4, textAlign: 'right'}}>14:32</div>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="card-header"><h3>История рассылок</h3></div>
            <div>
              {J.regionMessages.slice(0, 4).map(m => (
                <div key={m.id} style={{padding: '10px 16px', borderBottom: '1px solid var(--border)', fontSize: 12.5}}>
                  <div style={{display:'flex', justifyContent: 'space-between', alignItems:'center'}}>
                    <span className="text-strong">{m.region}</span>
                    {m.status === 'done' && <Badge variant="success" size="sm" icon="check">Done</Badge>}
                    {m.status === 'pending' && <Badge variant="warning" size="sm" icon="clock">Pending</Badge>}
                    {m.status === 'error' && <Badge variant="danger" size="sm" icon="x">Error</Badge>}
                  </div>
                  <div className="text-dim text-xs text-mono" style={{marginTop: 2}}>{m.date} · {m.sent}/{m.total}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ============================================================
// 2c. SEND SINGLE/BULK MESSAGE
// ============================================================
function SendSingleMessagePage() {
  const recipients = J.users.slice(0, 1);
  return (
    <div className="page">
      <div className="gradient-banner">
        <h2><Icon name="message-square" size={20}/> &nbsp;Отправить сообщение пользователю</h2>
        <p>Личное сообщение через бота. Поддерживается HTML и Markdown форматирование.</p>
        <div className="banner-badge"><Icon name="users" size={11}/> &nbsp;Выбрано пользователей: {recipients.length}</div>
      </div>

      <div style={{display: 'grid', gridTemplateColumns: '1fr 360px', gap: 20, alignItems: 'start'}}>
        <FormBlock title="Сообщение" icon="message-square" single>
          <Field label="💬 Текст сообщения" required>
            <Textarea rows={10} placeholder="Здравствуйте! Хотим сообщить..."/>
          </Field>
          <Field label="Режим парсинга">
            <Select>
              <option>Без форматирования</option>
              <option>HTML</option>
              <option>Markdown</option>
            </Select>
          </Field>
          <div className="form-footer" style={{marginTop: 16, position: 'static'}}>
            <Button variant="secondary">Отмена</Button>
            <Button variant="primary" icon="send">Отправить</Button>
          </div>
        </FormBlock>

        <div className="card">
          <div className="card-header"><h3>Список пользователей</h3><Badge variant="neutral">{recipients.length}</Badge></div>
          <div>
            {recipients.map(u => (
              <div key={u.id} style={{padding: '12px 16px', borderBottom: '1px solid var(--border)'}}>
                <div className="user-cell">
                  <Avatar name={u.first_name + ' ' + u.last_name}/>
                  <div>
                    <div className="user-name">{u.first_name} {u.last_name} <span className="text-muted text-xs">@{u.username}</span></div>
                    <div className="user-meta">ID: {u.id} · {u.phone}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// ============================================================
// 32. AUTH USERS (Django standard)
// ============================================================
function AuthUsersPage({ onNavigate }) {
  return (
    <div className="page">
      <PageHeader title="Admin foydalanuvchilar" subtitle="Django auth — admin paneliga kira oladigan foydalanuvchilar"
        actions={<Button variant="primary" icon="plus">Foydalanuvchi qo'shish</Button>}/>
      <div className="card">
        <div className="filter-bar">
          <SearchBar placeholder="Поиск username, email..."/>
          <div style={{flex: 1}}/>
          <FilterChip icon="shield">Roli</FilterChip>
          <FilterChip icon="check">Faolligi</FilterChip>
        </div>
        <div className="table-wrap">
          <table className="table">
            <thead>
              <tr>
                <th className="col-checkbox"><input className="checkbox" type="checkbox"/></th>
                <th>Username</th>
                <th>Ism</th>
                <th>Email</th>
                <th>Roli</th>
                <th>Active</th>
                <th>Так last login</th>
              </tr>
            </thead>
            <tbody>
              {J.authUsers.map(u => (
                <tr key={u.id}>
                  <td className="col-checkbox"><input className="checkbox" type="checkbox"/></td>
                  <td>
                    <div className="user-cell">
                      <Avatar name={u.name}/>
                      <div>
                        <div className="user-name">{u.username}</div>
                        <div className="user-meta">#{u.id}</div>
                      </div>
                    </div>
                  </td>
                  <td>{u.name}</td>
                  <td className="text-mono text-sm text-muted">{u.email}</td>
                  <td>
                    {u.is_superuser ? <Badge variant="danger" icon="shield">Superuser</Badge> :
                     <Badge variant="info" icon="user">Staff</Badge>}
                  </td>
                  <td>{u.is_staff ? <StatusBadges.active/> : <StatusBadges.inactive/>}</td>
                  <td><span className="text-mono text-xs text-muted">{u.last_login}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <Pagination total={4} page={1} perPage={25}/>
      </div>
    </div>
  );
}

// ============================================================
// 33. AUTH GROUPS
// ============================================================
function AuthGroupsPage() {
  return (
    <div className="page">
      <PageHeader title="Guruhlar" subtitle="Foydalanuvchilar guruhlari va ruxsatlari"
        actions={<Button variant="primary" icon="plus">Guruh qo'shish</Button>}/>
      <div className="card">
        <div className="table-wrap">
          <table className="table">
            <thead>
              <tr><th className="col-checkbox"><input className="checkbox" type="checkbox"/></th><th>Guruh nomi</th><th>Foydalanuvchilar</th><th>Ruxsatlar</th><th></th></tr>
            </thead>
            <tbody>
              {J.authGroups.map(g => (
                <tr key={g.id}>
                  <td className="col-checkbox"><input className="checkbox" type="checkbox"/></td>
                  <td>
                    <div style={{display:'flex', alignItems:'center', gap: 10}}>
                      <span style={{width: 28, height: 28, borderRadius: 6, background: 'var(--primary-soft)', color:'var(--primary)', display: 'grid', placeItems: 'center'}}>
                        <Icon name="shield" size={14}/>
                      </span>
                      <span className="text-strong" style={{fontWeight: 500}}>{g.name}</span>
                    </div>
                  </td>
                  <td><Badge variant="neutral">{g.users_count} ta</Badge></td>
                  <td className="text-muted">{g.permissions}</td>
                  <td style={{textAlign: 'right'}}><Button size="sm" variant="ghost" icon="edit">O'zgartirish</Button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

Object.assign(window, {
  DashboardPage, AnalyticsPage, UsersListPage,
  UserSantenikPage, UserSotuvchiPage,
  SendRegionMessagePage, SendSingleMessagePage,
  AuthUsersPage, AuthGroupsPage,
});
