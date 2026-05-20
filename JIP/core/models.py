"""
JIP — Sodiqlik Dasturi modellari.

TZ: JIP_FULL_TZ.md, bo'lim 5 (Ma'lumotlar Modeli).
"""
from __future__ import annotations

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


# ---------------------------------------------------------------------------
# 5.1. Geo modellari
# ---------------------------------------------------------------------------

class UzRegion(models.Model):
    code = models.CharField(max_length=50, unique=True, db_index=True)
    name_uz = models.CharField(max_length=120)
    name_ru = models.CharField(max_length=120)

    class Meta:
        verbose_name = _("Viloyat")
        verbose_name_plural = _("Viloyatlar")
        ordering = ['code']

    def __str__(self) -> str:
        return self.name_uz


class UzDistrict(models.Model):
    region = models.ForeignKey(UzRegion, on_delete=models.CASCADE, related_name='districts')
    code = models.CharField(max_length=100, db_index=True)
    name_uz = models.CharField(max_length=120)
    name_ru = models.CharField(max_length=120)

    class Meta:
        verbose_name = _("Tuman")
        verbose_name_plural = _("Tumanlar")
        unique_together = [('region', 'code')]
        ordering = ['region__code', 'code']

    def __str__(self) -> str:
        return f"{self.region.name_uz} / {self.name_uz}"


# ---------------------------------------------------------------------------
# 5.3. TelegramUser
# ---------------------------------------------------------------------------

class TelegramUser(models.Model):
    USER_TYPE_SANTENIK = 'santenik'
    USER_TYPE_SOTUVCHI = 'sotuvchi'
    USER_TYPE_CHOICES = [
        (USER_TYPE_SANTENIK, _("Santenik")),
        (USER_TYPE_SOTUVCHI, _("Sotuvchi")),
    ]

    LANG_UZ = 'uz_latin'
    LANG_RU = 'ru'
    LANGUAGE_CHOICES = [
        (LANG_UZ, _("O'zbek (Lotin)")),
        (LANG_RU, _("Русский")),
    ]

    telegram_id = models.BigIntegerField(unique=True, db_index=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True, db_index=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    region = models.ForeignKey(UzRegion, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    district = models.ForeignKey(UzDistrict, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, null=True, blank=True, db_index=True)
    points = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    is_active = models.BooleanField(default=True, db_index=True)
    language = models.CharField(max_length=15, choices=LANGUAGE_CHOICES, default=LANG_UZ)
    privacy_accepted = models.BooleanField(default=False)

    last_message_sent_at = models.DateTimeField(null=True, blank=True)
    blocked_bot_at = models.DateTimeField(null=True, blank=True)

    promo_failed_attempts = models.IntegerField(default=0)
    promo_block_stage = models.IntegerField(default=0)
    promo_blocked_until = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Telegram foydalanuvchisi")
        verbose_name_plural = _("Telegram foydalanuvchilari")
        ordering = ['-created_at']
        permissions = [
            ('send_region_messages', 'Can send region broadcasts'),
            ('change_user_type_call_center', 'Call Center: change user type'),
            ('add_seller_points', 'Can add points to seller'),
        ]

    def __str__(self) -> str:
        name = (self.first_name or '') + ' ' + (self.last_name or '')
        name = name.strip() or self.username or str(self.telegram_id)
        return f"{name} ({self.get_user_type_display() or '—'})"

    @property
    def full_name(self) -> str:
        return ((self.first_name or '') + ' ' + (self.last_name or '')).strip()

    def is_santenik(self) -> bool:
        return self.user_type == self.USER_TYPE_SANTENIK

    def is_sotuvchi(self) -> bool:
        return self.user_type == self.USER_TYPE_SOTUVCHI

    def is_promo_code_blocked(self):
        """3 ta noto'g'ri urinish → 24 soatga blok. Returns (blocked, stage, until)."""
        if self.promo_blocked_until and self.promo_blocked_until > timezone.now():
            return True, self.promo_block_stage, self.promo_blocked_until
        return False, 0, None

    def register_invalid_promo_attempt(self, source: str = 'unknown', raw_code: str = '') -> None:
        """Noto'g'ri urinish — counter oshadi, 3 ga yetganda blok."""
        from datetime import timedelta

        self.promo_failed_attempts = (self.promo_failed_attempts or 0) + 1
        max_attempts = getattr(settings, 'PROMO_MAX_INVALID_ATTEMPTS', 3)
        block_hours = getattr(settings, 'PROMO_BLOCK_DURATION_HOURS', 24)

        if self.promo_failed_attempts >= max_attempts:
            self.promo_block_stage = (self.promo_block_stage or 0) + 1
            self.promo_blocked_until = timezone.now() + timedelta(hours=block_hours)
            self.promo_failed_attempts = 0

        self.save(update_fields=['promo_failed_attempts', 'promo_block_stage', 'promo_blocked_until'])
        PromoCodeAttempt.objects.create(user=self, raw_code=raw_code, source=source, is_successful=False)

    def register_successful_promo(self, raw_code: str = '', source: str = 'unknown') -> None:
        """Muvaffaqiyatli urinishdan keyin counter 0 ga."""
        self.promo_failed_attempts = 0
        self.promo_blocked_until = None
        self.save(update_fields=['promo_failed_attempts', 'promo_blocked_until'])
        PromoCodeAttempt.objects.create(user=self, raw_code=raw_code, source=source, is_successful=True)

    def calculate_points(self, force: bool = False) -> int:
        """
        Santenik: skanlangan QR ballaridan jami − sovg'aga ketgan.
        Sotuvchi: SellerPointsTransaction ballaridan jami.
        """
        from django.core.cache import cache
        cache_key = f'tg_user_points:{self.pk}'
        if not force:
            cached = cache.get(cache_key)
            if cached is not None:
                return cached

        if self.user_type == self.USER_TYPE_SANTENIK:
            earned = self.scanned_qrcodes.filter(is_deleted=False).aggregate(s=models.Sum('points'))['s'] or 0
            spent = self.gift_redemptions.exclude(
                status__in=['rejected', 'cancelled_by_user']
            ).aggregate(s=models.Sum('gift__points_cost'))['s'] or 0
            balance = int(earned) - int(spent)
        elif self.user_type == self.USER_TYPE_SOTUVCHI:
            balance = self.seller_transactions.aggregate(s=models.Sum('points'))['s'] or 0
        else:
            balance = 0

        balance = max(0, int(balance))
        if balance != self.points:
            type(self).objects.filter(pk=self.pk).update(points=balance)
            self.points = balance
        cache.set(cache_key, balance, 60)
        return balance

    def invalidate_points_cache(self) -> None:
        from django.core.cache import cache
        cache.delete(f'tg_user_points:{self.pk}')


# ---------------------------------------------------------------------------
# 5.2. Store (YANGI)
# ---------------------------------------------------------------------------

class Store(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Do'kon nomi"))
    legal_name = models.CharField(max_length=255, blank=True, verbose_name=_("Yuridik nom"))
    phone = models.CharField(max_length=20)
    address = models.TextField(verbose_name=_("To'liq manzil"))
    region = models.ForeignKey(UzRegion, on_delete=models.PROTECT, related_name='stores')
    district = models.ForeignKey(UzDistrict, on_delete=models.PROTECT, null=True, blank=True, related_name='stores')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    logo = models.ImageField(upload_to='stores/logos/', null=True, blank=True)

    owner = models.ForeignKey(
        TelegramUser,
        on_delete=models.PROTECT,
        related_name='owned_stores',
        limit_choices_to={'user_type': TelegramUser.USER_TYPE_SOTUVCHI},
        verbose_name=_("Egasi (sotuvchi)"),
    )

    commission_percent = models.DecimalField(
        max_digits=5, decimal_places=2,
        default=5.00,
        verbose_name=_("Komissiya foizi"),
    )
    contract_signed_at = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Do'kon")
        verbose_name_plural = _("Do'konlar")
        ordering = ['region__code', 'name']
        indexes = [models.Index(fields=['is_active', 'region'])]

    def __str__(self) -> str:
        return self.name


# ---------------------------------------------------------------------------
# 5.4. QRCodeBatch (YANGI)
# ---------------------------------------------------------------------------

class QRCodeBatch(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'
    STATUS_CHOICES = [
        (STATUS_PENDING, _("Kutilmoqda")),
        (STATUS_PROCESSING, _("Generatsiya jarayonida")),
        (STATUS_COMPLETED, _("Tayyor")),
        (STATUS_FAILED, _("Xatolik")),
    ]
    DELIVERY_NOT_SHIPPED = 'not_shipped'
    DELIVERY_SHIPPED = 'shipped'
    DELIVERY_DELIVERED = 'delivered'
    DELIVERY_STATUS_CHOICES = [
        (DELIVERY_NOT_SHIPPED, _("Hali jo'natilmagan")),
        (DELIVERY_SHIPPED, _("Jo'natildi")),
        (DELIVERY_DELIVERED, _("Yetkazib berildi")),
    ]

    name = models.CharField(max_length=100, verbose_name=_("Batch nomi"))
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name='batches')
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    points_per_code = models.IntegerField(default=50, validators=[MinValueValidator(1)])

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING, db_index=True)
    zip_file = models.FileField(upload_to='batches/', null=True, blank=True)
    error_message = models.TextField(blank=True)

    delivery_status = models.CharField(
        max_length=20, choices=DELIVERY_STATUS_CHOICES, default=DELIVERY_NOT_SHIPPED, db_index=True,
    )
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    delivered_by = models.CharField(max_length=255, blank=True, verbose_name=_("Agent ismi"))

    created_by = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='batches_created',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Batch")
        verbose_name_plural = _("Batch'lar")
        ordering = ['-created_at']
        unique_together = [('name', 'store')]
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['store', 'delivery_status']),
        ]

    def __str__(self) -> str:
        return f"{self.name} — {self.store.name}"

    @property
    def scanned_count(self) -> int:
        return self.qr_codes.filter(is_scanned=True).count()

    def activation_rate(self) -> float:
        return (self.scanned_count / self.quantity * 100) if self.quantity else 0.0


# ---------------------------------------------------------------------------
# 5.5. QRCode (mono'dan o'zgartirilgan)
# ---------------------------------------------------------------------------

class QRCode(models.Model):
    code = models.CharField(max_length=255, unique=True, db_index=True)
    hash_code = models.CharField(max_length=32, unique=True, db_index=True)
    serial_number = models.CharField(max_length=50, unique=True, db_index=True)
    image_path = models.CharField(max_length=500, null=True, blank=True)
    points = models.IntegerField(validators=[MinValueValidator(0)])

    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name='qr_codes', db_index=True)
    batch = models.ForeignKey(QRCodeBatch, on_delete=models.PROTECT, related_name='qr_codes', db_index=True)

    generated_at = models.DateTimeField(auto_now_add=True)
    scanned_at = models.DateTimeField(null=True, blank=True)
    scanned_by = models.ForeignKey(
        TelegramUser,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='scanned_qrcodes',
        limit_choices_to={'user_type': TelegramUser.USER_TYPE_SANTENIK},
    )
    is_scanned = models.BooleanField(default=False, db_index=True)
    is_deleted = models.BooleanField(default=False, db_index=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Skretch-karta (QR)")
        verbose_name_plural = _("Skretch-kartalar")
        ordering = ['-generated_at']
        indexes = [
            models.Index(fields=['store', 'is_scanned']),
            models.Index(fields=['batch', 'is_scanned']),
            models.Index(fields=['is_scanned', 'scanned_at']),
        ]

    def __str__(self) -> str:
        if len(self.code) <= 3:
            return self.code
        return f"{self.code[:2]}{'*' * (len(self.code) - 3)}{self.code[-1]}"


# ---------------------------------------------------------------------------
# 5.6. Scan / Promo audit
# ---------------------------------------------------------------------------

class QRCodeScanAttempt(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='scan_attempts')
    qr_code = models.ForeignKey(QRCode, on_delete=models.CASCADE, related_name='scan_attempts')
    attempted_at = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("QR skanlash urinishi")
        verbose_name_plural = _("QR skanlash urinishlari")
        ordering = ['-attempted_at']
        indexes = [models.Index(fields=['user', '-attempted_at'])]


class PromoCodeAttempt(models.Model):
    SOURCE_BOT = 'bot'
    SOURCE_WEBAPP = 'webapp'
    SOURCE_UNKNOWN = 'unknown'
    SOURCE_CHOICES = [
        (SOURCE_BOT, 'Bot'),
        (SOURCE_WEBAPP, 'WebApp'),
        (SOURCE_UNKNOWN, 'Unknown'),
    ]

    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='promo_attempts')
    raw_code = models.CharField(max_length=255, blank=True)
    attempted_at = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default=SOURCE_UNKNOWN)

    class Meta:
        verbose_name = _("Promo-kod urinishi")
        verbose_name_plural = _("Promo-kod urinishlari")
        ordering = ['-attempted_at']
        indexes = [
            models.Index(fields=['user', '-attempted_at']),
            models.Index(fields=['is_successful', '-attempted_at']),
        ]


# ---------------------------------------------------------------------------
# 5.7. SellerPointsTransaction (YANGI)
# ---------------------------------------------------------------------------

class SellerPointsTransaction(models.Model):
    TYPE_MANUAL_ADD = 'manual_add'
    TYPE_SALES_BONUS = 'sales_bonus'
    TYPE_CORRECTION = 'correction'
    TYPE_PENALTY = 'penalty'
    TRANSACTION_TYPE_CHOICES = [
        (TYPE_MANUAL_ADD, _("Admin qo'shdi")),
        (TYPE_SALES_BONUS, _("Sotuv bonusi")),
        (TYPE_CORRECTION, _("Tuzatish")),
        (TYPE_PENALTY, _("Jarima")),
    ]

    seller = models.ForeignKey(
        TelegramUser,
        on_delete=models.PROTECT,
        related_name='seller_transactions',
        limit_choices_to={'user_type': TelegramUser.USER_TYPE_SOTUVCHI},
    )
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name='seller_transactions')

    transaction_type = models.CharField(
        max_length=20, choices=TRANSACTION_TYPE_CHOICES, default=TYPE_MANUAL_ADD,
    )
    points = models.IntegerField(help_text=_("Musbat — qo'shish, manfiy — ayirish"))

    sales_amount_usd = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True,
        help_text=_("Ushbu tranzaksiya qaysi sotuvga bog'liq (ixtiyoriy)"),
    )
    period_start = models.DateField(null=True, blank=True)
    period_end = models.DateField(null=True, blank=True)
    note = models.TextField(blank=True)

    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Sotuvchi tranzaksiyasi")
        verbose_name_plural = _("Sotuvchi tranzaksiyalari")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['seller', '-created_at']),
            models.Index(fields=['store', '-created_at']),
        ]


# ---------------------------------------------------------------------------
# 5.8. Gift + GiftRedemption
# ---------------------------------------------------------------------------

class Gift(models.Model):
    name_uz_latin = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255, blank=True)
    description_uz_latin = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)
    image = models.ImageField(upload_to='gifts/')
    points_cost = models.IntegerField(validators=[MinValueValidator(1)])
    stock_quantity = models.IntegerField(null=True, blank=True, help_text=_("Bo'sh = cheksiz"))
    is_active = models.BooleanField(default=True, db_index=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Sovg'a")
        verbose_name_plural = _("Sovg'alar")
        ordering = ['order', 'points_cost']

    def __str__(self) -> str:
        return self.name_uz_latin


class GiftRedemption(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_SENT = 'sent'
    STATUS_COMPLETED = 'completed'
    STATUS_REJECTED = 'rejected'
    STATUS_NOT_RECEIVED = 'not_received'
    STATUS_CANCELLED_BY_USER = 'cancelled_by_user'
    STATUS_CHOICES = [
        (STATUS_PENDING, _("So'rov qabul qilindi")),
        (STATUS_APPROVED, _("Mahsulot tayyorlash bosqichida")),
        (STATUS_SENT, _("Yetkazib berishga topshirildi")),
        (STATUS_COMPLETED, _("Yetkazib berildi")),
        (STATUS_REJECTED, _("Bekor qilindi")),
        (STATUS_NOT_RECEIVED, _("Foydalanuvchi olmadi")),
        (STATUS_CANCELLED_BY_USER, _("Foydalanuvchi bekor qildi")),
    ]

    user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name='gift_redemptions',
        limit_choices_to={'user_type': TelegramUser.USER_TYPE_SANTENIK},
    )
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE, related_name='redemptions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING, db_index=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    admin_notes = models.TextField(blank=True)
    user_confirmed = models.BooleanField(default=False)
    user_comment = models.TextField(blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Sovg'a buyurtmasi")
        verbose_name_plural = _("Sovg'a buyurtmalari")
        ordering = ['-requested_at']
        indexes = [models.Index(fields=['status', '-requested_at'])]
        permissions = [
            ('change_status_call_center', 'Call Center: change redemption status'),
            ('change_status_agent', 'Agent: change status (sent/completed only)'),
        ]


# ---------------------------------------------------------------------------
# 5.9. MonthlyPromoTicket
# ---------------------------------------------------------------------------

class MonthlyPromoTicket(models.Model):
    month = models.DateField(db_index=True)
    qr_code = models.OneToOneField(QRCode, on_delete=models.CASCADE, related_name='monthly_ticket')
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='monthly_promo_tickets')
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name='monthly_tickets')
    order = models.PositiveIntegerField(db_index=True)
    scanned_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Oylik lotereya bileti")
        verbose_name_plural = _("Oylik lotereya biletlari")
        constraints = [
            models.UniqueConstraint(fields=['order'], name='uniq_ticket_order_global'),
        ]
        indexes = [
            models.Index(fields=['month', 'user']),
            models.Index(fields=['month', 'store']),
        ]


# ---------------------------------------------------------------------------
# 5.10. BroadcastMessage + RegionMessageLog
# ---------------------------------------------------------------------------

class BroadcastMessage(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_QUEUED = 'queued'
    STATUS_SENDING = 'sending'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'
    STATUS_CHOICES = [
        (STATUS_DRAFT, _("Qoralama")),
        (STATUS_QUEUED, _("Navbatda")),
        (STATUS_SENDING, _("Jo'natilmoqda")),
        (STATUS_COMPLETED, _("Tugadi")),
        (STATUS_FAILED, _("Xatolik")),
    ]

    title = models.CharField(max_length=200)
    text_uz = models.TextField(blank=True)
    text_ru = models.TextField(blank=True)
    image = models.ImageField(upload_to='broadcasts/', null=True, blank=True)

    user_type_filter = models.CharField(
        max_length=20, choices=TelegramUser.USER_TYPE_CHOICES, blank=True,
    )
    region_filter = models.ForeignKey(UzRegion, on_delete=models.SET_NULL, null=True, blank=True)
    store_filter = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True)
    language_filter = models.CharField(
        max_length=15, choices=TelegramUser.LANGUAGE_CHOICES, blank=True,
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    total_recipients = models.IntegerField(default=0)
    sent_count = models.IntegerField(default=0)
    failed_count = models.IntegerField(default=0)

    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Mass-rassilka")
        verbose_name_plural = _("Mass-rassilka'lar")
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title


class RegionMessageLog(models.Model):
    broadcast = models.ForeignKey(
        BroadcastMessage, on_delete=models.CASCADE, related_name='logs', null=True, blank=True,
    )
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='broadcast_logs')
    sent_at = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)

    class Meta:
        verbose_name = _("Rassilka log")
        verbose_name_plural = _("Rassilka loglari")
        ordering = ['-sent_at']
        indexes = [models.Index(fields=['broadcast', '-sent_at'])]


# ---------------------------------------------------------------------------
# 5.11. Promotion / PrivacyPolicy / AdminContactSettings
# ---------------------------------------------------------------------------

class Promotion(models.Model):
    title_uz = models.CharField(max_length=200)
    title_ru = models.CharField(max_length=200, blank=True)
    text_uz = models.TextField(blank=True)
    text_ru = models.TextField(blank=True)
    image = models.ImageField(upload_to='promotions/', null=True, blank=True)
    link = models.URLField(blank=True)

    is_active = models.BooleanField(default=True, db_index=True)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Promotsiya banneri")
        verbose_name_plural = _("Promotsiya bannerlari")
        ordering = ['order', '-created_at']

    def __str__(self) -> str:
        return self.title_uz


class PrivacyPolicy(models.Model):
    version = models.CharField(max_length=20, unique=True)
    text_uz = models.TextField()
    text_ru = models.TextField()
    pdf_uz = models.FileField(upload_to='privacy/', null=True, blank=True)
    pdf_ru = models.FileField(upload_to='privacy/', null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Maxfiylik siyosati")
        verbose_name_plural = _("Maxfiylik siyosatlari")
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Privacy v{self.version}"


class AdminContactSettings(models.Model):
    support_telegram = models.CharField(max_length=100, default='@jip_support')
    support_phone = models.CharField(max_length=30, blank=True)
    support_email = models.EmailField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Admin kontaktlari")
        verbose_name_plural = _("Admin kontaktlari")

    def __str__(self) -> str:
        return self.support_telegram


# ---------------------------------------------------------------------------
# 5.12. VideoInstruction
# ---------------------------------------------------------------------------

class VideoInstruction(models.Model):
    title_uz = models.CharField(max_length=200)
    title_ru = models.CharField(max_length=200, blank=True)
    video_uz = models.FileField(upload_to='videos/', null=True, blank=True)
    video_ru = models.FileField(upload_to='videos/', null=True, blank=True)
    file_id_uz = models.CharField(max_length=255, blank=True, help_text=_("Telegram file_id (cache)"))
    file_id_ru = models.CharField(max_length=255, blank=True)
    thumb_uz = models.ImageField(upload_to='videos/thumbs/', null=True, blank=True)
    thumb_ru = models.ImageField(upload_to='videos/thumbs/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Yo'riqnoma video")
        verbose_name_plural = _("Yo'riqnoma videolari")
        ordering = ['order']

    def __str__(self) -> str:
        return self.title_uz


# ---------------------------------------------------------------------------
# 5.13. LiveStream + LiveStreamWinner
# ---------------------------------------------------------------------------

class LiveStream(models.Model):
    STATUS_PLANNED = 'planned'
    STATUS_LIVE = 'live'
    STATUS_FINISHED = 'finished'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PLANNED, _("Rejalashtirilgan")),
        (STATUS_LIVE, _("Efirda")),
        (STATUS_FINISHED, _("Tugagan")),
        (STATUS_CANCELLED, _("Bekor qilingan")),
    ]

    title_uz = models.CharField(max_length=200)
    title_ru = models.CharField(max_length=200, blank=True)
    description_uz = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)
    stream_url = models.URLField()
    starts_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PLANNED, db_index=True)
    cover_image = models.ImageField(upload_to='livestreams/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Jonli efir")
        verbose_name_plural = _("Jonli efirlar")
        ordering = ['-starts_at']

    def __str__(self) -> str:
        return self.title_uz


class LiveStreamWinner(models.Model):
    live_stream = models.ForeignKey(LiveStream, on_delete=models.CASCADE, related_name='winners')
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='livestream_wins')
    prize_text_uz = models.CharField(max_length=255)
    prize_text_ru = models.CharField(max_length=255, blank=True)
    announced_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Efir g'olibi")
        verbose_name_plural = _("Efir g'oliblari")
        ordering = ['-announced_at']


# ---------------------------------------------------------------------------
# 5.14. Monthly reminders
# ---------------------------------------------------------------------------

class MonthlyReminderSettings(models.Model):
    is_enabled = models.BooleanField(default=True)
    text_uz = models.TextField(blank=True)
    text_ru = models.TextField(blank=True)
    send_day = models.IntegerField(default=1, help_text=_("Oyning qaysi kuni (1-28)"))
    send_hour = models.IntegerField(default=10)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Oylik eslatma sozlamalari")
        verbose_name_plural = _("Oylik eslatma sozlamalari")


class MonthlyReminderLog(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='reminder_logs')
    month = models.DateField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Oylik eslatma logi")
        verbose_name_plural = _("Oylik eslatma loglari")
        unique_together = [('user', 'month')]
        ordering = ['-sent_at']
