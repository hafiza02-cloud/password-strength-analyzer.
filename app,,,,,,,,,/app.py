
import streamlit as st
from password_analyzer import analyze_password

st.set_page_config(
    page_title="Advanced Password Security Suite",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
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
p, label, [data-testid="stMarkdownContainer"] {
    color: #F4EDFF;
}
div[data-testid="stMetric"] {
    background: #17102B;
    border: 1px solid #8D48D9;
    padding: 16px;
    border-radius: 14px;
}
.stButton > button {
    background: linear-gradient(90deg, #7928CA, #B84DFF);
    color: white;
    border: 1px solid #D5A0FF;
    border-radius: 10px;
    font-weight: 600;
}
.stProgress > div > div > div {
    background-color: #B84DFF;
}
hr {
    border-color: #553276;
}
</style>
""", unsafe_allow_html=True)

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
        "Explore password security tools designed to help you "
        "understand risks and make safer password choices."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🔍 Analyze")
        st.write("Inspect password strength and security weaknesses.")

    with col2:
        st.markdown("### 🎲 Generate")
        st.write("Create strong, random passwords.")

    with col3:
        st.markdown("### ⚖️ Compare")
        st.write("Compare the security characteristics of two passwords.")

    st.info("Choose a tool from the sidebar to begin.")

elif page == "Password Analysis":
    st.subheader("🔍 Password Analysis")
    st.write("Analyze a fictional password as you type.")

    show_password = st.checkbox("Show password while typing")
    password = st.text_input(
        "Enter a test password",
        type="default" if show_password else "password",
        key="analysis_password"
    )

    if password:
        result = analyze_password(password)

        left, right = st.columns([1, 1])

        with left:
            st.metric("Strength Score", f"{result['score']}/100")
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

    else:
        st.info("Enter a fictional test password to see the analysis.")

elif page == "Password Generator":
    st.subheader("🎲 Password Generator")
    st.info("The generator will support customizable lengths from 16 to 24 characters.")

elif page == "Strength Comparison":
    st.subheader("⚖️ Strength Comparison")
    st.info("Compare two fictional passwords side by side.")

elif page == "Security Insights":
    st.subheader("🛡️ Security Insights")

    tips = [
        "Use a unique password for every account.",
        "Prefer long, unpredictable passwords or passphrases.",
        "Use a reputable password manager.",
        "Enable multifactor authentication where available.",
        "Avoid personal details and predictable keyboard patterns.",
        "Never share passwords or store them in plain text."
    ]

    for number, tip in enumerate(tips, start=1):
        st.markdown(f"**{number}.** {tip}")

elif page == "Breach Check":
    st.subheader("🕵️ Privacy-Preserving Breach Check")
    st.warning(
        "Breach checking requires a separate implementation. "
        "Never submit a real password to an untrusted service."
    )
    st.write(
        "We will use a privacy-preserving method that does not send "
        "the raw password to the breach-checking service."
    )

elif page == "About":
    st.subheader("About CyberShield")
    st.write(
        "CyberShield is a Python and Streamlit mini cybersecurity "
        "project focused on password strength, risk awareness, "
        "password generation and safer digital habits."
    )
    st.write("Design: Dark purple neon cybersecurity theme.")
    st.write("Password history: Not saved.")
    st.write("Account system: Not required.")

st.divider()
st.caption("Cybersecurity Mini Project | Python • Streamlit • GitHub")
