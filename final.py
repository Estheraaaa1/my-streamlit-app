#import 有的沒的東西
import streamlit as st
import time
import requests
import random
import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.font_manager as fm
from streamlit_extras.let_it_rain import rain
from opencc import OpenCC

# 簡體轉繁體
cc = OpenCC('s2t')  

# 網頁標題
st.set_page_config(page_title="canibeacouchpotatotoday?", layout="centered")

# 初始資料檢查 
csv_path = "mood_log.csv"

# 中文字型處理
import os
import urllib.request
import matplotlib.font_manager as fm
from pathlib import Path

# 建立 fonts 資料夾
fonts_dir = Path("fonts")
fonts_dir.mkdir(exist_ok=True)

# 字體來源（Google Noto Sans TC）
from pathlib import Path
import matplotlib.font_manager as fm

# 使用已上傳的字體檔案
font_path = Path("NotoSansTC-ExtraBold.ttf")
font_prop = fm.FontProperties(fname=str(font_path)) if font_path.exists() else None

# 一堆語言互相切換的對照表
lang_options = {
    "中文": "zh",
    "English": "en",
    "Čeština": "cz"
}
lang_display = st.sidebar.selectbox("🌐 語言 / Language / Jazyk", list(lang_options.keys()))
lang = lang_options[lang_display]  

#放幾個主要的城市翻譯
city_translation = {
    "台北": {"English": "Taipei", "Čeština": "Tchaj-pej"},
    "台中": {"English": "Taichung", "Čeština": "Tchaj-čung"},
    "台南": {"English": "Tainan", "Čeština": "Tchaj-nan"},
    
}

weather_translation = {
    "晴": {"English": "Sunny", "Čeština": "Slunečno"},
    "多雲": {"English": "Cloudy", "Čeština": "Zataženo"},
    "陰": {"English": "Overcast", "Čeština": "Zamračeno"},
    "小雨": {"English": "Light Rain", "Čeština": "Slabý déšť"},
}

text = {
    "zh": {
        "page_title": "我是一顆沙發馬鈴薯嗎？",
        "title": "aka 我到底要不要去早八😯ㄉ判斷器",
        "input_name": "你的暱稱是？",
        "input_city": "你現在在哪個城市？（輸入中文或英文）",
        "mood_prompt": "用表情表示你今天的心情：",
        "submit": "🔮 幫我判斷",
        "weather": "目前天氣",
        "advice_score": "🚦 出門建議指數",
        "quote": "📖 每日一句",
        "tab1": "🔮 判斷區",
        "tab2": "📊 心情紀錄",
        "tab3": "📈 心情趨勢",
        "clear_button": "🧹 清除所有紀錄",
        "clear_success": "✅ 所有紀錄已刪除！",
        "avg_mood": "最近平均心情",
        "unit_score": "分",
        "common_weather": "最常見天氣",
        "trend_title": "🧠 心情趨勢回顧",
        "select_month": "📆 選擇要查看的月份",
        "no_records": "這個月份還沒有任何心情紀錄哦！",
        "important_event": "今天有重要的出門行程嗎？",
        "early_class": "今天有早八嗎？",
        "history_title": "🗓️ 歷史紀錄",
        "invalid_city": "⚠️ 找不到這個城市，請檢查拼字或稍後再試。",
        "column_date": "日期",
        "column_city": "城市",
        "column_mood": "心情分數",
        "column_event": "重要行程",
        "column_weather": "天氣",
        "column_temp": "氣溫",
        "column_score": "出門指數",
        "column_suggestion": "系統建議",
        "trend_title": "🧠 心情趨勢回顧",
        "month_select": "📆 選擇要查看的月份",
        "no_data": "這個月份還沒有任何心情紀錄哦！",
        "trend_error": "⚠️ 發生錯誤：",
        "no_record": "目前還沒有任何紀錄，請先開始使用出門判斷器！",
        "mood_trend_chart": "{} 的心情趨勢",
        "y_label": "心情 (1-10)",
        "x_label": "日期",
        "potato_score": "馬鈴薯指數",  
        "potato_hint": "指數越高，越適合宅在家：\n🥔🥔🥔🥔🥔 = 超級想躺平\n🥔🥔🥔 = 不太想動\n🥔 = 精神滿滿，出門吧！",
        "emoji_style_prompt": "請選擇今天的 emoji 風格 🎭",
        "records_loaded": "✅ 已讀取筆數：{} 筆",

    },
    "en": {
        "page_title": "amiacouchpotato?",
        "title": "Should I go out today?",
        "input_name": "What's your name?",
        "input_city": "Which city are you in? (English)",
        "mood_prompt": "Choose an emoji to describe your mood:",
        "submit": "🔮 Let's see!",
        "weather": "Current weather",
        "advice_score": "🚦 Go-out Score",
        "quote": "📖 Daily Quote",
        "tab1": "🔮 Decision Zone",
        "tab2": "📊 Mood Records",
        "tab3": "📈 Mood Trends",
        "clear_button": "🧹 Clear All Records",
        "clear_success": "✅ All records deleted!",
        "avg_mood": "Recent Average Mood",
        "unit_score": "points",
        "common_weather": "Most Common Weather",
        "select_month": "📆 Select a month to view",
        "no_records": "No mood records for this month yet.",
        "important_event": "Do you have an important outing today?",
        "early_class": "Do you have an early class?",
        "common_weather": "Most Common Weather",
        "history_title": "🗓️ History Records",
        "invalid_city": "⚠️ Couldn't find this city. Please check the spelling.",
        "column_date": "Date",
        "column_city": "City",
        "column_mood": "Mood Score",
        "column_event": "Important Event",
        "column_weather": "Weather",
        "column_temp": "Temperature",
        "column_score": "Go-out Score",
        "column_suggestion": "System Suggestion",
        "trend_title": "🧠 Mood Trends Overview",
        "month_select": "📆 Select a month to view",
        "no_data": "No mood records found for this month!",
        "trend_error": "⚠️ Error occurred:",
        "no_record": "No records yet. Try using the app first!",
        "mood_trend_chart": "Mood Trend in {}",
        "y_label": "Mood (1-10)",
        "x_label": "Date",
        "potato_score": "Potato Score",
        "potato_hint": "🥔 The more potatoes, the lazier the mood:\n🥔🥔🥔🥔🥔 = Stay in, relax\n🥔🥔🥔 = Meh, maybe not today\n🥔 = Energetic! Go out and shine!",
        "emoji_style_prompt": "Choose your emoji mood style 🎭",
        "records_loaded": "✅ Records loaded: {}",
    },
    "cz": {
        "page_title": "amiacouchpotato?",
        "title": "Mám dnes jít ven?",
        "input_name": "Jak se jmenuješ?",
        "input_city": "Ve kterém městě se právě nacházíš? (česky nebo anglicky)",
        "mood_prompt": "Vyber emoji podle své nálady:",
        "submit": "🔮 Ukázat výsledek",
        "weather": "Aktuální počasí",
        "advice_score": "🚦 Doporučení jít ven",
        "quote": "📖 Citát dne",
        "tab1": "🔮 Mám dnes jít ven?",
        "tab2": "📊 Záznamy nálady",
        "tab3": "📈 Trendy nálady",
        "clear_button": "🧹 Vymazat všechny záznamy",
        "clear_success": "✅ Všechny záznamy byly smazány!",
        "avg_mood": "Průměrná nálada (poslední dny)",
        "unit_score": "bodů",
        "common_weather": "Nejčastější počasí",
        "select_month": "📆 Vyberte měsíc",
        "no_records": "Pro tento měsíc zatím neexistují žádné záznamy nálady.",
        "important_event": "Máš dnes důležitý program venku?",
        "early_class": "Máš dnes ranní výuku?",
        "history_title": "🗓️ Historie záznamů",
        "invalid_city": "⚠️ Město nebylo nalezeno. Zkontroluj prosím pravopis.",
        "column_date": "Datum",
        "column_city": "Město",
        "column_mood": "Skóre nálady",
        "column_event": "Důležitá událost",
        "column_weather": "Počasí",
        "column_temp": "Teplota",
        "column_score": "Skóre výstupu",
        "column_suggestion": "Doporučení systému",
        "trend_title": "🧠 Přehled nálad",
        "month_select": "📆 Vyberte měsíc k zobrazení",
        "no_data": "V tomto měsíci nejsou žádné záznamy o náladě!",
        "trend_error": "⚠️ Došlo k chybě:",
        "no_record": "Zatím žádné záznamy. Nejdřív si zkuste aplikaci!",
        "mood_trend_chart": "Trend nálady v {}",
        "y_label": "Nálada (1–10)",
        "x_label": "Datum",
        "potato_score": "🥔 Bramborové skóre",
        "potato_hint": "Čím více brambor, tím větší lenost:\n🥔🥔🥔🥔🥔 = Zůstaň doma a relaxuj\n🥔🥔🥔 = Dnes možná radši nic\n🥔 = Plný energie! Vyraž ven!",
        "emoji_style_prompt": "Vyber si styl emoji 🎭", 
        "records_loaded": "✅ Počet načtených záznamů: {}",

    }
}
# 封面圖
st.markdown(
    f"""
    <div style="text-align:center;">
        <img src="https://raw.githubusercontent.com/Estheraaaa1/my-streamlit-app/main/cover.jpg" width="500"/>
        <p style="font-size:18px;">{text[lang]["title"]}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 分頁設計 
tab1, tab2, tab3 = st.tabs([
    text[lang]["tab1"],
    text[lang]["tab2"],
    text[lang]["tab3"]
])
st.markdown("""
<style>
    /* 選項容器橫向排列 */
    div[data-baseweb="radio"] > div {
        flex-direction: row;
        justify-content: center;
        gap: 2rem;
    }

    /* 每個按鈕的樣式 */
    div[data-baseweb="radio"] label {
        font-size: 20px;
        font-weight: bold;
        color: #999;
        border-bottom: 3px solid transparent;
        padding: 4px 6px;
    }

    /* 被選中的樣式 */
    div[data-baseweb="radio"] label[data-selected="true"] {
        color: #d6336c !important;
        border-bottom: 3px solid #ff4b4b !important;
    }
</style>

""", unsafe_allow_html=True)


# ========== tab1: 判斷區 ==========
with tab1:
    # --- 城市對應表 ---
    city_map = {
        "台北": "Taipei", "臺北": "Taipei",
        "新北": "New Taipei", "桃園": "Taoyuan",
        "台中": "Taichung", "臺中": "Taichung",
        "台南": "Tainan", "臺南": "Tainan",
        "高雄": "Kaohsiung", "基隆": "Keelung",
        "新竹": "Hsinchu", "苗栗": "Miaoli",
        "彰化": "Changhua", "南投": "Nantou",
        "雲林": "Yunlin", "嘉義": "Chiayi",
        "屏東": "Pingtung", "宜蘭": "Yilan",
        "花蓮": "Hualien", "台東": "Taitung", "臺東": "Taitung",
        "澎湖": "Penghu", "金門": "Kinmen", "連江": "Lienchiang"
    }

    # --- emoji 樣式與語言對應 ---
    style_labels = {
        "zh": {"人物": "人物", "動物": "動物", "食物": "食物"},
        "en": {"人物": "People", "動物": "Animals", "食物": "Food"},
        "cz": {"人物": "Lidé", "動物": "Zvířata", "食物": "Jídlo"}
    }
    emoji_styles = {
        "人物": ["💀1", "😣2", "😞3", "🥺4", "😐5", "🙂6", "😊7", "😃8", "🤩9", "🥳10"],
        "動物": ["🐌1", "🐢2", "🐰3", "🐶4", "🐱5", "🐭6", "🦊7", "🐻8", "🦁9", "🦄10"],
        "食物": ["🥀1", "🥔2", "🥚3", "🍞4", "🍩5", "🍜6", "🍔7", "🍎8", "🍉9", "🍰10"]
    }
    display_labels = [style_labels[lang][k] for k in emoji_styles]
    reverse_style_labels = {v: k for k, v in style_labels[lang].items()}
    # 設定 emoji_style_display 預設值（如 session_state 裡有，但不在 display_labels 內，就重設）
    default_style = display_labels[0]

# 如果 emoji_style_display 不存在，設定初始值
    if "emoji_style_display" not in st.session_state:
        st.session_state["emoji_style_display"] = display_labels[0]

    # selectbox 選擇後直接綁定 session_state，不使用 on_change callback
    # 顯示選單，防止 session_state 值不在清單中
    emoji_style_display = st.selectbox(
        label=text[lang]["emoji_style_prompt"],
        options=display_labels,
        index=display_labels.index(st.session_state["emoji_style_display"]) if st.session_state["emoji_style_display"] in display_labels else 0,
        key="emoji_style_display"
    )
    
    # --- 根據選擇的風格取得 emoji 列表 ---
    emoji_style_key = reverse_style_labels[st.session_state["emoji_style_display"]]
    emoji_options = emoji_styles[emoji_style_key]

    # --- 放進 form 裡 ---
    msg_text = {
        "zh": {
            "go_out": "今天不能當馬鈴薯...",
            "maybe_go": "今天出不出門都可以喔～ it's up to you :)",
            "stay_home": "今天不出門也沒瓜西...",
            "sleep_potato": "今天你是一顆馬鈴薯，請躺平"
        },
        "en": {
            "go_out": "Don’t be a couch potato today — get out there! 😠🤜",
            "maybe_go": "It’s up to you today :)",
            "stay_home": "Staying in is totally fine...",
            "sleep_potato": "Just lie down and be a couch potato 🥔"
        },
        "cz": {
            "go_out": "Dnes nesmíš být gaučový brambor – jdi ven! 😠🤜",
            "maybe_go": "Dnes je to na tobě :)",
            "stay_home": "Dnes můžeš být gaučový brambor v klidu!",
            "sleep_potato": "Lehni si a buď brambora 🥔"
        }
    }

    with st.form("main_form"):
        st.markdown(f"#### {text[lang]['input_name']}")
        name = st.text_input("", key="name_input")
        st.markdown(f"#### {name} {text[lang]['input_city']}")
        location = st.text_input("", key="city_input")

        st.markdown(f"#### {text[lang]['mood_prompt']}")
        mood_emoji = st.select_slider(
            label="",
            options=emoji_options,
            value=emoji_options[4],
            key="mood_slider"
        )
        full_score_messages = {
                "人物": {
                    "zh": "你今天散發明星光芒 ✨😎",
                    "en": "You're shining like a superstar today! ✨😎",
                    "cz": "Dnes záříš jako hvězda! ✨😎"
                },
                "動物": {
                    "zh": "你今天是隻開心的獨角獸！🦄",
                    "en": "You're a happy unicorn today! 🦄",
                    "cz": "Dnes jsi šťastný jednorožec! 🦄"
                },
                "食物": {
                    "zh": "你今天是個甜甜ㄉ蛋糕～大家都想咬一口！",
                    "en": "You're a super sweet cake today—everyone wants a bite!",
                    "cz": "Dnes jsi slaďoučký dortík—všichni si chtějí kousnout!"
                }
            }
        low_mood_msg = {
                "人物": {
                        "zh": "你看起來一臉心累 QQ 沒事吧？🥺",
                        "en": "You look totally drained today... Are you okay? 🥺",
                        "cz": "Vypadáš úplně vyčerpaně... Jsi v pohodě? 🥺"
                 },
                 "動物": {
                        "zh": "你今天是隻超慢的小蝸牛，還好嗎？🫂",
                        "en": "You're a super slow little snail today. Everything okay? 🫂",
                        "cz": "Dnes jsi pomalý šneček. Je všechno v pořádku? 🫂"
                 },
                    "食物": {
                        "zh": "你今天像枯掉的花花🥀 是不是需要一點糖？",
                        "en": "You're like a wilted flower today 🥀 — maybe some sugar would help?",
                        "cz": "Dnes jsi jako zvadlá květina 🥀 — co takhle trochu cukru?"
                }
            }
        mood_score = emoji_options.index(mood_emoji) + 1
        style_key = emoji_style_key

        if mood_score == 10:
            # 根據 emoji 風格 + 語言，顯示不同訊息
            st.balloons()
            st.success(full_score_messages[style_key][lang])
            
        elif mood_score == 1:
            st.warning(low_mood_msg[style_key][lang])
            # 找到目前選擇的 emoji 風格 key（中文為主）
        else:
            st.balloons()
            st.success(full_score_messages[style_key][lang])

        important_event = st.checkbox(text[lang]["important_event"], key="event_checkbox_1")
        early_class = st.checkbox(text[lang]["early_class"], key="early_class_checkbox_1")
        submitted = st.form_submit_button(text[lang]["submit"])

    def get_weather(city_name, lang_code="zh"):
        api_key = "b157fc4014bf42f9bb641721252805"
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city_name}&lang={lang_code}"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            if "current" not in data:
                raise ValueError("無法取得天氣資料")
            weather = data["current"]["condition"]["text"]
            temp = data["current"]["temp_c"]
            return weather, temp
        except Exception:
            return None, None

    if submitted and location:
    
        has_event = important_event or early_class
        query_city = city_map.get(location, location)
        weather_desc, temp = get_weather(query_city, lang_code=lang)
        weather_desc = cc.convert(weather_desc)
        if weather_desc is None:
            st.warning(text[lang]["invalid_city"])
            weather_desc = "未知"
            temp = 25
        else:
            weather_icons = {
                "zh": {"晴": "☀️", "多雲": "⛅", "陰": "☁️", "小雨": "🌧️", "雷雨": "⛈️", "雪": "❄️"},
                "en": {"Sunny": "☀️", "Partly cloudy": "⛅", "Cloudy": "☁️", "Rain": "🌧️", "Thunderstorm": "⛈️", "Snow": "❄️"},
                "cs": {"Slunečno": "☀️", "Polojasno": "⛅", "Zataženo": "☁️", "Déšť": "🌧️", "Bouřka": "⛈️", "Sníh": "❄️"}
            }            
            icon = weather_icons.get(lang, {}).get(weather_desc, "🌈")
            st.write(f"{text[lang]['weather']}：{weather_desc}，{temp}°C")

        # 出門指數計算
        score = 0
        score += mood_score * 5  # 把心情當成最重要的，所以要乘以 5！
        if "雨" not in weather_desc: #政大生標準很低，不下雨就很開心
            score += 30
        if important_event: #有重要場合還是要出門、、、
            score += 30
        if early_class: #早八bad 扣二十分
            score -= 20
        if 22 <= temp <= 30: #22~30應該是最舒服的天氣？
            score += 15
        score = min(score, 100) #滿分100分

        # 動畫 & 心靈雞湯語錄
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        gif_box = st.empty()

        if score > 80:
            message = random.choice([msg_text[lang]["go_out"]])
            img_path = os.path.join(BASE_DIR, "goout.gif")
            time.sleep(2)
            gif_box.empty()
            rain(
                emoji="💥",
                font_size=54,
                falling_speed=5,
                animation_length="infinite",
            )
        elif score > 60:
            message = random.choice([msg_text[lang]["maybe_go"]])
            img_path = os.path.join(BASE_DIR, "maybe.gif")
            time.sleep(2)
            gif_box.empty()
            rain(
                emoji="✨",
                font_size=54,
                falling_speed=5,
                animation_length="infinite",
            )
        elif score > 30:
            message = random.choice([msg_text[lang]["stay_home"]])
            img_path = os.path.join(BASE_DIR, "stayhome.gif")
            time.sleep(2)
            gif_box.empty()
            rain(
                emoji="🤙",
                font_size=54,
                falling_speed=5,
                animation_length="infinite",
            )
        else:
            message = random.choice([msg_text[lang]["sleep_potato"]])
            img_path = os.path.join(BASE_DIR, "sleep.gif")
            time.sleep(2)
            gif_box.empty()
            rain(
                emoji="🥔",
                font_size=54,
                falling_speed=5,
                animation_length="infinite",
            )
        gif_box.image(img_path, use_container_width=True)
        time.sleep(3)
        gif_box.empty()

        # 🥔 分數轉馬鈴薯顆數（顆數越多 → 越不想出門）
        potato_count = round((100 - score) / 20)  # 例如：score=40 → 馬鈴薯 = 3
        if potato_count > 0:
            potatoes = "🥔" * potato_count
        else:
            potatoes = "0️⃣"      
        st.subheader(f"{text[lang]['potato_score']}{potatoes}")
        st.caption(text[lang]["potato_hint"])
        st.write(f"💬 {message}")
        # 每日語錄（多語言支援）
        if score > 80:
            quote_pool = {
                "zh": [
                    "你已經準備好大展身手啦！🌟",
                    "世界需要你這麼閃耀的人～✨",
                    "出門的你就是主角！🎬"
                ],
                "en": [
                    "You're ready to shine! 🌟",
                    "The world needs your light ✨",
                    "You're the main character today! 🎬"
                ],
                "cz": [
                    "Jsi připraven zazářit! 🌟",
                    "Svět potřebuje tvé světlo ✨",
                    "Dnes jsi hlavní postava! 🎬"
                ]
            }
        elif score > 60:
            quote_pool = {
                "zh": [
                    "出門不一定有收穫，但不試試怎麼知道？😉",
                    "隨便走走也可能遇到驚喜 🍀",
                    "你的決定永遠值得被尊重。"
                ],
                "en": [
                    "Going out might surprise you 🍀",
                    "Give it a try—you never know!",
                    "Your decision is always valid."
                ],
                "cz": [
                    "Možná tě dnes čeká překvapení 🍀",
                    "Zkus to – nikdy nevíš, co se stane!",
                    "Tvé rozhodnutí je vždy správné."
                ]
            }
        elif score > 40:
            quote_pool = {
                "zh": [
                    "不想出門也沒關係，你已經很努力了 🧸",
                    "今天沒力氣？那就給自己多一點空間。",
                    "不一定要做什麼，活著就很棒了 🐢"
                ],
                "en": [
                    "It's okay to stay in. You’ve done enough 🧸",
                    "No energy? Give yourself a break.",
                    "Just being alive is enough 🐢"
                ],
                "cz": [
                    "Zůstat doma je v pořádku 🧸",
                    "Nemáš sílu? Dej si pauzu.",
                    "Jen být naživu je dost 🐢"
                ]
            }
        else:
            quote_pool = {
                "zh": [
                    "沒事的，就算只想窩著也很 OK 🛋️",
                    "請躺平，明天再戰！💤",
                    "能好好休息的人最酷了。"
                ],
                "en": [
                    "It's okay to do nothing today 🛋️",
                    "Rest now, rise tomorrow! 💤",
                    "Those who rest well are the coolest."
                ],
                "cz": [
                    "Je v pořádku dnes nedělat nic 🛋️",
                    "Odpočiň si dnes, zítra bojuj dál! 💤",
                    "Odpočívající lidé jsou ti nejvíc cool."
                ]
            }
        st.markdown(f"#### {text[lang]['quote']}")
        st.success(random.choice(quote_pool[lang]))

        
        # 決定好 message 後再建立 df
        # 建立原始 DataFrame（用中文欄位名）
        log = {
            "日期": [datetime.today().strftime("%Y-%m-%d")],
            "城市": [location],
            "心情分數": [mood_score],
            "有行程": [has_event],
            "天氣": [weather_desc],
            "氣溫": [temp],
            "出門指數": [score],
            "系統建議": [message]
        }
        df = pd.DataFrame(log)

        # 建立顯示用的欄位名稱對應（根據語言）
        column_map = {
            "日期": text[lang]["column_date"],
            "城市": text[lang]["column_city"],
            "心情分數": text[lang]["column_mood"],
            "有行程": text[lang]["column_event"],
            "天氣": text[lang]["column_weather"],
            "氣溫": text[lang]["column_temp"],
            "出門指數": text[lang]["column_score"],
            "系統建議": text[lang]["column_suggestion"]
        }
        df_display = df.rename(columns=column_map)

        # 儲存用的 CSV 檔不變（使用原始欄位名）
        if not os.path.exists(csv_path) or os.stat(csv_path).st_size == 0:
            df.to_csv(csv_path, index=False)
        else:
            with open(csv_path, "r") as f:
                first_line = f.readline().strip()
            if "日期" in first_line:
                df.to_csv(csv_path, mode="a", index=False, header=False)
            else:
                df.to_csv(csv_path, index=False)

# ========== tab2: 歷史紀錄 ==========
import pandas as pd
data = {
    "日期": ["2025-05-29", "2025-05-30", "2025-05-31"]
}
with tab2:
    st.header(text[lang]["history_title"])
    if st.button(text[lang]["clear_button"]):
        if os.path.exists(csv_path):
            os.remove(csv_path)
            st.success(text[lang]["clear_success"])
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)

        # 翻譯天氣和城市
        if lang_display in ["English", "Čeština"]:
            df["天氣"] = df["天氣"].apply(lambda w: weather_translation.get(w, {}).get(lang_display, w))
            df["城市"] = df["城市"].apply(lambda c: city_translation.get(c, {}).get(lang_display, c))

        column_map = {
            "日期": text[lang]["column_date"],
            "城市": text[lang]["column_city"],
            "心情分數": text[lang]["column_mood"],
            "有行程": text[lang]["column_event"],
            "天氣": text[lang]["column_weather"],
            "氣溫": text[lang]["column_temp"],
            "出門指數": text[lang]["column_score"],
            "系統建議": text[lang]["column_suggestion"]
        }
        df_display = df.rename(columns=column_map)
        st.dataframe(df_display.tail(7))  # ✅ 無論語言都會顯示
        st.write(text[lang]["records_loaded"].format(len(df)))

        # ➤ 原始欄位 df 拿來計算平均
        if "心情分數" in df.columns:
            avg_mood = round(df["心情分數"].mean(), 1)
            st.markdown(f"**{text[lang]['avg_mood']}：** {avg_mood} {text[lang]['unit_score']}")
        else:
            st.warning("⚠️ 資料表裡沒有「心情分數」欄位，無法計算平均。")
                # ➤ 翻譯後欄位名稱（df_display）找最常見天氣
        if text[lang]["column_weather"] in df_display.columns:
            most_common_weather = df_display[text[lang]["column_weather"]].mode()[0]
            st.markdown(f"**{text[lang]['common_weather']}：** {most_common_weather}")
        else:
            st.warning("⚠️ 找不到翻譯後的天氣欄位，請檢查資料。")

# ========== tab3: 心情趨勢 ==========
from datetime import datetime
with tab3:
    st.markdown(f"### {text[lang]['trend_title']}")

    # 先檢查檔案是否存在與不為空
    if os.path.exists(csv_path) and os.stat(csv_path).st_size > 0:
        try:
            df = pd.read_csv(csv_path)

            # 確認關鍵欄位存在
            if "日期" not in df.columns or "心情分數" not in df.columns:
                st.error("❌ mood_log.csv 檔案格式錯誤，找不到 '日期' 或 '心情分數' 欄位。")
                st.write("📋 目前欄位：", df.columns.tolist())
            else:
                # 轉換欄位格式
                df["日期"] = pd.to_datetime(df["日期"], errors="coerce")
                df["心情分數"] = pd.to_numeric(df["心情分數"], errors="coerce")
                df = df.dropna(subset=["日期", "心情分數"])

                if df.empty:
                    st.info(text[lang]["no_data"])
                else:
                    # 加入月份欄位
                    df["月份"] = df["日期"].dt.strftime("%Y-%m")
                    today = datetime.today()
                    this_month = today.strftime("%Y-%m")
                    last_month = (today.replace(day=1) - pd.Timedelta(days=1)).strftime("%Y-%m")
                    unique_months = sorted(set(df["月份"].dropna().tolist() + [this_month, last_month]), reverse=True)

                    selected_month = st.selectbox(text[lang]["month_select"], unique_months)

                    # 過濾選定月份資料
                    month_df = df[df["月份"] == selected_month]

                    if month_df.empty:
                        st.info(text[lang]["no_data"])
                    else:
                        labels = month_df["日期"].dt.strftime('%m/%d')
                        scores = month_df["心情分數"]

                        fig, ax = plt.subplots(figsize=(6, 3))
                        ax.plot(labels, scores, marker="o", linestyle="-", color="#4B8BBE", linewidth=2)

                        for x, y in zip(labels, scores):
                            ax.text(x, y + 0.2, f"{y:.0f}", ha='center', fontsize=9, color="#333", fontproperties=font_prop)

                        ax.set_title(
                            text[lang]["mood_trend_chart"].format(selected_month),
                            fontproperties=font_prop, fontsize=14, fontweight="bold"
                        )
                        ax.set_ylabel(text[lang]["y_label"], fontproperties=font_prop, fontsize=12)
                        ax.set_xlabel(text[lang]["x_label"], fontproperties=font_prop, fontsize=12)
                        ax.set_ylim(0, 11)
                        ax.grid(True, linestyle="--", alpha=0.5)
                        st.pyplot(fig)

        except Exception as e:
            st.error(f"⚠️ 發生錯誤：{e}")
    else:
        st.info("⚠️ 尚未有任何心情記錄，請先在判斷區輸入資料喔！")
