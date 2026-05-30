// Mock data for JIP Admin Panel
// Realistic Uzbek names, regions, plausible numbers
window.JIP = (function() {

  const regions = [
    'Город Ташкент', 'Ташкентская область', 'Андижанская область',
    'Бухарская область', 'Ферганская область', 'Джизакская область',
    'Кашкадарьинская область', 'Навоийская область', 'Наманганская область',
    'Самаркандская область', 'Сурхандарьинская область', 'Сырдарьинская область',
    'Хорезмская область', 'Республика Каракалпакстан'
  ];

  const districtsByRegion = {
    'Город Ташкент': ['Юнусабадский', 'Чиланзарский', 'Мирабадский', 'Сергелийский', 'Яккасарайский', 'Шайхантахурский', 'Алмазарский', 'Учтепинский', 'Яшнабадский', 'Бектемирский', 'Мирзо-Улугбекский'],
    'Ташкентская область': ['Зангиатинский', 'Кибрайский', 'Янгиюль', 'Чирчик', 'Ангрен', 'Алмалык'],
    'Самаркандская область': ['Самарканд', 'Каттакурган', 'Ургут', 'Иштыхан'],
    'Бухарская область': ['Бухара', 'Каган', 'Гиждуван'],
    'Ферганская область': ['Фергана', 'Маргилан', 'Кокан'],
    'Андижанская область': ['Андижан', 'Асака', 'Ханабад'],
    'Наманганская область': ['Наманган', 'Чартак', 'Касансай'],
    'Хорезмская область': ['Ургенч', 'Хива', 'Питнак']
  };

  const firstNames = ['Шохрух', 'Бекзод', 'Жасур', 'Акмал', 'Санжар', 'Иброхим', 'Аббос', 'Рустам', 'Дилшод', 'Шерзод', 'Анвар', 'Фарход', 'Жахонгир', 'Олим', 'Хасан', 'Хусан', 'Алишер', 'Бахром', 'Камрон', 'Тимур', 'Зафар', 'Улугбек'];
  const lastNames = ['Каримов', 'Назаров', 'Юсупов', 'Расулов', 'Турсунов', 'Холматов', 'Эргашев', 'Икромов', 'Махмудов', 'Юлдашев', 'Норматов', 'Закиров', 'Олимов', 'Хасанов', 'Худойбердиев', 'Файзиев', 'Абдуллаев', 'Камолов', 'Латипов', 'Мирзаев'];

  function rnd(seed) {
    let s = seed;
    return function() {
      s = (s * 9301 + 49297) % 233280;
      return s / 233280;
    };
  }
  const r = rnd(42);
  const pick = (arr) => arr[Math.floor(r() * arr.length)];
  const pickN = (arr, n) => Array.from({length: n}, () => pick(arr));

  // === Users (23 total) ===
  function makePhone() {
    return '998' + [9,9,8,7,3,5,5,0,9,1,2,3,4,7][Math.floor(r()*14)] + Math.floor(r()*10) + ' ' +
      String(Math.floor(r() * 900) + 100) + ' ' + String(Math.floor(r() * 9000) + 1000);
  }

  const users = [];
  // 2 santeniks
  for (let i = 0; i < 2; i++) {
    const region = pick(regions);
    users.push({
      id: 672293616 + i,
      type: 'santenik',
      first_name: pick(firstNames),
      last_name: pick(lastNames),
      username: 'sodikov' + (i+1),
      phone: '+998 99 488 71' + String(70+i).padStart(2,'0'),
      region,
      district: pick(districtsByRegion[region] || ['—']),
      points: Math.floor(r() * 50000) + 5000,
      language: r() > 0.4 ? 'uz' : 'ru',
      is_active: true,
      seller_approved: false,
      created_at: '2026-05-' + String(15 + i).padStart(2, '0'),
      total_attempts: Math.floor(r() * 50) + 10,
      successful_attempts: Math.floor(r() * 20) + 1,
      latitude: 41.3 + r() * 0.5,
      longitude: 69.2 + r() * 0.5,
    });
  }
  // 21 sotuvchis
  for (let i = 0; i < 21; i++) {
    const region = pick(regions);
    const approved = r() > 0.3;
    users.push({
      id: 5000000000 + i * 13,
      type: 'sotuvchi',
      first_name: pick(firstNames),
      last_name: pick(lastNames),
      username: pick(['shop','store','market','sklad','mag']) + (i+1),
      phone: makePhone(),
      region,
      district: pick(districtsByRegion[region] || ['—']),
      points: Math.floor(r() * 20000),
      language: r() > 0.3 ? 'uz' : 'ru',
      is_active: r() > 0.1,
      seller_approved: approved,
      seller_approved_at: approved ? '2026-05-' + String(10 + Math.floor(r()*15)).padStart(2,'0') : null,
      created_at: '2026-05-' + String(10 + Math.floor(r()*15)).padStart(2,'0'),
      seller_code: 'JIP' + String(1000 + i).slice(-4) + 'E',
      store_id: 'ST-' + String(100 + i),
      batches_count: Math.floor(r() * 5) + 1,
      total_qr: (Math.floor(r() * 5) + 1) * 50,
      scanned_qr: Math.floor(r() * 10),
      latitude: 41.3 + r() * 0.5,
      longitude: 69.2 + r() * 0.5,
    });
  }

  // === QR codes (239 total — we'll generate ~50 visible) ===
  const stores = [];
  for (let i = 0; i < 12; i++) {
    const region = pick(regions);
    stores.push({
      id: i+1,
      name: pick(['Sadulla Jomiy', 'Bek Sanitex', 'Asaka Plast', 'Hamkor Trade', 'Olamjon', 'Toshkent Plyus', 'Buxoro Plast', 'Mega Sklad']) + ' ' + (i+1),
      address: 'ул. ' + pick(['Амира Темура', 'Бабура', 'Шота Руставели', 'Истиклол', 'Навои']) + ', ' + (Math.floor(r()*200)+1),
      region,
      district: pick(districtsByRegion[region] || ['—']),
      phone: makePhone(),
      owner_id: users.filter(u => u.type === 'sotuvchi')[i % 21]?.id,
      owner_name: (function(){const u = users.filter(u => u.type === 'sotuvchi')[i % 21]; return u ? u.first_name + ' ' + u.last_name : '—';})(),
      batches_count: Math.floor(r() * 6) + 1,
      total_qr: (Math.floor(r() * 6) + 1) * 50,
      scanned_qr: Math.floor(r() * 30),
      commission_rate: (r() * 10 + 3).toFixed(2),
      is_active: r() > 0.15,
    });
  }

  // === Batches (17) ===
  const batches = [];
  const batchPrefixes = ['S27-MAY-2026','S26-MAY-2026','S25-MAY-2026','S24-MAY-2026','S23-MAY-2026','S22-MAY-2026','M21-MAY-2026','M20-MAY-2026','S19-MAY-2026','A18-MAY-2026','S17-MAY-2026','S16-MAY-2026','M15-MAY-2026','S14-MAY-2026','A13-MAY-2026','S12-MAY-2026','S11-MAY-2026'];
  for (let i = 0; i < 17; i++) {
    const total = Math.floor(r() * 8 + 1) * 50;
    const scanned = Math.floor(r() * total * 0.6);
    const seller = users.filter(u => u.type === 'sotuvchi')[i % 21];
    const store = stores[i % stores.length];
    batches.push({
      id: i+1,
      name: batchPrefixes[i],
      seller_id: seller?.id,
      seller_name: seller ? seller.first_name + ' ' + seller.last_name : '—',
      store_id: store.id,
      store_name: store.name,
      quantity: total,
      points_per_card: 50,
      scanned,
      activation_pct: (scanned / total * 100),
      status: i < 3 ? 'pending' : (i < 14 ? 'active' : 'archived'),
      delivery: pick(['delivered','in_transit','pending']),
      created_at: '2026-05-' + String(11 + i).padStart(2, '0'),
    });
  }

  // === QR codes (sample) ===
  const qrcodes = [];
  for (let i = 0; i < 50; i++) {
    const b = batches[i % batches.length];
    const scanned = r() > 0.5;
    const scannedBy = scanned ? users[Math.floor(r() * users.length)] : null;
    qrcodes.push({
      id: i+1,
      serial: String(i+1).padStart(3, '0'),
      code: 'JIP' + Math.random().toString(36).substring(2,7).toUpperCase() + 'E',
      hash_code: 'h' + Math.random().toString(36).substring(2,12),
      store_id: b.store_id,
      store_name: b.store_name,
      batch_id: b.id,
      batch_name: b.name,
      points: 50,
      is_scanned: scanned,
      scanned_by_id: scannedBy?.id,
      scanned_by_name: scannedBy ? scannedBy.first_name + ' ' + scannedBy.last_name : null,
      scanned_at: scanned ? '2026-05-' + String(20 + Math.floor(r()*6)).padStart(2,'0') + ' ' + String(Math.floor(r()*24)).padStart(2,'0') + ':' + String(Math.floor(r()*60)).padStart(2,'0') : null,
      generated_at: '2026-05-' + String(15 + Math.floor(r()*10)).padStart(2,'0'),
      is_deleted: false,
    });
  }

  // === Gifts (catalogue) ===
  const gifts = [
    { id:1, name_uz:'AirPods 3-pokoleniya', name_ru:'AirPods 3-го поколения', price: 50000, image: '🎧', is_active: true, type:'electronics' },
    { id:2, name_uz:'Toshkent ekskursiyasi', name_ru:'Экскурсия в Ташкент', price: 25000, image: '🏛', is_active: true, type:'experience' },
    { id:3, name_uz:'Smart TV 43"', name_ru:'Smart TV 43"', price: 80000, image: '📺', is_active: true, type:'electronics' },
    { id:4, name_uz:'Powerbank 20 000 mAh', name_ru:'Powerbank 20 000 mAh', price: 8000, image: '🔋', is_active: true, type:'electronics' },
    { id:5, name_uz:'Brand qishki kurtka', name_ru:'Брендовая зимняя куртка', price: 35000, image: '🧥', is_active: false, type:'clothing' },
    { id:6, name_uz:'Naqd 1 000 000 so\'m', name_ru:'Наличные 1 000 000 сум', price: 50000, image: '💵', is_active: true, type:'cash' },
    { id:7, name_uz:'Smartphone Xiaomi', name_ru:'Смартфон Xiaomi', price: 90000, image: '📱', is_active: true, type:'electronics' },
    { id:8, name_uz:'BTS sport kostyumu', name_ru:'Спортивный костюм BTS', price: 15000, image: '👕', is_active: true, type:'clothing' },
  ];

  // === Gift redemptions (15) ===
  const redemptions = [];
  for (let i = 0; i < 15; i++) {
    const u = users[Math.floor(r() * users.length)];
    const g = gifts[Math.floor(r() * gifts.length)];
    const status = pick(['pending', 'pending', 'confirmed', 'confirmed', 'cancelled']);
    redemptions.push({
      id: 1000 + i,
      user_id: u.id,
      user_name: u.first_name + ' ' + u.last_name,
      phone: u.phone,
      region: u.region,
      gift_id: g.id,
      gift_name: g.name_ru,
      status,
      is_confirmed: status === 'confirmed' && r() > 0.4,
      created_at: '2026-05-' + String(18 + Math.floor(r()*8)).padStart(2,'0') + ' ' + String(Math.floor(r()*24)).padStart(2,'0') + ':' + String(Math.floor(r()*60)).padStart(2,'0'),
    });
  }

  // === Seller transactions (we'll show 30 of 1117) ===
  const txns = [];
  for (let i = 0; i < 30; i++) {
    const u = users.filter(u => u.type === 'sotuvchi')[Math.floor(r() * 21)];
    const type = pick(['sale_bonus', 'sale_bonus', 'sale_bonus', 'admin_add', 'correction']);
    txns.push({
      id: 10000 + i,
      created_at: '2026-05-' + String(15 + Math.floor(r()*11)).padStart(2,'0') + ' ' + String(Math.floor(r()*24)).padStart(2,'0') + ':' + String(Math.floor(r()*60)).padStart(2,'0'),
      seller_id: u.id,
      seller_name: u.first_name + ' ' + u.last_name,
      type,
      points: type === 'correction' ? -Math.floor(r()*500) : Math.floor(r()*2000)+100,
      sale_amount: type === 'sale_bonus' ? Math.floor(r()*1000)+50 : null,
      added_by: type === 'sale_bonus' ? 'Bot' : pick(['admin@jip', 'callcenter1', 'superadmin']),
    });
  }

  // === Seller registration codes ===
  const sellerCodes = [];
  for (let i = 0; i < 25; i++) {
    const used = r() > 0.4;
    const u = used ? users.filter(u => u.type === 'sotuvchi')[Math.floor(r()*21)] : null;
    sellerCodes.push({
      id: i+1,
      code: 'JIP' + String(1000 + i).slice(-4) + 'E',
      label: 'Партия ' + ['Север','Юг','Восток','Запад','Центр'][i % 5] + ' ' + (i+1),
      owner_id: u?.id,
      owner_name: u ? u.first_name + ' ' + u.last_name : '—',
      is_used: used,
      created_at: '2026-04-' + String(10 + (i % 20)).padStart(2,'0'),
    });
  }

  // === Activity log (264 — show 40) ===
  const actionTypes = [
    { code:'create', label:'Yaratildi', icon:'+', cls:'badge-success' },
    { code:'update', label:'O\'zgartirildi', icon:'✏', cls:'badge-info' },
    { code:'delete', label:'O\'chirildi', icon:'🗑', cls:'badge-danger' },
  ];
  const log = [];
  for (let i = 0; i < 40; i++) {
    const a = pick(actionTypes);
    log.push({
      id: i+1,
      timestamp: '2026-05-' + String(20 + Math.floor(r()*6)).padStart(2,'0') + ' ' + String(Math.floor(r()*24)).padStart(2,'0') + ':' + String(Math.floor(r()*60)).padStart(2,'0') + ':' + String(Math.floor(r()*60)).padStart(2,'0'),
      who: pick(['admin@jip', 'callcenter1', 'superadmin', 'Bot', 'manager2']),
      action: a,
      object_type: pick(['TelegramUser','QRCode','QRCodeBatch','Store','GiftRedemption','Gift']),
      object_label: '#' + String(Math.floor(r()*1000)+1),
      description: pick(['Изменён user_type','Новая партия создана','QR код активирован','Подтверждён сотрудник','Сменён регион']),
      ip: '178.' + Math.floor(r()*255) + '.' + Math.floor(r()*255) + '.' + Math.floor(r()*255),
    });
  }

  // Recent actions for dashboard
  const recentActions = log.slice(0, 10).map(l => ({
    object: l.object_type + ' ' + l.object_label,
    action: l.description,
    time: l.timestamp.slice(11),
  }));

  // === Livestreams ===
  const livestreams = [
    { id:1, title:'May oyi ochilishi', status:'completed', start_at:'2026-05-01 18:00', winners_count: 5 },
    { id:2, title:'O\'rta oy bayrami', status:'completed', start_at:'2026-05-15 19:00', winners_count: 3 },
    { id:3, title:'Yangi mahsulot taqdimoti', status:'scheduled', start_at:'2026-06-01 19:00', winners_count: 7 },
    { id:4, title:'JIP yillik tantanasi', status:'active', start_at:'2026-05-26 18:00', winners_count: 10 },
  ];

  // === Videos ===
  const videos = [
    { id:1, title:'QR kod qanday skanlanadi', url:'youtu.be/abc123', order:1, type:'santenik', is_active:true },
    { id:2, title:'Sotuvchi sifatida ro\'yxatdan o\'tish', url:'youtu.be/def456', order:1, type:'sotuvchi', is_active:true },
    { id:3, title:'Sovg\'a tanlash va so\'rash', url:'youtu.be/ghi789', order:2, type:'santenik', is_active:true },
    { id:4, title:'Partiya yaratish', url:'youtu.be/jkl012', order:2, type:'sotuvchi', is_active:true },
    { id:5, title:'Bonus tizimi', url:'youtu.be/mno345', order:3, type:'santenik', is_active:false },
  ];

  // === Region message log ===
  const regionMessages = [
    { id:1, date:'2026-05-26 14:32', region:'Город Ташкент', total: 12, sent: 12, errors: 0, status:'done', who:'admin@jip' },
    { id:2, date:'2026-05-25 10:15', region:'Все регионы', total: 23, sent: 21, errors: 2, status:'done', who:'admin@jip' },
    { id:3, date:'2026-05-23 16:00', region:'Самаркандская область', total: 4, sent: 4, errors: 0, status:'done', who:'superadmin' },
    { id:4, date:'2026-05-22 09:00', region:'Ферганская область', total: 3, sent: 0, errors: 0, status:'pending', who:'manager2' },
    { id:5, date:'2026-05-20 12:45', region:'Все регионы', total: 23, sent: 18, errors: 5, status:'error', who:'admin@jip' },
  ];

  // === Monthly reminder logs ===
  const reminderLogs = [
    { id:1, date:'2026-05-01 09:00', status:'done', sent: 21, errors: 0, duration:'4s' },
    { id:2, date:'2026-04-01 09:00', status:'done', sent: 19, errors: 1, duration:'5s' },
    { id:3, date:'2026-03-01 09:00', status:'done', sent: 17, errors: 0, duration:'3s' },
  ];

  // === Admin contacts ===
  const adminContacts = [
    { id:1, type:'Telegram', value:'@jip_support', is_active:true },
    { id:2, type:'Telefon', value:'+998 71 200-20-20', is_active:true },
    { id:3, type:'Email', value:'support@jip.uz', is_active:true },
    { id:4, type:'Telegram', value:'@jip_admin_old', is_active:false },
  ];

  // === Privacy policy ===
  const policies = [
    { id:1, title_uz:'Maxfiylik siyosati', title_ru:'Политика конфиденциальности', created:'2026-04-15', is_active:true },
    { id:2, title_uz:'Foydalanish shartlari', title_ru:'Условия использования', created:'2026-03-01', is_active:true },
  ];

  // === Django auth users / groups ===
  const authUsers = [
    { id:1, username:'superadmin', name:'Жасур Каримов', email:'super@jip.uz', is_superuser:true, is_staff:true, last_login:'2026-05-26 11:30' },
    { id:2, username:'admin@jip', name:'Шерзод Турсунов', email:'admin@jip.uz', is_superuser:false, is_staff:true, last_login:'2026-05-26 10:15' },
    { id:3, username:'callcenter1', name:'Алишер Юлдашев', email:'cc1@jip.uz', is_superuser:false, is_staff:true, last_login:'2026-05-25 18:42' },
    { id:4, username:'manager2', name:'Дилшод Махмудов', email:'m2@jip.uz', is_superuser:false, is_staff:true, last_login:'2026-05-24 14:08' },
  ];

  const authGroups = [
    { id:1, name:'Superadmin', users_count:1, permissions:'Все' },
    { id:2, name:'Admin', users_count:1, permissions:'42 разрешения' },
    { id:3, name:'Call Center', users_count:1, permissions:'4 разрешения' },
    { id:4, name:'Manager', users_count:1, permissions:'18 разрешений' },
  ];

  return {
    regions, districtsByRegion,
    users, stores, batches, qrcodes, gifts, redemptions,
    txns, sellerCodes, log, recentActions,
    livestreams, videos, regionMessages, reminderLogs,
    adminContacts, policies, authUsers, authGroups,
    stats: {
      users_total: 23,
      users_santenik: 2,
      users_sotuvchi: 21,
      batches_total: 17,
      batches_active: 11,
      qr_total: 239,
      qr_scanned: 47,
      gifts_pending: 15,
      txns_total: 1117,
      audit_total: 264,
    },
  };
})();
