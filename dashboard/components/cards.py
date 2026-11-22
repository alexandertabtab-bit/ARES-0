
import streamlit as st


def unit_card(code, title, description, status, active=False):
    color = "#22C58B" if active else "#8293A8"

    st.markdown(f"""
    <div class="ares-panel">
        <div style="color:#22D3EE;font-size:12px;
                    font-weight:800;letter-spacing:1.5px">
            {code}
        </div>
        <h3 style="margin:8px 0 4px">{title}</h3>
        <div class="ares-muted">{description}</div>
        <div style="margin-top:16px;color:{color};
                    font-size:12px;font-weight:700">
            ● {status}
        </div>
    </div>
    """, unsafe_allow_html=True)


def section_title(title, subtitle=None):
    st.markdown(f"### {title}")
    if subtitle:
        st.caption(subtitle)
