
import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Expense Categorizer", page_icon="", layout="wide")

st.title("Personal Expense Categorizer")
st.caption("Upload your transactions and let the model sort your spending into categories automatically.")

@st.cache_resource
def load_model():
    model = joblib.load("category_model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    return model, vectorizer

try:
    model, vectorizer = load_model()
except FileNotFoundError:
    st.error(
        "Model files not found. Run `python 02_train_classifier.py` first "
        "to train and save the model before launching this dashboard."
    )
    st.stop()

uploaded_file = st.file_uploader(
    "Upload a transactions CSV (needs 'date', 'description', 'amount' columns)",
    type="csv",
)

use_sample = st.checkbox("Use sample transactions.csv instead", value=not uploaded_file)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
elif use_sample:
    try:
        df = pd.read_csv("transactions.csv")
    except FileNotFoundError:
        st.warning("No transactions.csv found. Run 01_generate_data.py first, or upload your own file.")
        st.stop()
else:
    st.info("Upload a CSV or check the sample data box to get started.")
    st.stop()

if "category" in df.columns:
    df = df.drop(columns=["category"])

description_vectors = vectorizer.transform(df["description"])
df["predicted_category"] = model.predict(description_vectors)

st.subheader("Categorized Transactions")
st.dataframe(df, use_container_width=True)

st.subheader("Spending Summary by Category")

spend_df = df[df["amount"] < 0].copy()
spend_df["amount"] = spend_df["amount"].abs()
summary = spend_df.groupby("predicted_category")["amount"].sum().sort_values(ascending=False)

col1, col2 = st.columns([2, 1])
with col1:
    st.bar_chart(summary)
with col2:
    st.write("**Total spend per category:**")
    for category, total in summary.items():
        st.write(f"- {category}: ₹{total:,.0f}")

total_spend = spend_df["amount"].sum()
st.metric("Total Spending", f"₹{total_spend:,.0f}")
