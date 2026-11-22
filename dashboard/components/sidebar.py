
import streamlit as st


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding:12px 4px 22px">
            <div style="color:#22D3EE;font-size:12px;
                        font-weight:800;letter-spacing:3px">
                ARES SYSTEMS
            </div>
            <div style="color:white;font-size:25px;
                        font-weight:800">
                COMMAND
            </div>
            <div style="color:#91A3B8;font-size:11px">
                INDUSTRIAL SAFETY PLATFORM
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        st.markdown("**OPERATIONS**")
        st.caption("Select a page from the navigation menu above.")

        st.divider()

        st.markdown("**SYSTEM STATUS**")
        st.success("Unit C · Simulation active")
        st.info("Units A, B and D · Prototype")

        st.divider()
        st.caption("ARES · Student prototype · 2026")
