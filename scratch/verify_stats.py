import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mona.settings')
django.setup()

from core.dashboard_stats import build_promo_table_rows
from core.models import TelegramUser, UzRegion

# Check if there are any users without a region
undef_count = TelegramUser.objects.filter(region__isnull=True).count()
print(f"Users without region: {undef_count}")

# Test for electricians
rows = build_promo_table_rows('electrician', None, None, None)
print("\nElectrician Regional Rows:")
for r in rows:
    print(f"{r['name']}: Users={r['users']}, Cards={r['cards']}, Points={r['points']}")

# Check if 'Noma\'lum' is in the rows
undef_row = next((r for r in rows if r['name'] == "Noma'lum"), None)
if undef_row:
    print(f"\nFound Undefined row: {undef_row}")
else:
    print("\nUndefined row NOT found!")

# Test for sellers
rows_s = build_promo_table_rows('seller', None, None, None)
print("\nSeller Regional Rows:")
for r in rows_s:
    print(f"{r['name']}: Users={r['users']}, Cards={r['cards']}, Points={r['points']}")

# Check totals
total_row = rows[-1]
sum_users = sum(r['users'] for r in rows[:-1])
print(f"\nTotal Row Users: {total_row['users']}")
print(f"Sum of Rows Users: {sum_users}")

if total_row['users'] == sum_users:
    print("SUCCESS: Totals match the sum of rows.")
else:
    print("FAILURE: Totals do NOT match the sum of rows.")
