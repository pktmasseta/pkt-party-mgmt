
import streamlit as st
import uuid
import qrcode
from util import *
import os


SPREADSHEET = "https://docs.google.com/spreadsheets/d/1ACCF2-38_0ybYCbSbJzDTO5BX6cHDZIxDEWPLO9F7b8/edit?usp=sharing"


template_path = os.path.join(os.path.dirname(__file__), "template.png")
st.write(template_path)

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

        from PIL import Image, ImageDraw, ImageFilter
        import os

        template = Image.open(template_path)
        qr = Image.open(f'{uid}.png')
        width, height = qr.size
        os.remove(f'{uid}.png')

        template.paste(qr.resize((width * 2, height * 2)), (180, 300))
        st.image(template)


        new_row = {"Initials": initials, "Name": name, "PlusOnes": int(plus_ones), "Checked In": 0, "Unique ID": uid}
        df2 = df.append(new_row, ignore_index=True)
        st.write(df2)
        sheet.write_df(df2)

        st.info(f"If you messed up and want to edit the spreadsheet, click [here]({sheet.url}).")