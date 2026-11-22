
with status_col:
    st.markdown(
        '<div class="ares-section">ARES unit network</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # DRONE DEFINITIONS
    # -----------------------------------------------------

    unit_data = [
        {
            "code": "UNIT A",
            "name": "Rapid wildfire response",
            "desc": "Fire detection, thermal observation and perimeter mapping",
            "status": "CONCEPT / NOT CONNECTED",
            "mission": "Rapid wildfire response",
            "capabilities": "Aerial fire detection, thermal observation, perimeter mapping and initial incident assessment.",
            "deployment": "Wildfire detection and initial aerial assessment."
        },
        {
            "code": "UNIT B",
            "name": "Advanced intervention",
            "desc": "Specialized support for difficult fires and industrial incidents",
            "status": "CONCEPT / NOT CONNECTED",
            "mission": "Advanced intervention",
            "capabilities": "Specialized aerial assessment and intervention support for difficult wildfire and industrial incidents.",
            "deployment": "Severe industrial incidents and difficult wildfire conditions."
        },
        {
            "code": "UNIT C",
            "name": "Industrial intelligence",
            "desc": "Collects chemical, gas and environmental facility data",
            "status": "SIMULATION ACTIVE",
            "mission": "Industrial intelligence",
            "capabilities": "Facility chemical inventories, gas readings, environmental monitoring, hazard locations and industrial sensor information.",
            "deployment": "Permanent or scheduled monitoring of high-risk industrial facilities."
        },
        {
            "code": "UNIT D",
            "name": "Catastrophe response",
            "desc": "Large-scale emergency assessment alongside firefighters",
            "status": "PROTOTYPE",
            "mission": "Catastrophe response",
            "capabilities": "Large-scale aerial assessment, incident observation and emergency coordination support.",
            "deployment": "Major fires and catastrophes alongside firefighters and emergency services."
        }
    ]

    # -----------------------------------------------------
    # CLICKABLE DRONE CARDS
    # -----------------------------------------------------

    if "selected_unit" not in st.session_state:
        st.session_state["selected_unit"] = None

    for unit in unit_data:
        code = unit["code"]

        if st.button(
            f"🛰️  {code}  |  {unit['name']}\n"
            f"{unit['desc']}\n"
            f"● {unit['status']}",
            key=f"drone_{code}",
            use_container_width=True
        ):
            st.session_state["selected_unit"] = code

    # -----------------------------------------------------
    # SELECTED DRONE PROFILE
    # -----------------------------------------------------

    selected_unit = st.session_state["selected_unit"]

    if selected_unit:
        profile = next(
            unit for unit in unit_data
            if unit["code"] == selected_unit
        )

        st.divider()

        st.markdown(
            f'<div class="ares-section">{selected_unit} · OPERATIONAL PROFILE</div>',
            unsafe_allow_html=True
        )

        st.markdown(f"""
        <div class="ares-unit">
            <div class="ares-unit-code">{profile['code']}</div>
            <div class="ares-unit-name">{profile['mission']}</div>
            <div class="ares-unit-desc">
                <b>Capabilities</b><br>
                {profile['capabilities']}
            </div>
            <div class="ares-unit-desc" style="margin-top:15px">
                <b>Deployment conditions</b><br>
                {profile['deployment']}
            </div>
            <div class="ares-unit-status" style="color:#F2B84B">
                SIMULATED / PROTOTYPE DATA
            </div>
        </div>
        """, unsafe_allow_html=True)

        if selected_unit == "UNIT C":
            st.info(
                "Unit C communicates industrial hazard intelligence "
                "to the ARES Fire & Emergency Command Center. "
                "Human operators decide which response drones to deploy."
            )

        if st.button("Close drone profile", key="close_drone_profile"):
            st.session_state["selected_unit"] = None
            st.rerun()
