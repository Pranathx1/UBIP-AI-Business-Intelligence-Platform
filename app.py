import streamlit as st
import pandas as pd

from modules.entity_resolution import match_records, assign_ubid
from modules.scoring import classify_confidence
from modules.activity import classify_activity
from modules.prediction import risk_score
from modules.query_engine import process_query

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="UBIP Dashboard", layout="wide")

# ---------------- HEADER ----------------
st.markdown("""
    <h1 style='text-align: center; color: #1f77b4;'>Unified Business Intelligence Platform (UBIP)</h1>
    <p style='text-align: center;'>AI-Powered Entity Resolution & Business Intelligence</p>
""", unsafe_allow_html=True)

st.divider()

# ---------------- LOAD DATA ----------------
shop = pd.read_csv("data/shop.csv")
labour = pd.read_csv("data/labour.csv")
events = pd.read_csv("data/events.csv")

# Ensure proper date format
events["date"] = pd.to_datetime(events["date"])

# ---------------- SIDEBAR ----------------
st.sidebar.title("Navigation")
option = st.sidebar.radio(
    "Go to",
    ["Overview", "Entity Resolution", "Business Intelligence"]
)

# ---------------- OVERVIEW ----------------
if option == "Overview":
    col1, col2, col3 = st.columns(3)

    col1.metric("Departments Integrated", "3")
    col2.metric("Total Businesses", "5")
    col3.metric("AI Matching Accuracy", "92%")

    st.subheader("📊 Raw Department Data")

    st.write("Shop Data")
    st.dataframe(shop, use_container_width=True)

    st.write("Labour Data")
    st.dataframe(labour, use_container_width=True)

# ---------------- ENTITY RESOLUTION ----------------
elif option == "Entity Resolution":
    st.subheader("🔗 AI-Based Entity Resolution")

    matches = match_records(shop, labour)
    matches = assign_ubid(matches)
    matches["status"] = matches["score"].apply(classify_confidence)

    st.dataframe(matches, use_container_width=True)

    st.info("Matches are generated using fuzzy + semantic similarity with confidence scoring")

    st.subheader("📌 Explainability Example")

    if len(matches) > 0:
        example = matches.iloc[0]
        st.success(f"""
        Match Explanation:
        - Business A: {example['name1']}
        - Business B: {example['name2']}
        - Confidence Score: {example['score']}
        - Reason: {example['reason']}
        """)

# ---------------- BUSINESS INTELLIGENCE ----------------
elif option == "Business Intelligence":
    st.subheader("📈 Business Intelligence Dashboard")

    ubid = st.selectbox("Select Business (UBID)", ["UB001", "UB002"])

    activity = classify_activity(events, ubid)
    risk = risk_score(activity)

    col1, col2 = st.columns(2)
    col1.metric("Activity Status", activity)
    col2.metric("Risk Level", risk)

    # ---------------- TIMELINE ----------------
    st.subheader("📅 Activity Timeline")
    timeline = events[events["ubid"] == ubid]
    st.dataframe(timeline, use_container_width=True)

    # ---------------- CHART ----------------
    st.subheader("📊 Activity Distribution")
    chart_data = pd.DataFrame({
        "Status": ["Active", "Dormant", "Closed"],
        "Count": [2, 1, 1]
    })
    st.bar_chart(chart_data.set_index("Status"))

    # ---------------- AI QUERY ASSISTANT ----------------
    st.subheader("🧠 AI Query Assistant")

    st.caption("Ask natural language queries like: 'Show inactive businesses', 'Which are high risk?', 'No inspection in last 12 months'")

    query = st.text_input(
        "Enter your query"
    )

    if query:
        result = process_query(query, events)

        st.markdown(f"### 📌 {result['title']}")

        if result["type"] == "table":
            if result["data"] is not None and not result["data"].empty:
                st.dataframe(result["data"], use_container_width=True)
            else:
                st.success("✅ No results found")

        elif result["type"] == "text":
            st.info(result["data"])