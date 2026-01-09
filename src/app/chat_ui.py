import streamlit as st

def render_chat(messages):
    for msg in messages:
        role = msg.get("role", "assistant")
        content = msg.get("content", "")

        with st.chat_message(role):
            # Main message
            st.markdown(content)

            # Only assistants have extras
            if role != "assistant":
                continue

            # -----------------------
            # Confidence block
            # -----------------------
            if "confidence" in msg:
                conf = msg["confidence"]

                st.markdown(f"**Confidence:** `{conf.get('label', 'Unknown')}`")

                with st.expander("🔍 Confidence details"):
                    # Basic confidence details
                    details = conf.get("details", {})
                    for k, v in details.items():
                        st.markdown(f"- **{k}**: {v}")

                    # Evaluation KPIs (if available)
                    evaluation = conf.get("evaluation")
                    if evaluation:
                        st.markdown("### 📊 Evaluation KPIs")

                        for group, metrics in evaluation.items():
                            st.markdown(f"**{group.upper()}**")
                            for mk, mv in metrics.items():
                                st.markdown(f"- {mk}: {mv}")

            # -----------------------
            # Citations block
            # -----------------------
            if "citations" in msg and msg["citations"]:
                with st.expander("📚 Sources"):
                    for c in msg["citations"]:
                        source = c.get("source", "Unknown source")
                        page = c.get("page", "N/A")
                        st.markdown(f"- **{source}**, Page {page}")
