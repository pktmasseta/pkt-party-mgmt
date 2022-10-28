import streamlit as st
import gspread
import pandas as pd

password = st.secrets["PASSWORD"]

class Sheet:
    def __init__(self, ):
        self.initted = False

    def initialize(self):
        if not self.initted:
            self.url = "https://docs.google.com/spreadsheets/d/1ACCF2-38_0ybYCbSbJzDTO5BX6cHDZIxDEWPLO9F7b8/edit#gid=0"
            gc = gspread.service_account(filename="phi-kappa-theta-d7541d27ff30.json")
            sh = gc.open_by_url(self.url)
            self.worksheet = sh.sheet1
            self.initted = True

    def get_df(self):
        self.initialize()
        return pd.DataFrame(self.worksheet.get_all_records())

    def write_df(self, df):
        self.initialize()
        self.worksheet.update([df.columns.values.tolist()] + df.values.tolist())

sheet = Sheet()

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == password:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        return True