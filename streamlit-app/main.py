import streamlit as st
from prediction_helper import predict
from config import FIELD_ORDER
from ui_components import render_field, render_medical_history

st.set_page_config(layout="wide")

st.markdown("""
<style>
/* Keep columns top-aligned so right panel doesn't stretch */
div[data-testid="stHorizontalBlock"] {
    align-items: flex-start;
}
/* Stick the right panel to the top of the viewport */
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:last-child {
    position: sticky;
    top: 3rem;
}
</style>
""", unsafe_allow_html=True)

st.title("Healthcare Premium Prediction")

left_col, divider_col, right_col = st.columns([2, 0.05, 1])

with left_col:
    st.subheader("Enter your details:")
    user_input = {}

    with st.container(height=750, border=False):
        for i in range(0, len(FIELD_ORDER), 2):
            cols = st.columns(2)
            for col_index, field in enumerate(FIELD_ORDER[i:i+2]):
                with cols[col_index]:
                    user_input[field] = render_field(field, user_input)

        user_input["medical_history"] = render_medical_history()

with divider_col:
    st.markdown(
        "<div style='border-left: 2px solid #e0e0e0; height: 100%; min-height: 400px;'></div>",
        unsafe_allow_html=True
    )

with right_col:
    st.subheader("Prediction")
    st.write("")
    st.write("")

    if st.button("Predict Premium", use_container_width=True):
        prediction = predict(user_input)
        st.success("Estimated Annual Premium")
        st.metric(label="", value=f"₹ {prediction:,}")
