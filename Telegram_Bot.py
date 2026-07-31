import sqlite3
import requests
import time
from datetime import datetime
from telegram.ext import Updater, CommandHandler

TOKEN = '8734372802:AAF3KKneCCOEYdZz_Z6Zv4kx2nNo39NNgM0'

CATEGORIES = {
    # ═══ МУЖСКОЕ ═══
    'мужская обувь': 16,
    'мужские кроссовки': 16,
    'мужские куртки': 1231,
    'мужские штаны': 1224,
    'мужские джинсы': 1224,
    'мужские футболки': 1225,
    'мужские толстовки': 1228,
    'мужские рубашки': 1226,
    'мужские костюмы': 1232,
    'мужские шорты': 1227,
    'мужские свитера': 1229,
    'мужские аксессуары': 1241,
    'мужские шапки': 1241,
    'мужские ремни': 1241,
    # ═══ ЖЕНСКОЕ ═══
    'женская обувь': 1037,
    'женские кроссовки': 1037,
    'женские куртки': 1143,
    'женские штаны': 1138,
    'женские джинсы': 1138,
    'женские футболки': 1132,
    'женские платья': 1235,
    'женские юбки': 1136,
    'женские толстовки': 1133,
    'женские блузки': 1131,
    'женские свитера': 1134,
    'женские сумки': 1245,
    'женские аксессуары': 1244,
    'женские шапки': 1244,
    'женское бельё': 1140,
    'женские купальники': 1141,
    # ═══ УНИСЕКС ═══
    'обувь': 16,
    'кроссовки': 16,
    'куртки': 1231,
    'штаны': 1224,
    'джинсы': 1224,
    'футболки': 1225,
    'платья': 1235,
    'сумки': 1245,
    'толстовки': 1228,
    'рубашки': 1226,
    'свитера': 1229,
    'шорты': 1227,
    'аксессуары': 1241,
    'шапки': 1241,
    'ремни': 1241,
    'часы': 1246,
    'очки': 1246,
    'украшения': 1244,
    'парфюм': 1260,
    'спортивная одежда': 1230,
    'пальто': 1231,
    'пиджаки': 1232,
    'носки': 1243,
    'перчатки': 1241,
    'шарфы': 1241,
}

import os
COOKIE = os.environ.get('VINTED_COOKIE', '')

headers = {
    'accept': 'application/json,text/plain,*/*',
    'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': COOKIE,
    'locale': 'pl-PL',
    'referer': 'https://www.vinted.pl/catalog?search_text=Nike',
    'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
    'x-anon-id': 'dc3d5138-f0e2-44b6-b322-67bac0ad7f0e',
    'x-csrf-token': '75f6c9fa-dc8e-4e52-a000-e09dd4084b3e',
}

# ═══════════════════════════════════
# ОПРЕДЕЛЕНИЕ ЦВЕТА ПО HEX
# ═══════════════════════════════════

def hex_to_color_name(hex_color):
    if not hex_color:
        return None
    try:
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        if r < 50 and g < 50 and b < 50:
            return '⚫ Чёрный'
        elif r > 200 and g > 200 and b > 200:
            return '⚪ Белый'
        elif r > 180 and g > 180 and b > 180:
            return '🔘 Светло-серый'
        elif r > 100 and g > 100 and b > 100:
            return '🔘 Серый'
        elif r > 150 and g < 80 and b < 80:
            return '🔴 Красный'
        elif r < 80 and g < 80 and b > 150:
            return '🔵 Синий'
        elif r < 80 and g > 150 and b < 80:
            return '🟢 Зелёный'
        elif r > 180 and g > 100 and b < 50:
            return '🟠 Оранжевый'
        elif r > 200 and g > 200 and b < 80:
            return '🟡 Жёлтый'
        elif r > 100 and g < 60 and b > 100:
            return '🟣 Фиолетовый'
        elif r > 100 and g < 60 and b < 60:
            return '🟤 Коричневый'
        elif r > 180 and g < 100 and b > 150:
            return '🩷 Розовый'
        elif r > 150 and g > 150 and b < 80:
            return '🫒 Хаки'
        elif r < 80 and g > 100 and b > 100:
            return '🩵 Голубой'
        else:
            return '🔘 Серый'
    except:
        return None

def get_color(item):
    photos = item.get('photos', [])
    if photos:
        hex_color = photos[0].get('dominant_color', '')
        color = hex_to_color_name(hex_color)
        if color:
            return color
    return 'N/A'

# ═══════════════════════════════════
# БАЗА ДАННЫХ
# ═══════════════════════════════════

def create_database():
    conn = sqlite3.connect('vinted.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            title TEXT,
            brand TEXT,
            price REAL,
            currency TEXT,
            size TEXT,
            color TEXT,
            likes INTEGER DEFAULT 0,
            views INTEGER DEFAULT 0,
            url TEXT,
            first_seen TEXT,
            last_seen TEXT,
            sold INTEGER DEFAULT 0,
            days_to_sell REAL DEFAULT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS item_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER,
            price REAL,
            likes INTEGER,
            views INTEGER,
            recorded_at TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("База данных создана ✅")

# ═══════════════════════════════════
# СБОР ДАННЫХ С VINTED
# ═══════════════════════════════════

def get_items_from_vinted(query, pages=5, category_id=None):
    all_items = []
    session = requests.Session()

    for page in range(1, pages + 1):
        url = 'https://www.vinted.pl/api/v2/catalog/items'
        params = {
            'search_text': query,
            'per_page': 96,
            'page': page,
            'order': 'newest_first',
        }
        if category_id:
            params['catalog_ids[]'] = category_id

        response = session.get(url, headers=headers, params=params)
        print(f"Страница {page}: статус {response.status_code}")

        if response.status_code != 200:
            print(f"Ошибка: {response.text[:200]}")
            break

        items = response.json().get('items', [])
        print(f"Найдено: {len(items)}")

        if not items:
            break

        all_items.extend(items)
        time.sleep(2)

    return all_items

# ═══════════════════════════════════
# СОХРАНЕНИЕ
# ═══════════════════════════════════

def save_items(items):
    conn = sqlite3.connect('vinted.db')
    cursor = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_count = 0
    updated_count = 0

    for item in items:
        try:
            price_data = item.get('price', {})
            price = float(price_data.get('amount', 0))
            likes = item.get('favourite_count', 0)
            views = item.get('view_count', 0)
            item_id = item.get('id')
            color = get_color(item)

            cursor.execute('SELECT id FROM items WHERE id = ?', (item_id,))
            existing = cursor.fetchone()

            if existing:
                cursor.execute('''
                    UPDATE items SET
                        likes=?, views=?, last_seen=?, price=?, color=?
                    WHERE id=?
                ''', (likes, views, now, price, color, item_id))
                updated_count += 1
            else:
                cursor.execute('''
                    INSERT INTO items
                    (id, title, brand, price, currency, size, color,
                     likes, views, url, first_seen, last_seen, sold)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,0)
                ''', (
                    item_id,
                    item.get('title'),
                    item.get('brand_title'),
                    price,
                    price_data.get('currency_code', 'PLN'),
                    item.get('size_title', 'N/A'),
                    color,
                    likes, views,
                    f"https://www.vinted.pl/items/{item_id}",
                    now, now
                ))
                new_count += 1

            cursor.execute('''
                INSERT INTO item_history (item_id, price, likes, views, recorded_at)
                VALUES (?,?,?,?,?)
            ''', (item_id, price, likes, views, now))

        except Exception as e:
            print(f"Ошибка сохранения: {e}")
            continue

    conn.commit()
    conn.close()
    return new_count, updated_count

# ═══════════════════════════════════
# АНАЛИТИКА
# ═══════════════════════════════════

def calculate_analytics(query, items):
    prices = [float(i.get('price', {}).get('amount', 0))
              for i in items if i.get('price')]
    prices = [p for p in prices if p > 0]

    if not prices:
        return None

    likes_list = [i.get('favourite_count', 0) for i in items]
    avg_price = sum(prices) / len(prices)
    sorted_prices = sorted(prices)
    median = sorted_prices[len(sorted_prices) // 2]
    variance = sum((p - avg_price) ** 2 for p in prices) / len(prices)
    std_dev = variance ** 0.5
    avg_likes = sum(likes_list) / len(likes_list) if likes_list else 0
    demand_index = avg_likes / len(items) if items else 0

    sizes = {}
    for i in items:
        size = i.get('size_title', 'N/A')
        if size and size != 'N/A':
            sizes[size] = sizes.get(size, 0) + 1
    top_sizes = sorted(sizes.items(), key=lambda x: x[1], reverse=True)[:5]

    colors = {}
    for i in items:
        color = get_color(i)
        if color and color != 'N/A':
            colors[color] = colors.get(color, 0) + 1
    top_colors = sorted(colors.items(), key=lambda x: x[1], reverse=True)[:5]

    brands = {}
    for i in items:
        brand = i.get('brand_title', 'N/A')
        if brand and brand != 'N/A':
            brands[brand] = brands.get(brand, 0) + 1
    top_brands = sorted(brands.items(), key=lambda x: x[1], reverse=True)[:3]

    cheap = len([p for p in prices if p < avg_price * 0.7])
    mid = len([p for p in prices if avg_price * 0.7 <= p <= avg_price * 1.3])
    expensive = len([p for p in prices if p > avg_price * 1.3])

    cheapest = sorted(items, key=lambda x: float(
        x.get('price', {}).get('amount', 999)))[:3]

    score = 5.0
    if demand_index > 10: score += 2
    elif demand_index > 5: score += 1
    if std_dev < avg_price * 0.3: score += 1
    if len(items) > 200: score += 1
    if avg_likes > 15: score += 1
    score = min(10, max(1, score))

    return {
        'total': len(items),
        'avg_price': round(avg_price, 2),
        'median': round(median, 2),
        'min_price': round(min(prices), 2),
        'max_price': round(max(prices), 2),
        'std_dev': round(std_dev, 2),
        'avg_likes': round(avg_likes, 1),
        'demand_index': round(demand_index, 3),
        'cheap': cheap,
        'mid': mid,
        'expensive': expensive,
        'top_sizes': top_sizes,
        'top_colors': top_colors,
        'top_brands': top_brands,
        'score': round(score, 1),
        'cheapest': cheapest,
        'optimal_buy': round(avg_price * 0.65, 2),
        'optimal_sell': round(avg_price * 0.9, 2),
    }

# ═══════════════════════════════════
# TELEGRAM КОМАНДЫ
# ═══════════════════════════════════

def start(update, context):
    update.message.reply_text("""👋 Привет! Я Vinted Analytics Bot!

📊 Команды:
/item [бренд] | [категория] — полный анализ
/analyze [бренд] — анализ бренда
/categories — список всех категорий

Примеры:
/item Nike | мужские кроссовки
/item Zara | женские платья
/item Carhartt | мужские куртки""")

def categories(update, context):
    msg = "📋 ДОСТУПНЫЕ КАТЕГОРИИ:\n\n"
    msg += "👨 МУЖСКОЕ:\n"
    for k in CATEGORIES.keys():
        if 'мужск' in k:
            msg += f"  • {k}\n"
    msg += "\n👩 ЖЕНСКОЕ:\n"
    for k in CATEGORIES.keys():
        if 'женск' in k:
            msg += f"  • {k}\n"
    msg += "\n👕 УНИСЕКС:\n"
    for k in CATEGORIES.keys():
        if 'мужск' not in k and 'женск' not in k:
            msg += f"  • {k}\n"
    update.message.reply_text(msg)

def item_analyze(update, context):
    if not context.args:
        update.message.reply_text(
            'Напиши: /item Nike | мужские кроссовки\n'
            'или: /item Zara | женские платья'
        )
        return

    full_query = ' '.join(context.args)

    if '|' in full_query:
        parts = full_query.split('|')
        query = parts[0].strip()
        category_name = parts[1].strip().lower()
        category_id = CATEGORIES.get(category_name)
    else:
        query = full_query
        category_name = None
        category_id = None

    if category_name and not category_id:
        update.message.reply_text(
            f'❌ Категория "{category_name}" не найдена.\n'
            f'Напиши /categories чтобы увидеть все категории.'
        )
        return

    msg_text = f'🔍 Анализирую: {query}'
    if category_name:
        msg_text += f'\n📂 Категория: {category_name}'
    msg_text += '\n⏳ Подожди ~30 секунд...'
    update.message.reply_text(msg_text)

    items = get_items_from_vinted(query, pages=5, category_id=category_id)

    if not items:
        update.message.reply_text(f'❌ Ничего не найдено для {query}')
        return

    new, updated = save_items(items)
    data = calculate_analytics(query, items)

    if not data:
        update.message.reply_text('❌ Ошибка при анализе')
        return

    filled = int(data['score'])
    bar = '█' * filled + '░' * (10 - filled)
    cat_line = f"\n📂 Категория: {category_name}" if category_name else ""

    msg = f"""🎓 HARVARD ANALYTICS: {query}{cat_line}

📦 ПРЕДЛОЖЕНИЕ:
  Объявлений найдено: {data['total']}
  Новых сохранено: {new}
  Обновлено: {updated}

💰 ЦЕНОВОЙ АНАЛИЗ:
  Средняя цена: {data['avg_price']} PLN
  Медиана: {data['median']} PLN
  Мин: {data['min_price']} PLN
  Макс: {data['max_price']} PLN
  Отклонение: ±{data['std_dev']} PLN

❤️ ИНДЕКС СПРОСА:
  Среднее лайков: {data['avg_likes']}
  Лайков / Предложений: {data['demand_index']}

📊 РАСПРЕДЕЛЕНИЕ ЦЕН:
  🟢 Дёшево: {data['cheap']} шт
  🟡 Средне: {data['mid']} шт
  🔴 Дорого: {data['expensive']} шт

📐 ТОП РАЗМЕРЫ:"""

    for size, count in data['top_sizes']:
        msg += f"\n  • {size} — {count} шт"

    msg += "\n\n🎨 ТОП ЦВЕТА:"
    if data['top_colors']:
        for color, count in data['top_colors']:
            msg += f"\n  • {color} — {count} шт"
    else:
        msg += "\n  • Данные недоступны"

    msg += "\n\n🏆 ТОП БРЕНДЫ:"
    for brand, count in data['top_brands']:
        msg += f"\n  • {brand} — {count} шт"

    msg += f"""

📈 СКОРИНГ АКТИВА:
  {bar} {data['score']}/10

💡 РЕКОМЕНДАЦИЯ:
  Покупай за: до {data['optimal_buy']} PLN
  Продавай за: {data['optimal_sell']} PLN
  Потенциал: +{round(data['optimal_sell'] - data['optimal_buy'], 2)} PLN

🏷 САМЫЕ ДЕШЁВЫЕ СЕЙЧАС:"""

    for item in data['cheapest']:
        price = item.get('price', {}).get('amount', 'N/A')
        title = str(item.get('title', 'N/A'))[:25]
        size = item.get('size_title', '')
        url_item = f"https://www.vinted.pl/items/{item.get('id')}"
        msg += f"\n  • {title} ({size}) — {price} PLN\n    {url_item}"

    update.message.reply_text(msg)

def analyze(update, context):
    if not context.args:
        update.message.reply_text('Напиши: /analyze Nike')
        return
    brand = ' '.join(context.args)
    update.message.reply_text(f'🔍 Анализирую бренд {brand}...')
    items = get_items_from_vinted(brand, pages=3)
    if not items:
        update.message.reply_text(f'❌ Ничего не найдено для {brand}')
        return
    save_items(items)
    data = calculate_analytics(brand, items)
    if not data:
        update.message.reply_text('❌ Ошибка при анализе')
        return
    msg = f"""📊 АНАЛИЗ БРЕНДА: {brand}

📦 Объявлений: {data['total']}
💰 Средняя цена: {data['avg_price']} PLN
📉 Мин: {data['min_price']} PLN
📈 Макс: {data['max_price']} PLN
❤️ Среднее лайков: {data['avg_likes']}
📈 Скоринг: {data['score']}/10"""
    update.message.reply_text(msg)

# ═══════════════════════════════════
# ЗАПУСК
# ═══════════════════════════════════
# ═══════════════════════════════════
# МОНИТОРИНГ
# ═══════════════════════════════════

import threading


def check_sold_items():
    """Проверяет какие товары были проданы"""
    conn = sqlite3.connect('vinted.db')
    cursor = conn.cursor()

    # Берём товары которые видели за последние 7 дней
    cursor.execute('''
        SELECT id, first_seen, last_seen FROM items 
        WHERE sold = 0 
        AND first_seen < datetime('now', '-6 hours')
        AND last_seen > datetime('now', '-7 days')
    ''')
    items_to_check = cursor.fetchall()
    conn.close()

    if not items_to_check:
        print("Нет товаров для проверки")
        return

    print(f"Проверяю {len(items_to_check)} товаров...")
    session = requests.Session()
    sold_count = 0

    for item_id, first_seen, last_seen in items_to_check:
        try:
            url = f'https://www.vinted.pl/api/v2/items/{item_id}'
            response = session.get(url, headers=headers)

            if response.status_code == 404:
                # Товар исчез = продан
                conn = sqlite3.connect('vinted.db')
                cursor = conn.cursor()

                # Считаем время продажи
                cursor.execute('''
                    SELECT first_seen FROM items WHERE id = ?
                ''', (item_id,))
                row = cursor.fetchone()

                if row:
                    first_seen_dt = datetime.strptime(
                        row[0], '%Y-%m-%d %H:%M:%S'
                    )
                    days_to_sell = (
                                           datetime.now() - first_seen_dt
                                   ).total_seconds() / 86400

                    cursor.execute('''
                        UPDATE items SET 
                            sold = 1,
                            days_to_sell = ?
                        WHERE id = ?
                    ''', (round(days_to_sell, 2), item_id))

                    conn.commit()
                    sold_count += 1
                    print(f"Продан: {item_id} за {round(days_to_sell, 2)} дней")

                conn.close()

            time.sleep(0.5)

        except Exception as e:
            print(f"Ошибка проверки {item_id}: {e}")
            continue

    print(f"Проверка завершена. Продано: {sold_count}")


def get_sell_stats(query):
    """Получает статистику времени продажи из базы"""
    conn = sqlite3.connect('vinted.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT 
            COUNT(*) as total_sold,
            AVG(days_to_sell) as avg_days,
            MIN(days_to_sell) as min_days,
            MAX(days_to_sell) as max_days
        FROM items
        WHERE sold = 1
        AND title LIKE ?
    ''', (f'%{query}%',))

    row = cursor.fetchone()
    conn.close()
    return row


def monitor_loop():
    """Запускает мониторинг каждый час"""
    while True:
        print("🔍 Запускаю мониторинг продаж...")
        try:
            check_sold_items()
        except Exception as e:
            print(f"Ошибка мониторинга: {e}")
        print("⏰ Следующая проверка через 1 час")
        time.sleep(3600)  # каждый час


def sold_stats(update, context):
    """Команда /sold — статистика продаж"""
    if not context.args:
        update.message.reply_text('Напиши: /sold Nike кроссовки')
        return

    query = ' '.join(context.args)
    row = get_sell_stats(query)

    if not row or row[0] == 0:
        update.message.reply_text(
            f'❌ Нет данных о продажах для {query}\n'
            f'Бот собирает данные постепенно — попробуй завтра!'
        )
        return

    msg = f"""⚡️ СТАТИСТИКА ПРОДАЖ: {query}

✅ Продано товаров: {row[0]}
⏱ Среднее время продажи: {round(row[1], 1)} дней
🚀 Быстрейшая продажа: {round(row[2], 1)} дней
🐌 Дольше всего: {round(row[3], 1)} дней

💡 Вывод: товары этой категории
продаются в среднем за {round(row[1], 1)} дней"""

    update.message.reply_text(msg)
create_database()

updater = Updater(TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('analyze', analyze))
dp.add_handler(CommandHandler('item', item_analyze))
dp.add_handler(CommandHandler('categories', categories))
dp.add_handler(CommandHandler('sold', sold_stats))

print('🤖 Бот запущен!')
# Запускаем мониторинг в фоне
monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
monitor_thread.start()
print("⏰ Мониторинг продаж запущен!")

updater.start_polling()
updater.idle()
