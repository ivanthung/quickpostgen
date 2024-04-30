import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage
import json

class UserDataFirebase:
    def __init__(self):
        firebase_credentials = st.secrets["firebase_service_account"].to_dict()
        self.cred = credentials.Certificate(firebase_credentials)

        try:
            self.app = firebase_admin.get_app()
        except ValueError:
            self.app = firebase_admin.initialize_app(
                self.cred,
                {
                    "storageBucket": "streamlit-various.appspot.com",
                    "databaseURL": "https://streamlit-various.firebaseio.com",
                },
            )
        self.store = firestore.client()

    def download_json(self, file_path):
        """Download a JSON file from Firebase Storage."""
        bucket = storage.bucket(app=self.app)
        blob = bucket.blob(file_path)
        json_data = json.loads(blob.download_as_text())
        return json_data

    def upload_json(self, file_path, data):
        """Upload a dictionary as a JSON file to Firebase Storage."""
        bucket = storage.bucket(app=self.app)
        blob = bucket.blob(file_path)
        blob.upload_from_string(
            data=json.dumps(data, indent=4),
            content_type='application/json'
        )
        print(f"Data uploaded to {file_path} successfully.")

# Usage example
if __name__ == "__main__":
    database = UserDataFirebase()
    # Download JSON
    json_data = database.download_json("Metabolic cases loc.json")
    database.upload_json("Metabolic cases loc.json", json_data)