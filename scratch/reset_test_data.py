"""JIP prod test-datasini tozalash — psycopg2 orqali (Python 3.9 mos).

Django 5.0 lokal Python 3.9 da ishlamagani uchun, reset_for_launch
mantig'ini xom SQL bilan takrorlaydi. Xavfsizlik uchun:
  - Avval bazaning HAQIQIY FK grafini o'rganadi.
  - O'chiriladigan jadvallar to'plamini (14 ta "test data" ildizi + ularga
    bog'liq bolalar) hisoblaydi va SAQLANADIGAN jadvallarga tegmaydi.
  - Agar saqlanadigan jadval o'chiriladiganga NON-NULL FK bilan bog'langan
    bo'lsa — ABORT (ma'lumot yo'qotmaslik uchun).
  - Har bir o'chiriladigan jadvalni CSV ga backup qiladi.
  - --confirm bo'lsa: FK triggerlarni vaqtincha o'chirib DELETE qiladi,
    SellerRegistrationCode'ni reset qiladi, ketma-ketliklarni 1 dan boshlaydi.

Ishlatish:
    python reset_test_data.py "<PUBLIC_DATABASE_URL>"            # DRY-RUN
    python reset_test_data.py "<PUBLIC_DATABASE_URL>" --confirm   # HAQIQIY
"""
import sys
import os
import csv
import datetime
import psycopg2

# "Test data" ildizlari — reset_for_launch DELETE_ORDER bilan bir xil
SEED_TABLES = [
    'core_monthlypromoticket',
    'core_qrcodescanattempt',
    'core_promocodeattempt',
    'core_giftredemption',
    'core_sellerpointstransaction',
    'core_livestreamwinner',
    'core_qrcode',
    'core_sellerbatch',
    'core_qrcodebatch',
    'core_store',
    'core_seller',
    'core_regionmessagelog',
    'core_activitylog',
    'core_telegramuser',
]

# Hech qachon o'chmaydigan katalog/config jadvallari (FK bo'lsa NULL qilinadi)
KEEP_TABLES = {
    'core_gift', 'core_projectphoto', 'core_uzregion', 'core_uzdistrict',
    'core_promotion', 'core_privacypolicy', 'core_admincontactsettings',
    'core_videoinstruction', 'core_monthlyremindersettings',
    'core_monthlyreminderlog', 'core_broadcastmessage', 'core_livestream',
    'core_sellerregistrationcode', 'core_claudeinbox',
}


def get_fks(cur):
    """Barcha FK: (child_table, child_col, parent_table, is_nullable)."""
    cur.execute("""
        SELECT tc.table_name   AS child_table,
               kcu.column_name AS child_col,
               ccu.table_name  AS parent_table,
               col.is_nullable AS is_nullable
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
          ON tc.constraint_name = kcu.constraint_name AND tc.table_schema = kcu.table_schema
        JOIN information_schema.constraint_column_usage ccu
          ON tc.constraint_name = ccu.constraint_name AND tc.table_schema = ccu.table_schema
        JOIN information_schema.columns col
          ON col.table_name = tc.table_name AND col.column_name = kcu.column_name
         AND col.table_schema = tc.table_schema
        WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_schema = 'public';
    """)
    return cur.fetchall()


def main():
    if len(sys.argv) < 2:
        print("Xato: DATABASE_URL bering.\n  python reset_test_data.py '<URL>' [--confirm]")
        sys.exit(1)
    db_url = sys.argv[1]
    confirm = '--confirm' in sys.argv[2:]

    conn = psycopg2.connect(db_url)
    conn.autocommit = False
    cur = conn.cursor()

    fks = get_fks(cur)

    # Closure: SEED + ularga (transitive) bog'langan bola jadvallar
    to_delete = set(SEED_TABLES)
    changed = True
    while changed:
        changed = False
        for child, col, parent, nullable in fks:
            if parent in to_delete and child not in to_delete and child not in KEEP_TABLES:
                to_delete.add(child)
                changed = True

    # Xavfsizlik: SAQLANADIGAN jadval o'chiriladiganga NON-NULL FK bilan bog'langanmi?
    blockers = []
    keep_nulls = []  # (keep_table, col) — NULL qilinadi
    for child, col, parent, nullable in fks:
        if child in KEEP_TABLES and parent in to_delete:
            if nullable == 'YES':
                keep_nulls.append((child, col))
            else:
                blockers.append((child, col, parent))

    print("=" * 60)
    print("REJIM:", "HAQIQIY O'CHIRISH (--confirm)" if confirm else "DRY-RUN (hech narsa o'chmaydi)")
    print("=" * 60)

    if blockers:
        print("\n❌ ABORT — saqlanadigan jadval o'chiriladiganga NON-NULL bog'langan:")
        for c, col, p in blockers:
            print(f"   {c}.{col} -> {p}")
        sys.exit(2)

    # Sonlarni ko'rsatamiz
    print("\nO'CHIRILADIGAN jadvallar (yozuvlar soni):")
    total = 0
    counts = {}
    for t in sorted(to_delete):
        cur.execute('SELECT COUNT(*) FROM "%s"' % t)
        n = cur.fetchone()[0]
        counts[t] = n
        total += n
        print(f"   - {t}: {n}")
    print(f"\n   JAMI o'chadi: {total} yozuv")

    if keep_nulls:
        print("\nSAQLANADI, lekin FK NULL qilinadi:")
        for t, col in keep_nulls:
            print(f"   - {t}.{col} -> NULL")

    # SellerRegistrationCode reset (saqlanadi, faqat bo'shatiladi)
    cur.execute("SELECT COUNT(*) FROM core_sellerregistrationcode WHERE is_used = true")
    used_codes = cur.fetchone()[0]
    print(f"\nSotuvchi ID kodlari: {used_codes} ta 'ishlatilgan' -> bo'shatiladi (o'chmaydi)")

    # Saqlanadigan katalog (ishonch uchun)
    for t in ['core_gift', 'core_uzregion', 'core_promotion', 'core_sellerregistrationcode']:
        cur.execute('SELECT COUNT(*) FROM "%s"' % t)
        print(f"   SAQLANADI {t}: {cur.fetchone()[0]}")

    if not confirm:
        print("\n[DRY-RUN] Haqiqatan o'chirish uchun oxiriga --confirm qo'shing.")
        conn.rollback()
        conn.close()
        return

    # --- BACKUP (CSV) ---
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'reset_backup_%s' % ts)
    os.makedirs(backup_dir, exist_ok=True)
    print(f"\nBackup -> {backup_dir}")
    for t in sorted(to_delete):
        path = os.path.join(backup_dir, '%s.csv' % t)
        with open(path, 'w', newline='') as f:
            cur.copy_expert('COPY "%s" TO STDOUT WITH CSV HEADER' % t, f)
        print(f"   ✓ {t}.csv ({counts[t]} qator)")
    # SellerRegistrationCode ham backup (reset bo'ladi)
    with open(os.path.join(backup_dir, 'core_sellerregistrationcode.csv'), 'w', newline='') as f:
        cur.copy_expert('COPY core_sellerregistrationcode TO STDOUT WITH CSV HEADER', f)

    # --- O'CHIRISH ---
    print("\nO'chirilmoqda (FK triggerlar vaqtincha o'chirilgan)...")
    cur.execute("SET session_replication_role = replica;")
    for t in to_delete:
        cur.execute('DELETE FROM "%s"' % t)
    # KEEP jadvallaridagi FK larni NULL qilamiz
    for t, col in keep_nulls:
        cur.execute('UPDATE "%s" SET "%s" = NULL WHERE "%s" IS NOT NULL' % (t, col, col))
    # SellerRegistrationCode bo'shatamiz
    cur.execute("""UPDATE core_sellerregistrationcode
                   SET is_used = false, used_by_id = NULL, used_at = NULL
                   WHERE is_used = true OR used_by_id IS NOT NULL;""")
    # Ketma-ketliklarni 1 dan boshlaymiz
    for t in to_delete:
        cur.execute("""SELECT pg_get_serial_sequence(%s, 'id')""", (t,))
        seq = cur.fetchone()[0]
        if seq:
            cur.execute('ALTER SEQUENCE %s RESTART WITH 1' % seq)
    cur.execute("SET session_replication_role = origin;")

    conn.commit()
    print("\n✅ Tozalash tugadi. Tekshirish:")
    for t in ['core_telegramuser', 'core_qrcode', 'core_seller', 'core_giftredemption']:
        cur.execute('SELECT COUNT(*) FROM "%s"' % t)
        print(f"   {t}: {cur.fetchone()[0]}")
    cur.execute("SELECT COUNT(*) FROM core_gift")
    print(f"   SAQLANDI core_gift: {cur.fetchone()[0]}")
    conn.close()


if __name__ == '__main__':
    main()
