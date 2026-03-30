import streamlit as st
from config import FIELDS


def render_field(field, user_input):
    label = field.replace('_', ' ').title()

    if field in FIELDS["numerical"]:
        cfg = FIELDS["numerical"][field]
        return st.number_input(
            label,
            min_value=cfg["min"],
            max_value=cfg["max"],
            step=cfg["step"]
        )

    elif field == "income_level":
        income = user_input.get("income_lakhs", 0)
        if income < 10:
            auto_val = "<10L"
        elif 10 <= income <= 25:
            auto_val = "10L - 25L"
        elif 25 < income <= 40:
            auto_val = "25L - 40L"
        else:
            auto_val = "> 40L"
        return st.selectbox(
            label,
            FIELDS["categorical"]["income_level"],
            index=FIELDS["categorical"]["income_level"].index(auto_val),
            disabled=True
        )

    else:
        options = FIELDS["categorical"].get(field, [])
        key = f"pills_{field}"
        track_key = f"pills_track_{field}"
        if track_key not in st.session_state:
            st.session_state[track_key] = options[0]
        if st.session_state.get(key) is None and key in st.session_state:
            st.session_state[key] = st.session_state[track_key]
        result = st.pills(label, options, default=options[0], selection_mode="single", key=key)
        if result is not None:
            st.session_state[track_key] = result
        return result if result is not None else st.session_state[track_key]


def render_medical_history():
    conditions = FIELDS["categorical"]["medical_history"]
    selected = st.pills("Medical History", conditions, selection_mode="multi")
    return " & ".join(selected) if selected else "No Disease"
