from io import BytesIO

import streamlit as st
from PIL import Image

from agent import diagnose_leaf_image
from ui import (
    CUSTOM_CSS,
    render_back_button,
    render_result_dashboard,
    render_shell_close,
    render_shell_open,
    render_topbar,
    render_upload_state,
)


st.set_page_config(
    page_title="AI Plant Doctor",
    page_icon="AI",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def init_session_state():
    defaults = {
        "page_mode": "upload",
        "uploaded_image_bytes": None,
        "uploaded_image_name": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def load_uploaded_image():
    image_bytes = st.session_state.get("uploaded_image_bytes")
    if not image_bytes:
        st.session_state["page_mode"] = "upload"
        st.rerun()

    try:
        return Image.open(BytesIO(image_bytes)).convert("RGB")
    except Exception:
        st.error("Unable to read this image. Please upload a valid JPG, PNG, or WEBP file.")
        return None


def render_result_state():
    render_topbar(has_result=True)
    render_back_button()

    image = load_uploaded_image()
    if image is None:
        return

    with st.spinner("Checking leaf, detecting disease, and generating report..."):
        try:
            diagnosis = diagnose_leaf_image(image)
        except (FileNotFoundError, ValueError) as exc:
            st.error(str(exc))
            return
        except Exception as exc:
            st.error(f"Diagnosis failed: {exc}")
            return

    if diagnosis.report_warning:
        st.warning(diagnosis.report_warning)

    render_result_dashboard(image, diagnosis.model_result, diagnosis.report)


def main():
    init_session_state()
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    render_shell_open()

    if st.session_state["page_mode"] == "upload":
        render_upload_state()
    else:
        render_result_state()

    render_shell_close()


if __name__ == "__main__":
    main()
