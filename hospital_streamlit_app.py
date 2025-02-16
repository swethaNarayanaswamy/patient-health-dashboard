import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set page configuration
st.set_page_config(page_title="Hospital Data Dashboard", layout="wide")

# Load dataset
@st.cache_data  # Cache the data to improve performance
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Error loading the dataset: {e}")
        return None

def analyze_hospital_data(df):
    if df is None:
        return

    # Sidebar for filters
    st.sidebar.header("Filters")
    condition_filter = st.sidebar.multiselect("Select Condition", df["Condition"].unique())
    outcome_filter = st.sidebar.multiselect("Select Outcome", df["Outcome"].unique())

    # Apply filters
    if condition_filter:
        df = df[df["Condition"].isin(condition_filter)]
    if outcome_filter:
        df = df[df["Outcome"].isin(outcome_filter)]

    # Main dashboard
    st.title("🏥 Hospital Data Analysis Dashboard")
    st.markdown("### Overview of Patient Data, Treatment Costs, and Conditions")

    # Key Metrics in Columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Patients", df.shape[0])
    with col2:
        recovery_rate = (df[df['Outcome'] == 'Recovered'].shape[0] / df.shape[0]) * 100 if df.shape[0] > 0 else 0
        st.metric("Recovery Rate", f"{recovery_rate:.2f}%")
    with col3:
        st.metric("Total Treatment Cost", f"${df['Cost'].sum():,.2f}")
    with col4:
        st.metric("Average Treatment Cost", f"${df['Cost'].mean():,.2f}")

    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Patient Outcomes", "Cost Analysis", "Condition Analysis"])

    # Tab 1: Patient Outcomes
    with tab1:
        st.subheader("Patient Outcome Distribution")
        outcome_counts = df["Outcome"].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.pie(outcome_counts, labels=outcome_counts.index, autopct='%1.1f%%', colors=["lightblue", "lightcoral", "lightgreen"])
        st.pyplot(fig1)

    # Tab 2: Cost Analysis
    with tab2:
        st.subheader("Treatment Cost Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Total Cost by Condition**")
            cost_by_condition = df.groupby("Condition")["Cost"].sum().sort_values(ascending=False)
            fig2, ax2 = plt.subplots()
            cost_by_condition.plot(kind="bar", color="skyblue", ax=ax2)
            plt.xticks(rotation=45, ha='right')
            plt.ylabel("Total Cost")
            st.pyplot(fig2)
        with col2:
            st.markdown("**Average Cost by Condition**")
            avg_cost_by_condition = df.groupby("Condition")["Cost"].mean().sort_values(ascending=False)
            fig3, ax3 = plt.subplots()
            avg_cost_by_condition.plot(kind="bar", color="lightgreen", ax=ax3)
            plt.xticks(rotation=45, ha='right')
            plt.ylabel("Average Cost")
            st.pyplot(fig3)

    # Tab 3: Condition Analysis
    with tab3:
        st.subheader("Condition Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Top 10 Most Common Conditions**")
            disease_counts = df["Condition"].value_counts().nlargest(10)
            fig4, ax4 = plt.subplots()
            sns.barplot(x=disease_counts.index, y=disease_counts.values, palette="Blues_d", ax=ax4)
            plt.xticks(rotation=45, ha='right')
            plt.xlabel("Condition")
            plt.ylabel("Count")
            st.pyplot(fig4)
        with col2:
            st.markdown("**Length of Stay by Condition**")
            avg_stay_by_condition = df.groupby("Condition")["Length_of_Stay"].mean().sort_values(ascending=False)
            fig5, ax5 = plt.subplots()
            avg_stay_by_condition.plot(kind="bar", color="orange", ax=ax5)
            plt.xticks(rotation=45, ha='right')
            plt.ylabel("Average Length of Stay (Days)")
            st.pyplot(fig5)

    # Data Integrity Section in Expander
    with st.expander("Data Integrity Check"):
        st.subheader("Data Integrity Metrics")
        missing_values = df.isnull().sum().sum()
        duplicate_records = df.duplicated().sum()
        invalid_costs = (df["Cost"] < 0).sum()
        invalid_stay = (df["Length_of_Stay"] < 0).sum()
        total_issues = missing_values + duplicate_records + invalid_costs + invalid_stay
        data_accuracy = ((df.shape[0] - total_issues) / df.shape[0]) * 100 if df.shape[0] > 0 else 0

        st.write(f"Missing Values: {missing_values}")
        st.write(f"Duplicate Records: {duplicate_records}")
        st.write(f"Invalid Costs: {invalid_costs}")
        st.write(f"Invalid Length of Stay: {invalid_stay}")
        st.write(f"Data Accuracy: {data_accuracy:.2f}%")

if __name__ == "__main__":
   import os

file_path = "hospital data analysis.csv"

# Check if file exists (useful for Streamlit Cloud)
if not os.path.exists(file_path):
    st.error("Dataset not found! Please upload the correct CSV file.")
else:
    df = load_data(file_path)
    analyze_hospital_data(df)
