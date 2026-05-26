// Gifts, Gift redemptions, Seller transactions, Seller registration codes

const JG = window.JIP;

// ============================================================
// 13. GIFTS LIST
// ============================================================
function GiftsPage({ onNavigate }) {
  return (
    <div className="page">
      <PageHeader
        title="Sovg'alar katalogi"
        subtitle="Foydalanuvchilar tomonidan so'rashi mumkin bo'lgan sovg'alar"
        actions={<>
          <Button variant="secondary" icon="archive">Arxivga</Button>
          <Button variant="primary" icon="plus" onClick={() => onNavigate('/gifts/add')}>Yangi sovg'a</Button>
        </>}
      />

      <div className="card">
        <div className="filter-bar">
          <SearchBar placeholder="Nom yoki tur bo'yicha..."/>
          <div style={{flex:1}}/>
          <FilterChip icon="layers">Tur</FilterChip>
          <FilterChip icon="check" active>Faol</FilterChip>
        </div>

        <div style={{padding: 16, display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: 12}}>
          {JG.gifts.map(g => (
            <div key={g.id} style={{
              background: 'var(--surface-2)', borderRadius: 12, padding: 16,
              border: '1px solid var(--border)', display: 'flex', flexDirection: 'column', gap: 10,
              cursor: 'pointer', transition: 'border 120ms',
            }}
            onMouseEnter={e => e.currentTarget.style.borderColor = 'var(--border-strong)'}
            onMouseLeave={e => e.currentTarget.style.borderColor = 'var(--border)'}>
              <div style={{
                aspectRatio: '16/10', borderRadius: 8,
                background: 'linear-gradient(135deg, rgba(99,102,241,0.18), rgba(139,92,246,0.18))',
                display: 'grid', placeItems: 'center', fontSize: 48,
              }}>{g.image}</div>
              <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 6}}>
                <div style={{minWidth: 0, flex: 1}}>
                  <div style={{fontSize: 14, fontWeight: 500, color: 'var(--text-strong)', overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap'}}>{g.name_ru}</div>
                  <div className="text-xs text-muted">{g.name_uz}</div>
                </div>
                {g.is_active ? <Badge variant="success" size="sm" dot>Faol</Badge> : <Badge variant="neutral" size="sm" dot>Arxiv</Badge>}
              </div>
              <div style={{display:'flex', alignItems:'center', justifyContent:'space-between', borderTop: '1px solid var(--border)', paddingTop: 10}}>
                <span style={{
                  display: 'flex', alignItems: 'center', gap: 4,
                  color: 'var(--primary)', fontFamily: 'var(--font-mono)', fontWeight: 600, fontSize: 14,
                }}><Icon name="coin" size={14}/> {g.price.toLocaleString('ru')}</span>
                <Badge variant="info" outline size="sm">{g.type}</Badge>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ============================================================
// 14. GIFT ADD
// ============================================================
function GiftAddPage() {
  return (
    <div className="page">
      <PageHeader title="Yangi sovg'a" subtitle="Katalogga yangi sovg'a qo'shish"/>
      <div style={{display: 'grid', gridTemplateColumns: '1fr 320px', gap: 16, alignItems: 'start'}}>
        <FormBlock title="Sovg'a ma'lumotlari" icon="gift">
          <Field label="Nomi (UZ)" required><Input placeholder="AirPods 3-pokoleniya"/></Field>
          <Field label="Nomi (RU)" required><Input placeholder="AirPods 3-го поколения"/></Field>
          <Field label="Tavsif (UZ)" span2><Textarea rows={3} placeholder="Apple AirPods 3-pokoleniya. Active Noise Cancellation..."/></Field>
          <Field label="Tavsif (RU)" span2><Textarea rows={3} placeholder="Apple AirPods 3-го поколения. Активное шумоподавление..."/></Field>
          <Field label="Ball narxi" required hint="50 000 ball ~ $50">
            <Input type="number" defaultValue={50000} step={1000}/>
          </Field>
          <Field label="Tur">
            <Select>
              <option value="electronics">Elektronika</option>
              <option value="clothing">Kiyim</option>
              <option value="experience">Tajriba</option>
              <option value="cash">Naqd pul</option>
            </Select>
          </Field>
          <Field label="Faollik" span2>
            <label style={{display:'flex', alignItems:'center', gap: 8}}>
              <input type="checkbox" className="checkbox" defaultChecked/>
              <span className="text-sm">Sovg'a katalogda ko'rinadi</span>
            </label>
          </Field>
        </FormBlock>

        <div className="card">
          <div className="card-header"><h3>Tasvir</h3></div>
          <div style={{padding: 20}}>
            <div style={{
              aspectRatio: '1', border: '1.5px dashed var(--border-strong)',
              borderRadius: 12, display: 'grid', placeItems: 'center',
              color: 'var(--text-muted)', cursor: 'pointer', background: 'var(--surface-2)',
            }}>
              <div style={{textAlign: 'center'}}>
                <Icon name="image" size={32}/>
                <div className="text-sm" style={{marginTop: 6}}>Tashlang yoki <span style={{color:'var(--primary)'}}>tanlang</span></div>
                <div className="text-xs text-dim" style={{marginTop: 4}}>PNG, JPG, max 2MB</div>
              </div>
            </div>
          </div>
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
// 15. GIFT REDEMPTIONS LIST
// ============================================================
function RedemptionsPage({ onNavigate }) {
  const statusBadge = (s) => {
    if (s === 'pending') return <Badge variant="warning" icon="clock">Запрос принят</Badge>;
    if (s === 'confirmed') return <Badge variant="info" icon="check">Подтверждение получ.</Badge>;
    if (s === 'cancelled') return <Badge variant="danger" icon="x">Запрос отменён</Badge>;
    return <Badge variant="neutral">{s}</Badge>;
  };
  return (
    <div className="page">
      <PageHeader title="Sovg'a so'rovlari" subtitle="Foydalanuvchilar tomonidan so'ralgan sovg'alar"
        actions={<Button variant="secondary" icon="download">Eksport</Button>}/>

      <div className="card">
        <DateHierarchy items={['2026','Май','Все']} active={2}/>
        <div className="filter-bar">
          <SearchBar placeholder="Foydalanuvchi yoki sovg'a..."/>
          <div style={{flex:1}}/>
          <FilterChip icon="clock">Holat</FilterChip>
          <FilterChip icon="check">Tasdiqlash</FilterChip>
          <FilterChip icon="calendar">Sana</FilterChip>
        </div>

        <div className="table-wrap">
          <table className="table">
            <thead>
              <tr>
                <th>Zakaz</th><th>Foydalanuvchi</th><th>Telefon</th>
                <th>Регион</th><th>Sovg'a</th><th>Status</th><th>Tasdiqlash</th>
                <th>So'ralgan vaqt</th>
              </tr>
            </thead>
            <tbody>
              {JG.redemptions.map(r => (
                <tr key={r.id} onClick={() => onNavigate('/redemptions/edit')} style={{cursor:'pointer'}}>
                  <td><span className="code-mask">#{r.id}</span></td>
                  <td>
                    <div className="user-cell">
                      <Avatar name={r.user_name} size={28}/>
                      <div>
                        <div className="user-name" style={{fontSize: 12.5}}>{r.user_name}</div>
                        <div className="user-meta">ID: {r.user_id}</div>
                      </div>
                    </div>
                  </td>
                  <td><span className="text-mono text-sm">{r.phone}</span></td>
                  <td><Badge variant="info" icon="map-pin">{r.region.replace(' область', '').replace('Город ', '')}</Badge></td>
                  <td>
                    <div style={{display:'flex', alignItems:'center', gap: 8}}>
                      <span style={{
                        width: 28, height: 28, borderRadius: 6, display: 'grid', placeItems: 'center',
                        background: 'linear-gradient(135deg, rgba(99,102,241,0.18), rgba(139,92,246,0.18))', fontSize: 14,
                      }}>{JG.gifts.find(g => g.id === r.gift_id)?.image || '🎁'}</span>
                      <span className="text-strong" style={{fontSize: 12.5, fontWeight: 500}}>{r.gift_name}</span>
                    </div>
                  </td>
                  <td>{statusBadge(r.status)}</td>
                  <td>{r.is_confirmed ? <Badge variant="success" icon="check">Подтверждено</Badge> : <Badge variant="warning" icon="clock">Не подтверждено</Badge>}</td>
                  <td><span className="text-mono text-xs text-muted">{r.created_at}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <Pagination total={15} page={1} perPage={25}/>
      </div>
    </div>
  );
}

// ============================================================
// 16. REDEMPTION EDIT
// ============================================================
function RedemptionEditPage({ onNavigate }) {
  const r = JG.redemptions[0];
  const g = JG.gifts.find(x => x.id === r.gift_id);
  return (
    <div className="page">
      <PageHeader
        title={<span>Заявка <span className="code-mask">#{r.id}</span></span>}
        subtitle={<span>{r.user_name} · {r.created_at}</span>}
        actions={<>
          <Button variant="ghost" icon="history">История</Button>
          <Button variant="danger" icon="x">Отменить</Button>
          <Button variant="primary" icon="check">Сохранить</Button>
        </>}
      />

      <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16}}>
        <FormBlock title="Информация о запросе" icon="gift-redeem">
          <Field label="Участник" span2>
            <div className="input" style={{display:'flex', alignItems:'center', gap: 10}}>
              <Avatar name={r.user_name} size={26}/>
              <a style={{color: 'var(--primary)', cursor: 'pointer'}} onClick={() => onNavigate('/users/santenik')}>{r.user_name} · ID {r.user_id}</a>
            </div>
          </Field>
          <Field label="Sovg'a" span2>
            <div className="input" style={{display:'flex', alignItems:'center', gap: 10}}>
              <span style={{fontSize: 18}}>{g?.image}</span>
              <a style={{color: 'var(--primary)', cursor: 'pointer'}} onClick={() => onNavigate('/gifts')}>{r.gift_name}</a>
              <span className="text-mono" style={{marginLeft: 'auto', color: 'var(--primary)', fontWeight: 600}}>{g?.price.toLocaleString('ru')} ball</span>
            </div>
          </Field>
          <Field label="Регион"><Input defaultValue={r.region} readOnly/></Field>
          <Field label="Телефон"><Input defaultValue={r.phone} readOnly/></Field>
          <Field label="So'ralgan vaqt" span2><Input defaultValue={r.created_at} readOnly/></Field>
        </FormBlock>

        <FormBlock title="Обработка" icon="settings">
          <Field label="Holat" required span2>
            <Select defaultValue={r.status}>
              <option value="pending">🏆 Запрос принят к обработке</option>
              <option value="confirmed">✅ Подтверждение получения продукта</option>
              <option value="cancelled">❌ Запрос отменён</option>
            </Select>
          </Field>
          <Field label="is_confirmed" span2>
            <label style={{display:'flex', alignItems:'center', gap:8}}>
              <input type="checkbox" className="checkbox" defaultChecked={r.is_confirmed}/>
              <span className="text-sm">Foydalanuvchi sovg'ani oldi</span>
            </label>
          </Field>
          <Field label="Admin izoh" span2>
            <Textarea rows={5} placeholder="Sovg'a yetkazib berildi. Doimiy mijoz..."/>
          </Field>
        </FormBlock>
      </div>

      <div className="form-footer">
        <span className="text-muted text-sm">Sa'lash + Telegram xabari yuboriladi</span>
        <div style={{display:'flex', gap: 8}}>
          <Button variant="secondary">Bekor qilish</Button>
          <Button variant="primary" icon="check">Сохранить</Button>
        </div>
      </div>
    </div>
  );
}

// ============================================================
// 17. SELLER TRANSACTIONS
// ============================================================
function TransactionsPage({ onNavigate }) {
  const typeBadge = (t) => {
    if (t === 'sale_bonus') return <Badge variant="success" icon="trending-up">Sotuv bonusi</Badge>;
    if (t === 'admin_add') return <Badge variant="info" icon="plus">Admin qo'shdi</Badge>;
    if (t === 'correction') return <Badge variant="warning" icon="sliders">Tuzatish</Badge>;
    return <Badge>{t}</Badge>;
  };
  return (
    <div className="page">
      <PageHeader title="Sotuvchi tranzaksiyalari" subtitle="Sotuvchilar uchun ball harakatlari tarixi"
        actions={<>
          <Button variant="secondary" icon="download">Eksport</Button>
          <Button variant="primary" icon="plus" onClick={() => onNavigate('/transactions/add')}>Yangi</Button>
        </>}
      />

      <div className="kpi-grid">
        <KPI label="Jami tranzaksiyalar" value="1 117" icon="credit-card" color="indigo"/>
        <KPI label="Sotuv bonusi" value="893" icon="trending-up" color="emerald" hint="79.9%"/>
        <KPI label="Admin qo'shdi" value="178" icon="plus" color="blue" hint="15.9%"/>
        <KPI label="Tuzatish" value="46" icon="sliders" color="amber" hint="4.1%"/>
      </div>

      <div className="card">
        <div className="filter-bar">
          <SearchBar placeholder="Sotuvchi nomi..."/>
          <div style={{flex:1}}/>
          <FilterChip icon="users">Sotuvchi</FilterChip>
          <FilterChip icon="layers">Tur</FilterChip>
          <FilterChip icon="calendar">Sana</FilterChip>
        </div>
        <div className="table-wrap">
          <table className="table">
            <thead>
              <tr>
                <th>Vaqt</th><th>Sotuvchi</th><th>Tur</th>
                <th style={{textAlign:'right'}}>Ballar</th>
                <th style={{textAlign:'right'}}>Sotuv ($)</th>
                <th>Kim qo'shgan</th>
              </tr>
            </thead>
            <tbody>
              {JG.txns.map(t => (
                <tr key={t.id}>
                  <td><span className="text-mono text-xs text-muted">{t.created_at}</span></td>
                  <td>
                    <div className="user-cell">
                      <Avatar name={t.seller_name} size={26}/>
                      <span style={{fontSize: 12.5, color: 'var(--text-strong)', fontWeight: 500}}>{t.seller_name}</span>
                    </div>
                  </td>
                  <td>{typeBadge(t.type)}</td>
                  <td style={{textAlign:'right'}}>
                    <span className="text-mono" style={{
                      fontWeight: 600,
                      color: t.points >= 0 ? 'var(--success-fg)' : 'var(--danger-fg)',
                    }}>{t.points >= 0 ? '+' : ''}{t.points.toLocaleString('ru')}</span>
                  </td>
                  <td className="num" style={{textAlign:'right'}}>{t.sale_amount ? '$' + t.sale_amount : '—'}</td>
                  <td>
                    {t.added_by === 'Bot' ? <Badge variant="primary" icon="zap">Bot</Badge> :
                     <span className="text-mono text-sm text-muted">{t.added_by}</span>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <Pagination total={1117} page={1} perPage={25}/>
      </div>
    </div>
  );
}

// ============================================================
// 18. TRANSACTION ADD
// ============================================================
function TransactionAddPage() {
  return (
    <div className="page">
      <PageHeader title="Yangi tranzaksiya" subtitle="Sotuvchiga ball qo'shish yoki tuzatish"/>
      <FormBlock title="Tranzaksiya ma'lumotlari" icon="credit-card">
        <Field label="Sotuvchi" required span2>
          <Select>
            <option>— Sotuvchini tanlang —</option>
            {JG.users.filter(u => u.type === 'sotuvchi').map(u => (
              <option key={u.id}>{u.first_name} {u.last_name} (@{u.username}) · Joriy: {u.points.toLocaleString('ru')} ball</option>
            ))}
          </Select>
        </Field>
        <Field label="Tur" required>
          <Select>
            <option value="sale_bonus">Sotuv bonusi</option>
            <option value="admin_add">Admin qo'shdi</option>
            <option value="correction">Tuzatish</option>
          </Select>
        </Field>
        <Field label="Ballar" required hint="Manfiy raqam — kamaytirish">
          <Input type="number" placeholder="+1000"/>
        </Field>
        <Field label="Sotuv summasi ($)" hint="Sotuv bonusi uchun">
          <Input type="number" placeholder="50.00" step={0.01}/>
        </Field>
        <Field label="Izoh" span2><Textarea rows={3} placeholder="Iyul oyi premiyasi..."/></Field>
      </FormBlock>
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
// 19. SELLER REGISTRATION CODES
// ============================================================
function SellerCodesPage() {
  return (
    <div className="page">
      <PageHeader title="Sotuvchi ID lari" subtitle="Sotuvchilar uchun ro'yxatdan o'tish kodlari"
        actions={<>
          <Button variant="secondary" icon="download">Excel eksport</Button>
          <Button variant="primary" icon="sparkles">Yangi kodlar generatsiya</Button>
        </>}
      />

      <div className="kpi-grid">
        <KPI label="Jami kodlar" value="25" icon="id-card" color="indigo"/>
        <KPI label="Ishlatilgan" value="14" icon="check" color="emerald" hint="56%"/>
        <KPI label="Kutilmoqda" value="11" icon="clock" color="amber" hint="44%"/>
        <KPI label="Bu hafta yaratilgan" value="5" icon="sparkles" color="blue"/>
      </div>

      <div className="card">
        <div className="filter-bar">
          <SearchBar placeholder="Kod yoki label..."/>
          <div style={{flex:1}}/>
          <FilterChip icon="check">Ishlatilgan</FilterChip>
          <FilterChip icon="calendar">Yaratilgan sana</FilterChip>
        </div>
        <div className="table-wrap">
          <table className="table">
            <thead>
              <tr>
                <th className="col-checkbox"><input className="checkbox" type="checkbox"/></th>
                <th>Kod</th><th>Label</th><th>Egasi</th><th>Holat</th><th>Yaratilgan</th>
              </tr>
            </thead>
            <tbody>
              {JG.sellerCodes.map(c => (
                <tr key={c.id}>
                  <td className="col-checkbox"><input className="checkbox" type="checkbox"/></td>
                  <td><span className="code-mask">{c.code}</span></td>
                  <td>{c.label}</td>
                  <td>
                    {c.owner_name !== '—' ? (
                      <div className="user-cell">
                        <Avatar name={c.owner_name} size={24}/>
                        <span style={{fontSize: 12.5, fontWeight: 500, color: 'var(--text-strong)'}}>{c.owner_name}</span>
                      </div>
                    ) : <span className="text-dim text-sm">— hali ishlatilmagan —</span>}
                  </td>
                  <td>{c.is_used ? <StatusBadges.approved/> : <StatusBadges.pending/>}</td>
                  <td><span className="text-mono text-xs text-muted">{c.created_at}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <Pagination total={25} page={1} perPage={25}/>
      </div>
    </div>
  );
}

Object.assign(window, {
  GiftsPage, GiftAddPage,
  RedemptionsPage, RedemptionEditPage,
  TransactionsPage, TransactionAddPage,
  SellerCodesPage,
});
