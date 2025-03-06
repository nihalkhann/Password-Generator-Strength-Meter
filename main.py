import streamlit as st
import re
import string
import random
import pyperclip


st.set_page_config(page_title="Nihal : Password Generator & Strength Meter", page_icon="🔑", layout="centered")

st.markdown("""
<style>
    .card {
        background: #24244e;
        border-radius: 15px;
        padding: 2.5rem;
        margin-bottom: 2rem;
    }

    .very-weak { 
        color: #ff6b6b;
        font-weight: 700;
    }
    .weak { 
        color: #ffaa70; 
        font-weight: 700;
    }
    .medium { 
        color: #ffe97a; 
        font-weight: 700;
    }
    .strong { 
        color: #66ffcc; 
        font-weight: 700;
    }
    .very-strong { 
        color: #00e6b8; 
        font-weight: 700;
    }

    .stButton > button {
        background: linear-gradient(10deg, #5e5ce6 0%, #9b59b6 100%);
        border: none;
        border-radius: 10px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        letter-spacing: 1px;
    }

    .password-display {
        font-size: 1.4rem;
        background: #2d2d5e;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1.5rem 0;
        text-align: center;
        letter-spacing: 3px;
        
    }

    h1, h2, h3 {
        color: #e0e0e0;
        font-family: 'Poppins', sans-serif;
    }
    h1 {
        font-size: 2.5rem !important;
        margin-bottom: 2.5rem !important;
        text-align: center;
        background: linear-gradient(120deg, #5e5ce6 0%, #9b59b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .footer {
        text-align: center;
        font-size: 1rem;
        color: #b0b0cc;
        margin-top: 2rem;
        
    }
    

    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: #2d2d5e;
        padding: 0.75rem;
        border-radius: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3.8rem;
        border-radius: 12px;
        padding: 0 2rem;
        background: #24244e;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        font-weight: 600;
        color: #e0e0e0;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #5e5ce6 0%, #9b59b6 100%) !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)


def generate_password(length, use_digits, use_special):
    characters = string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


def evaluate_password_strength(password):
    has_lowercase = bool(re.search(r'[a-z]', password))
    has_uppercase = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    
    score = 0
    suggestions = []
    
    if len(password) >= 12:
        score += 1
    elif len(password) >= 8:
        score += 0.5
    else:
        suggestions.append("Use a longer password (at least 8 characters)")
    
    if not has_lowercase:
        suggestions.append("Include lowercase letters")
    else:
        score += 0.5
        
    if not has_uppercase:
        suggestions.append("Include uppercase letters")
    else:
        score += 0.5
        
    if not has_digit:
        suggestions.append("Include numbers")
    else:
        score += 0.5
        
    if not has_special:
        suggestions.append("Include special characters")
    else:
        score += 0.5
    
    return {
        'score': min(4, int(score)),
        'suggestions': suggestions
    }


def display_strength(password):
    if not password:
        return
        
    strength = evaluate_password_strength(password)
    score = strength['score']
    
    classes = {0: 'very-weak', 1: 'weak', 2: 'medium', 3: 'strong', 4: 'very-strong'}
    descriptions = {0: 'Very Weak', 1: 'Weak', 2: 'Medium', 3: 'Strong', 4: 'Very Strong'}
    
    st.markdown(f"""
    <div class="card">
        <h3>Password Strength</h3>
        <p>Your password is: <span class="{classes[score]}">{descriptions[score]}</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.progress(score/4)
    
    if strength['suggestions']:
        with st.expander("💡 How to improve your password", expanded=True):
            for suggestion in strength['suggestions']:
                st.markdown(f"• {suggestion}")


st.markdown("<h1>Password Generator & Strength Meter</h1>", unsafe_allow_html=True)


tabs = st.tabs(["✨ Generate Password", "🔍 Check Password Strength"])

with tabs[0]:
    
    col1, col2 = st.columns([7, 3])
    
    with col1:
        length = st.slider("Password Length", 6, 30, 10)
    
    with col2:
        use_digits = st.checkbox("Include Digits (0-9)", value=True)
        use_special = st.checkbox("Include Special (!@#$)", value=True)
    
    
    if st.button("Generate Secure Password", use_container_width=True):
        password = generate_password(length, use_digits, use_special)
        st.session_state['generated_password'] = password
        
        st.markdown(f"""
        <div class="password-display">
            {password}
        </div>
        """, unsafe_allow_html=True)
        
        display_strength(password)

    if 'generated_password' in st.session_state:
        if st.button("Copy to Clipboard", use_container_width=True):
            pyperclip.copy(st.session_state['generated_password'])
            st.success("Password copied to clipboard!", icon="✅")
    

with tabs[1]:
    
    manual_password = st.text_input("Enter a password to check its strength", type="password")
    
    if manual_password:
        display_strength(manual_password)
    else:
        st.info("Enter a password above to see its strength analysis")
    



st.markdown("""
<div class="footer">
    Made with ❤️ by Nihal Khan Ghauri
</div>
""", unsafe_allow_html=True)






