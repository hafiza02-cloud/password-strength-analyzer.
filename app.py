
import streamlit as st

from password_analyzer import analyze_password
from password_generator import generate_password
from report_generator import create_security_report
from breach_checker import check_password_breach

st.set_page_config(
    page_title="CyberShield | Password Security",
    page_icon="🔐",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top right, #241044, #090615 65%);
    color: #F4EDFF;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #190B30, #0B0718);
    border-right: 1px solid #7639B8;
}
h1, h2, h3 {
    color: #D9B2FF !important;
}
div[data-testid="stMetric"] {
    background: #17102B;
    border: 1px solid #8D48D9;
    padding: 14px;
    border-radius: 12px;
}
.stButton > button {
    background: linear-gradient(90deg, #7928CA, #B84DFF);
    color: white;
    border: 1px solid #D5A0FF;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


def show_analysis(password):
    result = analyze_password(password)

    left, right = st.columns(2)

    with left:
        st.metric("Security Score", f"{result['score']}/100")
        st.progress(result["score"] / 100)
        st.subheader(result["strength"])
        st.write(f"Risk level: **{result['risk']}**")

    with right:
        st.subheader("Security Checklist")
        for check, passed in result["checks"].items():
            st.write(f"{'✅' if passed else '❌'} {check}")

    st.subheader("💡 Recommendations")
    for tip in result["recommendations"]:
        st.write(f"• {tip}")

    return result


st.sidebar.markdown("# 🛡️ CyberShield")
st.sidebar.caption("PASSWORD SECURITY SUITE")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Dashboard",
        "Password Analysis",
        "Password Generator",
        "Strength Comparison",
        "Security Insights",
        "Breach Check",
        "About"
    ]
)

st.title("🔐 Advanced Password Security Suite")
st.caption("ANALYZE  •  GENERATE  •  COMPARE  •  PROTECT")
st.divider()


if page == "Dashboard":
    st.subheader("Welcome to CyberShield")
    st.write(
        "A password security toolkit for learning about password "
        "strength, predictable patterns, and safer digital habits."
    )

    a, b, c = st.columns(3)

    with a:
        st.markdown("### 🔍 Analyze")
        st.write("Inspect password strength and weaknesses.")

    with b:
        st.markdown("### 🎲 Generate")
        st.write("Create random passwords using Python secrets.")

    with c:
        st.markdown("### ⚖️ Compare")
        st.write("Compare the scores of two test passwords.")

    st.info("Select a feature from the sidebar to begin.")

    st.subheader("🔒 Quick Security Tips")
    st.write("• Use a unique password for every account.")
    st.write("• Prefer long, unpredictable passwords.")
    st.write("• Use a reputable password manager.")
    st.write("• Enable multifactor authentication.")


elif page == "Password Analysis":
    st.subheader("🔍 Password Analysis")
    st.warning("Use fictional test passwords only. Never enter a real account password.")

    visible = st.checkbox("Show password while typing")
    password = st.text_input(
        "Enter a fictional test password",
        type="default" if visible else "password"
    )

    if password:
        result = show_analysis(password)

        st.download_button(
            "📄 Download Security Report",
            data=create_security_report(result),
            file_name="password_security_report.csv",
            mime="text/csv"
        )


elif page == "Password Generator":
    st.subheader("🎲 Secure Password Generator")
    length = st.slider("Password length", 16, 24, 20)

    upper = st.checkbox("Uppercase letters", value=True)
    lower = st.checkbox("Lowercase letters", value=True)
    digits = st.checkbox("Numbers", value=True)
    symbols = st.checkbox("Symbols", value=True)

    if st.button("✨ Generate Password"):
        try:
            st.session_state["generated_password"] = generate_password(
                length=length,
                use_upper=upper,
                use_lower=lower,
                use_digits=digits,
                use_symbols=symbols
            )
        except ValueError as error:
            st.error(str(error))

    generated = st.session_state.get("generated_password")

    if generated:
        st.success("Password generated!")
        st.code(generated)
        st.caption("Use the code block's copy icon to copy it.")
        st.warning("Do not use passwords shown during public demonstrations for real accounts.")


elif page == "Strength Comparison":
    st.subheader("⚖️ Password Strength Comparison")
    st.warning("Use fictional passwords only.")

    first = st.text_input("First test password", type="password")
    second = st.text_input("Second test password", type="password")

    if st.button("Compare Passwords"):
        if not first or not second:
            st.error("Enter both test passwords.")
        else:
            one = analyze_password(first)
            two = analyze_password(second)

            left, right = st.columns(2)

            with left:
                st.markdown("### Password A")
                st.metric("Score", f"{one['score']}/100")
                st.write(f"Strength: **{one['strength']}**")
                st.write(f"Risk: **{one['risk']}**")
                for tip in one["recommendations"]:
                    st.write(f"• {tip}")

            with right:
                st.markdown("### Password B")
                st.metric("Score", f"{two['score']}/100")
                st.write(f"Strength: **{two['strength']}**")
                st.write(f"Risk: **{two['risk']}**")
                for tip in two["recommendations"]:
                    st.write(f"• {tip}")

            if one["score"] > two["score"]:
                st.info("Password A scores higher under these checks.")
            elif two["score"] > one["score"]:
                st.info("Password B scores higher under these checks.")
            else:
                st.info("Both passwords have the same score.")


elif page == "Security Insights":
    st.subheader("🛡️ Security Insights")

    tips = [
        "Use a unique password for every account.",
        "Prefer long, unpredictable passwords or passphrases.",
        "Use a reputable password manager.",
        "Enable multifactor authentication where possible.",
        "Avoid names, birthdays, and predictable sequences.",
        "Never share passwords or store them in plain text.",
        "Change a password if you suspect it has been exposed.",
        "Keep your device and applications updated."
    ]

    for number, tip in enumerate(tips, start=1):
        st.markdown(f"**{number}.** {tip}")

    st.info("A strength score is an estimate, not a guarantee of security.")


elif page == "Breach Check":
    st.subheader("🕵️ Privacy-Preserving Breach Check")
    st.warning(
        "Use fictional test passwords only. This feature contacts "
        "Have I Been Pwned to check known password exposures."
    )

    password = st.text_input("Fictional password to check", type="password")

    if st.button("Check Known Breaches"):
        if not password:
            st.error("Enter a fictional test password.")
        else:
            try:
                with st.spinner("Checking breach data..."):
                    result = check_password_breach(password)

                if result["breached"]:
                    st.error("This password appears in known breach data.")
                    st.metric("Recorded exposures", f"{result['count']:,}")
                else:
                    st.success("No match was found in the returned breach data.")
                    st.write("This does not guarantee the password is safe.")

            except Exception:
                st.error(
                    "Could not reach the breach-checking service. "
                    "Check your connection and try again."
                )


elif page == "About":
    st.subheader("About CyberShield")
    st.write(
        "CyberShield is an educational mini cybersecurity project "
        "built with Python and Streamlit."
    )
    st.write("**Features:** Analysis, generation, comparison, breach checks and reports.")
    st.write("**Privacy:** No password history or account system.")
    st.write("**Technologies:** Python, Streamlit, Requests and GitHub.")


st.divider()
st.caption("Cybersecurity Mini Project | Python • Streamlit • GitHub")
