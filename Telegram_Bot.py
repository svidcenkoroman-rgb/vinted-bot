import sqlite3
import requests
import time
import os
import re
import threading
from datetime import datetime
from telegram.ext import Updater, CommandHandler

TOKEN = '8734372802:AAF3KKneCCOEYdZz_Z6Zv4kx2nNo39NNgM0'
ADMIN_CHAT_ID = 7321242131

CATEGORIES = {
    'мужская обувь': 16, 'мужские кроссовки': 16, 'мужские куртки': 1231,
    'мужские штаны': 1224, 'мужские джинсы': 1224, 'мужские футболки': 1225,
    'мужские толстовки': 1228, 'мужские рубашки': 1226, 'мужские костюмы': 1232,
    'мужские шорты': 1227, 'мужские свитера': 1229, 'мужские аксессуары': 1241,
    'мужские шапки': 1241, 'мужские ремни': 1241,
    'женская обувь': 1037, 'женские кроссовки': 1037, 'женские куртки': 1143,
    'женские штаны': 1138, 'женские джинсы': 1138, 'женские футболки': 1132,
    'женские платья': 1235, 'женские юбки': 1136, 'женские толстовки': 1133,
    'женские блузки': 1131, 'женские свитера': 1134, 'женские сумки': 1245,
    'женские аксессуары': 1244, 'женские шапки': 1244, 'женское бельё': 1140,
    'женские купальники': 1141,
    'обувь': 16, 'кроссовки': 16, 'куртки': 1231, 'штаны': 1224,
    'джинсы': 1224, 'футболки': 1225, 'платья': 1235, 'сумки': 1245,
    'толстовки': 1228, 'рубашки': 1226, 'свитера': 1229, 'шорты': 1227,
    'аксессуары': 1241, 'шапки': 1241, 'ремни': 1241, 'часы': 1246,
    'очки': 1246, 'украшения': 1244, 'парфюм': 1260,
    'спортивная одежда': 1230, 'пальто': 1231, 'пиджаки': 1232,
    'носки': 1243, 'перчатки': 1241, 'шарфы': 1241,
}

COOKIE = '__ps_r=https://www.google.com/; __ps_lu=https://www.vinted.pl/; v_udt=UDdEZU55ZVR6bkZBaWdnOXo2TUpuQ2RCaFN3SC0tM1c4K0lGYW56SzhuWXF5My0tWlBQN25tdGdXNlJxbFRUYWhVOWZpUT09; anon_id=dc3d5138-f0e2-44b6-b322-67bac0ad7f0e; refresh_token_web=eyJraWQiOiJFNTdZZHJ1SHBsQWp1MmNObzFEb3JIM2oyN0J1NS1zX09QNVB3UGlobjVNIiwiYWxnIjoiUFMyNTYifQ.eyJhY2NvdW50X2lkIjozMTc3MTg4NDMwLCJhcHBfaWQiOjQsImF1ZCI6ImZyLmNvcmUuYXBpIiwiY2xpZW50X2lkIjoid2ViIiwiZXhwIjoxNzg2MTk5MDg2LCJpYXQiOjE3ODU1OTQyODYsImlzcyI6InZpbnRlZC1pYW0tc2VydmljZSIsImxvZ2luX3R5cGUiOjMsInB1cnBvc2UiOiJyZWZyZXNoIiwicm9sZXMiOiIiLCJzY29wZSI6InB1YmxpYyB1c2VyIiwic2lkIjoiNzJkNGUxZTYtMTc4NTU5NDI4NiIsInN1YiI6IjMxNzI3NjcwNDQiLCJjYyI6IlBMIiwiYW5pZCI6ImRjM2Q1MTM4LWYwZTItNDRiNi1iMzIyLTY3YmFjMGFkN2YwZSIsImFjdCI6eyJzdWIiOiIzMTcyNzY3MDQ0In19.KCl6SWmavsNXVjS3VPyjEDS37ynzCCUnHG44AnrSSBzRvowMTjaCCsUMxzxEU7b1JKFWzBdOLUfvYvlvczi1k53w-qQSS_bYM7eBQbjjLX7HZqcuNNCeDyXP6NGejxAwwsfeHQQUJz2OjYC_A8mgnfXCGHh81LPtN54zPgN8A6QV1Epp_6O0StFJ2O45MFq-VFZ-nofrQOhfIeP4brWKOocHyKwMlXIGc1GgVTlF7PHJN9Qi1uG51Ph8-aufUSMd4aI92c8NPmpKci-29PPyy9oywpeg28k7LcZnK5xl3EqPJOMlbltRioT_Tmqzkp0-mOjit0xevQPgUdOWZq3u9Q; access_token_web=eyJraWQiOiJFNTdZZHJ1SHBsQWp1MmNObzFEb3JIM2oyN0J1NS1zX09QNVB3UGlobjVNIiwiYWxnIjoiUFMyNTYifQ.eyJhY2NvdW50X2lkIjozMTc3MTg4NDMwLCJhcHBfaWQiOjQsImF1ZCI6ImZyLmNvcmUuYXBpIiwiY2xpZW50X2lkIjoid2ViIiwiZXhwIjoxNzg1NjAxNDg2LCJpYXQiOjE3ODU1OTQyODYsImlzcyI6InZpbnRlZC1pYW0tc2VydmljZSIsImxvZ2luX3R5cGUiOjMsInB1cnBvc2UiOiJhY2Nlc3MiLCJyb2xlcyI6IiIsInNjb3BlIjoicHVibGljIHVzZXIiLCJzaWQiOiI3MmQ0ZTFlNi0xNzg1NTk0Mjg2Iiwic3ViIjoiMzE3Mjc2NzA0NCIsImNjIjoiUEwiLCJhbmlkIjoiZGMzZDUxMzgtZjBlMi00NGI2LWIzMjItNjdiYWMwYWQ3ZjBlIiwiYWN0Ijp7InN1YiI6IjMxNzI3NjcwNDQifX0.b-ymSGjb3mzYvLuNdCPaGWnfk3lOjvKwric-s2FzbOp2w5_KGukFTZJtbSqLtO5ewN6T28xnO8KHnHkMjWC0OBtZk01FrutWxAD4RjyNSNcLlB2sVOl5Y7MjB0cgMcSgqJL5ic0pbze6rRoWalPGz03-6iYddPvV8j_FMX2EUlvHlPzP8Q9PfNkbe2f3_HGcfhhf51rkokDlYPf7rbU9CBc49PcUp1re9ORBCkYX2564Q75Oz7WRQktBVb0jHoVu51s7XriJ6trBLe0o6JXcdx0GS_J3ZLyWJ4sYcpva7-fptr8cCcqrDXHZ0R-kkMfdYGMqHhx7c7UafSGKjeldSQ; v_uid=3172767044; v_sid=72d4e1e6-1785594286; cf_clearance=KPC.nRMhMgiatAoQUm96k55rG3tag5BScFm4sJdnQ4M-1785599507-1.2.1.1-rvZqHVlkAyzpc_ozYosA0Fgf8oh0aig7cikSMbcM7m7TunBw2zHISFTzJE5ycKq3Q2T1GueupDlR3B4atROxbkHCCCOQMf.YpgJVlnroh6tHpO7PzJQURWyBumv7KaqDSe2J4F6UrcXB.IjSBcuh7.UWk1VBtMj4fnX5qOlb1VjdN1fSlGNYrXFRb1hsezWG1k6EDLrnYzNrD7NxBg4erPfjvYQc33p2H6Lw.fTSHNKcgej5.NxKoIM.u8aVZEnb5t0gJU.4WMCZC0mCEwhcNpw8hn7CO5r1lA5yAGKi8x6IE.G1oX_pXT6jjv9c28KbEexI402OajnlIdUM1r8fHXnx7Q0BhIohxwu_9IQbGcxhdxxSK6sCM9pj9EUP5CVwREbuoSWA7L8ZvmsBBvgRHp2a4Z6eu4egKjk8kbc0RozvGb4zitE0UCRq8n_fmr06qXGxYEvsvbKh6OcT7SUsLg; _vinted_fr_session=bXUxaXpyNEFaUmV6OEpJM3g3LytLc2tSYmRuYjM3WmhVdlJtR3NCSTJvRXkxNmVQRjQ1T01DUXpyTDhMQmhKd01FZkVVSlZNcThkWkdRNmJJSE5MTWlQVUtzaVZna1hPYUozdjZQWG9UVG5mc2Q1MFJiS1l1NXNGdG1Lb2NocDlodGNxNHdhWUdzSVhiajVKSlJHZ3hsWitOd3huVE5LK1Y3RGdnVTIvTnh2Q1VVdk8wOGp4UGk4MEVIbjdFMEhXbVh3eERHdk9ETjhrUmNtQndRVGRwMWRINEVuM3ppZzdwWGdWYThYWU9tMmV1cmFGeDhQTzA5cWxyaS9Hb2IwZk5EczUvYkg1WWRicSt1SWtrVTBBNmhkWkwwcTd1THp0ZTNOU1FudlJwLy9jWlh6b3dabElFcTc1b1hQMlcvTlpiUFRpUHVMamhwelZ3UE5sMTE2bkdvZmtoYnMzS3pzQTlBUVdJNEtSY1dLYjlpRzhRYW5tSW1hRVlLRmtXYUlPYmZEVTg0L3lkYkJUbXNkZEd1Wm42Rmx2N3VLamQzQWFjM0tEK25SNC9HYlFHVE4ya2UwcElhZDFVUVZuZ3VMTi0tZ2VmaytMOGVIbTQwbFdyTWxCUS92dz09--6faa73e1383104a87e26f10eb170330a73199b22; datadome=pPCXWmhfhIcGp9rMPPI_8Iji8s2HRkCZ1bxE_~JRRJC1G4CnzUiHd0cWcbACp3IxPwLiYWGOOAvirehkXiQcAcSyWpB5PVPMuHp29Emb3t_3cd9dByPYD5I1jWKGWr2D'

if os.path.exists('cookie.txt'):
    with open('cookie.txt', 'r') as f:
        saved = f.read().strip()
        if saved:
            COOKIE = saved
            print("Cookie загружены из файла ✅")

headers = {
    'accept': 'application/json,text/plain,*/*',
    'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': COOKIE.strip(),
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

def hex_to_color_name(hex_color):
    if not hex_color:
        return None
    try:
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        if r < 50 and g < 50 and b < 50: return '⚫ Чёрный'
        elif r > 200 and g > 200 and b > 200: return '⚪ Белый'
        elif r > 180 and g > 180 and b > 180: return '🔘 Светло-серый'
        elif r > 100 and g > 100 and b > 100: return '🔘 Серый'
        elif r > 150 and g < 80 and b < 80: return '🔴 Красный'
        elif r < 80 and g < 80 and b > 150: return '🔵 Синий'
        elif r < 80 and g > 150 and b < 80: return '🟢 Зелёный'
        elif r > 180 and g > 100 and b < 50: return '🟠 Оранжевый'
        elif r > 200 and g > 200 and b < 80: return '🟡 Жёлтый'
        elif r > 100 and g < 60 and b > 100: return '🟣 Фиолетовый'
        elif r > 100 and g < 60 and b < 60: return '🟤 Коричневый'
        elif r > 180 and g < 100 and b > 150: return '🩷 Розовый'
        elif r > 150 and g > 150 and b < 80: return '🫒 Хаки'
        elif r < 80 and g > 100 and b > 100: return '🩵 Голубой'
        else: return '🔘 Серый'
    except:
        return None

def get_color(item):
    photos = item.get('photos', [])
    if photos:
        color = hex_to_color_name(photos[0].get('dominant_color', ''))
        if color:
            return color
    return 'N/A'

def create_database():
    conn = sqlite3.connect('vinted.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY, title TEXT, brand TEXT, price REAL,
        currency TEXT, size TEXT, color TEXT, likes INTEGER DEFAULT 0,
        views INTEGER DEFAULT 0, url TEXT, first_seen TEXT, last_seen TEXT,
        sold INTEGER DEFAULT 0, days_to_sell REAL DEFAULT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS item_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT, item_id INTEGER,
        price REAL, likes INTEGER, views INTEGER, recorded_at TEXT)''')
    conn.commit()
    conn.close()
    print("База данных создана ✅")

def get_items_from_vinted(query, pages=5, category_id=None):
    all_items = []
    session = requests.Session()
    for page in range(1, pages + 1):
        url = 'https://www.vinted.pl/api/v2/catalog/items'
        params = {'search_text': query, 'per_page': 96, 'page': page, 'order': 'newest_first'}
        if category_id:
            params['catalog_ids[]'] = category_id
        print(f"Cookie: '{headers['cookie'][:30]}'")
        response = session.get(url, headers=headers, params=params)
        print(f"Страница {page}: статус {response.status_code}")
        if response.status_code != 200:
            print(f"Ошибка: {response.text[:200]}")
            if response.status_code == 401:
                try:
                    from telegram import Bot
                    Bot(token=TOKEN).send_message(
                        chat_id=ADMIN_CHAT_ID,
                        text='⚠️ Cookie истекли!\n\n1. Открой vinted.pl\n2. F12 → Network → Fetch/XHR\n3. Copy as cURL\n4. Напиши: /updatecookie [cURL]'
                    )
                except: pass
            break
        items = response.json().get('items', [])
        print(f"Найдено: {len(items)}")
        if not items: break
        all_items.extend(items)
        time.sleep(2)
    return all_items

def save_items(items):
    conn = sqlite3.connect('vinted.db')
    cursor = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_count = updated_count = 0
    for item in items:
        try:
            price_data = item.get('price', {})
            price = float(price_data.get('amount', 0))
            likes = item.get('favourite_count', 0)
            views = item.get('view_count', 0)
            item_id = item.get('id')
            color = get_color(item)
            cursor.execute('SELECT id FROM items WHERE id = ?', (item_id,))
            if cursor.fetchone():
                cursor.execute('UPDATE items SET likes=?,views=?,last_seen=?,price=?,color=? WHERE id=?',
                    (likes, views, now, price, color, item_id))
                updated_count += 1
            else:
                cursor.execute('INSERT INTO items (id,title,brand,price,currency,size,color,likes,views,url,first_seen,last_seen,sold) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,0)',
                    (item_id, item.get('title'), item.get('brand_title'), price,
                     price_data.get('currency_code', 'PLN'), item.get('size_title', 'N/A'),
                     color, likes, views, f"https://www.vinted.pl/items/{item_id}", now, now))
                new_count += 1
            cursor.execute('INSERT INTO item_history (item_id,price,likes,views,recorded_at) VALUES (?,?,?,?,?)',
                (item_id, price, likes, views, now))
        except Exception as e:
            print(f"Ошибка: {e}")
    conn.commit()
    conn.close()
    return new_count, updated_count

def calculate_analytics(query, items):
    prices = [float(i.get('price', {}).get('amount', 0)) for i in items if i.get('price')]
    prices = [p for p in prices if p > 0]
    if not prices: return None
    likes_list = [i.get('favourite_count', 0) for i in items]
    avg_price = sum(prices) / len(prices)
    median = sorted(prices)[len(prices) // 2]
    std_dev = (sum((p - avg_price) ** 2 for p in prices) / len(prices)) ** 0.5
    avg_likes = sum(likes_list) / len(likes_list) if likes_list else 0
    demand_index = avg_likes / len(items) if items else 0
    sizes = {}
    for i in items:
        s = i.get('size_title', 'N/A')
        if s and s != 'N/A': sizes[s] = sizes.get(s, 0) + 1
    colors = {}
    for i in items:
        c = get_color(i)
        if c and c != 'N/A': colors[c] = colors.get(c, 0) + 1
    brands = {}
    for i in items:
        b = i.get('brand_title', 'N/A')
        if b and b != 'N/A': brands[b] = brands.get(b, 0) + 1
    score = 5.0
    if demand_index > 10: score += 2
    elif demand_index > 5: score += 1
    if std_dev < avg_price * 0.3: score += 1
    if len(items) > 200: score += 1
    if avg_likes > 15: score += 1
    return {
        'total': len(items), 'avg_price': round(avg_price, 2),
        'median': round(median, 2), 'min_price': round(min(prices), 2),
        'max_price': round(max(prices), 2), 'std_dev': round(std_dev, 2),
        'avg_likes': round(avg_likes, 1), 'demand_index': round(demand_index, 3),
        'cheap': len([p for p in prices if p < avg_price * 0.7]),
        'mid': len([p for p in prices if avg_price * 0.7 <= p <= avg_price * 1.3]),
        'expensive': len([p for p in prices if p > avg_price * 1.3]),
        'top_sizes': sorted(sizes.items(), key=lambda x: x[1], reverse=True)[:5],
        'top_colors': sorted(colors.items(), key=lambda x: x[1], reverse=True)[:5],
        'top_brands': sorted(brands.items(), key=lambda x: x[1], reverse=True)[:3],
        'score': round(min(10, max(1, score)), 1),
        'cheapest': sorted(items, key=lambda x: float(x.get('price', {}).get('amount', 999)))[:3],
        'optimal_buy': round(avg_price * 0.65, 2),
        'optimal_sell': round(avg_price * 0.9, 2),
    }

def start(update, context):
    update.message.reply_text("""👋 Привет! Я Vinted Analytics Bot!

📊 Команды:
/item [бренд] | [категория] — полный анализ
/analyze [бренд] — анализ бренда
/categories — список категорий
/sold [запрос] — статистика продаж

Примеры:
/item Nike | мужские кроссовки
/item Zara | женские платья""")

def categories(update, context):
    msg = "📋 КАТЕГОРИИ:\n\n👨 МУЖСКОЕ:\n"
    for k in CATEGORIES:
        if 'мужск' in k: msg += f"  • {k}\n"
    msg += "\n👩 ЖЕНСКОЕ:\n"
    for k in CATEGORIES:
        if 'женск' in k: msg += f"  • {k}\n"
    msg += "\n👕 УНИСЕКС:\n"
    for k in CATEGORIES:
        if 'мужск' not in k and 'женск' not in k: msg += f"  • {k}\n"
    update.message.reply_text(msg)

def item_analyze(update, context):
    if not context.args:
        update.message.reply_text('Напиши: /item Nike | мужские кроссовки')
        return
    full_query = ' '.join(context.args)
    if '|' in full_query:
        parts = full_query.split('|')
        query = parts[0].strip()
        category_name = parts[1].strip().lower()
        category_id = CATEGORIES.get(category_name)
        if not category_id:
            update.message.reply_text(f'❌ Категория "{category_name}" не найдена. Напиши /categories')
            return
    else:
        query = full_query
        category_name = None
        category_id = None
    msg_text = f'🔍 Анализирую: {query}'
    if category_name: msg_text += f'\n📂 Категория: {category_name}'
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
    bar = '█' * int(data['score']) + '░' * (10 - int(data['score']))
    cat_line = f"\n📂 Категория: {category_name}" if category_name else ""
    msg = f"""🎓 HARVARD ANALYTICS: {query}{cat_line}

📦 ПРЕДЛОЖЕНИЕ:
  Объявлений: {data['total']}
  Новых: {new} / Обновлено: {updated}

💰 ЦЕНОВОЙ АНАЛИЗ:
  Средняя: {data['avg_price']} PLN
  Медиана: {data['median']} PLN
  Мин: {data['min_price']} PLN
  Макс: {data['max_price']} PLN
  Отклонение: ±{data['std_dev']} PLN

❤️ ИНДЕКС СПРОСА:
  Среднее лайков: {data['avg_likes']}
  Лайков/Предложений: {data['demand_index']}

📊 РАСПРЕДЕЛЕНИЕ ЦЕН:
  🟢 Дёшево: {data['cheap']} шт
  🟡 Средне: {data['mid']} шт
  🔴 Дорого: {data['expensive']} шт

📐 ТОП РАЗМЕРЫ:"""
    for s, c in data['top_sizes']: msg += f"\n  • {s} — {c} шт"
    msg += "\n\n🎨 ТОП ЦВЕТА:"
    if data['top_colors']:
        for col, c in data['top_colors']: msg += f"\n  • {col} — {c} шт"
    else: msg += "\n  • Данные недоступны"
    msg += "\n\n🏆 ТОП БРЕНДЫ:"
    for b, c in data['top_brands']: msg += f"\n  • {b} — {c} шт"
    msg += f"""

📈 СКОРИНГ: {bar} {data['score']}/10

💡 РЕКОМЕНДАЦИЯ:
  Покупай до: {data['optimal_buy']} PLN
  Продавай за: {data['optimal_sell']} PLN
  Потенциал: +{round(data['optimal_sell'] - data['optimal_buy'], 2)} PLN

🏷 САМЫЕ ДЕШЁВЫЕ:"""
    for item in data['cheapest']:
        price = item.get('price', {}).get('amount', 'N/A')
        title = str(item.get('title', 'N/A'))[:25]
        size = item.get('size_title', '')
        msg += f"\n  • {title} ({size}) — {price} PLN\n    https://www.vinted.pl/items/{item.get('id')}"
    update.message.reply_text(msg)

def analyze(update, context):
    if not context.args:
        update.message.reply_text('Напиши: /analyze Nike')
        return
    brand = ' '.join(context.args)
    update.message.reply_text(f'🔍 Анализирую {brand}...')
    items = get_items_from_vinted(brand, pages=3)
    if not items:
        update.message.reply_text(f'❌ Ничего не найдено')
        return
    save_items(items)
    data = calculate_analytics(brand, items)
    if not data:
        update.message.reply_text('❌ Ошибка')
        return
    update.message.reply_text(f"""📊 АНАЛИЗ: {brand}
📦 Объявлений: {data['total']}
💰 Средняя: {data['avg_price']} PLN
📉 Мин: {data['min_price']} PLN
📈 Макс: {data['max_price']} PLN
❤️ Лайков: {data['avg_likes']}
📈 Скоринг: {data['score']}/10""")

def check_sold_items():
    conn = sqlite3.connect('vinted.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT id, first_seen, last_seen FROM items 
        WHERE sold = 0 AND first_seen < datetime('now', '-6 hours')
        AND last_seen > datetime('now', '-7 days')''')
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
            response = session.get(f'https://www.vinted.pl/api/v2/items/{item_id}', headers=headers)
            if response.status_code == 404:
                conn = sqlite3.connect('vinted.db')
                cursor = conn.cursor()
                cursor.execute('SELECT first_seen FROM items WHERE id = ?', (item_id,))
                row = cursor.fetchone()
                if row:
                    days = (datetime.now() - datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')).total_seconds() / 86400
                    cursor.execute('UPDATE items SET sold=1, days_to_sell=? WHERE id=?', (round(days, 2), item_id))
                    conn.commit()
                    sold_count += 1
                conn.close()
            time.sleep(0.5)
        except Exception as e:
            print(f"Ошибка: {e}")
    print(f"Продано: {sold_count}")

def get_sell_stats(query):
    conn = sqlite3.connect('vinted.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT COUNT(*), AVG(days_to_sell), MIN(days_to_sell), MAX(days_to_sell)
        FROM items WHERE sold = 1 AND title LIKE ?''', (f'%{query}%',))
    row = cursor.fetchone()
    conn.close()
    return row

def monitor_loop():
    while True:
        print("🔍 Запускаю мониторинг продаж...")
        try:
            check_sold_items()
        except Exception as e:
            print(f"Ошибка: {e}")
        print("⏰ Следующая проверка через 1 час")
        time.sleep(3600)

def sold_stats(update, context):
    if not context.args:
        update.message.reply_text('Напиши: /sold Nike')
        return
    query = ' '.join(context.args)
    row = get_sell_stats(query)
    if not row or row[0] == 0:
        update.message.reply_text(f'❌ Нет данных для {query}\nПопробуй завтра!')
        return
    update.message.reply_text(f"""⚡️ ПРОДАЖИ: {query}
✅ Продано: {row[0]}
⏱ Среднее время: {round(row[1], 1)} дней
🚀 Быстрейшая: {round(row[2], 1)} дней
🐌 Дольше всего: {round(row[3], 1)} дней""")

def update_cookie(update, context):
    if not context.args:
        update.message.reply_text('📋 Напиши: /updatecookie [вставь cURL]')
        return
    curl_text = ' '.join(context.args)
    cookie_match = re.search(r"-b '([^']+)'", curl_text) or re.search(r'-b "([^"]+)"', curl_text)
    if not cookie_match:
        update.message.reply_text('❌ Не могу найти cookie. Скопируй "Copy as cURL"')
        return
    new_cookie = cookie_match.group(1).strip()
    global headers
    headers['cookie'] = new_cookie
    with open('cookie.txt', 'w') as f:
        f.write(new_cookie)
    session = requests.Session()
    response = session.get('https://www.vinted.pl/api/v2/catalog/items',
        headers=headers, params={'search_text': 'Nike', 'per_page': 1})
    if response.status_code == 200:
        update.message.reply_text('✅ Cookie обновлены!')
    else:
        update.message.reply_text(f'⚠️ Статус {response.status_code}. Попробуй /item Nike')

create_database()

updater = Updater(TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('analyze', analyze))
dp.add_handler(CommandHandler('item', item_analyze))
dp.add_handler(CommandHandler('categories', categories))
dp.add_handler(CommandHandler('sold', sold_stats))
dp.add_handler(CommandHandler('updatecookie', update_cookie))

print('🤖 Бот запущен!')
monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
monitor_thread.start()
print("⏰ Мониторинг продаж запущен!")

updater.start_polling()
updater.idle()
