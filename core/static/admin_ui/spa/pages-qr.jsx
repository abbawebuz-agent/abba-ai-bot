// QR codes, Batches, Stores pages

const JQ = window.JIP;

// ============================================================
// 8. QR CODES LIST
// ============================================================
function QRCodesPage({ onNavigate }) {
  const [filter, setFilter] = useState({ scanned: 'all' });
  const filtered = JQ.qrcodes.filter(q => {
    if (filter.scanned === 'scanned') return q.is_scanned;
    if (filter.scanned === 'unscanned') return !q.is_scanned;
    return true;
  });
  return (
    <div className="page">
      <PageHeader
        title="QR kodlar"
        subtitle="Barcha generatsiya qilingan QR kodlar va ularning ishlatilish holati"
        actions={<>
          <Select style={{width: 160}}><option>Май 2026</option><option>Апрель 2026</option><option>Март 2026</option></Select>
          <Button variant="success" icon="download">Эксport oylik (Excel)</Button>
          <Button variant="secondary" icon="download" disabled={filter.scanned !== 'scanned'}>Эксport tarix</Button>
          <Button variant="primary" icon="plus" onClick={() => onNavigate('/qrcodes/generate')}>Generatsiya</Button>
        </>}
      />

      <div className="kpi-grid">
        <KPI label="Jami QR kodlar" value="239" icon="qrcode" color="indigo" hint="Hammasi"/>
        <KPI label="Ishlatilgan" value="47" icon="check" color="emerald" hint="19.7% aktivatsiya"/>
        <KPI label="Kutilmoqda" value="192" icon="clock" color="amber" hint="Hali skanlanmagan"/>
        <KPI label="O'chirilgan" value="0" icon="trash" color="rose" hint="Tizimdan"/>
      </div>

      <div className="card">
        <div className="filter-bar">
          <SearchBar placeholder="Serial yoki kod bo'yicha qidirish..."/>
          <div style={{flex: 1}}/>
          <FilterChip icon="store">Магазин</FilterChip>
          <FilterChip icon="box">Партия</FilterChip>
          <FilterChip icon="check" active={filter.scanned !== 'all'} onClick={() => setFilter(f => ({...f, scanned: f.scanned === 'scanned' ? 'unscanned' : f.scanned === 'unscanned' ? 'all' : 'scanned'}))}>
            {filter.scanned === 'scanned' ? 'Использован' : filter.scanned === 'unscanned' ? 'Не использован' : 'Holat: Hammasi'}
          </FilterChip>
          <FilterChip icon="trash">Удалён</FilterChip>
        </div>

        <div className="table-wrap">
          <table className="table">
            <thead>
              <tr>
                <th className="col-checkbox"><input className="checkbox" type="checkbox"/></th>
                <th>QR-код</th>
                <th>Do'kon</th>
                <th>Партия</th>
                <th style={{textAlign: 'right'}}>Баллы</th>
                <th>Статус</th>
                <th>Пользователь</th>
                <th>Generated at</th>
              </tr>
            </thead>
            <tbody>
              {filtered.slice(0, 25).map(q => (
                <tr key={q.id} onClick={() => onNavigate('/qrcodes/edit')} style={{cursor: 'pointer'}}>
                  <td className="col-checkbox" onClick={e => e.stopPropagation()}><input className="checkbox" type="checkbox"/></td>
                  <td>
                    <div style={{display: 'flex', alignItems: 'center', gap: 10}}>
                      <span style={{
                        width: 32, height: 32, borderRadius: 6, background: 'var(--surface-2)',
                        border: '1px solid var(--border)', display: 'grid', placeItems: 'center',
                        color: q.is_scanned ? 'var(--success)' : 'var(--text-muted)',
                      }}><Icon name="qrcode" size={16}/></span>
                      <div>
                        <div style={{fontSize: 13, color: 'var(--text-strong)', fontWeight: 500}}>#{q.serial}</div>
                        <div><span className="code-mask">{q.is_scanned ? q.code : 'JIP*****E'}</span></div>
                      </div>
                    </div>
                  </td>
                  <td><Badge variant="info" icon="store">{q.store_name}</Badge></td>
                  <td><span className="text-mono text-xs">{q.batch_name}</span></td>
                  <td style={{textAlign: 'right'}}><span className="text-mono" style={{color: 'var(--primary)', fontWeight: 600}}>{q.points}</span></td>
                  <td>{q.is_scanned ? <StatusBadges.scanned/> : <StatusBadges.unscanned/>}</td>
                  <td>
                    {q.scanned_by_name ? (
                      <div className="user-cell">
                        <Avatar name={q.scanned_by_name} size={26}/>
                        <div><div className="user-name" style={{fontSize: 12.5}}>{q.scanned_by_name}</div><div className="user-meta">ID: {q.scanned_by_id}</div></div>
                      </div>
                    ) : <span className="text-dim text-sm">—</span>}
                  </td>
                  <td><span className="text-mono text-xs text-muted">{q.scanned_at || q.generated_at}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <Pagination total={239} page={1} perPage={25}/>
      </div>
    </div>
  );
}

// ============================================================
// 9. QR CODE EDIT
// ============================================================
function QRCodeEditPage({ onNavigate }) {
  const q = JQ.qrcodes.find(x => x.is_scanned) || JQ.qrcodes[0];
  const isScanned = q.is_scanned;
  return (
    <div className="page">
      <PageHeader
        title={<span>QR код #{q.serial}</span>}
        subtitle={<span>Партия: <span className="text-mono">{q.batch_name}</span> · Magazin: {q.store_name}</span>}
        actions={<>
          <Button variant="ghost" icon="history">История</Button>
          {isScanned && <Button variant="secondary" icon="zap" style={{color: 'var(--warning)', borderColor: 'var(--warning)'}}>⚠ Cancel Scans</Button>}
          <Button variant="primary" icon="check">Сохранить</Button>
        </>}
      />

      {!isScanned && (
        <div style={{
          background: 'var(--warning-soft)', border: '1px solid rgba(245, 158, 11, 0.3)',
          borderRadius: 12, padding: 16, display: 'flex', alignItems: 'flex-start', gap: 12,
        }}>
          <Icon name="lock" size={20} style={{color: 'var(--warning)', flexShrink: 0, marginTop: 2}}/>
          <div>
            <div style={{color: 'var(--warning-fg)', fontWeight: 600, marginBottom: 2}}>Информация о безопасности</div>
            <div style={{color: 'var(--text-muted)', fontSize: 13}}>
              Код QR-кода скрыт для безопасности до того как он будет отсканирован санитарным техником.
              Серийный номер: <span className="text-mono text-strong">{q.serial}</span>
            </div>
          </div>
        </div>
      )}

      <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16}}>
        <FormBlock title="QR код ma'lumotlari" icon="qrcode">
          <Field label="Serial number" required><Input defaultValue={q.serial} readOnly/></Field>
          <Field label="Code" hint={isScanned ? 'Visible — kod ishlatilgan' : 'Скрыт'}>
            <div className="input" style={{fontFamily: 'var(--font-mono)'}}>{isScanned ? q.code : 'JIP*****E'}</div>
          </Field>
          <Field label="Hash code" span2 hint={isScanned ? 'Salted SHA-256' : 'Скрыт'}>
            <div className="input" style={{fontFamily: 'var(--font-mono)', fontSize: 11.5}}>{isScanned ? q.hash_code : '••••••••••••'}</div>
          </Field>
          <Field label="Points"><Input defaultValue={q.points}/></Field>
          <Field label="Магазин">
            <Select defaultValue={q.store_name}>{JQ.stores.map(s => <option key={s.id}>{s.name}</option>)}</Select>
          </Field>
          <Field label="Партия">
            <Select defaultValue={q.batch_name}>{JQ.batches.map(b => <option key={b.id}>{b.name}</option>)}</Select>
          </Field>
          <Field label="is_deleted">
            <label style={{display: 'flex', alignItems: 'center', gap: 8}}><input type="checkbox" className="checkbox"/> <span className="text-sm">O'chirilgan</span></label>
          </Field>
        </FormBlock>

        <FormBlock title="Skanlash ma'lumotlari" icon="check" badge={isScanned ? <Badge variant="success" icon="check">Использован</Badge> : <Badge variant="warning" icon="clock">Не использован</Badge>}>
          <Field label="is_scanned">
            <label style={{display: 'flex', alignItems: 'center', gap: 8}}><input type="checkbox" className="checkbox" defaultChecked={isScanned}/> <span className="text-sm">Skanlangan</span></label>
          </Field>
          <Field label="Scanned at"><Input defaultValue={q.scanned_at || '—'} readOnly/></Field>
          <Field label="Scanned by" span2>
            {q.scanned_by_name ? (
              <div className="input" style={{display:'flex', alignItems:'center', gap: 10}}>
                <Avatar name={q.scanned_by_name} size={22}/>
                <a style={{color: 'var(--primary)', cursor: 'pointer'}} onClick={() => onNavigate('/users/santenik')}>{q.scanned_by_name} · ID {q.scanned_by_id}</a>
              </div>
            ) : <Input defaultValue="—" readOnly/>}
          </Field>
          <Field label="Generated at" span2><Input defaultValue={q.generated_at} readOnly/></Field>
        </FormBlock>
      </div>

      <div className="card">
        <div className="card-header">
          <h3>QR код urunishlari</h3>
          <Badge variant="neutral">3 ta</Badge>
        </div>
        <div className="table-wrap">
          <table className="table inline-table">
            <thead><tr><th>Attempted at</th><th>Raw code</th><th>Status</th><th>Source</th></tr></thead>
            <tbody>
              <tr><td className="text-mono text-xs text-muted">2026-05-25 14:32:18</td><td><span className="code-mask">jip{q.code.slice(3, 8).toLowerCase()}e</span></td><td><Badge variant="success" size="sm">success</Badge></td><td>Telegram bot</td></tr>
              <tr><td className="text-mono text-xs text-muted">2026-05-25 14:31:42</td><td><span className="code-mask">jip0000e</span></td><td><Badge variant="danger" size="sm">failed</Badge></td><td>Telegram bot</td></tr>
              <tr><td className="text-mono text-xs text-muted">2026-05-25 14:31:18</td><td><span className="code-mask">jipxxxxe</span></td><td><Badge variant="danger" size="sm">failed</Badge></td><td>Telegram bot</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

// ============================================================
// 35. QR GENERATE
// ============================================================
function QRGeneratePage() {
  return (
    <div className="page">
      <PageHeader title="QR generatsiya" subtitle="Bir tanlovda партия uchun barcha QR kodlarini avtomatik generatsiya qilish"/>
      <FormBlock title="Yangi QR partiyasini generatsiya qilish" icon="sparkles">
        <Field label="Partiya nomi" required>
          <Input placeholder="S27-MAY-2026"/>
        </Field>
        <Field label="Sotuvchi (autocomplete)" required>
          <Select>
            <option>— Tanlang —</option>
            {JQ.users.filter(u => u.type === 'sotuvchi').slice(0, 8).map(u => (
              <option key={u.id}>{u.first_name} {u.last_name} (@{u.username})</option>
            ))}
          </Select>
        </Field>
        <Field label="Magazin" required>
          <Select>{JQ.stores.map(s => <option key={s.id}>{s.name}</option>)}</Select>
        </Field>
        <Field label="Kartalar soni" required hint="Har karta 50 ball">
          <Input type="number" defaultValue={50} min={1} max={500}/>
        </Field>
        <Field label="Har karta uchun ball">
          <Input type="number" defaultValue={50}/>
        </Field>
        <Field label="Status">
          <Select><option>Faollashtirilmagan</option><option>Faollashtirilgan</option></Select>
        </Field>
        <div className="span-2" style={{
          padding: 16, background: 'var(--primary-soft)', borderRadius: 8, fontSize: 13,
          borderLeft: '3px solid var(--primary)', color: 'var(--text)',
        }}>
          <strong>50 × 50 = 2,500 ball</strong> sotuvchiga avtomatik qo'shiladi. Saqlangandan keyin QR kodlar generatsiya qilinadi va ZIP fayl yuklab olish uchun tayyor bo'ladi.
        </div>
      </FormBlock>
      <div className="form-footer">
        <span className="text-muted text-sm">Generatsiya 5-15 soniya davom etadi</span>
        <div style={{display: 'flex', gap: 8}}>
          <Button variant="secondary">Bekor qilish</Button>
          <Button variant="primary" icon="sparkles">Generatsiya qilish</Button>
        </div>
      </div>
    </div>
  );
}

// ============================================================
// 5. BATCHES LIST
// ============================================================
function BatchesPage({ onNavigate }) {
  const colorFor = pct => pct >= 50 ? 'success' : (pct >= 20 ? 'warning' : 'danger');
  return (
    <div className="page">
      <PageHeader
        title="Партии"
        subtitle="QR kodlar partiyalari — har biri 50-400 ta kartani o'z ichiga oladi"
        actions={<>
          <Button variant="secondary" icon="download">Eksport</Button>
          <Button variant="primary" icon="plus" onClick={() => onNavigate('/batches/add')}>Yangi партия</Button>
        </>}
      />

      <div className="card">
        <div className="filter-bar">
          <SearchBar placeholder="Партия nomi yoki sotuvchi..."/>
          <div style={{flex: 1}}/>
          <FilterChip icon="store">Магазин</FilterChip>
          <FilterChip icon="users">Sotuvchi</FilterChip>
          <FilterChip icon="check" active>Holat: Faol</FilterChip>
        </div>

        <div className="table-wrap">
          <table className="table">
            <thead>
              <tr>
                <th className="col-checkbox"><input className="checkbox" type="checkbox"/></th>
                <th>Партия nomi</th>
                <th>Sotuvchi</th>
                <th style={{textAlign: 'right'}}>Miqdor</th>
                <th style={{textAlign: 'right'}}>Ball/karta</th>
                <th>Aktivatsiya</th>
                <th style={{textAlign: 'right'}}>Skanlangan</th>
                <th>Holat</th>
                <th>Yetkazib berish</th>
              </tr>
            </thead>
            <tbody>
              {JQ.batches.map(b => (
                <tr key={b.id} onClick={() => onNavigate('/batches/edit')} style={{cursor: 'pointer'}}>
                  <td className="col-checkbox" onClick={e => e.stopPropagation()}><input className="checkbox" type="checkbox"/></td>
                  <td>
                    <div style={{display: 'flex', alignItems: 'center', gap: 10}}>
                      <span style={{width: 32, height: 32, borderRadius: 6, background: 'var(--primary-soft)', color: 'var(--primary)', display: 'grid', placeItems: 'center'}}><Icon name="box" size={14}/></span>
                      <div>
                        <div className="text-mono text-strong" style={{fontSize: 13, fontWeight: 500}}>{b.name}</div>
                        <div className="text-xs text-muted">{b.store_name}</div>
                      </div>
                    </div>
                  </td>
                  <td>
                    <div className="user-cell">
                      <Avatar name={b.seller_name} size={26}/>
                      <div>
                        <div className="user-name" style={{fontSize: 12.5}}>{b.seller_name}</div>
                        <div className="user-meta">ID: {b.seller_id}</div>
                      </div>
                    </div>
                  </td>
                  <td className="num" style={{textAlign: 'right'}}>{b.quantity}</td>
                  <td className="num" style={{textAlign: 'right', color: 'var(--primary)'}}>{b.points_per_card}</td>
                  <td>
                    <div style={{display: 'flex', flexDirection: 'column', gap: 4, minWidth: 100}}>
                      <span className="text-mono text-xs" style={{color: b.activation_pct >= 50 ? 'var(--success-fg)' : b.activation_pct >= 20 ? 'var(--warning-fg)' : 'var(--danger-fg)'}}>{b.activation_pct.toFixed(1)}%</span>
                      <div className={'progress ' + colorFor(b.activation_pct)}>
                        <div style={{width: Math.min(b.activation_pct, 100) + '%'}}/>
                      </div>
                    </div>
                  </td>
                  <td className="num" style={{textAlign: 'right'}}>{b.scanned}/{b.quantity}</td>
                  <td>
                    {b.status === 'active' ? <Badge variant="success" dot>Faol</Badge> :
                     b.status === 'pending' ? <Badge variant="warning" dot>Kutilmoqda</Badge> :
                     <Badge variant="neutral" dot>Arxiv</Badge>}
                  </td>
                  <td>
                    {b.delivery === 'delivered' ? <Badge variant="success" icon="check" size="sm">Доставлено</Badge> :
                     b.delivery === 'in_transit' ? <Badge variant="info" icon="send" size="sm">В пути</Badge> :
                     <Badge variant="warning" icon="clock" size="sm">Ожидает</Badge>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <Pagination total={17} page={1} perPage={25}/>
      </div>
    </div>
  );
}

// ============================================================
// 6. BATCH ADD
// ============================================================
function BatchAddPage() {
  return (
    <div className="page">
      <PageHeader title="Yangi партия" subtitle="Sotuvchi tanlang va miqdorni kiriting"/>
      <FormBlock title="Партия ma'lumotlari" icon="box">
        <Field label="Sotuvchi (autocomplete)" required hint="Ballar (50 × miqdor) sotuvchiga avtomatik qo'shiladi" span2>
          <div style={{display: 'flex', gap: 8}}>
            <Select style={{flex: 1}}>
              <option>— Sotuvchini tanlang —</option>
              {JQ.users.filter(u => u.type === 'sotuvchi').slice(0, 10).map(u => (
                <option key={u.id}>{u.first_name} {u.last_name} (@{u.username}) · {u.region}</option>
              ))}
            </Select>
            <Button variant="secondary" icon="edit"/>
            <Button variant="secondary" icon="plus"/>
            <Button variant="secondary" icon="eye"/>
          </div>
        </Field>
        <Field label="Miqdor (kartalar soni)" required hint="1 dan 500 gacha">
          <Input type="number" defaultValue={50} min={1} max={500}/>
        </Field>
        <Field label="Magazin">
          <Select>{JQ.stores.map(s => <option key={s.id}>{s.name}</option>)}</Select>
        </Field>
        <div className="span-2" style={{
          padding: 16, background: 'var(--primary-soft)', borderRadius: 8, fontSize: 13,
          borderLeft: '3px solid var(--primary)', display: 'flex', alignItems: 'center', gap: 12
        }}>
          <Icon name="sparkles" size={18} style={{color: 'var(--primary)', flexShrink: 0}}/>
          <span><strong>QR kodlar saqlangandan keyin avtomatik generatsiya qilinadi.</strong> Sotuvchiga 2 500 ball qo'shiladi.</span>
        </div>
      </FormBlock>

      <div className="form-footer">
        <span className="text-muted text-sm">Yangi yozuv</span>
        <div style={{display: 'flex', gap: 8}}>
          <Button variant="ghost">Сохранить и добавить</Button>
          <Button variant="secondary">Сохранить и продолжить</Button>
          <Button variant="primary" icon="check">Saqlash</Button>
        </div>
      </div>
    </div>
  );
}

// ============================================================
// 7. BATCH EDIT (with QR inline list)
// ============================================================
function BatchEditPage({ onNavigate }) {
  const b = JQ.batches[0];
  return (
    <div className="page">
      <PageHeader
        title={<span>Партия <span className="text-mono">{b.name}</span></span>}
        subtitle={<span>{b.scanned}/{b.quantity} ishlatilgan · {b.activation_pct.toFixed(1)}% aktivatsiya</span>}
        actions={<>
          <Button variant="secondary" icon="download">ZIP yuklab olish</Button>
          <Button variant="ghost" icon="history">История</Button>
          <Button variant="primary" icon="check">Сохранить</Button>
        </>}
      />

      <div className="kpi-grid">
        <KPI label="Jami QR" value={b.quantity} icon="qrcode" color="indigo"/>
        <KPI label="Skanlangan" value={b.scanned} icon="check" color="emerald"/>
        <KPI label="Aktivatsiya" value={b.activation_pct.toFixed(1) + '%'} icon="trending-up" color={b.activation_pct >= 50 ? 'emerald' : b.activation_pct >= 20 ? 'amber' : 'rose'}/>
        <KPI label="Ball/karta" value={b.points_per_card} icon="coin" color="blue"/>
      </div>

      <FormBlock title="Партия ma'lumotlari" icon="box">
        <Field label="Партия nomi" required><Input defaultValue={b.name}/></Field>
        <Field label="Status">
          <Select defaultValue={b.status}>
            <option value="pending">Faollashtirilmagan</option>
            <option value="active">Faollashtirilgan</option>
            <option value="archived">Arxivlangan</option>
          </Select>
        </Field>
        <Field label="Sotuvchi" required>
          <div className="input" style={{display: 'flex', alignItems: 'center', gap: 10}}>
            <Avatar name={b.seller_name} size={22}/>
            <a style={{color:'var(--primary)', cursor:'pointer'}} onClick={() => onNavigate('/users/sotuvchi')}>{b.seller_name}</a>
          </div>
        </Field>
        <Field label="Magazin"><Select defaultValue={b.store_name}>{JQ.stores.map(s => <option key={s.id}>{s.name}</option>)}</Select></Field>
        <Field label="Miqdor"><Input defaultValue={b.quantity} readOnly/></Field>
        <Field label="Ball/karta"><Input defaultValue={b.points_per_card}/></Field>
        <Field label="Yetkazib berish holati">
          <Select defaultValue={b.delivery}>
            <option value="pending">Ожидает</option>
            <option value="in_transit">В пути</option>
            <option value="delivered">Доставлено</option>
          </Select>
        </Field>
        <Field label="Yaratilgan"><Input defaultValue={b.created_at + ' 09:42'} readOnly/></Field>
      </FormBlock>

      <div className="card">
        <div className="card-header">
          <h3>QR kodlar ro'yxati</h3>
          <Badge variant="neutral">{b.quantity} ta</Badge>
        </div>
        <div className="table-wrap" style={{maxHeight: 400}}>
          <table className="table inline-table">
            <thead><tr><th>Serial</th><th>Code</th><th style={{textAlign:'right'}}>Ball</th><th>Status</th><th>Skanlangan</th></tr></thead>
            <tbody>
              {JQ.qrcodes.filter(q => q.batch_name === b.name).slice(0, 15).map(q => (
                <tr key={q.id}>
                  <td><span className="code-mask">#{q.serial}</span></td>
                  <td><span className="code-mask">{q.is_scanned ? q.code : 'JIP*****E'}</span></td>
                  <td className="num text-mono" style={{textAlign:'right', color:'var(--primary)'}}>{q.points}</td>
                  <td>{q.is_scanned ? <StatusBadges.scanned/> : <StatusBadges.unscanned/>}</td>
                  <td className="text-xs text-mono text-muted">{q.scanned_by_name || '—'}</td>
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
// 10. STORES LIST
// ============================================================
function StoresPage({ onNavigate }) {
  return (
    <div className="page">
      <PageHeader
        title="Do'konlar"
        subtitle="JIP partneri bo'lgan barcha do'konlar"
        actions={<>
          <Button variant="secondary" icon="download">Eksport</Button>
          <Button variant="primary" icon="plus" onClick={() => onNavigate('/stores/add')}>Yangi do'kon</Button>
        </>}
      />
      <div className="card">
        <div className="filter-bar">
          <SearchBar placeholder="Do'kon nomi, telefoni..."/>
          <div style={{flex: 1}}/>
          <FilterChip icon="map-pin">Viloyat</FilterChip>
          <FilterChip icon="check">Faollik</FilterChip>
        </div>
        <div className="table-wrap">
          <table className="table">
            <thead>
              <tr>
                <th>Do'kon</th><th>Viloyat / Tuman</th><th>Egasi</th><th>Telefon</th>
                <th style={{textAlign:'right'}}>Партия</th><th>Aktivatsiya</th>
                <th style={{textAlign:'right'}}>Komissiya</th><th>Holat</th>
              </tr>
            </thead>
            <tbody>
              {JQ.stores.map(s => {
                const pct = (s.scanned_qr / s.total_qr * 100);
                const color = pct >= 50 ? 'var(--success-fg)' : pct >= 20 ? 'var(--warning-fg)' : 'var(--danger-fg)';
                return (
                  <tr key={s.id} onClick={() => onNavigate('/stores/edit')} style={{cursor:'pointer'}}>
                    <td>
                      <div style={{display:'flex', alignItems:'center', gap: 10}}>
                        <span style={{width: 32, height: 32, borderRadius: 6, background: 'var(--info-soft)', color: 'var(--info)', display: 'grid', placeItems: 'center'}}><Icon name="store" size={15}/></span>
                        <div>
                          <div className="text-strong" style={{fontWeight: 500}}>{s.name}</div>
                          <div className="text-xs text-muted">{s.address}</div>
                        </div>
                      </div>
                    </td>
                    <td>
                      <div style={{display:'flex', flexDirection:'column', gap: 3}}>
                        <Badge variant="info" icon="map-pin">{s.region.replace(' область', '').replace('Город ', '')}</Badge>
                        <Badge variant="warning" outline size="sm">{s.district}</Badge>
                      </div>
                    </td>
                    <td>
                      <div className="user-cell">
                        <Avatar name={s.owner_name} size={26}/>
                        <span style={{fontSize: 12.5, color:'var(--text-strong)', fontWeight: 500}}>{s.owner_name}</span>
                      </div>
                    </td>
                    <td><span className="text-mono text-sm">{s.phone}</span></td>
                    <td className="num" style={{textAlign:'right'}}>{s.batches_count}</td>
                    <td>
                      <div style={{display:'flex', flexDirection:'column', gap: 4, minWidth: 110}}>
                        <span className="text-mono text-xs" style={{color}}>{pct.toFixed(1)}% ({s.scanned_qr}/{s.total_qr})</span>
                        <div className="progress"><div style={{width: Math.min(pct, 100) + '%', background: color}}/></div>
                      </div>
                    </td>
                    <td className="num" style={{textAlign:'right'}}><span style={{color: 'var(--primary)', fontWeight: 600}}>{s.commission_rate}%</span></td>
                    <td>{s.is_active ? <StatusBadges.active/> : <StatusBadges.inactive/>}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
        <Pagination total={12} page={1} perPage={25}/>
      </div>
    </div>
  );
}

// ============================================================
// 11. STORE EDIT
// ============================================================
function StoreEditPage({ onNavigate }) {
  const s = JQ.stores[0];
  return (
    <div className="page">
      <PageHeader
        title={s.name}
        subtitle={<span>{s.region} · {s.district} · {s.batches_count} ta партия</span>}
        actions={<>
          <Button variant="ghost" icon="history">История</Button>
          <Button variant="primary" icon="check">Сохранить</Button>
        </>}
      />
      <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16}}>
        <FormBlock title="Asosiy ma'lumotlar" icon="store">
          <Field label="Do'kon nomi" required span2><Input defaultValue={s.name}/></Field>
          <Field label="Manzil" span2><Input defaultValue={s.address}/></Field>
          <Field label="Viloyat (autocomplete)" required>
            <Select defaultValue={s.region}>{JQ.regions.map(r => <option key={r}>{r}</option>)}</Select>
          </Field>
          <Field label="Tuman" required>
            <Select defaultValue={s.district}>
              {(JQ.districtsByRegion[s.region] || ['—']).map(d => <option key={d}>{d}</option>)}
            </Select>
          </Field>
          <Field label="Egasi (autocomplete)" span2>
            <Select defaultValue={s.owner_name}>
              {JQ.users.filter(u => u.type === 'sotuvchi').slice(0, 12).map(u => (
                <option key={u.id}>{u.first_name} {u.last_name}</option>
              ))}
            </Select>
          </Field>
          <Field label="Telefon" required><Input defaultValue={s.phone}/></Field>
          <Field label="Komissiya foizi" hint="0-100%"><Input defaultValue={s.commission_rate}/></Field>
          <Field label="Faollik" span2>
            <label style={{display:'flex', alignItems:'center', gap:8}}><input type="checkbox" className="checkbox" defaultChecked={s.is_active}/> <span className="text-sm">Faol</span></label>
          </Field>
        </FormBlock>

        <FormBlock title="Aktivlik" icon="bar-chart">
          <div className="span-2" style={{display:'grid', gridTemplateColumns:'repeat(2, 1fr)', gap: 12}}>
            <div style={{padding: 16, background: 'var(--surface-2)', borderRadius: 8, border:'1px solid var(--border)'}}>
              <div className="text-xs text-muted" style={{marginBottom: 4}}>Jami QR</div>
              <div style={{fontSize: 24, fontWeight: 600, color: 'var(--text-strong)'}}>{s.total_qr}</div>
            </div>
            <div style={{padding: 16, background: 'var(--surface-2)', borderRadius: 8, border:'1px solid var(--border)'}}>
              <div className="text-xs text-muted" style={{marginBottom: 4}}>Skanlangan</div>
              <div style={{fontSize: 24, fontWeight: 600, color: 'var(--success-fg)'}}>{s.scanned_qr}</div>
            </div>
            <div style={{padding: 16, background: 'var(--surface-2)', borderRadius: 8, border:'1px solid var(--border)', gridColumn:'1/-1'}}>
              <div className="text-xs text-muted" style={{marginBottom: 4}}>Aktivatsiya foizi</div>
              <div style={{fontSize: 22, fontWeight: 600, color: 'var(--primary)', marginBottom: 8}}>{(s.scanned_qr / s.total_qr * 100).toFixed(1)}%</div>
              <div className="progress"><div style={{width: Math.min(s.scanned_qr/s.total_qr*100, 100)+'%'}}/></div>
            </div>
          </div>
        </FormBlock>
      </div>

      <div className="card">
        <div className="card-header"><h3>Партия (do'konga biriktirilgan)</h3><Badge variant="neutral">{s.batches_count} ta</Badge></div>
        <div className="table-wrap">
          <table className="table inline-table">
            <thead><tr><th>Партия</th><th>Sotuvchi</th><th style={{textAlign:'right'}}>Jami</th><th>Aktivatsiya</th><th>Holat</th></tr></thead>
            <tbody>
              {JQ.batches.filter(b => b.store_id === s.id).slice(0, 5).map(b => (
                <tr key={b.id}>
                  <td className="text-mono">{b.name}</td>
                  <td>{b.seller_name}</td>
                  <td className="num" style={{textAlign:'right'}}>{b.quantity}</td>
                  <td className="text-mono text-xs">{b.activation_pct.toFixed(1)}%</td>
                  <td>{b.status === 'active' ? <Badge variant="success" dot>Faol</Badge> : <Badge variant="neutral" dot>—</Badge>}</td>
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
// 12. STORE ADD
// ============================================================
function StoreAddPage() {
  return (
    <div className="page">
      <PageHeader title="Yangi do'kon" subtitle="JIP partneri sifatida ro'yxatdan o'tkazish"/>
      <FormBlock title="Asosiy ma'lumotlar" icon="store">
        <Field label="Do'kon nomi" required span2><Input placeholder="Sadulla Jomiy 2"/></Field>
        <Field label="Manzil" span2><Input placeholder="ул. Амира Темура, 25"/></Field>
        <Field label="Viloyat" required>
          <Select><option>— Tanlang —</option>{JQ.regions.map(r => <option key={r}>{r}</option>)}</Select>
        </Field>
        <Field label="Tuman" required><Select><option>— Avval viloyat —</option></Select></Field>
        <Field label="Egasi (sotuvchi)" span2>
          <Select><option>— Tanlang —</option>{JQ.users.filter(u => u.type === 'sotuvchi').slice(0,10).map(u => <option key={u.id}>{u.first_name} {u.last_name}</option>)}</Select>
        </Field>
        <Field label="Telefon" required><Input placeholder="+998 99 488 71 77"/></Field>
        <Field label="Komissiya foizi (%)"><Input type="number" defaultValue={7.43} step={0.01}/></Field>
        <Field label="Faollik" span2>
          <label style={{display:'flex', alignItems:'center', gap:8}}><input type="checkbox" className="checkbox" defaultChecked/> <span className="text-sm">Faol</span></label>
        </Field>
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

Object.assign(window, {
  QRCodesPage, QRCodeEditPage, QRGeneratePage,
  BatchesPage, BatchAddPage, BatchEditPage,
  StoresPage, StoreEditPage, StoreAddPage,
});
