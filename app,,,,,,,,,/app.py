
import streamlit as st
import pandas as pd
import secrets
import string

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
    background: radial-gradient(circle at top right,
    #241044, #090615 65%);
    color: #F4EDFF;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#190B30,#0B0718);
    border-right: 1px solid #7639B8;
}
h1,h2,h3 {
    color: #D9B2FF !important;
}
div[data-testid="stMetric"] {
    background: #17102B;
    border: 1px solid #8D48D9;
    padding: 14px;
    border-radius: 12px;
}
.stButton > button {
    background: linear-gradient(90deg,#7928CA,#B84DFF);
    color: white;
    border: 1px solid #D5A0FF;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


def show_analysis(password, heading="Analysis"):
    result = analyze_password(password)

    st.subheader(heading)
    left, right = st.columns(2)

    with left:
        st.metric("Security score", f"{result['score']}/100")
        st.progress(result["score"] / 100)
        st.write(f"**Strength:** {result['strength']}")
        st.write(f"**Risk:** {result['risk']}")

    with right:
        st.write("**Security checklist**")
        for check, passed in result["checks"].items():
            st.write(f"{'✅' if passed else '❌'} {check}")

    st.write("**Recommendations**")
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
        "Explore password security tools designed to help you "
        "understand risks and improve your password habits."
    )

    a, b, c = st.columns(3)
    with a:
        st.markdown("### 🔍 Analyze")
        st.write("Inspect password strength and weaknesses.")
    with b:
        st.markdown("### 🎲 Generate")
        st.write("Create unpredictable passwords.")
    with c:
        st.markdown("### ⚖️ Compare")
        st.write("Compare two password security scores.")

    st.info("Choose a tool from the sidebar to get started.")
    st.subheader("🔒 Security principles")
    st.write(
        "Use unique passwords, prefer long passphrases, "
        "enable multifactor authentication, and use a "
        "reputable password manager."
    )


elif page == "Password Analysis":
    st.subheader("🔍 Password Analysis")
    st.warning(
        "Use a fictional test password only. Never enter a password "
        "that protects a real account."
    )

    show = st.checkbox("Show password while typing")
    password = st.text_input(
        "Enter a fictional test password",
        type="default" if show else "password"
    )

    if password:
        result = show_analysis(password)
        st.download_button(
            "📄 Download Security Report (CSV)",
            data=create_security_report(result),
            file_name="password_security_report.csv",
            mime="text/csv"
        )


elif page == "Password Generator":
    st.subheader("🎲 Secure Password Generator")
    st.write("Generate a random password between 16 and 24 characters.")

    length = st.slider("Password length", 16, 24, 20)
    upper = st.checkbox("Uppercase letters", value=True)
    lower = st.checkbox("Lowercase letters", value=True)
    digits = st.checkbox("Numbers", value=True)
    symbols = st.checkbox("Symbols", value=True)

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
            "Copy it now if needed. Avoid sharing it or using "
            "a password displayed during a public demonstration."
        )
        st.code(
            f"Generated password: {generated}",
            language=None
        )
        st.write(
            "Use the copy icon on the code block to copy the password."
        )


elif page == "Strength Comparison":
    st.subheader("⚖️ Compare Passwords")
    st.warning("Use fictional examples only.")

    first = st.text_input("First test password", type="password")
    second = st.text_input("Second test password", type="password")

    if st.button("Compare Passwords"):
        if not first or not second:
            st.error("Enter both test passwords.")
        else:
            result1 = analyze_password(first)
            result2 = analyze_password(second)

            left, right = st.columns(2)
            with left:
                st.markdown("### Password A")
                st.metric("Score", f"{result1['score']}/100")
                st.write(f"**Strength:** {result1['strength']}")
                st.write(f"**Risk:** {result1['risk']}")
                for tip in result1["recommendations"]:
                    st.write(f"• {tip}")

            with right:
                st.markdown("### Password B")
                st.metric("Score", f"{result2['score']}/100")
                st.write(f"**Strength:** {result2['strength']}")
                st.write(f"**Risk:** {result2['risk']}")
                for tip in result2["recommendations"]:
                    st.write(f"• {tip}")

            if result1["score"] > result2["score"]:
                st.info("Password A scores higher in these checks.")
            elif result2["score"] > result1["score"]:
                st.info("Password B scores higher in these checks.")
            else:
                st.info("Both passwords have the same score.")


elif page == "Security Insights":
    st.subheader("🛡️ Security Insights")

    tips = [
        "Use a different password for every account.",
        "Prefer long, unpredictable passwords or passphrases.",
        "Use a reputable password manager.",
        "Enable multifactor authentication wherever possible.",
        "Avoid names, birthdays, and predictable sequences.",
        "Never share passwords or save them in plain text.",
        "Change a password promptly if you suspect it was exposed.",
        "Keep your operating system and applications updated."
    ]

    for number, tip in enumerate(tips, start=1):
        st.markdown(f"**{number}.** {tip}")

    st.info(
        "A strength score is an educational estimate, not a "
        "guarantee that a password cannot be cracked."
    )


elif page == "Breach Check":
    st.subheader("🕵️ Privacy-Preserving Breach Check")
    st.warning(
        "Use fictional examples only. This feature contacts "
        "Have I Been Pwned to check known password exposures."
    )

    test_password = st.text_input(
        "Fictional password to check",
        type="password"
    )

    if st.button("Check Known Breaches"):
        if not test_password:
            st.error("Enter a fictional test password.")
        else:
            try:
                with st.spinner("Checking breach data..."):
                    result = check_password_breach(test_password)

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
                        "This does not guarantee the password is safe."
                    )
            except Exception:
                st.error(
                    "The breach service could not be reached. "
                    "Check your connection and try again."
                )


elif page == "About":
    st.subheader("About CyberShield")
    st.write(
        "CyberShield is an educational cybersecurity project "
        "built with Python and Streamlit."
    )
    st.write("**Features:** Password analysis, generation, comparison,")
    st.write("breach checking, security guidance and downloadable reports.")
    st.write("**Privacy:** No password history or account system.")
    st.write("**Technologies:** Python, Streamlit, Requests and GitHub.")


st.divider()
st.caption(
    "Cybersecurity Mini Project | Python • Streamlit • GitHub"
)
