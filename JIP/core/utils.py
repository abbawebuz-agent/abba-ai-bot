"""
Utility funksiyalar — QR generatsiya, hash, serial number.
"""
from __future__ import annotations

import io
import secrets
import string
import zipfile
from pathlib import Path

import qrcode
from django.conf import settings


# 0/O, 1/I/l olib tashlangan (chunki o'qishda chalkash)
HASH_ALPHABET = ''.join(c for c in (string.ascii_uppercase + string.digits) if c not in '0O1I')


def generate_hash(length: int = 6) -> str:
    return ''.join(secrets.choice(HASH_ALPHABET) for _ in range(length))


def generate_unique_hash(model_cls, field: str = 'hash_code', length: int = 6, max_attempts: int = 30) -> str:
    """Unique hash — modelga tegmaslikgacha urinish."""
    for _ in range(max_attempts):
        candidate = generate_hash(length)
        if not model_cls.objects.filter(**{field: candidate}).exists():
            return candidate
    # Fallback — uzunroq
    return generate_hash(length + 2)


def generate_serial(store_id: int, batch_id: int, sequence: int) -> str:
    """Batch ichida unique serial — STORE_ID + BATCH_ID + sequence."""
    return f"S{store_id:04d}B{batch_id:04d}N{sequence:05d}"


def make_qr_png(payload: str) -> bytes:
    """QR PNG (telegram bot deep-link payload bilan)."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10, border=2,
    )
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()


def telegram_bot_username() -> str:
    return getattr(settings, 'TELEGRAM_BOT_USERNAME', '') or ''


def build_deeplink(hash_code: str) -> str:
    """QR ichidagi payload — `/start <hash>` deep-link."""
    username = telegram_bot_username()
    if username:
        return f"https://t.me/{username}?start={hash_code}"
    return hash_code


def build_batch_zip(batch) -> bytes:
    """Batch dagi barcha QR'lar uchun ZIP fayl yaratish."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        for qr in batch.qr_codes.all().order_by('serial_number'):
            payload = build_deeplink(qr.hash_code)
            png = make_qr_png(payload)
            zf.writestr(f"{qr.serial_number}.png", png)
        # Lookup ro'yxati
        manifest = '\n'.join(
            f"{qr.serial_number}\t{qr.hash_code}\t{qr.code}\t{qr.points}"
            for qr in batch.qr_codes.all().order_by('serial_number')
        )
        zf.writestr('manifest.tsv', manifest)
    return buf.getvalue()
