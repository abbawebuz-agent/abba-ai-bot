"""
Core models for the mona project.
"""
import hashlib
import secrets
import string
import random
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from simple_history.models import HistoricalRecords
from datetime import timedelta
from datetime import date


class UzRegion(models.Model):
    """Справочник вилоятов Узбекистана (код совпадает с region_filter рассылок)."""
    code = models.CharField(max_length=50, unique=True, db_index=True)
    name_uz = models.CharField(max_length=120)
    name_ru = models.CharField(max_length=120)

    class Meta:
        verbose_name = _('Viloyat')
        verbose_name_plural = _('Viloyatlar')
        ordering = ['code']

    def __str__(self):
        # Tilga qarab — UZ aktif bo'lsa name_uz, RU bo'lsa name_ru
        from django.utils.translation import get_language
        if get_language() and get_language().startswith('ru') and self.name_ru:
            return self.name_ru
        return self.name_uz or self.name_ru or self.code


class UzDistrict(models.Model):
    """Справочник туманов/районов внутри вилоята."""
    region = models.ForeignKey(
        UzRegion,
        on_delete=models.CASCADE,
        related_name='districts',
        db_index=True,
    )
    code = models.CharField(max_length=100, db_index=True)
    name_uz = models.CharField(max_length=120)
    name_ru = models.CharField(max_length=120)

    class Meta:
        verbose_name = _('Tuman')
        verbose_name_plural = _('Tumanlar')
        ordering = ['region__code', 'code']
        constraints = [
            models.UniqueConstraint(fields=['region', 'code'], name='uniq_district_per_region'),
        ]

    def __str__(self):
        from django.utils.translation import get_language
        if get_language() and get_language().startswith('ru') and self.name_ru:
            return self.name_ru
        return self.name_uz or self.name_ru or self.code


class Store(models.Model):
    """Do'kon — JIP loyalty platformasi yangi modeli.

    Har QR-batch bitta do'konga biriktiriladi. Sotuvchi (TelegramUser
    user_type='sotuvchi') bitta do'konning egasi bo'ladi.
    """

    name = models.CharField(max_length=255, verbose_name="Do'kon nomi")
    legal_name = models.CharField(
        max_length=255, blank=True, verbose_name="Yuridik nomi"
    )
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    address = models.TextField(verbose_name="To'liq manzil")

    region = models.ForeignKey(
        UzRegion,
        on_delete=models.PROTECT,
        related_name='stores',
        verbose_name='Viloyat',
    )
    district = models.ForeignKey(
        UzDistrict,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='stores',
        verbose_name='Tuman',
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    logo = models.ImageField(
        upload_to='stores/logos/', null=True, blank=True, verbose_name='Logo'
    )

    owner = models.ForeignKey(
        'TelegramUser',
        on_delete=models.PROTECT,
        related_name='owned_stores',
        limit_choices_to={'user_type': 'sotuvchi'},
        verbose_name="Egasi (sotuvchi)",
        null=True,
        blank=True,
        help_text="Bo'sh bo'lishi mumkin — admin keyinroq biriktiradi",
    )

    commission_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=5.00,
        verbose_name="Komissiya foizi",
    )
    contract_signed_at = models.DateField(
        null=True, blank=True, verbose_name="Shartnoma sanasi"
    )

    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Faol')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Do'kon"
        verbose_name_plural = "Do'konlar"
        ordering = ['region__code', 'name']
        indexes = [
            models.Index(fields=['is_active', 'region']),
        ]

    def __str__(self):
        return f"{self.name} ({self.region.code if self.region_id else '—'})"

    def total_qr_codes(self):
        """Do'konga biriktirilgan jami QR-kartalar soni."""
        return self.qr_codes.filter(is_deleted=False).count()

    def scanned_qr_codes(self):
        """Skanlangan kartalar soni."""
        return self.qr_codes.filter(is_scanned=True, is_deleted=False).count()

    def activation_rate(self):
        """Aktivatsiya darajasi (%)."""
        total = self.total_qr_codes()
        if not total:
            return 0
        return round(self.scanned_qr_codes() / total * 100, 2)


class TelegramUser(models.Model):
    """Модель пользователя Telegram (JIP — santenik va sotuvchi)."""
    USER_TYPE_CHOICES = [
        ('santenik', 'Santenik'),
        ('sotuvchi', 'Sotuvchi'),
    ]
    
    telegram_id = models.BigIntegerField(unique=True, db_index=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    region = models.ForeignKey(
        UzRegion,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='telegram_users',
        db_index=True,
        verbose_name='Viloyat',
    )
    district = models.ForeignKey(
        UzDistrict,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        db_index=True,
        verbose_name='Tuman',
    )
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        null=True,
        blank=True
    )
    points = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True, verbose_name='Faol', db_index=True)
    language = models.CharField(
        max_length=15,
        choices=[
            ('uz_latin', 'O\'zbek (Lotin)'),
            ('ru', 'Русский'),
        ],
        default='uz_latin',
        verbose_name='Til'
    )
    privacy_accepted = models.BooleanField(default=False, verbose_name='Maxfiylik siyosatiga rozilik')
    last_message_sent_at = models.DateTimeField(null=True, blank=True, verbose_name='Oxirgi xabar yuborilgan vaqt')
    blocked_bot_at = models.DateTimeField(null=True, blank=True, verbose_name='Botni bloklagan vaqt')
    # Поля для блокировки по неверным промокодам
    promo_failed_attempts = models.IntegerField(default=0, verbose_name='Noto‘g‘ri promokod urinishlari (ketma-ket)')
    promo_block_stage = models.IntegerField(
        default=0,
        verbose_name='Promokod bloklash bosqichi (0 — yo‘q, 3 — faqat eski cheksiz blok)'
    )
    promo_blocked_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Promokod kiritishni bloklash tugash vaqti'
    )
    # Sotuvchi tasdiqlash tizimi
    seller_approved = models.BooleanField(
        default=False,
        verbose_name='Sotuvchi tasdiqlangan',
        db_index=True,
        help_text='Faqat sotuvchilar uchun. Admin tasdiqlagunicha False.'
    )
    seller_approved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Tasdiqlangan vaqt'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = _('Telegram foydalanuvchisi')
        verbose_name_plural = _('Telegram foydalanuvchilari')
        ordering = ['region__code', 'district__code', '-created_at']
        permissions = [
            ('send_region_messages', 'Can send messages to users by region'),
            ('change_user_type_call_center', 'Call Center: Can change user type'),
        ]
    
    def update_location(self, *, use_nominatim=False):
        """
        Заполняет region/district по координатам.
        Порядок: 1) локальный GeoJSON мультиполигонов (admin_level=6), если файл задан;
        2) при use_nominatim — Nominatim + эвристика тумана; иначе — эвристика вилоят/туман.
        """
        if self.latitude is None or self.longitude is None:
            self.region = None
            self.district = None
            return

        from core.boundary_lookup import resolve_uz_from_boundary_geojson
        from core.geocoding import resolve_uz_region_district
        from core.regions import (
            get_closest_district_code_in_region,
            get_district_by_coordinates,
            get_region_by_coordinates,
        )

        def _district_heuristic(region_obj):
            dc, _ = get_district_by_coordinates(
                self.latitude, self.longitude, region_obj.code
            )
            if not dc:
                dc, _ = get_closest_district_code_in_region(
                    self.latitude, self.longitude, region_obj.code
                )
            if dc:
                return UzDistrict.objects.filter(region=region_obj, code=dc).first()
            return None

        br, bd = resolve_uz_from_boundary_geojson(self.latitude, self.longitude)
        if bd is not None:
            self.region = br
            self.district = bd
            return

        if use_nominatim:
            r_obj, d_obj = resolve_uz_region_district(self.latitude, self.longitude)
            if r_obj is not None:
                self.region = r_obj
                self.district = d_obj if d_obj and d_obj.region_id == r_obj.id else None
                # Nominatim часто даёт вилоят, но название тумана в OSM не совпадает с БД —
                # тогда дополняем туман эвристикой внутри уже выбранного вилоята.
                if not self.district_id:
                    self.district = _district_heuristic(r_obj)
                return

        region_code = get_region_by_coordinates(self.latitude, self.longitude)
        if not region_code:
            self.region = None
            self.district = None
            return

        try:
            self.region = UzRegion.objects.get(code=region_code)
        except UzRegion.DoesNotExist:
            self.region = None
            self.district = None
            return

        self.district = _district_heuristic(self.region)

    def refresh_location_from_geocoder(self):
        """Полное обновление вилоят/тумана с запросом к Nominatim (регистрация в боте, действие в админке)."""
        self.update_location(use_nominatim=True)

    def save(self, *args, **kwargs):
        """При полном save обновляет вилоят/туман только эвристикой, без Nominatim (см. refresh_location_from_geocoder)."""
        update_fields = kwargs.get('update_fields')
        if update_fields is not None:
            super().save(*args, **kwargs)
            return

        if self.latitude is not None and self.longitude is not None:
            should_geo = not self.pk
            if self.pk:
                prev = type(self).objects.filter(pk=self.pk).values('latitude', 'longitude').first()
                if prev:
                    should_geo = (
                        prev['latitude'] != self.latitude or prev['longitude'] != self.longitude
                    )
            if should_geo:
                self.update_location(use_nominatim=False)
        else:
            self.region = None
            self.district = None

        super().save(*args, **kwargs)

    def get_region(self):
        """Код вилоята из БД (без запросов к геокодеру). Для фильтров с координатами без FK см. get_user_region_code."""
        return self.region.code if self.region_id else None

    def get_region_display(self, language='ru'):
        """Название вилоята: из FK или подпись по эвристике координат (без Nominatim)."""
        from core.regions import get_region_by_coordinates, get_region_name

        code = self.region.code if self.region_id else None
        if code is None and self.latitude is not None and self.longitude is not None:
            code = get_region_by_coordinates(self.latitude, self.longitude)
        if code is None:
            return None
        return get_region_name(code, language)

    def get_district(self):
        """Код тумана из БД (без геокодера)."""
        return self.district.code if self.district_id else None

    def get_district_display(self, language='ru'):
        """Название тумана: из FK или эвристика по координатам (без Nominatim)."""
        from core.regions import (
            get_closest_district_code_in_region,
            get_district_by_coordinates,
            get_district_name,
            get_region_by_coordinates,
        )

        if self.district_id and self.region_id:
            return get_district_name(self.district.code, self.region.code, language)
        if self.latitude is None or self.longitude is None:
            return None
        region_code = self.region.code if self.region_id else get_region_by_coordinates(
            self.latitude, self.longitude
        )
        if region_code is None:
            return None
        district_code, _ = get_district_by_coordinates(
            self.latitude, self.longitude, region_code
        )
        if district_code is None:
            district_code, _ = get_closest_district_code_in_region(
                self.latitude, self.longitude, region_code
            )
        if district_code is None:
            return None
        return get_district_name(district_code, region_code, language)
    
    def calculate_points(self, force=False):
        """Рассчёт баллов:
        - santenik: QR-skanlardan jami − sovg'aga ketgan (faol redemption'lar)
        - sotuvchi: SellerPointsTransaction yig'indisi (musbat va manfiy)
        Redis cache 1 daqiqa.
        """
        from django.core.cache import cache

        cache_key = f'user_points_{self.id}'
        if not force:
            try:
                cached = cache.get(cache_key)
                if cached is not None:
                    return cached
            except Exception:
                pass  # Cache xato bo'lsa, qayta hisoblaymiz

        if self.user_type == 'sotuvchi':
            total = SellerPointsTransaction.objects.filter(
                seller=self,
            ).aggregate(total=models.Sum('points'))['total'] or 0
            calculated = max(0, total)
        else:
            # santenik (yoki rol belgilanmagan) — eski mantiq
            total_earned = QRCode.objects.filter(
                scanned_by=self, is_scanned=True, is_deleted=False,
            ).aggregate(total=models.Sum('points'))['total'] or 0

            total_spent = GiftRedemption.objects.filter(
                user=self
            ).exclude(
                status__in=['rejected', 'cancelled_by_user', 'not_received']
            ).aggregate(
                total=models.Sum('gift__points_cost')
            )['total'] or 0

            calculated = max(0, total_earned - total_spent)

        if self.points != calculated:
            TelegramUser.objects.filter(id=self.id).update(points=calculated)
            self.points = calculated

        try:
            cache.set(cache_key, calculated, 60)
        except Exception:
            pass  # Cache xato — DB qiymati yetarli
        return calculated
    
    def invalidate_points_cache(self):
        """Инвалидирует кеш баллов пользователя. Cache xato bo'lsa - sukut."""
        try:
            from django.core.cache import cache
            cache.delete(f'user_points_{self.id}')
        except Exception:
            # Redis/cache mavjud bo'lmasa, batch save'ni sindirmasin
            import logging
            logging.getLogger(__name__).warning(
                "invalidate_points_cache: cache xato (e'tibor berilmadi)"
            )
    
    # ──────────────────────────────────────────────────────────────────────
    # Promo code lock helpers
    # ──────────────────────────────────────────────────────────────────────
    def is_promo_code_blocked(self):
        """
        Проверяет, заблокирован ли пользователь для ввода промокодов.

        Логика: только блокировка на 1 день (нет 5 минут и навсегда).
        Returns (blocked: bool, block_type: str, blocked_until: datetime | None)
        block_type: 'none' | '1d' | 'permanent' (permanent только для старых записей)
        """
        now = timezone.now()

        # Старая перманентная блокировка (для обратной совместимости)
        if self.promo_block_stage >= 3:
            return True, 'permanent', None

        # Временная блокировка на день
        if self.promo_blocked_until and self.promo_blocked_until > now:
            return True, '1d', self.promo_blocked_until

        # Время блокировки истекло — снимаем
        if self.promo_blocked_until and self.promo_blocked_until <= now:
            self.promo_blocked_until = None
            self.promo_failed_attempts = 0
            TelegramUser.objects.filter(id=self.id).update(
                promo_blocked_until=None,
                promo_failed_attempts=0,
            )

        return False, 'none', None
    
    def register_invalid_promo_attempt(self, source: str, raw_code: str = ""):
        """
        Регистрирует неверную попытку ввода промокода.

        Алгоритм:
        - Счётчик только подряд: при верном вводе обнуляется (2 неверных + верный → с нуля).
        - 3 неверных подряд ИЛИ 3 неверных за текущий день → блокировка на 1 день (не на 5 минут и не навсегда).
        """
        from .models import PromoCodeAttempt

        now = timezone.now()
        today = now.date()

        # Всегда пишем попытку в лог
        PromoCodeAttempt.objects.create(
            user=self,
            raw_code=raw_code or "",
            attempted_at=now,
            is_successful=False,
            source=source,
        )

        if self.promo_block_stage >= 3:
            return {'blocked': True, 'block_type': 'permanent', 'blocked_until': None}

        if self.promo_blocked_until and self.promo_blocked_until > now:
            return {
                'blocked': True,
                'block_type': '1d',
                'blocked_until': self.promo_blocked_until,
            }

        # Сколько неверных попыток сегодня (уже с учётом только что созданной)
        today_failed = PromoCodeAttempt.objects.filter(
            user=self,
            is_successful=False,
            attempted_at__date=today,
        ).count()

        if today_failed >= 3:
            # Лимит дня: 3 неверных в день → блок на 1 день
            self.promo_blocked_until = now + timedelta(days=1)
            self.promo_failed_attempts = 0
            TelegramUser.objects.filter(id=self.id).update(
                promo_blocked_until=self.promo_blocked_until,
                promo_failed_attempts=0,
            )
            return {
                'blocked': True,
                'block_type': '1d',
                'blocked_until': self.promo_blocked_until,
            }

        # Увеличиваем только подряд идущие неверные
        consecutive = (self.promo_failed_attempts or 0) + 1
        self.promo_failed_attempts = consecutive

        if consecutive >= 3:
            self.promo_blocked_until = now + timedelta(days=1)
            self.promo_failed_attempts = 0
            TelegramUser.objects.filter(id=self.id).update(
                promo_failed_attempts=0,
                promo_blocked_until=self.promo_blocked_until,
            )
            return {
                'blocked': True,
                'block_type': '1d',
                'blocked_until': self.promo_blocked_until,
            }

        TelegramUser.objects.filter(id=self.id).update(
            promo_failed_attempts=self.promo_failed_attempts,
        )
        return {'blocked': False, 'block_type': 'none', 'blocked_until': None}
    
    def register_successful_promo(self, raw_code: str = "", source: str = ""):
        """
        Фиксирует успешный ввод промокода и обнуляет счётчик подряд идущих
        неверных попыток (2 неверных + верный → счётчик с нуля).
        """
        from .models import PromoCodeAttempt

        now = timezone.now()

        PromoCodeAttempt.objects.create(
            user=self,
            raw_code=raw_code or "",
            attempted_at=now,
            is_successful=True,
            source=source or 'unknown',
        )

        if self.promo_block_stage < 3:
            self.promo_failed_attempts = 0
            if self.promo_blocked_until and self.promo_blocked_until <= now:
                self.promo_blocked_until = None

            TelegramUser.objects.filter(id=self.id).update(
                promo_failed_attempts=self.promo_failed_attempts,
                promo_blocked_until=self.promo_blocked_until,
            )
    
    def __str__(self):
        return f"{self.first_name or 'Unknown'} (@{self.username or 'no_username'})"


class PendingSellerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type='sotuvchi', seller_approved=False)


class PendingSellerRequest(TelegramUser):
    """Tasdiqlanmagan sotuvchi arizalari — proxy model (alohida admin menyusi uchun)."""

    objects = PendingSellerManager()

    class Meta:
        proxy = True
        verbose_name = "Zapros (sotuvchi arizasi)"
        verbose_name_plural = "Zaproslar"


class SellerRegistrationCode(models.Model):
    """Sotuvchi ro'yxatdan o'tishi uchun bir martalik 8 raqamli unikal ID."""
    code = models.CharField(max_length=8, unique=True, verbose_name='ID (8 raqam)')
    label = models.CharField(max_length=255, blank=True, verbose_name='Izoh (ixtiyoriy)')
    is_used = models.BooleanField(default=False, db_index=True, verbose_name='Ishlatilgan')
    used_by = models.ForeignKey(
        TelegramUser, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='seller_codes',
        verbose_name='Kim ishlatdi',
    )
    used_at = models.DateTimeField(null=True, blank=True, verbose_name='Ishlatilgan vaqt')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Sotuvchi ID"
        verbose_name_plural = "Sotuvchi IDlari"
        ordering = ['-created_at']

    def __str__(self):
        used_info = f' — {self.used_by.first_name or self.used_by.telegram_id}' if self.is_used and self.used_by else ''
        return f'{self.code}{used_info}'

    @classmethod
    def generate_unique_code(cls):
        import random
        for _ in range(20):
            code = str(random.randint(10000000, 99999999))
            if not cls.objects.filter(code=code).exists():
                return code
        raise ValueError('Unikal ID yaratib bo\'lmadi — qayta urinib ko\'ring')


class QRCodeBatch(models.Model):
    """Skretch-karta partiyasi — JIP loyalty yangi modeli.

    Har batch bitta do'konga biriktiriladi. Admin batch yaratganda
    Celery `generate_batch_zip` task QR rasm va ZIP yaratadi.
    """

    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('processing', 'Generatsiya jarayonida'),
        ('completed', 'Tayyor'),
        ('failed', 'Xatolik'),
    ]
    DELIVERY_STATUS_CHOICES = [
        ('not_shipped', "Hali jo'natilmagan"),
        ('shipped', "Jo'natildi"),
        ('delivered', 'Yetkazib berildi'),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name="Batch nomi",
        help_text="Avtomatik: STORE-MAY-2026-001",
    )
    seller = models.ForeignKey(
        'TelegramUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='seller_batches',
        limit_choices_to={'user_type': 'sotuvchi'},
        verbose_name='Sotuvchi',
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.PROTECT,
        related_name='batches',
        verbose_name="Do'kon",
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Miqdor (kartalar soni)',
    )
    points_per_code = models.IntegerField(
        default=50,
        validators=[MinValueValidator(1)],
        verbose_name='Har karta uchun ball',
    )

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending',
        verbose_name='Holat',
    )
    zip_file = models.FileField(
        upload_to='batches/', null=True, blank=True, verbose_name='ZIP fayl',
    )
    error_message = models.TextField(blank=True, verbose_name='Xato xabari')

    delivery_status = models.CharField(
        max_length=20,
        choices=DELIVERY_STATUS_CHOICES,
        default='not_shipped',
        verbose_name='Yetkazib berish holati',
    )
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    delivered_by = models.CharField(
        max_length=255, blank=True, verbose_name='Agent ismi',
    )

    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='batches_created',
        verbose_name="Kim yaratgan",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Batch'
        verbose_name_plural = "Batch'lar"
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'store'], name='uniq_batch_name_per_store',
            ),
        ]
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['store', 'delivery_status']),
        ]

    def __str__(self):
        return f"{self.name} → {self.store.name} ({self.quantity} dona)"

    @classmethod
    def generate_name(cls, store):
        """Avtomatik batch nomi: STORE{ID}-{MAY}-{2026}-{001}."""
        now = timezone.now()
        month_str = now.strftime('%b').upper()
        year_str = now.year
        prefix = f"STORE{store.id}-{month_str}-{year_str}"
        existing = cls.objects.filter(
            store=store,
            name__startswith=prefix,
        ).count()
        return f"{prefix}-{existing + 1:03d}"

    def activation_rate(self):
        """Skanlash darajasi (%)."""
        scanned = self.qr_codes.filter(is_scanned=True).count()
        return round((scanned / self.quantity * 100), 2) if self.quantity else 0


class QRCode(models.Model):
    """Модель QR-кода (скретч-карты) — JIP yangi struktura.

    Endi har QR-karta do'kon (`store`) va batch (`batch`) ga biriktirilgan.
    Eski `code_type` field deprecated — faqat santenik foydalanishi mumkin.
    """

    code = models.CharField(max_length=255, unique=True, db_index=True)
    hash_code = models.CharField(max_length=32, unique=True, db_index=True)
    serial_number = models.CharField(max_length=50, unique=True, db_index=True, verbose_name='Seriya raqami')
    image_path = models.CharField(max_length=500, null=True, blank=True)
    points = models.IntegerField(validators=[MinValueValidator(0)])

    # JIP-yangi bog'lanishlar
    store = models.ForeignKey(
        Store,
        on_delete=models.PROTECT,
        related_name='qr_codes',
        db_index=True,
        null=True,  # Eski ma'lumotlar uchun — migration'da default LEGACY_STORE
        blank=True,
        verbose_name="Do'kon",
    )
    batch = models.ForeignKey(
        QRCodeBatch,
        on_delete=models.PROTECT,
        related_name='qr_codes',
        db_index=True,
        null=True,
        blank=True,
        verbose_name='Batch',
    )

    generated_at = models.DateTimeField(auto_now_add=True)
    scanned_at = models.DateTimeField(null=True, blank=True)
    scanned_by = models.ForeignKey(
        TelegramUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='scanned_qrcodes',
        limit_choices_to={'user_type': 'santenik'},
    )
    is_scanned = models.BooleanField(default=False, db_index=True)
    is_deleted = models.BooleanField(default=False, db_index=True, verbose_name=_('Oʻchirilgan (yumshoq)'))

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Skretch-karta (QR)')
        verbose_name_plural = _('Skretch-kartalar')
        ordering = ['-generated_at']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['hash_code']),
            models.Index(fields=['is_scanned']),
            models.Index(fields=['store', 'is_scanned']),
            models.Index(fields=['batch', 'is_scanned']),
        ]
        permissions = [
            ('view_qrcode_detail', 'Can view QR code details'),
            ('generate_qrcodes', 'Can generate QR codes'),
        ]
    
    def __str__(self):
        """Маскирует код (JIPABC123 → JI*****3)."""
        if len(self.code) > 5:
            prefix = self.code[:2]
            suffix = self.code[-1]
            masked = '*' * max(1, len(self.code) - 3)
            masked_code = f"{prefix}{masked}{suffix}"
        else:
            masked_code = self.code
        store_name = self.store.name if self.store_id else 'NO-STORE'
        return f"{masked_code} → {store_name}"

    @classmethod
    def generate_hash(cls, length=6):
        """
        Генерирует уникальный короткий хеш для QR-кода.
        
        Args:
            length: Длина хеша (минимум 6 символов, по умолчанию 6)
        
        Returns:
            str: Уникальный хеш-код из букв и цифр
        """
        # Используем буквы и цифры для более короткого кода
        characters = string.ascii_uppercase + string.digits
        
        # Убираем похожие символы для избежания путаницы (0, O, I, 1)
        characters = ''.join(c for c in characters if c not in '0O1I')
        
        max_attempts = 1000  # Защита от бесконечного цикла
        attempts = 0
        
        while attempts < max_attempts:
            # Генерируем случайный код заданной длины
            hash_code = ''.join(random.choice(characters) for _ in range(length))
            
            # Проверяем уникальность
            if not cls.objects.filter(hash_code=hash_code).exists():
                return hash_code
            
            attempts += 1
        
        # Если не удалось найти уникальный код за 1000 попыток, увеличиваем длину
        if attempts >= max_attempts:
            return cls.generate_hash(length + 1)
    
    @classmethod
    def generate_serial_number(cls, batch):
        """Batch ichida unique serial: STORE{store_id}-B{batch_id}-{NNNNN}."""
        prefix = f"S{batch.store_id}B{batch.id}"
        existing_count = cls.objects.filter(batch=batch).count()
        new_num = existing_count + 1
        serial_number = f"{prefix}-{new_num:05d}"

        max_attempts = 1000
        attempts = 0
        while cls.objects.filter(serial_number=serial_number).exists() and attempts < max_attempts:
            new_num += 1
            serial_number = f"{prefix}-{new_num:05d}"
            attempts += 1

        return serial_number

    @classmethod
    def create_code(cls, batch, points=None):
        """Yangi QR-karta yaratish — batch + store kontekstida.

        Kod format: JIP{hash}. Prefix endi konfiguratsiya emas, hardcoded.
        """
        hash_code = cls.generate_hash()
        code = f"JIP{hash_code}"

        if points is None:
            points = batch.points_per_code

        # Create QR first, then update serial number (needs ID)
        qr = cls.objects.create(
            code=code,
            hash_code=hash_code,
            serial_number=f"TEMP-{hash_code}",
            points=points,
            store=batch.store,
            batch=batch,
        )
        qr.serial_number = cls.generate_serial_number(batch)
        qr.save(update_fields=['serial_number'])
        return qr


class MonthlyPromoTicket(models.Model):
    """
    Билет месячного розыгрыша = один отсканированный QR-промокод.

    Создаётся в момент успешной активации QR-кода. `order` — порядковый
    номер билета внутри (month, user_type), нужен для аудита/розыгрыша.
    Количество шансов пользователя в месяце = count его билетов в этом месяце.
    """

    month = models.DateField(db_index=True, verbose_name='Oy (1-kun)')
    qr_code = models.OneToOneField(
        'QRCode',
        on_delete=models.CASCADE,
        related_name='monthly_ticket',
        verbose_name='QR-promokod',
    )
    user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name='monthly_promo_tickets',
        verbose_name=_('Member'),
    )
    user_type = models.CharField(
        max_length=20,
        choices=TelegramUser.USER_TYPE_CHOICES,
        db_index=True,
        verbose_name='Foydalanuvchi turi',
        default='santenik',
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.PROTECT,
        related_name='monthly_tickets',
        null=True,
        blank=True,
        verbose_name="Do'kon",
    )
    order = models.PositiveIntegerField(
        db_index=True,
        verbose_name='Bilet №',
        help_text='Глобальный порядковый номер билета по user_type (не сбрасывается каждый месяц).',
    )
    scanned_at = models.DateTimeField(verbose_name='Skanerlash vaqti')
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Monthly promo ticket'
        verbose_name_plural = 'Monthly promo tickets'
        ordering = ['-month', 'user_type', 'order']
        constraints = [
            models.UniqueConstraint(
                fields=['user_type', 'order'],
                name='uniq_ticket_order_global_per_type',
            ),
        ]
        indexes = [
            models.Index(fields=['month', 'user'], name='idx_ticket_month_user'),
            models.Index(fields=['month', 'store'], name='idx_ticket_month_store'),
        ]

    def __str__(self):
        return f"{self.month} {self.user_type} #{self.order} — qr {self.qr_code_id}"

    @staticmethod
    def month_start(d) -> date:
        if hasattr(d, 'date'):
            d = d.date()
        return date(d.year, d.month, 1)


class QRCodeScanAttempt(models.Model):
    """Модель для отслеживания попыток сканирования QR-кода."""
    user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name='scan_attempts'
    )
    qr_code = models.ForeignKey(
        QRCode,
        on_delete=models.CASCADE,
        related_name='scan_attempts'
    )
    attempted_at = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = _('Skanerlash urinishi')
        verbose_name_plural = _('Skanerlash urinishlari')
        ordering = ['-attempted_at']
        # Удален unique_together, так как пользователь может делать несколько попыток сканирования одного QR-кода
    
    def __str__(self):
        status = 'Muvaffaqiyatli' if self.is_successful else 'Muvaffaqiyatsiz'
        # Для коротких кодов показываем полностью или первые символы
        code_display = self.qr_code.code if len(self.qr_code.code) <= 10 else f"{self.qr_code.code[:10]}..."
        return f"{self.user} - {code_display} - {status}"


class SellerPointsTransaction(models.Model):
    """Sotuvchi balansidagi tranzaksiya — JIP yangi modeli.

    Sotuvchi ball faqat admin tomonidan qo'shiladi (santenik avtomatik).
    Sotuvchi sovg'aga ayirboshlamaydi — faqat balansni ko'radi.
    """

    TRANSACTION_TYPE_CHOICES = [
        ('manual_add', "Admin qo'shdi"),
        ('sales_bonus', 'Sotuv bonusi'),
        ('bonus', 'Batch bonusi'),
        ('correction', 'Tuzatish'),
        ('penalty', 'Jarima'),
    ]

    seller = models.ForeignKey(
        'TelegramUser',
        on_delete=models.PROTECT,
        related_name='seller_transactions',
        limit_choices_to={'user_type': 'sotuvchi'},
        verbose_name='Sotuvchi',
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.PROTECT,
        related_name='seller_transactions',
        verbose_name="Do'kon",
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPE_CHOICES,
        default='manual_add',
        verbose_name='Tur',
    )
    points = models.IntegerField(
        help_text="Musbat — qo'shish, manfiy — ayirish",
        verbose_name='Ballar',
    )

    sales_amount_usd = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Sotuv summasi ($)",
        help_text="Tranzaksiya bog'liq sotuv summasi (ixtiyoriy)",
    )
    period_start = models.DateField(null=True, blank=True, verbose_name='Davr (boshlanish)')
    period_end = models.DateField(null=True, blank=True, verbose_name='Davr (tugash)')
    note = models.TextField(blank=True, verbose_name='Izoh')

    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='seller_transactions_created',
        verbose_name="Kim qo'shgan",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Sotuvchi tranzaksiyasi'
        verbose_name_plural = 'Sotuvchi tranzaksiyalari'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['seller', '-created_at']),
            models.Index(fields=['store', '-created_at']),
        ]
        permissions = [
            ('add_seller_points', 'Can add points to seller'),
        ]

    def __str__(self):
        sign = '+' if self.points >= 0 else ''
        return f"{self.seller} | {sign}{self.points} | {self.created_at:%Y-%m-%d}"


class Gift(models.Model):
    """Модель подарка — faqat santenik uchun (TZ: user_type olib tashlangan)."""

    name_uz_latin = models.CharField(max_length=255, verbose_name='Nomi (O\'zbek lotin)')
    name_ru = models.CharField(max_length=255, blank=True, verbose_name='Nomi (Ruscha)')
    description_uz_latin = models.TextField(blank=True, verbose_name='Tavsif (O\'zbek lotin)')
    description_ru = models.TextField(blank=True, verbose_name='Tavsif (Ruscha)')
    image = models.ImageField(upload_to='gifts/', verbose_name='Rasm')
    points_cost = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Ballar narxi'
    )
    stock_quantity = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Zaxira miqdori',
        help_text="Bo'sh qoldirilsa, cheksiz",
    )
    is_active = models.BooleanField(default=True, verbose_name='Faol')
    order = models.IntegerField(default=0, verbose_name='Tartib raqami', help_text='Kichikroq raqam yuqorida ko\'rsatiladi')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Sovg‘a')
        verbose_name_plural = _('Sovg‘alar ro‘yxati')
        ordering = ['order', 'points_cost', 'name_uz_latin']
        indexes = [
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.name_uz_latin} ({self.points_cost} ball)"
    
    def get_name(self, language='uz_latin'):
        """
        Возвращает название подарка на указанном языке.
        
        Args:
            language: Язык ('uz_latin' или 'ru')
        
        Returns:
            str: Название подарка на указанном языке
        """
        if language == 'ru' and self.name_ru:
            return self.name_ru
        return self.name_uz_latin or self.name_ru or ''


class GiftRedemption(models.Model):
    """Модель получения подарка пользователем."""
    STATUS_CHOICES = [
        ('pending', _('So\'rov qabul qilindi')),
        ('approved', _('Mahsulot tayyorlash bosqichida')),
        ('sent', _('Mahsulot yetkazib berish xizmatiga topshirildi')),
        ('completed', _('Mahsulotni qabul qilganingizni tasdiqlang')),
        ('rejected', _('So\'rov bekor qilindi (administrator bilan bog\'laning)')),
        ('not_received', _('Sovg\'a berilmagan (foydalanuvchi olmadi)')),
        ('cancelled_by_user', _('Foydalanuvchi tomonidan bekor qilindi')),
    ]

    user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name='gift_redemptions',
        verbose_name=_('Member'),
        limit_choices_to={'user_type': 'santenik'},
    )
    gift = models.ForeignKey(
        Gift,
        on_delete=models.CASCADE,
        related_name='redemptions',
        verbose_name='Sovg\'a'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Holat'
    )
    requested_at = models.DateTimeField(auto_now_add=True, verbose_name='So\'ralgan vaqt')
    admin_notes = models.TextField(blank=True, verbose_name='Administrator eslatmalari')
    # Поле delivery_status удалено - теперь используется только status
    user_confirmed = models.BooleanField(default=False, verbose_name='Foydalanuvchi tomonidan tasdiqlandi')
    user_comment = models.TextField(blank=True, verbose_name='Foydalanuvchi sharhi')
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name='Tasdiqlangan vaqt')
    
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = _('Sovg‘a olish uchun arizalar')
        verbose_name_plural = _('Sovg‘a olish uchun arizalar')
        ordering = ['-requested_at']
        permissions = [
            ('change_status_call_center', 'Call Center: Can change redemption status'),
            ('change_status_agent', 'Agent: Can change redemption status (sent/completed only)'),
        ]
    
    def __str__(self):
        gift_name = self.gift.name_uz_latin or self.gift.name_ru or 'Подарок'
        return f"{self.user} - {gift_name} ({self.get_status_display()})"


class BroadcastMessage(models.Model):
    """Модель для массовых рассылок."""
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('sending', _('Sending')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
    ]
    
    title = models.CharField(max_length=255, verbose_name='Yuborish nomi')
    message_text = models.TextField(verbose_name='Xabar matni')
    image = models.ImageField(
        upload_to='broadcasts/',
        verbose_name='Rasm',
        null=True,
        blank=True,
        help_text='Ixtiyoriy. Rasm qo\'shilsa, xabar caption sifatida yuboriladi. HTML formatlash va havolalar qo\'llab-quvvatlanadi.'
    )
    user_type_filter = models.CharField(
        max_length=20,
        choices=TelegramUser.USER_TYPE_CHOICES,
        null=True,
        blank=True,
        verbose_name='Foydalanuvchi turi bo\'yicha filtr'
    )
    # Фильтрация по региону
    REGION_CHOICES = [
        ('', 'Barcha viloyatlar'),  # Все области
        ('tashkent_city', 'Toshkent shahri'),
        ('tashkent_region', 'Toshkent viloyati'),
        ('andijan', 'Andijon viloyati'),
        ('bukhara', 'Buxoro viloyati'),
        ('jizzakh', 'Jizzax viloyati'),
        ('kashkadarya', 'Qashqadaryo viloyati'),
        ('navoi', 'Navoiy viloyati'),
        ('namangan', 'Namangan viloyati'),
        ('samarkand', 'Samarqand viloyati'),
        ('surkhandarya', 'Surxondaryo viloyati'),
        ('syrdarya', 'Sirdaryo viloyati'),
        ('fergana', 'Farg\'ona viloyati'),
        ('khorezm', 'Xorazm viloyati'),
        ('karakalpakstan', 'Qoraqalpog\'iston Respublikasi'),
    ]
    region_filter = models.CharField(
        max_length=50,
        choices=REGION_CHOICES,
        null=True,
        blank=True,
        verbose_name='Viloyat bo\'yicha filtr',
        help_text='Tanlangan viloyatdagi foydalanuvchilarga xabar yuborish uchun viloyatni tanlang. Bo\'sh qoldirilsa, barcha viloyatlarga yuboriladi.'
    )
    # Фильтр по языку
    LANGUAGE_CHOICES = [
        ('uz_latin', 'O\'zbek (Lotin)'),
        ('ru', 'Русский'),
    ]
    language_filter = models.CharField(
        max_length=15,
        choices=LANGUAGE_CHOICES,
        null=True,
        blank=True,
        verbose_name='Til bo\'yicha filtr'
    )
    store_filter = models.ForeignKey(
        Store,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='broadcasts',
        verbose_name="Do'kon bo'yicha filtr",
        help_text="Tanlangan do'kon foydalanuvchilariga (sotuvchilar yoki uning santeniklariga).",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Holat'
    )
    total_users = models.IntegerField(default=0, verbose_name='Jami foydalanuvchilar')
    sent_count = models.IntegerField(default=0, verbose_name='Yuborildi')
    failed_count = models.IntegerField(default=0, verbose_name='Xatolar')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan')
    started_at = models.DateTimeField(null=True, blank=True, verbose_name='Yuborish boshlangan')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Yakunlangan')
    
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = _('Xabarlar yuborish')
        verbose_name_plural = _('Xabarlar yuborish')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


class RegionMessageLog(models.Model):
    """Лог рассылки по области (результаты Celery-задачи)."""
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('running', _('Running')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
        ('cancelled', _('Cancelled')),
    ]
    region_code = models.CharField(max_length=50, verbose_name='Область', db_index=True)
    user_type_filter = models.CharField(max_length=20, null=True, blank=True, verbose_name='Фильтр типа')
    language_filter = models.CharField(max_length=15, null=True, blank=True, verbose_name='Фильтр языка')
    total = models.IntegerField(default=0, verbose_name='Всего получателей')
    sent_count = models.IntegerField(default=0, verbose_name='Отправлено')
    failed_count = models.IntegerField(default=0, verbose_name='Ошибок')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='running', db_index=True)
    initiated_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Запустил'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Запущена')
    scheduled_at = models.DateTimeField(
        null=True, blank=True, db_index=True,
        verbose_name='Запланирована на',
        help_text='Время отправки для отложенной рассылки.'
    )
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Завершена')
    error_message = models.TextField(blank=True, verbose_name='Сообщение об ошибке')
    message_text = models.TextField(blank=True, verbose_name='Текст сообщения')
    image_storage_path = models.CharField(
        max_length=500, blank=True,
        verbose_name='Путь к фото',
        help_text='Относительный путь в default_storage; используется для отложенной рассылки.'
    )

    class Meta:
        verbose_name = _('Лог рассылки по области')
        verbose_name_plural = _('Логи рассылок по областям')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.region_code} — {self.sent_count}/{self.total} ({self.get_status_display()})"


class Promotion(models.Model):
    """Модель для акций/баннеров в слайдере Web App."""
    title = models.CharField(max_length=255, verbose_name='Sarlavha', blank=True, null=True)
    image = models.ImageField(upload_to='promotions/', verbose_name='Rasm')
    date = models.DateField(verbose_name='Sana', blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='Faol', db_index=True)
    order = models.IntegerField(default=0, verbose_name='Tartib raqami', help_text='Kichikroq raqam yuqorida ko\'rsatiladi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Yangilangan')
    
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = _('Aksiya')
        verbose_name_plural = _('Aksiyalar')
        ordering = ['order', '-created_at']
        indexes = [
            models.Index(fields=['is_active', 'order']),
        ]
    
    def __str__(self):
        if self.date:
            date_str = self.date.strftime('%d.%m.%Y')
        else:
            date_str = "Sana yo'q"
        title_str = self.title or "—"
        return f"{title_str} ({date_str})"


class PrivacyPolicy(models.Model):
    """Модель для политики конфиденциальности."""
    pdf_uz_latin = models.FileField(blank=True, null=True, upload_to='privacy_policy/', verbose_name='PDF файл (O\'zbek lotin)', help_text='PDF файл политики конфиденциальности для узбекского языка (латиница)')
    pdf_ru = models.FileField(blank=True, null=True, upload_to='privacy_policy/', verbose_name='PDF файл (Ruscha)', help_text='PDF файл политики конфиденциальности для русского языка')
    is_active = models.BooleanField(default=True, verbose_name='Faol')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Yangilangan')
    
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = _('Maxfiylik siyosati')
        verbose_name_plural = _('Maxfiylik siyosati')
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Maxfiylik siyosati (Yangilangan: {self.updated_at.strftime('%d.%m.%Y %H:%M')})"



class PromoCodeAttempt(models.Model):
    """
    Лог попыток ввода промокода (короткий код / hash) пользователем.
    
    Используется для:
    - анализа подозрительной активности (возможный мошенник)
    - применения алгоритма блокировки по неверным вводам
    """
    SOURCE_CHOICES = [
        ('bot', 'Telegram bot'),
        ('webapp', 'Telegram Web App'),
        ('unknown', 'Unknown'),
    ]
    
    user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name='promo_code_attempts',
        verbose_name='Foydalanuvchi',
    )
    raw_code = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Kiritilgan promokod',
        help_text='Foydalanuvchi kiritgan asl matn (kod mavjud bo‘lmasligi mumkin)',
    )
    attempted_at = models.DateTimeField(auto_now_add=True, verbose_name='Urinish vaqti')
    is_successful = models.BooleanField(default=False, verbose_name='Muvaffaqiyatli')
    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default='unknown',
        verbose_name='Manba',
        help_text='Qayerdan kiritilgan: bot yoki Web App',
    )
    
    class Meta:
        verbose_name = _('Promokod urinishlari')
        verbose_name_plural = _('Promokod urinishlari')
        ordering = ['-attempted_at']
        indexes = [
            models.Index(fields=['attempted_at']),
            models.Index(fields=['source']),
            models.Index(fields=['is_successful']),
        ]
    
    def __str__(self):
        status = '✅' if self.is_successful else '❌'
        src = dict(self.SOURCE_CHOICES).get(self.source, self.source)
        return f"{status} {self.user} — {self.raw_code or '—'} ({src})"


class AdminContactSettings(models.Model):
    """Модель для настроек контакта администратора в Web App."""
    CONTACT_TYPE_CHOICES = [
        ('telegram', 'Telegram username'),
        ('phone', 'Telefon raqami'),
        ('link', 'Havola (URL)'),
    ]
    
    contact_type = models.CharField(
        max_length=20,
        choices=CONTACT_TYPE_CHOICES,
        default='telegram',
        verbose_name='Kontakt turi',
        help_text='Telegram username, telefon raqami yoki havola'
    )
    contact_value = models.CharField(
        max_length=255,
        verbose_name='Kontakt qiymati',
        help_text='Telegram username (@ belgisisiz), telefon raqami (+998901234567) yoki to\'liq havola (https://...)'
    )
    is_active = models.BooleanField(default=True, verbose_name='Faol')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Yangilangan')
    
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = _('Admin kontakt sozlamalari')
        verbose_name_plural = _('Admin kontakt sozlamalari')
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.get_contact_type_display()}: {self.contact_value}"
    
    def get_contact_url(self):
        """Возвращает URL для контакта в зависимости от типа."""
        if self.contact_type == 'telegram':
            # Убираем @ если есть
            username = self.contact_value.lstrip('@')
            return f"https://t.me/{username}"
        elif self.contact_type == 'phone':
            # Для телефона возвращаем сам номер (tel: не поддерживается в Telegram Web App)
            # Telegram Web App не поддерживает tel: протокол, поэтому возвращаем просто номер
            return self.contact_value
        elif self.contact_type == 'link':
            # Возвращаем ссылку как есть
            return self.contact_value
        return None
    
    @classmethod
    def get_active_contact(cls):
        """Возвращает первую активную настройку контакта (для обратной совместимости)."""
        return cls.get_active_contacts().first()

    @classmethod
    def get_active_contacts(cls):
        """Возвращает все активные настройки контакта (Telegram, телефон, ссылка)."""
        return cls.objects.filter(is_active=True).order_by('contact_type', '-updated_at')


class VideoInstruction(models.Model):
    """Модель для видео инструкций. 4 видео: электрики (UZ/RU) и предприниматели (UZ/RU)."""
    # Электрики
    video_electrician_uz = models.FileField(
        upload_to='video_instructions/',
        null=True, blank=True,
        verbose_name='Video — Elektrik (O\'zbek)',
        help_text='Video fayl elektriklar uchun o\'zbek tilida'
    )
    video_electrician_ru = models.FileField(
        upload_to='video_instructions/',
        null=True, blank=True,
        verbose_name='Video — Elektrik (Ruscha)',
        help_text='Video fayl elektriklar uchun rus tilida'
    )
    thumb_electrician_uz = models.ImageField(
        upload_to='video_instructions/thumbs/',
        null=True, blank=True,
        verbose_name='Thumbnail — Elektrik (O\'zbek)',
        help_text='JPEG, max 320x320, 200KB. Oldindan ko\'rinish uchun.'
    )
    thumb_electrician_ru = models.ImageField(
        upload_to='video_instructions/thumbs/',
        null=True, blank=True,
        verbose_name='Thumbnail — Elektrik (Ruscha)',
        help_text='JPEG, max 320x320, 200KB. Превью для видео.'
    )
    # Предприниматели (продавцы)
    video_seller_uz = models.FileField(
        upload_to='video_instructions/',
        null=True, blank=True,
        verbose_name='Video — Tadbirkor (O\'zbek)',
        help_text='Video fayl tadbirkorlar uchun o\'zbek tilida'
    )
    video_seller_ru = models.FileField(
        upload_to='video_instructions/',
        null=True, blank=True,
        verbose_name='Video — Tadbirkor (Ruscha)',
        help_text='Video fayl tadbirkorlar uchun rus tilida'
    )
    thumb_seller_uz = models.ImageField(
        upload_to='video_instructions/thumbs/',
        null=True, blank=True,
        verbose_name='Thumbnail — Tadbirkor (O\'zbek)',
        help_text='JPEG, max 320x320, 200KB.'
    )
    thumb_seller_ru = models.ImageField(
        upload_to='video_instructions/thumbs/',
        null=True, blank=True,
        verbose_name='Thumbnail — Tadbirkor (Ruscha)',
        help_text='JPEG, max 320x320, 200KB.'
    )
    # Telegram file_id (avtomatik)
    file_id_electrician_uz = models.CharField(max_length=255, null=True, blank=True, verbose_name='file_id Elektrik UZ')
    file_id_electrician_ru = models.CharField(max_length=255, null=True, blank=True, verbose_name='file_id Elektrik RU')
    file_id_seller_uz = models.CharField(max_length=255, null=True, blank=True, verbose_name='file_id Tadbirkor UZ')
    file_id_seller_ru = models.CharField(max_length=255, null=True, blank=True, verbose_name='file_id Tadbirkor RU')
    is_active = models.BooleanField(default=True, verbose_name='Faol')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Yangilangan')
    
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = _('Video ko\'rsatma')
        verbose_name_plural = _('Video ko\'rsatmalar')
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Video ko'rsatma (Yangilangan: {self.updated_at.strftime('%d.%m.%Y %H:%M')})"
    
    def get_video_file(self, user_type: str, language: str):
        """Возвращает видео файл для user_type и language."""
        key = f'video_{user_type}_{"uz" if language == "uz_latin" else "ru"}'
        return getattr(self, key, None)
    
    def get_thumb_file(self, user_type: str, language: str):
        """Возвращает thumbnail для user_type и language."""
        key = f'thumb_{user_type}_{"uz" if language == "uz_latin" else "ru"}'
        return getattr(self, key, None)
    
    def get_file_id(self, user_type: str, language: str):
        """Возвращает file_id для user_type и language."""
        key = f'file_id_{user_type}_{"uz" if language == "uz_latin" else "ru"}'
        return getattr(self, key, None)
    
    def set_file_id(self, user_type: str, language: str, file_id: str):
        """Устанавливает file_id для user_type и language."""
        key = f'file_id_{user_type}_{"uz" if language == "uz_latin" else "ru"}'
        setattr(self, key, file_id)
        self.save(update_fields=[key])
    
    @classmethod
    def get_active_instruction(cls):
        """Возвращает активную видео инструкцию."""
        return cls.objects.filter(is_active=True).first()



class MonthlyReminderSettings(models.Model):
    """
    Настройки ежемесячного push-уведомления для пользователей,
    которые не выбрали роль или не завершили регистрацию.
    Singleton-модель: используется первая (и единственная) запись.
    """
    is_active = models.BooleanField(
        default=False,
        verbose_name='Включено',
        help_text='Если выключено — рассылка не выполняется.',
    )
    time_of_day = models.TimeField(
        default='10:00',
        verbose_name='Время отправки',
        help_text='Локальное время (Asia/Tashkent), 1-го числа каждого месяца.',
    )
    text_uz_latin = models.TextField(
        verbose_name='Текст (uz_latin)',
        help_text='Поддерживается HTML: &lt;b&gt;, &lt;i&gt;, &lt;a href&gt;. По умолчанию для пользователей с языком uz_latin или без указанного языка.',
    )
    text_ru = models.TextField(
        verbose_name='Текст (ru)',
        help_text='Поддерживается HTML. Для пользователей с языком ru.',
    )
    image = models.ImageField(
        upload_to='monthly_reminders/',
        null=True,
        blank=True,
        verbose_name='Картинка (опционально)',
        help_text='Если загружена — текст идёт как подпись к фото.',
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменено')

    class Meta:
        verbose_name = 'Ежемесячное напоминание (настройки)'
        verbose_name_plural = 'Ежемесячное напоминание (настройки)'

    def __str__(self):
        return f'Ежемесячное напоминание ({"вкл" if self.is_active else "выкл"}, {self.time_of_day})'


class MonthlyReminderLog(models.Model):
    """Лог запусков ежемесячного напоминания. Один запуск = одна строка."""
    STATUS_CHOICES = [
        ('running', 'Выполняется'),
        ('completed', 'Завершено'),
        ('failed', 'Ошибка'),
    ]
    month_key = models.CharField(
        max_length=7,
        unique=True,
        db_index=True,
        verbose_name='Месяц (YYYY-MM)',
        help_text='Уникальный ключ месяца — защита от двойного запуска.',
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='running',
        db_index=True,
        verbose_name='Статус',
    )
    total = models.IntegerField(default=0, verbose_name='Всего получателей')
    sent_count = models.IntegerField(default=0, verbose_name='Отправлено')
    failed_count = models.IntegerField(default=0, verbose_name='Ошибок')
    started_at = models.DateTimeField(auto_now_add=True, verbose_name='Запущено')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Завершено')
    error_message = models.TextField(blank=True, verbose_name='Сообщение об ошибке')

    class Meta:
        verbose_name = 'Ежемесячное напоминание (лог)'
        verbose_name_plural = 'Ежемесячное напоминание (логи)'
        ordering = ['-started_at']

    def __str__(self):
        return f'{self.month_key} — {self.sent_count}/{self.total} ({self.get_status_display()})'


class LiveStream(models.Model):
    """Прямой эфир розыгрыша. Может быть предстоящим или прошедшим (по scheduled_at)."""
    title_uz_latin = models.CharField(max_length=255, verbose_name='Sarlavha (O\'zbek lotin)')
    title_ru = models.CharField(max_length=255, blank=True, verbose_name='Sarlavha (Ruscha)')
    description_uz_latin = models.TextField(blank=True, verbose_name='Tavsif (O\'zbek lotin)')
    description_ru = models.TextField(blank=True, verbose_name='Tavsif (Ruscha)')
    scheduled_at = models.DateTimeField(verbose_name='Efir vaqti', db_index=True)
    stream_url = models.URLField(verbose_name='Efir havolasi', help_text='Telegram/YouTube va boshqa havola')
    banner = models.ImageField(
        upload_to='live_streams/banners/',
        blank=True,
        null=True,
        verbose_name='Webapp banneri',
        help_text='Webapp ichida efir kartochkasi va detal sahifasida ko\'rsatiladi'
    )
    participants_count = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Ishtirokchilar soni',
        help_text='Webapp\'da ko\'rsatiladigan ishtirokchilar soni (qo\'lda kiritiladi)'
    )
    is_active = models.BooleanField(default=True, verbose_name='Faol', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Jonli efir')
        verbose_name_plural = _('Jonli efirlar')
        ordering = ['-scheduled_at']
        indexes = [
            models.Index(fields=['is_active', 'scheduled_at']),
        ]

    def __str__(self):
        return f"{self.title_uz_latin} — {self.scheduled_at:%d.%m.%Y %H:%M}"

    def get_title(self, language='uz_latin'):
        if language == 'ru' and self.title_ru:
            return self.title_ru
        return self.title_uz_latin or self.title_ru or ''

    def get_description(self, language='uz_latin'):
        if language == 'ru' and self.description_ru:
            return self.description_ru
        return self.description_uz_latin or self.description_ru or ''

    @property
    def is_past(self):
        return self.scheduled_at < timezone.now()


class LiveStreamWinner(models.Model):
    """Победитель прямого эфира. Тип (электрик/продавец) берётся из user.user_type."""
    live_stream = models.ForeignKey(
        LiveStream,
        on_delete=models.CASCADE,
        related_name='winners',
        verbose_name='Jonli efir',
    )
    user = models.ForeignKey(
        TelegramUser,
        on_delete=models.PROTECT,
        related_name='live_stream_wins',
        verbose_name='G\'olib',
    )
    prize_text_uz_latin = models.CharField(max_length=255, blank=True, verbose_name='Sovg\'a (O\'zbek lotin)')
    prize_text_ru = models.CharField(max_length=255, blank=True, verbose_name='Sovg\'a (Ruscha)')
    position = models.PositiveIntegerField(default=0, verbose_name='Tartib raqami')
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Jonli efir g\'olibi')
        verbose_name_plural = _('Jonli efir g\'oliblari')
        ordering = ['live_stream', 'position', 'id']
        indexes = [
            models.Index(fields=['live_stream', 'position']),
        ]

    def __str__(self):
        return f"{self.live_stream} — {self.user}"

    def get_prize_text(self, language='uz_latin'):
        if language == 'ru' and self.prize_text_ru:
            return self.prize_text_ru
        return self.prize_text_uz_latin or self.prize_text_ru or ''
