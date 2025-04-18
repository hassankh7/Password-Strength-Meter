import streamlit as st
import re
import random
import string

# Title
st.title("🔒 Smart Password Strength Checker")
st.markdown("Check how strong your password is or generate a new secure one instantly!")

# Password Strength Logic
def evaluate_strength(pwd: str) -> str:
    strength = 0
    if len(pwd) >= 8:
        strength += 1
    if re.search(r"[a-z]", pwd) and re.search(r"[A-Z]", pwd):
        strength += 1
    if re.search(r"\d", pwd):
        strength += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd):
        strength += 1

    if strength == 4:
        return "✅ Strong"
    elif strength == 3:
        return "🟡 Moderate"
    elif strength == 2:
        return "🟠 Weak"
    else:
        return "🔴 Very Weak"

# Session state for previous passwords
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar Choice
st.sidebar.header("🛠 Choose Action")
option = st.sidebar.selectbox("What do you want to do?", ["Check Password", "Generate Password"])

# Password Checker
if option == "Check Password":
    user_pwd = st.text_input("🔑 Enter Your Password", type="password", placeholder="e.g. MyS3cureP@ss")

    if user_pwd:
        if user_pwd in st.session_state.history:
            st.error("🚫 You already used this one. Try something else!")
        else:
            st.session_state.history.append(user_pwd)
            if len(st.session_state.history) > 5:
                st.session_state.history.pop(0)

            result = evaluate_strength(user_pwd)
            st.subheader(f"Strength: {result}")

            # Feedback
            if "Very Weak" in result:
                st.error("❌ Too weak! Use a mix of letters, numbers, and symbols.")
            elif "Weak" in result:
                st.warning("⚠️ Needs improvement. Try adding more variety.")
            elif "Moderate" in result:
                st.info("🆗 Not bad, but could be stronger.")
            elif "Strong" in result:
                st.success("💪 Perfect! Keep it secure.")

        # Show History
        with st.expander("📂 Last 5 Checked Passwords"):
            for i, item in enumerate(st.session_state.history[::-1], start=1):
                st.markdown(f"{i}. `{item}`")

# Password Generator
else:
    st.subheader("🔧 Generate a Strong Password")

    length = st.slider("Password Length", 8, 20, 12)
    use_digits = st.checkbox("Include Numbers", value=True)
    use_specials = st.checkbox("Include Special Characters", value=True)

    def create_password(length, use_digits, use_specials):
        characters = string.ascii_letters
        if use_digits:
            characters += string.digits
        if use_specials:
            characters += "!@#$%^&*()_+-=[]{}|;:,.<>?/"
        return ''.join(random.choice(characters) for _ in range(length))

    if st.button("🔁 Generate Now"):
        new_password = create_password(length, use_digits, use_specials)
        st.success(f"🔐 Your New Password: `{new_password}`")
        st.info("Copy and save this password somewhere safe.")