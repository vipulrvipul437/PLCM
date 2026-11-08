import streamlit as st
import pandas as pd
import re

# Set page config
st.set_page_config(page_title="Veda eScoot X1 PLM Agent", page_icon="🛵", layout="centered")

st.title("🛵 Veda eScoot X1 - PLM AI Agent")
st.write("Ask natural language questions about scooter components, ECRs, testing, and maintenance.")

@st.cache_data
def load_data():
    # Load all relevant sheets from the Excel file
    excel_path = "Veda_eScoot_X1_Data.xlsx" 
    try:
        xls = pd.ExcelFile(excel_path)
        sheets = {sheet_name: pd.read_excel(xls, sheet_name) for sheet_name in xls.sheet_names}
        return sheets
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None

data = load_data()

def answer_question(query, data):
    if not data:
        return "Dataset non loaded. Please make sure 'Veda_eScoot_X1_Data.xlsx' is present."
    
    query_lower = query.lower()
    
    # Question 1: Battery capacity
    if "battery" in query_lower and ("capacity" in query_lower or "spec" in query_lower or "what is" in query_lower):
        # Look in Components or Requirements
        for sheet_name, df in data.items():
            df_str = df.astype(str)
            match = df_str[df_str.apply(lambda row: row.str.contains("battery", case=False).any(), axis=1)]
            if not match.empty:
                return f"**Battery Specifications Found:**\n\n" + match.to_markdown(index=False)
        return "Battery specifications could not be found in the dataset."

    # Question 2: Major components
    elif "major component" in query_lower or "list components" in query_lower or "all components" in query_lower:
        for sheet_name in data.keys():
            if "component" in sheet_name.lower():
                return f"**Scooter Components List ({sheet_name}):**\n\n" + data[sheet_name].head(10).to_markdown(index=False)
        return "Component information found across sheets:\n" + ", ".join(data.keys())

    # Question 3: Open engineering changes
    elif "open" in query_lower and ("change" in query_lower or "ecr" in query_lower):
        for sheet_name, df in data.items():
            df_str = df.astype(str)
            open_ecrs = df[df_str.apply(lambda row: row.str.contains("open", case=False).any(), axis=1)]
            if not open_ecrs.empty:
                return f"**Currently Open Engineering Changes:**\n\n" + open_ecrs.to_markdown(index=False)
        return "No open engineering change requests (ECRs) found in the dataset."

    # Question 4 & 5: Specific ECR query (e.g., ECR-001)
    elif "ecr-" in query_lower or "ecr" in query_lower:
        ecr_match = re.search(r'ecr[-\s]?\d+', query_lower)
        ecr_id = ecr_match.group(0).upper().replace(" ", "-") if ecr_match else "ECR"
        
        results = []
        for sheet_name, df in data.items():
            df_str = df.astype(str)
            matched = df[df_str.apply(lambda row: row.str.contains(ecr_id, case=False).any(), axis=1)]
            if not matched.empty:
                results.append(f"**From Sheet '{sheet_name}':**\n" + matched.to_markdown(index=False))
        
        if results:
            return f"### Information for {ecr_id}\n\n" + "\n\n".join(results)
        return f"No records found for {ecr_id} across dataset sheets."

    # Question 6: Maintenance / Service actions
    elif "maintenance" in query_lower or "service" in query_lower or "braking" in query_lower or "brake" in query_lower:
        for sheet_name, df in data.items():
            if any(k in sheet_name.lower() for k in ["maint", "service", "brake", "component"]):
                df_str = df.astype(str)
                brake_records = df[df_str.apply(lambda row: row.str.contains("brake|braking|maintenance", case=False, regex=True).any(), axis=1)]
                if not brake_records.empty:
                    return f"**Maintenance & Service Information ({sheet_name}):**\n\n" + brake_records.to_markdown(index=False)
        return "No specific maintenance actions found for the specified component."

    # General Fallback Keyword Search
    else:
        results = []
        words = [w for w in query_lower.split() if len(w) > 3]
        for sheet_name, df in data.items():
            df_str = df.astype(str)
            for word in words:
                matched = df[df_str.apply(lambda row: row.str.contains(word, case=False).any(), axis=1)]
                if not matched.empty:
                    results.append(f"**Matches in '{sheet_name}' for '{word}':**\n" + matched.head(3).to_markdown(index=False))
                    break
        if results:
            return "Here are the relevant records found matching your query:\n\n" + "\n\n".join(results)
        return "I couldn't find specific information for your query in the dataset. Please try rephrasing or asking about components, ECRs, validation tests, or maintenance records."

# User Input
user_query = st.text_input("Enter your question about the Veda eScoot X1:", placeholder="e.g., What validation tests are required for ECR-001?")

if st.button("Submit Question") or user_query:
    if user_query.strip():
        with st.spinner("Analyzing PLM dataset..."):
            ans = answer_question(user_query, data)
            st.markdown(ans)
    else:
        st.warning("Please enter a question.")
