"""Fayl turiga qarab storage tanlovi — rasm / raw (PDF, ZIP) / video.

CLOUDINARY_URL env mavjud bo'lsa → Cloudinary CDN (doimiy, Railway efemer FS
muammosi yo'q). Bo'lmasa → lokal FileSystemStorage (eski xatti-harakat).

Bu funksiyalar FileField/ImageField'da `storage=` callable sifatida ishlatiladi.
Django callable storage'ni MIGRATSIYAGA bog'lamaydi (rasman qo'llab-quvvatlanadigan
"storage'ni migratsiyasiz almashtirish" usuli) — shuning uchun migration shart emas.

⚠️ NEGA har turga alohida: global `MediaCloudinaryStorage` BARCHA faylni "image"
turida yuklaydi → PDF Cloudinary'da bloklanadi, video xato beradi. Shuning uchun:
  - rasm  → MediaCloudinaryStorage (resource_type=image)
  - PDF/ZIP → RawMediaCloudinaryStorage (resource_type=raw)
  - video → VideoMediaCloudinaryStorage (resource_type=video)
"""
from django.conf import settings
from django.core.files.storage import FileSystemStorage


def _cloudinary_active() -> bool:
    return bool(getattr(settings, 'CLOUDINARY_URL', ''))


def image_storage():
    """Rasm fayllari uchun (gifts, projects, promotions, thumbs, banners)."""
    if _cloudinary_active():
        from cloudinary_storage.storage import MediaCloudinaryStorage
        return MediaCloudinaryStorage()
    return FileSystemStorage()


def raw_storage():
    """Rasm bo'lmagan hujjatlar uchun (PDF, ZIP) — raw resource_type."""
    if _cloudinary_active():
        from cloudinary_storage.storage import RawMediaCloudinaryStorage
        return RawMediaCloudinaryStorage()
    return FileSystemStorage()


def video_storage():
    """Video fayllar uchun (instruksiya videolari) — video resource_type."""
    if _cloudinary_active():
        from cloudinary_storage.storage import VideoMediaCloudinaryStorage
        return VideoMediaCloudinaryStorage()
    return FileSystemStorage()
