
import streamlit as st
import uuid
import qrcode
from util import *

SPREADSHEET = "https://docs.google.com/spreadsheets/d/1ACCF2-38_0ybYCbSbJzDTO5BX6cHDZIxDEWPLO9F7b8/edit?usp=sharing"

if check_password():
    st.title("PKT Invite Site")
    df = sheet.get_df()

    f"""
**Current Total Invite Count:** {df["PlusOnes"].sum() + len(df)}
"""

    initials = st.text_input("Initials")
    name = st.text_input("Name of Invite")
    plus_ones = st.number_input("Plus Ones", min_value=0, max_value=10)
    generate = st.button("Generate")



    if generate:
        uid = uuid.uuid4()
        img = qrcode.make(uid)
        img.save(f"{uid}.png")
        st.image(f"{uid}.png")

        new_row = {"Initials": initials, "Name": name, "PlusOnes": int(plus_ones), "Checked In": 0, "Unique ID": uid}
        df2 = df.append(new_row, ignore_index=True)
        st.write(df2)
        sheet.write_df(df2)

        st.info(f"If you messed up and want to edit the spreadsheet, click [here]({sheet.url}).")