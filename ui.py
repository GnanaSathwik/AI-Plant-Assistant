import html

import streamlit as st


CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --panel: #ffffff;
        --panel-soft: #f8fbf8;
        --line: #dfe8df;
        --text: #1f2a22;
        --muted: #5d6b60;
        --green: #49a64d;
        --green-dark: #1f6e31;
        --green-soft: #edf7ef;
        --warning: #ee9b16;
        --shadow: 0 18px 40px rgba(6, 27, 18, 0.16);
    }

    * {
        font-family: 'Manrope', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 12% 12%, rgba(73, 166, 77, 0.14), transparent 24%),
            radial-gradient(circle at 86% 18%, rgba(73, 166, 77, 0.12), transparent 28%),
            linear-gradient(180deg, #f4fbf5 0%, #eaf6ec 52%, #e3f1e6 100%);
        color: var(--text);
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    .stDeployButton,
    #MainMenu,
    footer,
    section[data-testid="stSidebar"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }

    .block-container {
        max-width: 1240px;
        padding-top: 1.3rem;
        padding-bottom: 2rem;
    }

    .dashboard-shell {
        background: rgba(255, 255, 255, 0.98);
        border: 1.5px solid #000000;
        border-radius: 28px;
        box-shadow: var(--shadow);
        padding: 1.5rem 1.5rem 1rem 1.5rem;
    }

    .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.15rem;
    }

    .topbar h1 {
        margin: 0;
        font-size: 1.7rem;
        line-height: 1.2;
        color: #142018;
        font-weight: 800;
    }

    .action-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.9rem 1.2rem;
        border-radius: 14px;
        background: linear-gradient(180deg, #5cbe62 0%, #409b45 100%);
        color: #ffffff;
        font-size: 0.98rem;
        font-weight: 800;
        text-decoration: none;
        box-shadow: 0 10px 18px rgba(73, 166, 77, 0.22);
    }

    .upload-state {
        display: grid;
        place-items: center;
        min-height: 62vh;
        padding: 1rem 0 0.5rem 0;
    }

    .front-wrap {
        width: min(1120px, 100%);
        margin: 0 auto;
    }

    .front-hero {
        text-align: center;
        margin-bottom: 1rem;
    }

    .front-spark {
        color: #efc23a;
        font-size: 1.9rem;
        line-height: 1;
        margin-bottom: 0.15rem;
    }

    .front-title-row {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1.4rem;
        margin-bottom: 0.45rem;
    }

    .front-title-icon {
        color: #67b26d;
        font-size: 2rem;
        line-height: 1;
    }

    .front-title {
        margin: 0;
        color: #14512b;
        font-size: clamp(3rem, 5vw, 4rem);
        line-height: 1.04;
        font-weight: 800;
    }

    .front-tagline {
        color: #359243;
        font-size: 1.05rem;
        font-weight: 800;
        margin-bottom: 0.55rem;
    }

    .front-copy {
        max-width: 560px;
        margin: 0 auto;
        color: #35453a;
        font-size: 0.98rem;
        line-height: 1.6;
    }

    .upload-card {
        width: min(680px, 100%);
        background: var(--panel-soft);
        border: 1.5px solid #000000;
        border-radius: 22px;
        padding: 1.4rem;
        margin: 0 auto;
    }

    .upload-drop {
        border: 1.5px dashed #000000;
        border-radius: 18px;
        padding: 2rem 1.25rem;
        text-align: center;
        background: #ffffff;
    }

    .upload-badge {
        display: grid;
        place-items: center;
        width: 72px;
        height: 72px;
        margin: 0 auto 1rem auto;
        border-radius: 50%;
        background: var(--green-soft);
        color: var(--green-dark);
        font-size: 2rem;
        font-weight: 800;
    }

    .upload-title {
        font-size: 1.2rem;
        font-weight: 800;
        color: #17311f;
        margin-bottom: 0.35rem;
    }

    .upload-copy {
        color: var(--muted);
        font-size: 0.96rem;
        margin-bottom: 1rem;
    }

    div[data-testid="stFileUploader"] {
        max-width: 220px;
        margin: 0 auto;
    }

    div[data-testid="stFileUploader"] > label,
    div[data-testid="stFileUploader"] small,
    div[data-testid="stFileUploader"] [data-testid="stFileUploaderDropzoneInstructions"] {
        display: none;
    }

    div[data-testid="stFileUploader"] section {
        background: transparent;
        border: 0;
        padding: 0;
    }

    div[data-testid="stFileUploader"] button {
        width: 100%;
        min-height: 50px;
        border: 0;
        border-radius: 12px;
        background: linear-gradient(180deg, #58b75d 0%, #3e9644 100%);
        color: white;
        font-size: 0;
        font-weight: 800;
        box-shadow: 0 12px 22px rgba(73, 166, 77, 0.2);
    }

    div[data-testid="stFileUploader"] button::after {
        content: "+ Upload Image";
        font-size: 0.98rem;
    }

    .front-upload-btn-wrap {
        display: flex;
        justify-content: center;
        margin-top: 0.7rem;
        margin-bottom: 1.25rem;
    }

    .front-section-title {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.5rem;
        margin: 0.55rem 0 0.85rem 0;
        color: #193b24;
        font-size: 0.98rem;
        font-weight: 800;
    }

    .front-section-title span {
        color: #d9c866;
        font-size: 1rem;
    }

    .front-feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-bottom: 1.4rem;
    }

    .front-feature-card,
    .front-step-card,
    .front-tip-card {
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid #dfe8df;
        border-radius: 22px;
        box-shadow: 0 14px 28px rgba(18, 34, 20, 0.06);
    }

    .front-feature-card {
        display: grid;
        grid-template-columns: 74px 1fr;
        gap: 1rem;
        align-items: center;
        padding: 1.3rem 1.25rem;
    }

    .front-circle {
        width: 74px;
        height: 74px;
        border-radius: 50%;
        border: 2px solid #89c68d;
        display: grid;
        place-items: center;
        color: #49a64d;
        font-size: 2rem;
        font-weight: 800;
        background: rgba(237, 247, 239, 0.95);
    }

    .front-card-title {
        color: #1c3123;
        font-size: 0.98rem;
        font-weight: 800;
        margin-bottom: 0.35rem;
    }

    .front-card-copy {
        color: #536359;
        font-size: 0.92rem;
        line-height: 1.55;
    }

    .front-step-card {
        display: grid;
        grid-template-columns: 1fr auto 1fr auto 1fr;
        gap: 1rem;
        align-items: center;
        padding: 1.3rem 1.35rem;
        margin-bottom: 1rem;
    }

    .front-step {
        display: grid;
        grid-template-columns: 74px 1fr;
        gap: 1rem;
        align-items: center;
    }

    .front-arrow {
        color: #b6c4b8;
        font-size: 2rem;
        line-height: 1;
    }

    .front-tip-card {
        display: grid;
        grid-template-columns: 74px 1fr;
        gap: 1rem;
        align-items: center;
        padding: 1.1rem 1.25rem;
    }

    .grid-3 {
        display: grid;
        grid-template-columns: 1.12fr 0.9fr 1.08fr;
        gap: 1rem;
    }

    .grid-3-bottom {
        display: grid;
        grid-template-columns: 1.1fr 0.48fr 0.52fr;
        gap: 1rem;
        margin-top: 1rem;
    }

    .mini-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.8rem;
        margin-top: 1rem;
    }

    .panel-card {
        background: #ffffff;
        border: 1.5px solid #000000;
        border-radius: 18px;
        padding: 1.2rem;
        box-shadow: 0 8px 24px rgba(20, 32, 24, 0.05);
        height: 100%;
    }

    .panel-title {
        font-size: 0.95rem;
        font-weight: 800;
        color: #172118;
        margin-bottom: 0.9rem;
    }

    .leaf-image-wrap img {
        width: 100%;
        aspect-ratio: 0.9 / 1;
        object-fit: cover;
        border-radius: 14px;
        border: 1.5px solid #000000;
    }

    .sub-btn {
        display: inline-flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        min-height: 46px;
        border: 1.5px solid #000000;
        border-radius: 12px;
        background: #ffffff;
        color: #2f7e37;
        font-size: 0.95rem;
        font-weight: 800;
        margin-top: 1rem;
    }

    .disease-head {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .disease-name {
        font-size: 2.15rem;
        line-height: 1.08;
        color: #1d5c2a;
        font-weight: 800;
        margin-bottom: 0.3rem;
    }

    .plant-name {
        font-size: 1.05rem;
        color: #2f3f33;
        font-weight: 600;
    }

    .disease-icon {
        display: grid;
        place-items: center;
        width: 76px;
        height: 76px;
        border-radius: 50%;
        background: var(--green-soft);
        color: var(--green);
        font-size: 2rem;
        flex: 0 0 auto;
    }

    .risk-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        color: #d48309;
        font-size: 0.95rem;
        font-weight: 700;
        margin-bottom: 1.35rem;
    }

    .copy-block {
        color: #425145;
        font-size: 1rem;
        line-height: 1.75;
    }

    .list-clean {
        display: grid;
        gap: 0.9rem;
    }

    .list-item {
        display: grid;
        grid-template-columns: 34px 1fr;
        gap: 0.8rem;
        align-items: start;
        color: #304036;
        font-size: 0.98rem;
        line-height: 1.55;
    }

    .list-icon {
        display: grid;
        place-items: center;
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background: var(--green-soft);
        color: var(--green);
        font-size: 1.1rem;
        font-weight: 800;
    }

    .fert-row {
        display: grid;
        grid-template-columns: 42px 1fr auto;
        gap: 0.9rem;
        align-items: start;
        padding: 0.85rem 0;
        border-bottom: 1px solid #edf2ed;
    }

    .fert-row:last-child {
        border-bottom: 0;
        padding-bottom: 0.2rem;
    }

    .fert-name {
        color: #16231a;
        font-size: 0.98rem;
        font-weight: 800;
        margin-bottom: 0.18rem;
    }

    .fert-copy {
        color: #5f6f64;
        font-size: 0.9rem;
        line-height: 1.45;
    }

    .fert-dose {
        color: #3b72b4;
        font-size: 0.92rem;
        font-weight: 700;
        text-align: right;
        min-width: 110px;
    }

    .mini-card {
        background: #ffffff;
        border: 1.5px solid #000000;
        border-radius: 16px;
        padding: 1rem 1.2rem;
        box-shadow: 0 8px 18px rgba(20, 32, 24, 0.04);
    }

    .mini-label {
        color: #172118;
        font-size: 0.92rem;
        font-weight: 800;
        margin-bottom: 0.55rem;
    }

    .mini-value {
        color: #415145;
        font-size: 1rem;
        font-weight: 600;
        line-height: 1.5;
    }

    .confidence-wrap {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.65rem;
    }

    .confidence-ring {
        width: 118px;
        height: 118px;
        border-radius: 50%;
        display: grid;
        place-items: center;
        background: conic-gradient(#49a64d var(--confidence), #e7f1e8 0);
    }

    .confidence-inner {
        width: 90px;
        height: 90px;
        border-radius: 50%;
        background: #ffffff;
        display: grid;
        place-items: center;
        font-size: 1.6rem;
        font-weight: 800;
        color: #172118;
    }

    .confidence-copy {
        text-align: center;
        color: #516055;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    .chat-btn {
        display: inline-flex;
        justify-content: center;
        align-items: center;
        gap: 0.5rem;
        min-height: 48px;
        padding: 0 1.1rem;
        border-radius: 12px;
        background: linear-gradient(180deg, #58b75d 0%, #3e9644 100%);
        color: #ffffff;
        font-size: 0.96rem;
        font-weight: 800;
        margin-top: 1rem;
    }

    .footnote {
        margin-top: 0.75rem;
        color: #6b776d;
        font-size: 0.88rem;
    }

    @media (max-width: 1100px) {
        .grid-3,
        .grid-3-bottom,
        .mini-grid {
            grid-template-columns: 1fr;
        }

        .front-feature-grid,
        .front-step-card {
            grid-template-columns: 1fr;
        }

        .front-arrow {
            display: none;
        }
    }
</style>
"""


def render_shell_open():
    st.markdown('<div class="dashboard-shell">', unsafe_allow_html=True)


def render_shell_close():
    st.markdown("</div>", unsafe_allow_html=True)


def render_back_button():
    if st.button("Back to Upload", key="back_to_upload"):
        st.session_state["page_mode"] = "upload"
        st.session_state["uploaded_image_bytes"] = None
        st.session_state["uploaded_image_name"] = None
        st.rerun()


def render_topbar(has_result: bool):
    title_text = "Diagnosis Result" if has_result else ""
    if not has_result:
        return
    action_markup = ""
    st.markdown(
        f"""
        <div class="topbar">
            <h1>{title_text}</h1>
            {action_markup}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_upload_state():
    st.markdown(
        """
        <div class="upload-state">
            <div class="front-wrap">
                <div class="front-hero">
                    <div class="front-spark">&#10022;</div>
                    <div class="front-title-row">
                        <div class="front-title-icon">&#9094;</div>
                        <h1 class="front-title">AI Plant Doctor</h1>
                        <div class="front-title-icon">&#9094;</div>
                    </div>
                    <div class="front-tagline">Smart. Accurate. Instant Plant Care.</div>
                    <div class="front-copy">Upload a leaf image and get an AI-powered diagnosis,<br>treatment suggestions, and care tips.</div>
                </div>
                <div class="upload-card">
                    <div class="upload-drop">
                        <div class="upload-badge">&#10501;</div>
                        <div class="upload-title">Upload Leaf Image</div>
                        <div class="upload-copy">Choose a clear plant leaf image to generate an AI diagnosis report.</div>
        """,
        unsafe_allow_html=True,
    )
    uploaded_file = st.file_uploader(
        "Upload leaf image",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed",
    )
    if uploaded_file is not None:
        st.session_state["uploaded_image_bytes"] = uploaded_file.getvalue()
        st.session_state["uploaded_image_name"] = uploaded_file.name
        st.session_state["page_mode"] = "result"
        st.rerun()
    st.markdown(
        """
                    </div>
                </div>
                <div class="front-upload-btn-wrap"></div>
                <div class="front-section-title"><span>&#10022;</span> Why AI Plant Doctor? <span>&#10022;</span></div>
                <div class="front-feature-grid">
                    <div class="front-feature-card">
                        <div class="front-circle">&#9711;</div>
                        <div>
                            <div class="front-card-title">Disease Detection</div>
                            <div class="front-card-copy">Detects plant diseases accurately using advanced AI models.</div>
                        </div>
                    </div>
                    <div class="front-feature-card">
                        <div class="front-circle">&#9881;</div>
                        <div>
                            <div class="front-card-title">Treatment Suggestions</div>
                            <div class="front-card-copy">Get effective treatment and fertilizer recommendations.</div>
                        </div>
                    </div>
                    <div class="front-feature-card">
                        <div class="front-circle">&#128202;</div>
                        <div>
                            <div class="front-card-title">Health Report</div>
                            <div class="front-card-copy">Detailed health insights and prevention tips for your plant.</div>
                        </div>
                    </div>
                </div>
                <div class="front-section-title"><span>&#10022;</span> How It Works <span>&#10022;</span></div>
                <div class="front-step-card">
                    <div class="front-step">
                        <div class="front-circle">&#10501;</div>
                        <div>
                            <div class="front-card-title">1. Upload Image</div>
                            <div class="front-card-copy">Upload a clear leaf image.</div>
                        </div>
                    </div>
                    <div class="front-arrow">&#8594;</div>
                    <div class="front-step">
                        <div class="front-circle">AI</div>
                        <div>
                            <div class="front-card-title">2. AI Analysis</div>
                            <div class="front-card-copy">Our AI analyzes the leaf image.</div>
                        </div>
                    </div>
                    <div class="front-arrow">&#8594;</div>
                    <div class="front-step">
                        <div class="front-circle">&#128203;</div>
                        <div>
                            <div class="front-card-title">3. Get Results</div>
                            <div class="front-card-copy">Receive diagnosis, treatment and tips.</div>
                        </div>
                    </div>
                </div>
                <div class="front-tip-card">
                    <div class="front-circle">&#128161;</div>
                    <div>
                        <div class="front-card-title">Tip</div>
                        <div class="front-card-copy">For best results, upload a high-quality image of the affected leaf with good lighting.</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return uploaded_file


def risk_label(confidence: float) -> str:
    if confidence >= 85:
        return "High Confidence"
    if confidence >= 60:
        return "Moderate Risk"
    return "Low Confidence"


def disease_type(disease_name: str) -> str:
    lowered = disease_name.lower()
    if "virus" in lowered:
        return "Viral"
    if "bacterial" in lowered:
        return "Bacterial"
    if "mildew" in lowered or "blight" in lowered or "mold" in lowered or "rot" in lowered or "spot" in lowered:
        return "Fungal"
    if lowered == "healthy":
        return "Healthy"
    return "Plant Stress"


def affected_area(disease_name: str) -> str:
    lowered = disease_name.lower()
    if "root" in lowered:
        return "Roots"
    if "fruit" in lowered:
        return "Fruit"
    return "Leaves"


def fertilizer_rows(fertilizers):
    rows = []
    fallback_doses = ["50-60 g/plant", "30-40 g/plant", "20-30 g/plant", "Apply as directed"]
    for index, item in enumerate((fertilizers or [])[:4]):
        if isinstance(item, dict):
            name = str(item.get("name", "Recommended Fertilizer"))
            copy = str(item.get("description", "Supports balanced recovery and crop health."))
            dose = str(item.get("dose", fallback_doses[min(index, len(fallback_doses) - 1)]))
        else:
            name = str(item)
            copy = "Supports plant recovery and nutrient balance."
            dose = fallback_doses[min(index, len(fallback_doses) - 1)]
        rows.append((name, copy, dose))

    if not rows:
        rows = [
            ("Balanced NPK", "Supports steady plant growth.", "Use as directed"),
            ("Organic Compost", "Improves soil structure and moisture retention.", "Apply around root zone"),
        ]
    return rows


def render_result_dashboard(image, model_result: dict, report: dict):
    plant_name = html.escape(model_result.get("plant_name", "Unknown Plant"))
    disease_name = html.escape(model_result.get("disease_name", "Unknown Disease"))
    confidence = float(model_result.get("confidence", 0.0))
    confidence_ring = max(0, min(confidence, 100))
    description = report.get("description") or "No description available."
    treatments = report.get("treatment_steps") or []
    fertilizers = fertilizer_rows(report.get("recommended_fertilizers"))
    tips = report.get("tips_for_improvement") or []

    if not tips:
        tips = [
            "Rotate crops to prevent disease buildup in soil.",
            "Maintain proper spacing between plants.",
            "Use disease-free seeds or seedlings.",
            "Monitor regularly and act early.",
        ]

    top_col1, top_col2, top_col3 = st.columns([1.15, 0.95, 1.1], gap="large")

    with top_col1:
        st.markdown('<div class="panel-card"><div class="panel-title">Uploaded Leaf</div>', unsafe_allow_html=True)
        st.markdown('<div class="leaf-image-wrap">', unsafe_allow_html=True)
        st.image(image, use_container_width=True)
        st.markdown('</div><div class="sub-btn">Upload Another Leaf</div></div>', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="mini-card">
                <div class="mini-label">Affected Crop</div>
                <div class="mini-value">{plant_name}</div>
            </div>
            <div class="mini-card">
                <div class="mini-label">Disease Type</div>
                <div class="mini-value">{html.escape(disease_type(html.unescape(disease_name)))}</div>
            </div>
            <div class="mini-card">
                <div class="mini-label">Affects</div>
                <div class="mini-value">{html.escape(affected_area(html.unescape(disease_name)))}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="panel-card"><div class="panel-title">Additional Tips</div><div class="list-clean">', unsafe_allow_html=True)
        for tip in tips[:4]:
            st.markdown(
                f"""
                <div class="list-item">
                    <div class="list-icon">&#10003;</div>
                    <div>{html.escape(str(tip))}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown(
            """
            </div>
            <div style="display:flex; justify-content:flex-end; margin-top: 0.5rem; font-size: 6rem; line-height: 1;">&#127793;</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with top_col2:
        st.markdown(
            f"""
            <div class="panel-card">
                <div class="panel-title">Detected Disease</div>
                <div class="disease-head">
                    <div>
                        <div class="disease-name">{disease_name}</div>
                        <div class="plant-name">{plant_name}</div>
                    </div>
                    <div class="disease-icon">&#127811;</div>
                </div>
                <div class="risk-pill">&#9888; {risk_label(confidence)}</div>
                <div class="panel-title" style="margin-bottom: 0.45rem;">Description</div>
                <div class="copy-block">{html.escape(str(description))}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with top_col3:
        st.markdown('<div class="panel-card"><div class="panel-title">Treatment</div><div class="list-clean">', unsafe_allow_html=True)
        for step in treatments[:5]:
            st.markdown(
                f"""
                <div class="list-item">
                    <div class="list-icon">&#10003;</div>
                    <div>{html.escape(str(step))}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown('</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="panel-card"><div class="panel-title">Recommended Fertilizers</div>', unsafe_allow_html=True)
        for name, copy, dose in fertilizers:
            st.markdown(
                f"""
                <div class="fert-row">
                    <div class="list-icon">&#10047;</div>
                    <div>
                        <div class="fert-name">{html.escape(name)}</div>
                        <div class="fert-copy">{html.escape(copy)}</div>
                    </div>
                    <div class="fert-dose">Dose<br>{html.escape(dose)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

    summary_spacer, summary_right = st.columns([1.58, 0.9], gap="large")

    with summary_spacer:
        st.markdown("<div></div>", unsafe_allow_html=True)

    with summary_right:
        st.markdown(
            f"""
            <div class="panel-card">
                <div class="panel-title">Confidence Score</div>
                <div class="confidence-wrap">
                    <div class="confidence-ring" style="--confidence: {confidence_ring}%;">
                        <div class="confidence-inner">{confidence_ring:.0f}%</div>
                    </div>
                    <div class="confidence-copy">
                        <strong>{risk_label(confidence)}</strong><br>
                        Our AI model is {confidence_ring:.0f}% sure about this diagnosis.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<div></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="footnote">
            Note: This is an AI-generated diagnosis. Please consult a local agricultural expert for final confirmation.
        </div>
        """,
        unsafe_allow_html=True,
    )

