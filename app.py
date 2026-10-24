import streamlit as st
from PIL import Image
from utils.ai_service import analyze_image, ask_construction_assistant

st.set_page_config(
    page_title="Construction Intelligence AI",
    page_icon="🏗️",
    layout="wide",
)

st.title("🏗️ Multimodal Construction Intelligence Platform")

st.write(
    "An AI-powered platform for construction safety, "
    "crack diagnostics, cost estimation, and weather-aware guidance."
)

st.sidebar.title("Navigation")

module = st.sidebar.radio(
    "Choose a module",
    [
        "Home",
        "Site Safety & PPE Audit",
        "Crack Diagnostics",
        "Planning & Cost Estimation",
        "Daily Site Assistant",
    ],
)

if module == "Home":
    st.markdown(
        """
        <div style="
            background: linear-gradient(120deg, #123047, #237a78);
            padding: 32px;
            border-radius: 16px;
            color: white;
            margin-bottom: 24px;
        ">
            <h1>🏗️ Construction Intelligence AI</h1>
            <p style="font-size: 18px;">
                Smarter construction decisions powered by multimodal AI.
            </p>
            <p>
                Analyze safety, inspect visible defects, estimate costs,
                and receive weather-aware guidance.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Platform Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            "**🦺 Site Safety & PPE Audit**\n\n"
            "Analyze construction images for visible PPE and potential hazards."
        )

        st.info(
            "**💰 Planning & Cost Estimation**\n\n"
            "Estimate project budgets and illustrative material requirements."
        )

    with col2:
        st.info(
            "**🧱 Crack Diagnostics**\n\n"
            "Identify possible concrete defects and recommended next steps."
        )

        st.info(
            "**🌦️ Daily Site Assistant**\n\n"
            "Receive weather-aware safety guidance and ask construction questions."
        )

    st.divider()

    st.subheader("How to Use the Platform")

    st.markdown(
        """
        1. Choose a module from the sidebar.
        2. Upload an image for safety or crack analysis.
        3. Enter project details to estimate costs and materials.
        4. Select the current weather and ask the AI assistant a question.
        """
    )

    st.warning(
        "AI outputs are preliminary guidance. Cost and material estimates "
        "use simplified assumptions. Always consult qualified construction "
        "and safety professionals for real-world decisions."
    )

elif module == "Site Safety & PPE Audit":
    st.subheader("🦺 Site Safety & PPE Audit")

    uploaded_file = st.file_uploader(
        "Upload a construction site image",
        type=["jpg", "jpeg", "png"],
        key="safety_image",
    )

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded site image", use_container_width=True)

        if st.button("Analyze Site Safety"):
            with st.spinner("Analyzing image..."):
                prompt = """
                Analyze this construction site image for visible safety issues.

                Return:
                1. Overall safety status: Safe, Caution, or Unsafe.
                2. A safety score from 0 to 100, based only on visible evidence.
                3. Visible PPE: helmets, high-visibility vests, boots, and harnesses.
                4. Hazards, their severity, and recommended corrective actions.

                Clearly state when an item cannot be confirmed from the image.
                Do not claim that unseen PPE is missing.
                This is a preliminary visual assessment, not a certified safety inspection.
                """
                result = analyze_image(image, prompt)
                st.markdown("### Safety Analysis")
                st.write(result)

elif module == "Crack Diagnostics":
    st.subheader("🧱 Crack Diagnostics")

    uploaded_file = st.file_uploader(
        "Upload an image of a crack or concrete defect",
        type=["jpg", "jpeg", "png"],
        key="crack_image",
    )

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded defect image", use_container_width=True)

        if st.button("Analyze Crack"):
            with st.spinner("Analyzing visible defect..."):
                prompt = """
                Describe the visible crack or concrete defect in this image.

                Include:
                1. Possible defect category: hairline, settlement, structural shear,
                   thermal expansion, spalling, or uncertain.
                2. Visible characteristics.
                3. Possible causes, clearly labeled as possibilities.
                4. Recommended next steps and urgency.
                5. Whether an on-site professional inspection is advisable.

                Do not invent crack width measurements from an image without a scale.
                Do not claim to certify structural safety. If uncertain, say so.
                """
                result = analyze_image(image, prompt)
                st.markdown("### Crack Analysis")
                st.write(result)

elif module == "Planning & Cost Estimation":
    st.subheader("💰 Planning & Cost Estimation")

    structure = st.selectbox(
        "Structure type",
        ["Residential", "Commercial", "Industrial"],
    )

    area = st.number_input(
        "Built-up area (square feet)",
        min_value=100,
        value=1000,
        step=100,
    )

    tier = st.selectbox(
        "City category",
        ["Tier 1", "Tier 2", "Tier 3"],
    )

    progress = st.slider("Construction completed (%)", 0, 100, 25)

    # Illustrative rates only; replace with locally verified rates.
    rates = {
        "Tier 1": 2500,
        "Tier 2": 2000,
        "Tier 3": 1700,
    }

    if structure == "Commercial":
        rate = rates[tier] * 1.2
    elif structure == "Industrial":
        rate = rates[tier] * 1.4
    else:
        rate = rates[tier]

    estimated_budget = area * rate
    estimated_incurred = estimated_budget * progress / 100
    # Illustrative material estimates only
    cement_bags = area * 0.4
    steel_kg = area * 4.0

    st.subheader("Estimated Material Requirements")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "Estimated Cement",
            f"{cement_bags:,.0f} bags")

    with col2:
        st.metric(
            "Estimated Steel",
            f"{steel_kg:,.0f} kg")

    st.metric("Illustrative Project Budget", f"₹{estimated_budget:,.0f}")
    st.metric("Estimated Cost at Current Progress", f"₹{estimated_incurred:,.0f}")

    st.progress(progress / 100)
    st.write(f"Construction progress: **{progress}%**")

    st.caption(
        "Illustrative estimates only. Rates are assumptions, not live market prices. "
        "Actual costs depend on location, design, materials, labor, and site conditions. "
        "This calculation does not provide a property market valuation."
    )

elif module == "Daily Site Assistant":
    st.subheader("🌦️ Daily Site Assistant")

    weather = st.selectbox(
        "Current weather condition",
        ["Normal", "High Wind", "Heavy Rain", "Extreme Heat"],
    )

    advice = {
        "Normal": (
            "Follow the site's approved safety plan, inspect equipment, "
            "and use required PPE."
        ),
        "High Wind": (
            "Review site wind limits and secure loose materials. "
            "Pause crane, lifting, or work-at-height activities when required "
            "by the site safety plan."
        ),
        "Heavy Rain": (
            "Check drainage, slippery surfaces, electrical hazards, and excavation "
            "stability. Stop affected work when site conditions are unsafe."
        ),
        "Extreme Heat": (
            "Provide drinking water, rest breaks, shade, and heat-stress monitoring. "
            "Adjust work schedules according to site safety procedures."
        ),
    }

    st.warning(advice[weather])

    st.markdown("### Ask the Construction Assistant")

    question = st.text_area(
        "Enter your construction-related question",
        placeholder="Example: What precautions should we take during heavy rain?",
    )

    if st.button("Ask Assistant"):
        if question.strip():
            with st.spinner("Preparing guidance..."):
                result = ask_construction_assistant(question, weather)
                st.write(result)
        else:
            st.warning("Please enter a question first.")


        if question.strip():
            prompt = f"""
            You are a construction information assistant.
            Give practical, clear, safety-conscious general guidance.

            Current weather condition: {weather}
            User question: {question}

            Mention when the user should consult a qualified site engineer
            or safety professional. Do not invent site-specific facts.
            """
            with st.spinner("Preparing guidance..."):
                result = analyze_image(
                    Image.new("RGB", (1, 1), color="white"),
                    prompt,
                )
                st.write(result)
        else:
            st.warning("Please enter a question first.")
