
import os
import uuid

import qrcode
import streamlit as st
from util import *

SPREADSHEET = "https://docs.google.com/spreadsheets/d/1ACCF2-38_0ybYCbSbJzDTO5BX6cHDZIxDEWPLO9F7b8/edit?usp=sharing"


template_path = os.path.join(os.path.dirname(__file__), "template.jpeg")
font_path = os.path.join(os.path.dirname(__file__), "arial.ttf")

if check_password():
    st.title("PKT Invite Site")
    df = sheet.get_df()

    f"""
**Current Total Invite Count:** {df["PlusOnes"].sum() + len(df) - 1}
"""

    initials = st.text_input("Initials")
    name = st.text_input("Name of Invite")
    plus_ones = st.number_input("Plus Ones", min_value=0, max_value=5)
    generate = st.button("Generate")



    if generate:
        uid = str(uuid.uuid4())
        img = qrcode.make(uid)
        img.save(f"{uid}.png")

        import os

        from PIL import Image, ImageDraw, ImageFont


        template = Image.open(template_path)
        qr = Image.open(f'{uid}.png')
        width, height = qr.size
        os.remove(f'{uid}.png')

        font = ImageFont.truetype(font_path, 48)
        scale = 0.8
        template.paste(qr.resize((round(width * scale), round(height * scale))), (290, 800))
        draw = ImageDraw.Draw(template)
        draw.text((0, 0), f"{initials} - {name}" + ( f" + {plus_ones} plus ones" if plus_ones > 0 else ""),  fill=(0, 0, 0), stroke_fill=(255, 255, 255), stroke_width=3, font=font)

        st.image(template)

        new_row = {"Initials": initials, "Name": name, "PlusOnes": int(plus_ones), "Checked In": 0, "Unique ID": uid}
        df2 = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        st.write(df2)
        sheet.write_df(df2)

        st.info(f"If you messed up and want to edit the spreadsheet, click [here]({sheet.url}).")