import streamlit as st

# --- НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="Email Generator", page_icon="📧", layout="centered")

# --- ИНИЦИАЛИЗАЦИЯ (State) ---
if 'email_input_key' not in st.session_state:
    st.session_state.email_input_key = ""

# --- ФУНКЦИИ (CALLBACKS) ---
def paste_example():
    # Эта функция срабатывает при нажатии кнопки примера
    st.session_state.email_input_key = "name@gmail.com"
    # Показываем красивое уведомление
    st.toast("✅ Пример name@gmail.com успешно вставлен!", icon='🪄')

def show_download_toast():
    # Уведомление при скачивании
    st.toast("💾 Файл сохранен в загрузки!", icon='📂')

# --- СТИЛИ CSS (Оформление) ---
st.markdown("""
<style>
    /* 1. Скрываем скрепку (Anchor link) */
    [data-testid="stHeaderActionElements"] { display: none !important; }

    /* 2. Стиль для кнопок каналов (Автор) */
    .custom-link {
        display: inline-block;
        text-decoration: none;
        color: white !important;
        font-weight: bold;
        width: 100%;
        padding: 12px;
        text-align: center;
        border-radius: 10px;
        margin-bottom: 10px;
        transition: 0.3s;
        font-size: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .custom-link:hover { 
        opacity: 0.9; 
        transform: translateY(-2px); 
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }
    .crypto { background: linear-gradient(135deg, #ff6600 0%, #ff8533 100%); }
    .resources { background: linear-gradient(135deg, #0088cc 0%, #33aadd 100%); }
    
    /* Убираем лишние отступы сверху */
    .block-container { padding-top: 2rem; }
    
    /* Делаем поле ввода чуть красивее */
    .stTextInput input {
        border-radius: 8px;
    }
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

# --- БЛОК ВВОДА С КНОПКОЙ ---
# Создаем две колонки: широкую для ввода и узкую для кнопки
col1, col2 = st.columns([3, 1.2])

with col1:
    # Поле ввода связано с переменной в session_state
    email_input = st.text_input(
        "Введите ваш email", 
        key="email_input_key",
        placeholder="vash_email@gmail.com",
        label_visibility="collapsed" # Скрываем надпись, т.к. placeholder понятен
    )

with col2:
    # Кнопка, которая вызывает функцию paste_example
    st.button("🪄 Вставить пример", on_click=paste_example, help="Нажмите, чтобы автоматически вставить name@gmail.com", use_container_width=True)

# --- ОБРАБОТКА ---
if email_input:
    if is_valid_email(email_input):
        local, domain = email_input.split('@')
        num_gaps = len(local) - 1
        total_variants = 2 ** num_gaps if num_gaps > 0 else 1
        
        # Зеленая плашка успеха
        st.success(f"✅ Email корректный! Вариантов: **{total_variants:,}**")
        
        # Настройки генерации
        c1, c2 = st.columns([1.5, 1])
        with c1:
            mode = st.radio("Режим:", ["Количество", "Все сразу"], horizontal=True, label_visibility="collapsed")
        
        limit = None
        if mode == "Количество":
            with c2:
                limit = st.number_input("Сколько штук?", min_value=1, max_value=total_variants, value=min(100, total_variants), label_visibility="collapsed")

        st.write("") # Отступ
        
        # ГЛАВНАЯ КНОПКА
        if st.button("🚀 Сгенерировать", type="primary", use_container_width=True):
            with st.spinner("Генерируем..."):
                results = generate_emails(local, domain, limit if mode == "Количество" else None)
                result_text = "\n".join(results)
                
                # Сохраняем результат
                st.session_state['result'] = result_text
                st.session_state['count'] = len(results)
                
                # Показываем уведомление о завершении
                st.toast(f"Готово! Сгенерировано {len(results)} адресов", icon='🎉')
                
    else:
        st.error("❌ Некорректный формат. Нужен email вида name@gmail.com")

# --- ВЫВОД РЕЗУЛЬТАТА ---
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
            use_container_width=True,
            on_click=show_download_toast # Вызываем уведомление при скачивании
        )

    # st.code автоматически добавляет кнопку копирования справа сверху!
    # Она сама показывает "Copied!", когда на нее нажимаешь.
    st.code(st.session_state['result'], language="text")
    st.caption("ℹ️ Чтобы скопировать список, нажмите маленькую иконку 📄 в правом верхнем углу блока с результатами.")

# --- ПОДВАЛ (АВТОР) ---
st.divider()
st.caption("📢 Полезные ресурсы автора:")
col_a, col_b = st.columns(2)
with col_a:
    st.markdown('<a href="https://t.me/All_Win_Bel" target="_blank" class="custom-link crypto">💎 Канал по крипте</a>', unsafe_allow_html=True)
with col_b:
    st.markdown('<a href="https://t.me/crypto_resurs" target="_blank" class="custom-link resources">🧰 Канал с полезностями</a>', unsafe_allow_html=True)
