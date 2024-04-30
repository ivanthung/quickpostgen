import json
import streamlit as st
from utils.firebase_storage import UserDataFirebase
from streamlit_float  import float_init

st.set_page_config(page_title="Metabolic - Quick case study review tool", layout="wide")
st.title("Metabolic - Quick case study review tool")

session = st.session_state
float_init()

if "data" not in session:
    session.database = UserDataFirebase()
    session.data = session.database.download_json("Metabolic cases loc.json")

col1, col2 = st.columns([1, 5])
col1.float()
def save_data(data):
    with col1:
        with st.spinner("Saving changes..."):
            session.database.upload_json("Metabolic cases loc.json", data)

# Streamlit UI Layout
def app():
    save_button = col1.empty()

    # Define the source2 substrings for filtering
    filter_options = ["SOTA", "Arup", "EMF", "WGBC", "WBCSD", "ce-toolkit.dhub.arup.com"]
    selected_filter = st.sidebar.selectbox("Filter by source2", ["All"] + filter_options)


    # Function to filter keys based on selected source2 substring
    def filter_keys_by_source2(selected_filter):
        if selected_filter == "All":
            return list(session.data.keys())
        else:
            return [key for key in session.data if selected_filter in session.data[key]['source2']]


    filtered_keys = filter_keys_by_source2(selected_filter)

    # Sidebar for selecting title from filtered keys
    selected_title_key = st.sidebar.radio("Select a Title", filtered_keys, format_func=lambda x: session.data[x]['title'])

    # Display editable fields in the main area
    if selected_title_key:
        item = session.data[selected_title_key]
        fields = {field: col2.text_area(field.capitalize(), value=str(item[field]), key=str(item['id'])+str(field)) for field in item if
                  field not in ['id', 'framework_elements', 'locations']}

        if save_button.button("Save Changes"):
            # Update the data with new values
            for field in fields:
                session.data[selected_title_key][field] = fields[field].strip()

            save_data(session.data)
            col1.success("Changes saved successfully!")

    json_str = json.dumps(session.data, indent=2)
    col1.download_button(
        label="Download JSON Data",
        data=json_str,
        file_name="Metabolic_cases_loc.json",
        mime="application/json"
    )

if __name__ == '__main__':
    app()