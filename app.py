import streamlit as st

# --- НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="Email Generator", page_icon="📧", layout="centered")

# --- СТИЛИ CSS (КРАСОТА) ---
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
    }
    .custom-link {
        display: inline-block;
        text-decoration: none;
        color: white !important;
        font-weight: bold;
        width: 100%;
        padding: 12px;
        text-align: center;
        border-radius: 8px;
        margin-bottom: 10px;
        transition: 0.3s;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    .custom-link:hover {
        opacity: 0.9;
        transform: translateY(-2px);
    }
    .crypto { background: linear-gradient(135deg, #ff6600 0%, #ff8533 100%); }
    .resources { background: linear-gradient(135deg, #0088cc 0%, #33aadd 100%); }
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
st.write("Сделайте из одной почты тысячи уникальных вариантов (Gmail воспринимает их как одну почту, а сайты — как разные).")

email_input = st.text_input("Введите ваш email (например: name@gmail.com)")

if email_input:
    if is_valid_email(email_input):
        local, domain = email_input.split('@')
        num_gaps = len(local) - 1
        total_variants = 2 ** num_gaps if num_gaps > 0 else 1
        
        st.success(f"✅ Email корректный! Доступно вариантов: **{total_variants:,}**")
        
        # Выбор режима
        mode = st.radio("Режим:", ["Сгенерировать количество", "Сгенерировать ВСЕ"], horizontal=True)
        
        limit = None
        if mode == "Сгенерировать количество":
            limit = st.number_input("Сколько штук?", min_value=1, max_value=total_variants, value=min(100, total_variants))

        # Кнопка запуска
        if st.button("🚀 Запустить генерацию", type="primary"):
            with st.spinner("Генерируем..."):
                results = generate_emails(local, domain, limit if mode == "Сгенерировать количество" else None)
                result_text = "\n".join(results)
                
                # Показываем результат
                st.subheader(f"Результат ({len(results)} шт.)")
                st.code(result_text, language="text") # Кнопка копирования встроенная
                
    else:
        st.error("❌ Ошибка формата email")

# --- ПОДВАЛ (АВТОР) ---
st.divider()
st.write("📢 **Полезные ресурсы автора:**")

col1, col2 = st.columns(2)
with col1:
    st.markdown('<a href="https://t.me/All_Win_Bel" target="_blank" class="custom-link crypto">💎 Канал по крипте</a>', unsafe_allow_html=True)
with col2:
    st.markdown('<a href="https://t.me/crypto_resurs" target="_blank" class="custom-link resources">🧰 Канал с полезностями</a>', unsafe_allow_html=True)
