import streamlit as st

# --- НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="Email Generator", page_icon="📧", layout="centered")

# --- ИНИЦИАЛИЗАЦИЯ STATE (Чтобы работала вставка при клике) ---
if 'email_input' not in st.session_state:
    st.session_state.email_input = ""

# Функция для вставки примера
def paste_example():
    st.session_state.email_input = "name@gmail.com"

# --- СТИЛИ CSS ---
st.markdown("""
<style>
    /* 1. Скрываем скрепку (Anchor link) */
    [data-testid="stHeaderActionElements"] { display: none !important; }

    /* 2. Стиль для кнопки-примера (делаем её похожей на ссылку) */
    div.stButton.example-btn > button {
        background-color: transparent !important;
        border: none !important;
        color: #3498db !important; /* Цвет ссылки */
        padding: 0 !important;
        margin: 0 !important;
        font-size: 1rem !important;
        text-decoration: underline !important;
        cursor: pointer !important;
        line-height: 1.5 !important;
        height: auto !important;
        display: inline-flex !important;
    }
    div.stButton.example-btn > button:hover {
        color: #ff6600 !important; /* Цвет при наведении */
    }
    div.stButton.example-btn > button:focus {
        box-shadow: none !important;
        outline: none !important;
    }

    /* 3. Обычные стили для кнопок каналов */
    .custom-link {
        display: inline-block;
        text-decoration: none;
        color: white !important;
        font-weight: bold;
        width: 100%;
        padding: 10px;
        text-align: center;
        border-radius: 8px;
        margin-bottom: 8px;
        transition: 0.3s;
        font-size: 15px;
    }
    .custom-link:hover { opacity: 0.85; transform: translateY(-1px); }
    .crypto { background-color: #e67e22; }
    .resources { background-color: #2980b9; }
    
    /* Отступ сверху */
    .block-container { padding-top: 2rem; }
    
    /* Выравнивание текста и кнопки в одну строку */
    .row-widget { display: flex; align-items: baseline; gap: 5px; }
</style>
""", unsafe_allow_html=True)

# --- ЛОГИКА ГЕНЕРАЦИИ ---
def is_valid_email(email):
    if '@' not in email or email.count('@') != 1:
        return False
    local, domain = email.split('@')
    return bool(local and domain and not local.startswith('.') and not local.endswith('.'))

def generate_emails(local, domain, max_count=None):
    n = len(local)
    num_gaps = max(n - 1, 0)
    total = 1 << num_gaps
    limit = total if max_count is None else min(max_count, total)
    emails = []
    for mask in range(limit):
        modified = []
        for i in range(n):
            modified.append(local[i])
            if i < num_gaps and (mask & (1 << (num_gaps - 1 - i))):
                modified.append('.')
        emails.append(''.join(modified) + '@' + domain)
    return emails

# --- ИНТЕРФЕЙС ---
st.title("📧 Генератор Email")
st.write("Сделайте из одной почты тысячи уникальных вариантов.")

# --- ХИТРАЯ ВЕРСТКА: Текст + Кнопка в одну строку ---
# Создаем колонки, чтобы кнопка стояла рядом с текстом
col_text, col_btn, col_end = st.columns([1.65, 1, 2]) 

with col_text:
    st.markdown("<div style='text-align: right; padding-top: 5px;'>Введите ваш email (например: </div>", unsafe_allow_html=True)

with col_btn:
    # Оборачиваем кнопку в div с классом example-btn для CSS стилизации
    st.markdown('<div class="example-btn">', unsafe_allow_html=True)
    st.button("name@gmail.com", on_click=paste_example, key="ex_btn")
    st.markdown('</div>', unsafe_allow_html=True)

with col_end:
     st.markdown("<div style='padding-top: 5px;'>)</div>", unsafe_allow_html=True)

# ПОЛЕ ВВОДА (Скрываем стандартный label, так как сделали свой выше)
email_input = st.text_input(
    "Label скрыт", 
    value=st.session_state.email_input, 
    key="email_input_widget",
    label_visibility="collapsed",
    placeholder="name@gmail.com"
)

# Синхронизация виджета со стейтом (если пользователь вводит руками)
if email_input != st.session_state.email_input:
    st.session_state.email_input = email_input

# --- ОБРАБОТКА ---
if email_input:
    if is_valid_email(email_input):
        local, domain = email_input.split('@')
        num_gaps = len(local) - 1
        total_variants = 2 ** num_gaps if num_gaps > 0 else 1
        
        st.success(f"✅ Email корректный! Вариантов: **{total_variants:,}**")
        
        c1, c2 = st.columns([1.5, 1])
        with c1:
            mode = st.radio("Режим:", ["Количество", "Все сразу"], horizontal=True, label_visibility="collapsed")
        
        limit = None
        if mode == "Количество":
            with c2:
                limit = st.number_input("Сколько штук?", min_value=1, max_value=total_variants, value=min(100, total_variants), label_visibility="collapsed")

        st.write("")
        
        if st.button("🚀 Сгенерировать", type="primary", use_container_width=True):
            with st.spinner("Работаем..."):
                results = generate_emails(local, domain, limit if mode == "Количество" else None)
                result_text = "\n".join(results)
                st.session_state['result'] = result_text
                st.session_state['count'] = len(results)
    else:
        st.error("❌ Ошибка формата email")

# --- РЕЗУЛЬТАТ ---
if 'result' in st.session_state:
    st.divider()
    col_head, col_btn = st.columns([2, 1])
    with col_head:
        st.markdown(f"### Результат ({st.session_state['count']} шт.)")
    with col_btn:
        st.download_button(
            label="💾 Скачать .txt",
            data=st.session_state['result'],
            file_name="emails.txt",
            mime="text/plain",
            use_container_width=True 
        )
    st.code(st.session_state['result'], language="text")

# --- ПОДВАЛ ---
st.divider()
st.caption("📢 Полезные ресурсы автора:")
col_a, col_b = st.columns(2)
with col_a:
    st.markdown('<a href="https://t.me/All_Win_Bel" target="_blank" class="custom-link crypto">💎 Канал по крипте</a>', unsafe_allow_html=True)
with col_b:
    st.markdown('<a href="https://t.me/crypto_resurs" target="_blank" class="custom-link resources">🧰 Канал с полезностями</a>', unsafe_allow_html=True)
