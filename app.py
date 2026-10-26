
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

# High-contrast cyber theme
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #10091F, #211038);
    color: #FFFFFF;
}

.stApp p,
.stApp li,
.stApp label,
.stApp span,
.stApp [data-testid="stMarkdownContainer"] {
    color: #F8F5FF;
}

h1, h2, h3, h4 {
    color: #E5C6FF !important;
}

[data-testid="stSidebar"] {
    background: #160C27;
    border-right: 1px solid #9D5CE5;
}

[data-testid="stMetric"] {
    background: #241638;
    border: 1px solid #C084FC;
    border-radius: 12px;
    padding: 14px;
}

[data-testid="stMetricLabel"] {
    color: #E9D5FF !important;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
}

.stButton > button,
.stDownloadButton > button {
    background: #7E22CE;
    color: #FFFFFF !important;
    border: 1px solid #D8B4FE;
    border-radius: 10px;
    font-weight: 600;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #9333EA;
    color: #FFFFFF !important;
    border: 1px solid #FFFFFF;
}

input, textarea {
    color: #FFFFFF !important;
    background-color: #26183B !important;
}

div[data-baseweb="select"] {
    color: #FFFFFF;
}

.stProgress > div > div > div {
    background-color: #C084FC;
}

hr {
    border-color: #8050A8;
}

</style>
""", unsafe_allow_html=True)


def show_analysis(password):
    result = analyze_password(password)

    left, right = st.columns(2)

    with left:
        st.metric("Security Score", f"{result['score']}/100")
        st.progress(result["score"] / 100)
        st.subheader(f"Strength: {result['strength']}")
        st.write(f"**Risk level:** {result['risk']}")

    with right:
        st.subheader("Security Checklist")
        for check, passed in result["checks"].items():
            st.write(f"{'✅' if passed else '❌'} {check}")

    st.subheader("💡 Recommendations")
    for tip in result["recommendations"]:
        st.write(f"• {tip}")

    return result


# Sidebar navigation
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


# 1. Dashboard
if page == "Dashboard":
    st.subheader("Welcome to CyberShield")

    st.write(
        "A password security toolkit for understanding password "
        "strength, detecting predictable patterns, and improving "
        "digital safety."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🔍 Analyze")
        st.write("Inspect password strength and security weaknesses.")

    with col2:
        st.markdown("### 🎲 Generate")
        st.write("Create random passwords using Python's secrets module.")

    with col3:
        st.markdown("### ⚖️ Compare")
        st.write("Compare two test passwords side by side.")

    st.info("Choose a feature from the sidebar to begin.")

    st.subheader("🔒 Essential Security Tips")
    st.write("• Use a unique password for every account.")
    st.write("• Prefer long, unpredictable passwords or passphrases.")
    st.write("• Use a reputable password manager.")
    st.write("• Enable multifactor authentication.")
    st.write("• Never share passwords with other people.")


# 2. Password Analysis
elif page == "Password Analysis":
    st.subheader("🔍 Password Analysis")

    st.warning(
        "Use fictional test passwords only. Never enter a password "
        "that protects a real account."
    )

    visible = st.checkbox("Show password while typing")

    password = st.text_input(
        "Enter a fictional test password",
        type="default" if visible else "password"
    )

    if password:
        result = show_analysis(password)

        st.download_button(
            "📄 Download Security Report (CSV)",
            data=create_security_report(result),
            file_name="password_security_report.csv",
            mime="text/csv"
        )


# 3. Password Generator
elif page == "Password Generator":
    st.subheader("🎲 Secure Password Generator")

    st.write("Choose a length between 16 and 24 characters.")

    length = st.slider("Password length", 16, 24, 20)

    upper = st.checkbox("Uppercase letters (A–Z)", value=True)
    lower = st.checkbox("Lowercase letters (a–z)", value=True)
    digits = st.checkbox("Numbers (0–9)", value=True)
    symbols = st.checkbox("Symbols (!@#$ etc.)", value=True)

    if st.button("✨ Generate Password"):
        try:
            generated = generate_password(
                length=length,
                use_upper=upper,
                use_lower=lower,
                use_digits=digits,
                use_symbols=symbols
            )
            st.session_state["generated_password"] = generated

        except ValueError as error:
            st.error(str(error))

    generated = st.session_state.get("generated_password")

    if generated:
        st.success("Password generated successfully.")
        st.code(generated)

        st.caption(
            "Use the code block's copy icon to copy the password."
        )

        st.warning(
            "Do not use a password displayed during a public "
            "demonstration for a real account."
        )


# 4. Strength Comparison
elif page == "Strength Comparison":
    st.subheader("⚖️ Password Strength Comparison")

    st.warning("Use fictional test passwords only.")

    first = st.text_input("First test password", type="password")
    second = st.text_input("Second test password", type="password")

    if st.button("Compare Passwords"):
        if not first or not second:
            st.error("Please enter both test passwords.")

        else:
            one = analyze_password(first)
            two = analyze_password(second)

            left, right = st.columns(2)

            with left:
                st.markdown("### Password A")
                st.metric("Score", f"{one['score']}/100")
                st.write(f"**Strength:** {one['strength']}")
                st.write(f"**Risk:** {one['risk']}")

                for tip in one["recommendations"]:
                    st.write(f"• {tip}")

            with right:
                st.markdown("### Password B")
                st.metric("Score", f"{two['score']}/100")
                st.write(f"**Strength:** {two['strength']}")
                st.write(f"**Risk:** {two['risk']}")

                for tip in two["recommendations"]:
                    st.write(f"• {tip}")

            if one["score"] > two["score"]:
                st.success("Password A scores higher under these checks.")

            elif two["score"] > one["score"]:
                st.success("Password B scores higher under these checks.")

            else:
                st.info("Both passwords have the same score.")


# 5. Security Insights
elif page == "Security Insights":
    st.subheader("🛡️ Security Insights")

    tips = [
        "Use a unique password for every account.",
        "Prefer long, unpredictable passwords or passphrases.",
        "Use a reputable password manager.",
        "Enable multifactor authentication whenever possible.",
        "Avoid names, birthdays, and predictable sequences.",
        "Never share passwords or store them in plain text.",
        "Change a password if you suspect it has been exposed.",
        "Keep your devices and applications updated."
    ]

    for number, tip in enumerate(tips, start=1):
        st.markdown(f"**{number}.** {tip}")

    st.info(
        "A password strength score is an educational estimate, "
        "not a guarantee of security."
    )


# 6. Breach Check
elif page == "Breach Check":
    st.subheader("🕵️ Privacy-Preserving Breach Check")

    st.warning(
        "Use fictional test passwords only. This feature contacts "
        "Have I Been Pwned to check known password exposures."
    )

    password = st.text_input(
        "Fictional password to check",
        type="password"
    )

    if st.button("Check Known Breaches"):
        if not password:
            st.error("Please enter a fictional test password.")

        else:
            try:
                with st.spinner("Checking breach data..."):
                    result = check_password_breach(password)

                if result["breached"]:
                    st.error(
                        "This password appears in known breach data."
                    )
                    st.metric(
                        "Recorded exposures",
                        f"{result['count']:,}"
                    )

                else:
                    st.success(
                        "No match was found in the returned breach data."
                    )
                    st.write(
                        "This does not guarantee that the password "
                        "is safe or has never been exposed."
                    )

            except Exception:
                st.error(
                    "The breach service could not be reached. "
                    "Check your connection and try again."
                )


# 7. About
elif page == "About":
    st.subheader("About CyberShield")

    st.write(
        "CyberShield is an educational mini cybersecurity project "
        "built with Python and Streamlit."
    )

    st.markdown("### Features")
    st.write("• Password strength analysis")
    st.write("• Secure random password generation")
    st.write("• Side-by-side password comparison")
    st.write("• Privacy-preserving breach checking")
    st.write("• Downloadable security reports")
    st.write("• Security recommendations")

    st.markdown("### Technologies")
    st.write("Python • Streamlit • Requests • GitHub")

    st.markdown("### Privacy")
    st.write(
        "The application does not intentionally save password "
        "history. Avoid entering real passwords into this demo."
    )


st.divider()
st.caption(
    "Cybersecurity Mini Project | Python • Streamlit • GitHub"
)
