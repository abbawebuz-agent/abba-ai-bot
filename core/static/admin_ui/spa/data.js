// JIP Admin SPA — Mock / seed data
// Real stats are patched over these by window.DJANGO_STATS in app.jsx

window.JIP = {
  stats: {
    users_total:    0,
    users_santenik: 0,
    users_sotuvchi: 0,
    batches_total:  0,
    batches_active: 0,
    qr_total:       0,
    qr_scanned:     0,
    gifts_pending:  0,
    txns_total:     0,
    audit_total:    0,
  },

  users: [],
  batches: [],
  qrcodes: [],
  stores: [],
  gifts: [],
  redemptions: [],
  transactions: [],
  sellerCodes: [],
  livestreams: [],
  videos: [],
  activity: [],
  regionLog: [],
  monthlyLog: [],
  contacts: [],

  // Chart seed data (weekly scans, monthly registrations)
  charts: {
    weeklyScans:  [0, 0, 0, 0, 0, 0, 0],
    monthlyRegs:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  },
};
