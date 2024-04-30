import streamlit as st
st.title("Case Study Review Tool")
st.markdown("""

We have collected a number of case studies from your studies, reports and collections.
The purpose now is to review these case studies to see if they are correct and if we can use them.
Instructions:
- In the left sidebar, filter on your organisation.
- In the sidebar, select a case study to review.
- In the main area, you can edit the case study.
- If you are happy with the changes, press the "Save Changes" button before selecting another case study.
""")
st.page_link("pages/1_Edit case studies.py", label="Go to review tool", icon="🏠")

