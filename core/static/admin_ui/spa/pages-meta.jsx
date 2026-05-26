// Meta/system pages: activity log, livestreams, region log, videos,
// monthly settings, monthly log, admin contacts, privacy policy

const JM = window.JIP;

// ============================================================
// 20. ACTIVITY LOG
// ============================================================
function ActivityLogPage() {
  const actionBadge = (a) => {
    const map = {
      create: { variant: 'success', icon: 'plus', label: 'Yaratildi' },
      update: { variant: 'info', icon: 'edit', label: "O'zgartirildi" },
      delete: { variant: 'danger', icon: 'trash', label: "O'chirildi" },
    };
    const m = map[a.code] || map.update;
    return <Badge variant={m.variant} icon={m.icon}>{m.label}</Badge>;
  };
  return (
    <div className="page">
      <PageHeader
        title="Faollik tarixi"
        subtitle="Tizimda sodir bo'lgan barcha o'zgarishlar audit logi"
        actions={<Button variant="secondary" icon="download">Eksport</Button>}
      />
      <div className="card">
        <DateHierarchy items={['2026', 'Май', '24', '25', '26']} active={4}/>
        <div className="filter-bar">
          <SearchBar placeholder="Kim, qaysi obyekt..."/>
          <div style={{flex:1}}/>
          <FilterChip icon="user">Kim</FilterChip>
          <FilterChip icon="sparkles">Amal</FilterChip>
          <FilterChip icon="box">Obyekt turi</FilterChip>
          <FilterChip icon="calendar">Sana</FilterChip>
        </div>
        <div className="table-wrap">
          <table className="table">
            <thead>
              <tr>
                <th className="col-checkbox"><input className="checkbox" type="checkbox"/></th>
                <th>Vaqt</th>
                <th>Kim</th>
                <th>Amal</th>
                <th>Obyekt</th>
                <th>Tavsif</th>
                <th>IP</th>
              </tr>
            </thead>
            <tbody>
              {JM.log.map(l => (
                <tr key={l.id}>
                  <td className="col-checkbox"><input className="checkbox" type="checkbox"/></td>
                  <td><span className="text-mono text-xs text-muted">{l.timestamp}</span></td>
                  <td>
                    <div className="user-cell">
                      <Avatar name={l.who} size={24}/>
                      <span className="text-mono text-sm" style={{color: 'var(--text-strong)', fontWeight: 500}}>{l.who}</span>
                    </div>
                  </td>
                  <td>{actionBadge(l.action)}</td>
                  <td>
                    <div style={{display:'flex', flexDirection:'column', gap: 2}}>
                      <span style={{fontSize: 12.5, color: 'var(--text-strong)', fontWeight: 500}}>{l.object_type}</span>
                      <span className="text-mono text-xs text-muted">{l.object_label}</span>
                    </div>
                  </td>
                  <td className="text-sm">{l.description}</td>
                  <td><span className="text-mono text-xs text-muted">{l.ip}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <Pagination total={264} page={1} perPage={40}/>
      </div>
    </div>
  );
}

// ============================================================
// 21. LIVESTREAMS LIST
// ============================================================
function LivestreamsPage({ onNavigate }) {
  const statusBadge = (s) => {
    if (s === 'scheduled') return <Badge variant="info" icon="clock">Rejalashtirilgan</Badge>;
    if (s === 'active') return <Badge variant="success" icon="radio">Faol</Badge>;
    if (s === 'completed') return <Badge variant="neutral" icon="check">Tugagan</Badge>;
    return <Badge>{s}</Badge>;
  };
  return (
    <div className="page">
      <PageHeader title="Jonli efirlar" subtitle="LiveStream sessiyalari va g'oliblar ro'yxati"
        actions={<Button variant="primary" icon="plus" onClick={() => onNavigate('/livestreams/add')}>Yangi efir</Button>}
      />

      <div className="kpi-grid">
        <KPI label="Jami efirlar" value="4" icon="radio" color="indigo"/>
        <KPI label="Tugagan" value="2" icon="check" color="emerald"/>
        <KPI label="Faol" value="1" icon="zap" color="amber"/>
        <KPI label="Rejalashtirilgan" value="1" icon="clock" color="blue"/>
      </div>

      <div className="card">
        <div className="filter-bar">
          <SearchBar placeholder="Sarlavha bo'yicha..."/>
          <div style={{flex:1}}/>
          <FilterChip icon="check">Holat</FilterChip>
        </div>
        <div className="table-wrap">
          <table className="table">
            <thead><tr><th>Sarlavha</th><th>Holat</th><th>Boshlanish vaqti</th><th style={{textAlign:'right'}}>G'oliblar soni</th><th></th></tr></thead>
            <tbody>
              {JM.livestreams.map(ls => (
                <tr key={ls.id}>
                  <td>
                    <div style={{display:'flex', alignItems:'center', gap: 10}}>
                      <span style={{width: 32, height: 32, borderRadius: 6, background: 'var(--danger-soft)', color: 'var(--danger)', display: 'grid', placeItems: 'center'}}>
                        <Icon name="radio" size={14}/>
                      </span>
                      <span className="text-strong" style={{fontWeight: 500}}>{ls.title}</span>
                    </div>
                  </td>
                  <td>{statusBadge(ls.status)}</td>
                  <td><span className="text-mono text-sm text-muted">{ls.start_at}</span></td>
                  <td className="num" style={{textAlign:'right'}}>{ls.winners_count}</td>
                  <td style={{textAlign:'right'}}><Button size="sm" variant="ghost" icon="edit">Tahrirlash</Button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

// ============================================================
// 22. LIVESTREAM ADD
// ============================================================
function LivestreamAddPage() {
  return (
    <div className="page">
      <PageHeader title="Yangi jonli efir" subtitle="LiveStream sessiyasini rejalashtirish"/>
      <FormBlock title="Asosiy ma'lumotlar" icon="radio">
        <Field label="Sarlavha" required span2><Input placeholder="Yangi mahsulot taqdimoti"/></Field>
        <Field label="Tavsif (HTML)" span2><Textarea rows={5} placeholder="<p>Iyun oyida bo'lib o'tadigan...</p>"/></Field>
        <Field label="Boshlanish vaqti" required><Input type="datetime-local"/></Field>
        <Field label="G'oliblar soni"><Input type="number" defaultValue={5} min={1}/></Field>
        <Field label="Faollik" span2>
          <label style={{display:'flex', alignItems:'center', gap: 8}}><input type="checkbox" className="checkbox" defaultChecked/> <span className="text-sm">Faol</span></label>
        </Field>
      </FormBlock>

      <div className="card">
        <div className="card-header">
          <h3>G'oliblar ro'yxati (inline)</h3>
          <Button size="sm" variant="secondary" icon="plus">Qo'shish</Button>
        </div>
        <div className="table-wrap">
          <table className="table inline-table">
            <thead><tr><th>O'rin</th><th>Foydalanuvchi</th><th>Sovg'a</th><th></th></tr></thead>
            <tbody>
              {[1,2,3].map(i => (
                <tr key={i}>
                  <td><Badge variant={i === 1 ? 'warning' : 'neutral'} outline>{i}-o'rin</Badge></td>
                  <td><Select><option>— Tanlang —</option>{JM.users.slice(0, 6).map(u => <option key={u.id}>{u.first_name} {u.last_name}</option>)}</Select></td>
                  <td><Select><option>— Tanlang —</option>{JM.gifts.slice(0, 4).map(g => <option key={g.id}>{g.name_ru}</option>)}</Select></td>
                  <td style={{textAlign:'right'}}><Button size="sm" variant="ghost" icon="x"/></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="form-footer">
        <span className="text-muted text-sm">Yangi yozuv</span>
        <div style={{display:'flex', gap: 8}}>
          <Button variant="secondary">Bekor qilish</Button>
          <Button variant="primary" icon="check">Saqlash</Button>
        </div>
      </div>
    </div>
  );
}

// ============================================================
// 23. REGION LOG
// ============================================================
function RegionLogPage() {
  const statusBadge = (s) => {
    const map = {
      pending: { v:'warning', i:'clock', l:'Kutilmoqda' },
      sending: { v:'info', i:'send', l:'Yuborilmoqda' },
      done: { v:'success', i:'check', l:'Bajarildi' },
      error: { v:'danger', i:'x', l:'Xato' },
    };
    const m = map[s] || map.pending;
    return <Badge variant={m.v} icon={m.i}>{m.l}</Badge>;
  };
  return (
    <div className="page">
      <PageHeader title="Viloyat xabarlari logi" subtitle="Viloyatlar bo'yicha yuborilgan ommaviy xabarlar tarixi"/>

      <div className="card">
        <div className="filter-bar">
          <SearchBar placeholder="Viloyat yoki yuboruvchi..."/>
          <div style={{flex:1}}/>
          <FilterChip icon="check">Holat</FilterChip>
          <FilterChip icon="calendar">Sana</FilterChip>
        </div>
        <div className="table-wrap">
          <table className="table">
            <thead>
              <tr><th>Sana</th><th>Viloyat</th><th style={{textAlign:'right'}}>Jami</th><th style={{textAlign:'right'}}>Yuborildi</th><th style={{textAlign:'right'}}>Xato</th><th>Holat</th><th>Kim yubordi</th></tr>
            </thead>
            <tbody>
              {JM.regionMessages.map(m => (
                <tr key={m.id}>
                  <td><span className="text-mono text-xs text-muted">{m.date}</span></td>
                  <td><Badge variant="info" icon="map-pin">{m.region}</Badge></td>
                  <td className="num" style={{textAlign:'right'}}>{m.total}</td>
                  <td className="num" style={{textAlign:'right', color: 'var(--success-fg)'}}>{m.sent}</td>
                  <td className="num" style={{textAlign:'right', color: m.errors > 0 ? 'var(--danger-fg)' : 'var(--text-dim)'}}>{m.errors}</td>
                  <td>{statusBadge(m.status)}</td>
                  <td><span className="text-mono text-sm text-muted">{m.who}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

// ============================================================
// 24. VIDEOS LIST
// ============================================================
function VideosPage({ onNavigate }) {
  return (
    <div className="page">
      <PageHeader title="Video ko'rsatmalar" subtitle="Foydalanuvchilar uchun video instruktsiyalar"
        actions={<Button variant="primary" icon="plus" onClick={() => onNavigate('/videos/add')}>Yangi video</Button>}/>

      <div className="card">
        <div className="filter-bar">
          <SearchBar placeholder="Sarlavha..."/>
          <div style={{flex:1}}/>
          <FilterChip icon="users">Tur (santenik/sotuvchi)</FilterChip>
          <FilterChip icon="check">Faolligi</FilterChip>
        </div>
        <div className="table-wrap">
          <table className="table">
            <thead>
              <tr><th>Video</th><th>Tur</th><th style={{textAlign:'right'}}>Tartib</th><th>Faollik</th><th></th></tr>
            </thead>
            <tbody>
              {JM.videos.map(v => (
                <tr key={v.id}>
                  <td>
                    <div style={{display:'flex', alignItems:'center', gap: 10}}>
                      <span style={{width: 48, height: 32, borderRadius: 6, background: '#000', display: 'grid', placeItems: 'center', color: 'white'}}>
                        <Icon name="play" size={14}/>
                      </span>
                      <div>
                        <div className="text-strong" style={{fontWeight: 500}}>{v.title}</div>
                        <div className="text-xs text-muted text-mono">{v.url}</div>
                      </div>
                    </div>
                  </td>
                  <td>{v.type === 'santenik' ? <Badge variant="warning" icon="wrench">Santenik</Badge> : <Badge variant="info" icon="store">Sotuvchi</Badge>}</td>
                  <td className="num" style={{textAlign:'right'}}>{v.order}</td>
                  <td>{v.is_active ? <StatusBadges.active/> : <StatusBadges.inactive/>}</td>
                  <td style={{textAlign:'right'}}>
                    <Button size="sm" variant="ghost" icon="edit"/>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

// ============================================================
// 25. VIDEO ADD
// ============================================================
function VideoAddPage() {
  return (
    <div className="page">
      <PageHeader title="Yangi video qo'shish"/>
      <FormBlock title="Video ma'lumotlari" icon="video">
        <Field label="Sarlavha (UZ)" required><Input placeholder="QR kod skanlash"/></Field>
        <Field label="Sarlavha (RU)" required><Input placeholder="Сканирование QR-кода"/></Field>
        <Field label="Video URL (YouTube)" required span2 hint="Faqat YouTube URL formatida">
          <div className="input-group">
            <span className="prefix"><Icon name="video" size={14}/></span>
            <input className="input" placeholder="https://youtu.be/abc123"/>
          </div>
        </Field>
        <Field label="Tartib raqami"><Input type="number" defaultValue={1} min={1}/></Field>
        <Field label="Tur" required>
          <Select>
            <option value="santenik">Santenik uchun</option>
            <option value="sotuvchi">Sotuvchi uchun</option>
          </Select>
        </Field>
        <Field label="Faollik" span2>
          <label style={{display:'flex', alignItems:'center', gap: 8}}><input type="checkbox" className="checkbox" defaultChecked/> <span className="text-sm">Botda ko'rsatilsin</span></label>
        </Field>
      </FormBlock>
      <div className="form-footer">
        <Button variant="secondary">Bekor qilish</Button>
        <Button variant="primary" icon="check">Saqlash</Button>
      </div>
    </div>
  );
}

// ============================================================
// 26. MONTHLY REMINDER SETTINGS
// ============================================================
function MonthlySettingsPage() {
  const [on, setOn] = useState(true);
  return (
    <div className="page">
      <PageHeader title="Oylik eslatma sozlamalari" subtitle="Har oyning birinchi sanasida sotuvchilarga avtomatik xabar yuboriladi"/>

      <FormBlock title="Avtomatik eslatma" icon="bell" badge={on ? <Badge variant="success" dot>YOQILGAN</Badge> : <Badge variant="neutral" dot>O'CHIRILGAN</Badge>}>
        <div className="span-2" style={{
          padding: 16, background: on ? 'var(--success-soft)' : 'var(--surface-2)',
          borderRadius: 8, display: 'flex', alignItems: 'center', gap: 14,
          border: '1px solid ' + (on ? 'rgba(16, 185, 129, 0.3)' : 'var(--border)'),
        }}>
          <Toggle on={on} onChange={setOn}/>
          <div style={{flex: 1}}>
            <div style={{color: 'var(--text-strong)', fontWeight: 500, fontSize: 13.5}}>{on ? 'Avtomatik eslatma yoqilgan' : 'Avtomatik eslatma o\'chirilgan'}</div>
            <div className="text-xs text-muted" style={{marginTop: 2}}>
              {on ? 'Har oyning 1-sanasida belgilangan vaqtda bot xabar yuboradi' : 'Hech qanday avtomatik xabar yuborilmaydi'}
            </div>
          </div>
        </div>

        <Field label="🕐 Yuborish vaqti (HH:MM)" hint="Asia/Tashkent vaqti">
          <Input type="time" defaultValue="09:00"/>
        </Field>
        <Field label="Maksimal urinish">
          <Input type="number" defaultValue={3} min={1} max={10}/>
        </Field>

        <Field label="Xabar matni (UZ)" span2>
          <Textarea rows={4} defaultValue="Assalomu alaykum! Yangi oy boshlandi. Bu oyda JIP partnyorlar uchun maxsus aksiyalar bor — botga kirib batafsil ma'lumot oling."/>
        </Field>
        <Field label="Xabar matni (RU)" span2>
          <Textarea rows={4} defaultValue="Здравствуйте! Начался новый месяц. В этом месяце для партнёров JIP — специальные акции. Зайдите в бот за подробностями."/>
        </Field>
      </FormBlock>

      <div className="form-footer">
        <span className="text-muted text-sm">Sozlamalar avtomatik tatbiq etiladi</span>
        <Button variant="primary" icon="check">Sozlamalarni saqlash</Button>
      </div>
    </div>
  );
}

// ============================================================
// 27. MONTHLY REMINDER LOG
// ============================================================
function MonthlyLogPage() {
  return (
    <div className="page">
      <PageHeader title="Oylik eslatma logi" subtitle="Har oylik avtomatik eslatma jo'natilishlari tarixi"/>
      <div className="card">
        <div className="table-wrap">
          <table className="table">
            <thead><tr><th>Sana</th><th>Holat</th><th style={{textAlign:'right'}}>Yuborilganlar</th><th style={{textAlign:'right'}}>Xatolar</th><th>Vaqt</th></tr></thead>
            <tbody>
              {JM.reminderLogs.map(r => (
                <tr key={r.id}>
                  <td><span className="text-mono text-sm text-muted">{r.date}</span></td>
                  <td><Badge variant={r.status === 'done' ? 'success' : 'danger'} icon={r.status === 'done' ? 'check' : 'x'}>{r.status === 'done' ? 'Bajarildi' : 'Xato'}</Badge></td>
                  <td className="num" style={{textAlign:'right', color: 'var(--success-fg)'}}>{r.sent}</td>
                  <td className="num" style={{textAlign:'right', color: r.errors > 0 ? 'var(--danger-fg)' : 'var(--text-dim)'}}>{r.errors}</td>
                  <td><span className="text-mono text-xs text-muted">{r.duration}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

// ============================================================
// 28. ADMIN CONTACTS
// ============================================================
function AdminContactsPage() {
  const iconFor = (t) => t === 'Telegram' ? 'send' : t === 'Telefon' ? 'phone' : 'message-circle';
  return (
    <div className="page">
      <PageHeader title="Admin kontaktlari" subtitle="Botda «Yordam» bo'limida foydalanuvchilarga ko'rsatiladigan kontaktlar"
        actions={<Button variant="primary" icon="plus">Kontakt qo'shish</Button>}/>
      <div className="card">
        <div className="table-wrap">
          <table className="table">
            <thead><tr><th>Tur</th><th>Qiymat</th><th>Faollik</th><th></th></tr></thead>
            <tbody>
              {JM.adminContacts.map(c => (
                <tr key={c.id}>
                  <td>
                    <div style={{display:'flex', alignItems:'center', gap: 10}}>
                      <span style={{width: 32, height: 32, borderRadius: 6, background: 'var(--primary-soft)', color: 'var(--primary)', display: 'grid', placeItems: 'center'}}>
                        <Icon name={iconFor(c.type)} size={14}/>
                      </span>
                      <span className="text-strong" style={{fontWeight: 500}}>{c.type}</span>
                    </div>
                  </td>
                  <td><span className="text-mono">{c.value}</span></td>
                  <td>{c.is_active ? <StatusBadges.active/> : <StatusBadges.inactive/>}</td>
                  <td style={{textAlign:'right'}}>
                    <Button size="sm" variant="ghost" icon="edit"/>
                    <Button size="sm" variant="ghost" icon="trash"/>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

// ============================================================
// 29. PRIVACY POLICY
// ============================================================
function PrivacyPolicyPage() {
  return (
    <div className="page">
      <PageHeader title="Maxfiylik siyosati" subtitle="Botda foydalanuvchilarga ko'rsatiladigan privacy hujjat"
        actions={<Button variant="primary" icon="plus">Yangi hujjat</Button>}/>
      <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16}}>
        {JM.policies.map(p => (
          <div key={p.id} className="card">
            <div className="card-header">
              <div style={{display: 'flex', alignItems: 'center', gap: 10}}>
                <span style={{width: 32, height: 32, borderRadius: 6, background: 'var(--primary-soft)', color: 'var(--primary)', display: 'grid', placeItems: 'center'}}>
                  <Icon name="file-text" size={14}/>
                </span>
                <h3>{p.title_ru}</h3>
              </div>
              {p.is_active ? <StatusBadges.active/> : <StatusBadges.inactive/>}
            </div>
            <div style={{padding: 16}}>
              <div className="text-sm text-muted" style={{marginBottom: 4}}>UZ nomi</div>
              <div className="text-strong" style={{marginBottom: 12}}>{p.title_uz}</div>
              <div className="text-sm text-muted" style={{marginBottom: 4}}>Yaratilgan</div>
              <div className="text-mono text-sm" style={{marginBottom: 12}}>{p.created}</div>
              <div style={{display: 'flex', gap: 8, marginTop: 16}}>
                <Button size="sm" variant="secondary" icon="edit">Tahrirlash</Button>
                <Button size="sm" variant="ghost" icon="eye">Ko'rish</Button>
              </div>
            </div>
          </div>
        ))}
      </div>

      <FormBlock title="HTML editor" icon="code" single>
        <Field label="Sarlavha (UZ)"><Input defaultValue="Maxfiylik siyosati"/></Field>
        <Field label="Sarlavha (RU)"><Input defaultValue="Политика конфиденциальности"/></Field>
        <Field label="Matn (UZ) — HTML"><Textarea rows={8} defaultValue="<h2>Ma'lumotlarni yig'ish</h2>&#10;<p>JIP GROUP foydalanuvchilarning shaxsiy ma'lumotlarini...</p>"/></Field>
        <Field label="Matn (RU) — HTML"><Textarea rows={8} defaultValue="<h2>Сбор данных</h2>&#10;<p>JIP GROUP собирает следующие персональные данные пользователей...</p>"/></Field>
        <Field label="Faollik">
          <label style={{display:'flex', alignItems:'center', gap: 8}}><input type="checkbox" className="checkbox" defaultChecked/> <span className="text-sm">Faol</span></label>
        </Field>
      </FormBlock>
    </div>
  );
}

Object.assign(window, {
  ActivityLogPage, LivestreamsPage, LivestreamAddPage,
  RegionLogPage, VideosPage, VideoAddPage,
  MonthlySettingsPage, MonthlyLogPage,
  AdminContactsPage, PrivacyPolicyPage,
});
