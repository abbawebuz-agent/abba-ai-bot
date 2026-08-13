"""
HTML → Telegram uchun xavfsiz HTML.

Telegram Bot API faqat cheklangan teglarni qo'llab-quvvatlaydi:
b, strong, i, em, u, ins, s, strike, del, a, code, pre, blockquote,
tg-spoiler, span (faqat class="tg-spoiler"), tg-emoji.

Admin panelidagi Quill muharriri esa <p>, <span style="...">, <ul>, <li>,
&nbsp; kabi narsalarni chiqaradi — ular Telegram'da
"Bad Request: can't parse entities / unsupported start tag" xatosini beradi
va rassilka BUTUNLAY yiqiladi (0 yuborildi).

Shu sababli bu modul HTML'ni qayta quradi: ruxsat etilgan teglarni qoldiradi,
qolganlarini matnini saqlagan holda olib tashlaydi.

Modul ataylab faqat standart kutubxonaga tayanadi (Django/aiogram import yo'q) —
shuning uchun uni alohida test qilish mumkin.
"""
import re
from html import escape as _escape
from html.parser import HTMLParser

# Telegram qo'llab-quvvatlaydigan teglar (atributsiz chiqariladi, <a> dan tashqari)
TELEGRAM_ALLOWED_TAGS = {
    'b', 'strong', 'i', 'em', 'u', 'ins', 's', 'strike', 'del',
    'code', 'pre', 'blockquote', 'tg-spoiler',
}

# Yangi qatorga o'tkaziladigan blok teglar
_BLOCK_TAGS = {
    'p', 'div', 'section', 'article', 'header', 'footer', 'main', 'aside',
    'ul', 'ol', 'li', 'table', 'tr', 'td', 'th', 'tbody', 'thead',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'figure', 'figcaption', 'hr',
}

# Ichidagi matn ham tashlab yuboriladi
_DROP_CONTENT_TAGS = {'script', 'style', 'head', 'title', 'noscript'}

# Yopilmaydigan (void) teglar
_VOID_TAGS = {'br', 'img', 'hr', 'input', 'meta', 'link', 'source', 'area', 'col'}

_SAFE_URL_RE = re.compile(r'^(https?://|tg://|mailto:|t\.me/)', re.I)


class _TelegramHTMLCleaner(HTMLParser):
    """HTML'ni Telegram qo'llab-quvvatlaydigan ko'rinishga keltiradi."""

    def __init__(self, keep_tags: bool = True):
        super().__init__(convert_charrefs=True)
        self.keep_tags = keep_tags
        self._out = []
        self._stack = []      # [(manba_tegi, chiqarilgan_teg|None)]
        self._skip_depth = 0

    # --- yordamchi ---
    def _emit(self, text):
        self._out.append(text)

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()

        if tag in _DROP_CONTENT_TAGS:
            self._skip_depth += 1
            self._stack.append((tag, None))
            return
        if self._skip_depth:
            if tag not in _VOID_TAGS:
                self._stack.append((tag, None))
            return

        if tag == 'br':
            self._emit('\n')
            return
        if tag in _VOID_TAGS:
            if tag == 'hr':
                self._emit('\n')
            return

        emitted = None
        if self.keep_tags and tag in TELEGRAM_ALLOWED_TAGS:
            emitted = tag
            self._emit(f'<{tag}>')
        elif self.keep_tags and tag == 'a':
            href = ''
            for k, v in attrs:
                if k.lower() == 'href' and v:
                    href = v.strip()
                    break
            if href and _SAFE_URL_RE.match(href):
                emitted = 'a'
                self._emit(f'<a href="{_escape(href, quote=True)}">')
        elif self.keep_tags and tag == 'span':
            classes = ''
            for k, v in attrs:
                if k.lower() == 'class' and v:
                    classes = v.lower()
                    break
            if 'tg-spoiler' in classes:
                emitted = 'tg-spoiler'
                self._emit('<tg-spoiler>')
            # <span style="color: ..."> — teg tashlanadi, matni qoladi
        else:
            if tag in _BLOCK_TAGS:
                self._emit('\n')
                if tag == 'li':
                    self._emit('• ')

        self._stack.append((tag, emitted))

    def handle_startendtag(self, tag, attrs):
        tag = tag.lower()
        if tag == 'br' and not self._skip_depth:
            self._emit('\n')

    def handle_endtag(self, tag):
        tag = tag.lower()
        # Stack'dan mos ochilgan tegni topamiz (noto'g'ri yopilgan HTML uchun)
        idx = None
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i][0] == tag:
                idx = i
                break
        if idx is None:
            return
        for src, emitted in reversed(self._stack[idx:]):
            if src in _DROP_CONTENT_TAGS:
                self._skip_depth = max(0, self._skip_depth - 1)
                continue
            if self._skip_depth:
                continue
            if emitted:
                self._emit(f'</{emitted}>')
            elif src == 'li':
                # ro'yxat bandlari orasida bo'sh qator kerak emas
                pass
            elif src in _BLOCK_TAGS:
                self._emit('\n')
        del self._stack[idx:]

    def handle_data(self, data):
        if self._skip_depth or not data:
            return
        # convert_charrefs=True — &nbsp; allaqachon \xa0 ga aylangan
        data = data.replace('\xa0', ' ')
        self._emit(_escape(data, quote=False) if self.keep_tags else data)

    def close_result(self) -> str:
        # Ochiq qolgan teglarni yopamiz
        for src, emitted in reversed(self._stack):
            if emitted:
                self._emit(f'</{emitted}>')
        self._stack.clear()
        return ''.join(self._out)


def _normalize(text: str) -> str:
    # Qator oxiridagi bo'shliqlar
    text = re.sub(r'[ \t]+\n', '\n', text)
    text = re.sub(r'\n[ \t]+', '\n', text)
    # 3+ qator uzilishi → 2 (bitta bo'sh qator)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def sanitize_html_for_telegram(text: str) -> str:
    """HTML matnni Telegram qabul qiladigan HTML'ga aylantiradi."""
    if not text:
        return text
    parser = _TelegramHTMLCleaner(keep_tags=True)
    parser.feed(text)
    parser.close()
    return _normalize(parser.close_result())


def html_to_plain_text(text: str) -> str:
    """Barcha teglarni olib tashlab, sof matn qaytaradi (parse_mode'siz zaxira yuborish uchun)."""
    if not text:
        return text
    parser = _TelegramHTMLCleaner(keep_tags=False)
    parser.feed(text)
    parser.close()
    return _normalize(parser.close_result())


def visible_text_length(text: str) -> int:
    """Telegram hisoblaydigan (teglarsiz) matn uzunligi."""
    return len(html_to_plain_text(text or ''))
