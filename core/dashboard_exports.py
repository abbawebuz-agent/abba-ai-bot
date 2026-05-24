import io
from datetime import datetime, date
from django.utils import timezone
from django.utils.translation import gettext as _, get_language
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter

# Localization Map for KPI metrics to ensure 100% translation in RU/UZ
LOCALIZATION_MAP = {
    'ru': {
        'summary_title': "Краткий обзор показателей",
        'trends_title': "Тренды роста",
        'geo_title': "Региональная аналитика",
        'risk_title': "Аудит безопасности",
        
        'col_id': "ID",
        'col_tg_id': "Telegram ID",
        'col_first_name': "Имя",
        'col_last_name': "Фамилия",
        'col_username': "Имя пользователя",
        'col_phone': "Телефон",
        'col_type': "Тип",
        'col_region': "Регион",
        'col_district': "Район",
        'col_points': "Баллы",
        'col_joined_at': "Дата регистрации",
        
        'col_promo_code': "Промо-код",
        'col_points_val': "Номинал баллов",
        'col_category': "Категория",
        'col_scanned_at': "Дата сканирования",
        
        'col_gift_name': "Название подарка",
        'col_points_cost': "Стоимость (баллы)",
        'col_status': "Статус",
        'col_requested_at': "Дата заявки",
        'col_admin_notes': "Заметки админа",
        'col_user_comment': "Комментарий пользователя",
        'col_confirmed_at': "Дата подтверждения",
        
        'col_group': "Раздел",
        'col_metric': "Показатель",
        'col_value': "Значение",
        
        'col_date': "Дата",
        'col_new_users': "Новые пользователи",
        'col_activations': "Активации QR",
        'col_earned': "Заработано баллов",
        'col_requests': "Заявки на подарки",
        
        'col_territory': "Территория",
        'col_participants': "Участники",
        'col_total_pts': "Всего баллов",
        
        'col_user': "Пользователь",
        'col_failed': "Неудачные попытки",
        'sec_distribution': "Распределение целостности аккаунтов",
        'sec_suspects': "Топ подозрительных пользователей",
        
        'users': "Пользователи",
        'inventory': "Инвентарь и QR",
        'economy': "Экономика баллов",
        'gifts': "Подарки и Награды",
        'security': "Безопасность",
        
        'total_reg': "Всего зарегистрировано",
        'elec': "Сантехники",
        'stores': "Магазины / Продавцы",
        'unsel': "Невыбранный профиль",
        
        'qr_total': "Всего QR-кодов в обороте",
        'qr_scanned_e': "Активировано (Сантехники)",
        'qr_scanned_s': "Активировано (Магазины)",
        'qr_unscanned': "Неиспользованные коды",
        
        'pts_earned': "Всего заработано баллов",
        'pts_spent': "Потрачено баллов (награды)",
        'pts_potential': "Потенциал (неактивные коды)",
        
        'red_total': "Всего заявок на подарки",
        'red_comp_e': "Выдано наград (Сантехники)",
        'red_comp_s': "Выдано наград (Магазины)",
        
        'fail_scans': "Неудачные попытки сканирования",
        'success_rate': "Доля успеха (валидные коды)",
        'clean_base': "Чистая база пользователей",

        'qr_e_title': "QR-коды: Сантехники",
        'qr_s_title': "QR-коды: Магазины",
        'pool_e_title': "Баланс баллов: Сантехники",
        'pool_s_title': "Баланс баллов: Магазины",
        'red_status_title': "Статус выдачи подарков",
        'period_delta': "За выбранный период",
        'lifetime_total': "Всего за все время",
        'pts_scanned': "Сканировано баллов",

        'report_users': "Отчет по пользователям",
        'report_scans': "Журнал активаций",
        'report_gifts': "Заявки на подарки",
        'col_undefined': "Не определено",
    },
    'uz': {
        'summary_title': "Ko'rsatkichlar qisqacha sharhi",
        'trends_title': "O'sish tendentsiyalari",
        'geo_title': "Mintaqaviy tahlil",
        'risk_title': "Xavfsizlik auditi",
        
        'report_users': "Foydalanuvchilar bo'yicha hisobot",
        'report_scans': "Faollashtirish jurnali",
        'report_gifts': "Sovg'alar uchun arizalar",
    
        'col_id': "ID",
        'col_tg_id': "Telegram ID",
        'col_first_name': "Ism",
        'col_last_name': "Familiya",
        'col_username': "Foydalanuvchi nomi",
        'col_phone': "Telefon",
        'col_type': "Turi",
        'col_region': "Viloyat",
        'col_district': "Tuman",
        'col_points': "Ballar",
        'col_joined_at': "Ro'yxatdan o'tgan sana",
        
        'col_promo_code': "Promo-kod",
        'col_points_val': "Ballar nominali",
        'col_category': "Kategoriya",
        'col_scanned_at': "Skanerlangan sana",
        
        'col_gift_name': "Sovg'a nomi",
        'col_points_cost': "Qiymati (ballar)",
        'col_status': "Status",
        'col_requested_at': "Ariza sanasi",
        'col_admin_notes': "Admin eslatmalari",
        'col_user_comment': "Foydalanuvchi izohi",
        'col_confirmed_at': "Tasdiqlangan sana",
        
        'col_group': "Bo'lim",
        'col_metric': "Ko'rsatkich",
        'col_value': "Qiymat",
        
        'col_date': "Sana",
        'col_new_users': "Yangi foydalanuvchilar",
        'col_activations': "QR faollashtirish",
        'col_earned': "To'plangan ballar",
        'col_requests': "Sovg'a so'rovlari",
        
        'col_territory': "Hudud",
        'col_participants': "Ishtirokchilar",
        'col_total_pts': "Jami ballar",
        
        'col_user': "Foydalanuvchi",
        'col_failed': "Muvaffaqiyatsiz urinishlar",
        'sec_distribution': "Hisob qaydnomalarining yaxlitligi taqsimoti",
        'sec_suspects': "Eng shubhali foydalanuvchilar",
        
        'users': "Foydalanuvchilar",
        'inventory': "Inventar va QR",
        'economy': "Ballar iqtisodiyoti",
        'gifts': "Sovg'alar va Mukofotlar",
        'security': "Xavfsizlik",
        
        'total_reg': "Jami ro'yxatdan o'tganlar",
        'elec': "Elektriklar",
        'stores': "Do'konlar / Sotuvchilar",
        'unsel': "Tanlanmagan profil",
        
        'qr_total': "Muomaladagi jami QR-kodlar",
        'qr_scanned_e': "Faollashtirilgan (Elektriklar)",
        'qr_scanned_s': "Faollashtirilgan (Do'konlar)",
        'qr_unscanned': "Ishlatilmagan kodlar",
        
        'pts_earned': "Jami to'plangan ballar",
        'pts_spent': "Sarflangan ballar (sovg'alar)",
        'pts_potential': "Potentsial (faol bo'lmagan kodlar)",
        
        'red_total': "Sovg'alar uchun jami arizalar",
        'red_comp_e': "Berilgan mukofotlar (Elektriklar)",
        'red_comp_s': "Berilgan mukofotlar (Do'konlar)",
        
        'fail_scans': "Muvaffaqiyatsiz skanerlash urinishlari",
        'success_rate': "Muvaffaqiyat ulushi (haqiqiy kodlar)",
        'clean_base': "Toza foydalanuvchilar bazasi",

        'qr_e_title': "QR-kodlar: Elektriklar",
        'qr_s_title': "QR-kodlar: Do'konlar",
        'pool_e_title': "Ballar balansi: Elektriklar",
        'pool_s_title': "Ballar balansi: Do'konlar",
        'red_status_title': "Sovg'alar holati",
        'period_delta': "Tanlangan davr uchun",
        'lifetime_total': "Barcha vaqt davomida",
        'pts_scanned': "Skanerlangan ballar",

        # Module Titles
        'users_list': "Foydalanuvchilar ro'yxati",
        'gifts_list': "Sovg'alar ro'yxati",
        'redemptions_list': "Arizalar ro'yxati",
        'activations_list': "Faollashtirishlar jurnali",

        # Extra Columns
        'col_serial': "Seriya raqami",
        'col_scanned_by': "Skanerlagan foydalanuvchi",
        'col_points_earned': "Yig'ilgan ballar",
        'col_status_uz': "Holati",
        'col_undefined': "Noma'lum",
    }
}

def apply_header_styling(sheet, columns_count):
    """Применяет профессиональный стиль к первой строке (заголовкам)."""
    header_font = Font(bold=True, color="FFFFFF", size=11)
    header_fill = PatternFill(start_color="1F2937", end_color="1F2937", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    
    for col in range(1, columns_count + 1):
        cell = sheet.cell(row=1, column=col)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        
    sheet.row_dimensions[1].height = 25
    sheet.freeze_panes = "A2"

def auto_adjust_columns(sheet):
    """Автоматически подбирает ширину колонок и настраивает выравнивание."""
    for col in sheet.columns:
        max_length = 0
        column_index = col[0].column
        column_letter = get_column_letter(column_index)
        
        for cell in col:
            # Настройка выравнивания: Числа вправо, Текст влево
            if isinstance(cell.value, (int, float)):
                cell.alignment = Alignment(horizontal="right")
            elif cell.row > 1: # Пропускаем заголовки (они в центре)
                cell.alignment = Alignment(horizontal="left")
                
            try:
                val = str(cell.value)
                if val and val != 'None' and len(val) > max_length:
                    max_length = len(val)
            except:
                pass
        
        adjusted_width = (max_length + 4)
        sheet.column_dimensions[column_letter].width = min(adjusted_width, 60)

def generate_full_dashboard_excel(stats_data):
    """Генерирует Excel со всеми вкладками дашборда (Force Uzbek)."""
    wb = Workbook()
    
    # Force Uzbek for all labels
    lang = 'uz'
    lm = LOCALIZATION_MAP[lang]
    
    # 1. Summary Sheet
    ws_summary = wb.active
    ws_summary.title = lm['summary_title'][:31]
    _fill_summary_sheet(ws_summary, stats_data, lm)
    
    # 2. Growth Trends
    ws_trends = wb.create_sheet(lm['trends_title'])
    _fill_trends_sheet(ws_trends, stats_data.get('charts'), lm)
    
    # 3. Regional Stats
    ws_geo = wb.create_sheet(lm['geo_title'])
    _fill_regional_sheet(ws_geo, stats_data, lm)
    
    # 4. Security & Audit
    ws_risk = wb.create_sheet(lm['risk_title'])
    _fill_security_sheet(ws_risk, stats_data.get('intelligence_stats'), lm)
    
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer

def _fill_summary_sheet(ws, data, lm):
    g = data.get('general_stats', {})
    i = data.get('intelligence_stats', {})
    
    headers = [lm['col_group'], lm['col_metric'], lm['period_delta'], lm['lifetime_total']]
    for col, val in enumerate(headers, 1):
        ws.cell(row=1, column=col, value=val)
    
    rows = [
        # 1. Members
        (lm['users'], lm['total_reg'], g.get('users_total', 0), g.get('life_u_total', 0)),
        (lm['users'], lm['elec'], g.get('users_electrician', 0), g.get('life_u_e', 0)),
        (lm['users'], lm['stores'], g.get('users_seller', 0), g.get('life_u_s', 0)),
        (lm['users'], lm['unsel'], g.get('users_unselected', 0), g.get('life_u_unselected', 0)),
        
        # Spacer
        ("", "", "", ""),
        
        # 2. Electrician Codes
        (lm['qr_e_title'], lm['qr_total'], "-", g.get('life_qr_e_total', 0)),
        (lm['qr_e_title'], lm['qr_scanned_e'], g.get('qr_e_scanned', 0), g.get('life_qr_e_scanned', 0)),
        (lm['qr_e_title'], lm['qr_unscanned'], "-", g.get('life_qr_e_unscanned', 0)),
        
        # 3. Store Codes
        (lm['qr_s_title'], lm['qr_total'], "-", g.get('life_qr_s_total', 0)),
        (lm['qr_s_title'], lm['qr_scanned_s'], g.get('qr_s_scanned', 0), g.get('life_qr_s_scanned', 0)),
        (lm['qr_s_title'], lm['qr_unscanned'], "-", g.get('life_qr_s_unscanned', 0)),
        
        # Spacer
        ("", "", "", ""),
        
        # 4. Point Economy
        (lm['economy'], lm['pts_earned'], g.get('points_total', 0), g.get('life_points_total', 0)),
        (lm['economy'], lm['elec'], g.get('points_electrician', 0), "-"),
        (lm['economy'], lm['stores'], g.get('points_seller', 0), "-"),
        
        # 5. Electrician Pool
        (lm['pool_e_title'], lm['qr_total'], "-", g.get('pool_e_total', 0)),
        (lm['pool_e_title'], lm['pts_scanned'], g.get('pool_e_scanned', 0), g.get('life_pool_e_scanned', 0)),
        (lm['pool_e_title'], lm['pts_spent'], g.get('pool_e_spent', 0), g.get('life_pool_e_spent', 0)),
        (lm['pool_e_title'], lm['pts_potential'], "-", g.get('pool_e_unscanned', 0)),
        
        # 6. Store Pool
        (lm['pool_s_title'], lm['qr_total'], "-", g.get('pool_s_total', 0)),
        (lm['pool_s_title'], lm['pts_scanned'], g.get('pool_s_scanned', 0), g.get('life_pool_s_scanned', 0)),
        (lm['pool_s_title'], lm['pts_spent'], g.get('pool_s_spent', 0), g.get('life_pool_s_spent', 0)),
        (lm['pool_s_title'], lm['pts_potential'], "-", g.get('pool_s_unscanned', 0)),
        
        # Spacer
        ("", "", "", ""),
        
        # 7. Gifts Overview
        (lm['gifts'], lm['red_total'], g.get('gifts_total', 0), g.get('life_gifts_total', 0)),
        (lm['gifts'], lm['elec'], g.get('gifts_electrician', 0), g.get('life_gifts_e', 0)),
        (lm['gifts'], lm['stores'], g.get('gifts_seller', 0), g.get('life_gifts_s', 0)),
        
        # 8. Redemption Status (Breakdown)
        (lm['red_status_title'], lm['red_comp_e'], g.get('gift_redemptions_electrician', {}).get('topshirilgan', {}).get('count', 0), "-"),
        (lm['red_status_title'], lm['red_comp_s'], g.get('gift_redemptions_seller', {}).get('topshirilgan', {}).get('count', 0), "-"),
        
        # Spacer
        ("", "", "", ""),
        
        # 9. Security & Audit
        (lm['security'], lm['fail_scans'], i.get('failed_attempts', 0), i.get('failed_attempts_life', 0)),
        (lm['security'], lm['success_rate'], f"{i.get('success_rate', 0)}%", "-"),
        (lm['security'], lm['clean_base'], f"{i.get('clean_percentage', 0)}%", "-"),
    ]
    
    for r_idx, row in enumerate(rows, 2):
        for c_idx, val in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx, value=val)
            
    apply_header_styling(ws, len(headers))
    auto_adjust_columns(ws)

def _fill_trends_sheet(ws, charts, lm):
    if not charts:
        return
    
    labels = charts.get('labels', [])
    reg_series = charts.get('reg_series', [])
    act_series = charts.get('act_series', [])
    pts_series = charts.get('act_pts_series', [])
    red_series = charts.get('red_series', [])
    
    headers = [lm['col_date'], lm['col_new_users'], lm['col_activations'], lm['col_earned'], lm['col_requests']]
    for col, val in enumerate(headers, 1):
        ws.cell(row=1, column=col, value=val)
        
    for i, date_label in enumerate(labels):
        row = [
            date_label,
            reg_series[i] if i < len(reg_series) else 0,
            act_series[i] if i < len(act_series) else 0,
            pts_series[i] if i < len(pts_series) else 0,
            red_series[i] if i < len(red_series) else 0,
        ]
        for c_idx, val in enumerate(row, 1):
            ws.cell(row=i + 2, column=c_idx, value=val)
            
    apply_header_styling(ws, len(headers))
    auto_adjust_columns(ws)

def _fill_regional_sheet(ws, data, lm):
    promo_rows = data.get('promo_rows', [])
    tab = data.get('tab', 'General')
    region_name = data.get('drill_region_name') or (lm['geo_title'])
    
    title_text = f"{lm['geo_title']} ({tab}) - {region_name}"
    ws.cell(row=1, column=1, value=title_text)
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=4)
    ws.cell(row=1, column=1).font = Font(bold=True, size=14)
    
    headers = [lm['col_territory'], lm['col_participants'], lm['col_activations'], lm['col_total_pts'], lm['pts_spent']]
    for col, val in enumerate(headers, 1):
        ws.cell(row=3, column=col, value=val)
        
    for r_idx, row in enumerate(promo_rows, 4):
        ws.cell(row=r_idx, column=1, value=row.get('name'))
        ws.cell(row=r_idx, column=2, value=row.get('users'))
        ws.cell(row=r_idx, column=3, value=row.get('cards'))
        ws.cell(row=r_idx, column=4, value=row.get('points'))
        ws.cell(row=r_idx, column=5, value=row.get('spent'))
        
        if row.get('is_total'):
            for c in range(1, 6):
                ws.cell(row=r_idx, column=c).font = Font(bold=True)
                ws.cell(row=r_idx, column=c).fill = PatternFill(start_color="F3F4F6", end_color="F3F4F6", fill_type="solid")

    apply_header_styling_range(ws, 3, 4, color="4B5563")
    
    ws.freeze_panes = "A4"
    auto_adjust_columns(ws)

def generate_regional_excel(data):
    """Генерирует Excel только для региональной таблицы."""
    wb = Workbook()
    lang = 'uz'
    lm = LOCALIZATION_MAP[lang]
    
    ws = wb.active
    ws.title = lm['geo_title'][:31]
    _fill_regional_sheet(ws, data, lm)
    
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer

def _fill_security_sheet(ws, intelligence, lm):
    if not intelligence:
        return
    
    # 1. Integrity Segments
    ws.cell(row=1, column=1, value=lm['sec_distribution'])
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=2)
    ws.cell(row=1, column=1).font = Font(bold=True, size=12)
    
    segments = intelligence.get('segments', {})
    row_idx = 2
    for seg, val in segments.items():
        ws.cell(row=row_idx, column=1, value=seg.upper())
        ws.cell(row=row_idx, column=2, value=val)
        row_idx += 1
    
    # 2. Leaderboard
    ws.cell(row=row_idx + 2, column=1, value=lm['sec_suspects'])
    ws.merge_cells(start_row=row_idx + 2, start_column=1, end_row=row_idx + 2, end_column=3)
    ws.cell(row=row_idx + 2, column=1).font = Font(bold=True, size=12)
    
    headers = [lm['col_user'], lm['col_phone'], lm['col_failed']]
    for col, val in enumerate(headers, 1):
        ws.cell(row=row_idx + 3, column=col, value=val)
        
    leaderboard = intelligence.get('leaderboard', [])
    for i, user in enumerate(leaderboard):
        name = f"{user.get('first_name') or ''} {user.get('last_name') or ''}"
        ws.cell(row=row_idx + 4 + i, column=1, value=name)
        ws.cell(row=row_idx + 4 + i, column=2, value=user.get('phone_number'))
        ws.cell(row=row_idx + 4 + i, column=3, value=user.get('promo_failed_attempts'))
    
    apply_header_styling_range(ws, row_idx + 3, 3)
    auto_adjust_columns(ws)

def apply_header_styling_range(sheet, row, columns_count, color="1F2937"):
    header_font = Font(bold=True, color="FFFFFF", size=11)
    header_fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center")
    
    for col in range(1, columns_count + 1):
        cell = sheet.cell(row=row, column=col)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment

def generate_module_excel(module_title, data_list, headers_map):
    """Генерирует Excel для табличных данных с поддержкой локализации (Force Uzbek)."""
    wb = Workbook()
    ws = wb.active
    
    lang = 'uz'
    lm = LOCALIZATION_MAP[lang]
    
    # Translate Title if it's a key
    ws.title = lm.get(module_title, module_title)[:31]
    
    # Headers
    for col, (field, label) in enumerate(headers_map, 1):
        # Translate Label if it's a key
        final_label = lm.get(label, label)
        ws.cell(row=1, column=col, value=final_label)
        
    # Data
    for r_idx, item in enumerate(data_list, 2):
        for c_idx, (field, label) in enumerate(headers_map, 1):
            val = ""
            if callable(field):
                val = field(item)
            elif isinstance(item, dict):
                val = item.get(field, "")
            else:
                # Optimized field retrieval with display name support
                if field == 'status' and hasattr(item, 'get_status_display'):
                    val = item.get_status_display()
                elif field == 'user_type' and hasattr(item, 'get_user_type_display'):
                    val = item.get_user_type_display()
                elif field == 'region' and hasattr(item, 'region'):
                    val = item.region.name_uz if item.region else lm.get('col_undefined', "Noma'lum")
                elif field == 'district' and hasattr(item, 'district'):
                    val = item.district.name_uz if item.district else lm.get('col_undefined', "Noma'lum")
                else:
                    val = getattr(item, field, '')
                
            if isinstance(val, (datetime, date)):
                if hasattr(val, 'tzinfo') and val.tzinfo:
                    val = val.replace(tzinfo=None)
            
            ws.cell(row=r_idx, column=c_idx, value=val if val is not None else "")
            
    apply_header_styling(ws, len(headers_map))
    auto_adjust_columns(ws)
    
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer
