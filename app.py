import streamlit as st

# --- НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="Email Generator", page_icon="📧", layout="centered")

# --- СТИЛИ CSS ---
st.markdown("""
<style>
    /* 1. Скрываем кнопку-скрепку (Anchor link) рядом с заголовками */
    [data-testid="stHeaderActionElements"] {
        display: none !important;
    }

    /* 2. Стиль для кнопок внизу (Каналы) - делаем чуть спокойнее */
    .custom-link {
        display: inline-block;
        text-decoration: none;
        color: white !important;
        font-weight: bold;
        width: 100%;
        padding: 10px; /* Чуть меньше отступы */
        text-align: center;
        border-radius: 8px;
        margin-bottom: 8px;
        transition: 0.3s;
        font-size: 15px;
    }
    .custom-link:hover {
        opacity: 0.85; 
        transform: translateY(-1px);
    }
    /* Цвета каналов */
    .crypto { background-color: #e67e22; } /* Спокойный оранжевый */
    .resources { background-color: #2980b9; } /* Спокойный синий */
    
    /* Убираем лишние отступы сверху */
    .block-container {
        padding-top: 2rem;
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

email_input = st.text_input("Введите ваш email (например: name@gmail.com)")

if email_input:
    if is_valid_email(email_input):
        local, domain = email_input.split('@')
        num_gaps = len(local) - 1
        total_variants = 2 ** num_gaps if num_gaps > 0 else 1
        
        st.success(f"✅ Email корректный! Вариантов: **{total_variants:,}**")
        
        # Настройки в одну строку для компактности
        c1, c2 = st.columns([1.5, 1])
        with c1:
            mode = st.radio("Режим:", ["Количество", "Все сразу"], horizontal=True, label_visibility="collapsed")
        
        limit = None
        if mode == "Количество":
            with c2:
                limit = st.number_input("Сколько штук?", min_value=1, max_value=total_variants, value=min(100, total_variants), label_visibility="collapsed")

        st.write("") # Небольшой отступ
        
        # Кнопка запуска (Primary - единственная яркая кнопка действия)
        if st.button("🚀 Сгенерировать", type="primary", use_container_width=True):
            with st.spinner("Работаем..."):
                results = generate_emails(local, domain, limit if mode == "Количество" else None)
                result_text = "\n".join(results)
                
                # Сохраняем в сессию
                st.session_state['result'] = result_text
                st.session_state['count'] = len(results)
                
    else:
        st.error("❌ Ошибка формата email")

# --- ВЫВОД РЕЗУЛЬТАТА ---
if 'result' in st.session_state:
    st.divider()
    
    # СОЗДАЕМ КОЛОНКИ: Заголовок слева, Кнопка скачивания справа
    col_head, col_btn = st.columns([2, 1])
    
    with col_head:
        # Просто текст, без ссылки-скрепки
        st.markdown(f"### Результат ({st.session_state['count']} шт.)")
        
    with col_btn:
        # Кнопка скачивания (обычная серая, не яркая)
        st.download_button(
            label="💾 Скачать .txt",
            data=st.session_state['result'],
            file_name="emails.txt",
            mime="text/plain",
            use_container_width=True 
        )

    # Поле с текстом (Кнопка копирования ВСТРОЕНА в него справа сверху)
    st.code(st.session_state['result'], language="text")

# --- ПОДВАЛ ---
st.divider()
st.caption("📢 Полезные ресурсы автора:")

col_a, col_b = st.columns(2)
with col_a:
    st.markdown('<a href="https://t.me/All_Win_Bel" target="_blank" class="custom-link crypto">💎 Канал по крипте</a>', unsafe_allow_html=True)
with col_b:
    st.markdown('<a href="https://t.me/crypto_resurs" target="_blank" class="custom-link resources">🧰 Канал с полезностями</a>', unsafe_allow_html=True)
