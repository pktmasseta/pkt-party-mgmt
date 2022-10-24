
import streamlit as st
import uuid
import qrcode
from util import *
import os


SPREADSHEET = "https://docs.google.com/spreadsheets/d/1ACCF2-38_0ybYCbSbJzDTO5BX6cHDZIxDEWPLO9F7b8/edit?usp=sharing"


template_path = os.path.join(os.path.dirname(__file__), "template.jpg")
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
        uid = uuid.uuid4()
        img = qrcode.make(uid)
        img.save(f"{uid}.png")

        from PIL import Image, ImageFont, ImageDraw
        import os



        template = Image.open(template_path)
        qr = Image.open(f'{uid}.png')
        width, height = qr.size
        os.remove(f'{uid}.png')

        font = ImageFont.truetype(font_path, 24)
        scale = 0.5
        template.paste(qr.resize((round(width * scale), round(height * scale))), (220, 450))
        draw = ImageDraw.Draw(template)
        draw.text((80, 840), f"{initials} - {name}" + ( f" + {plus_ones} plus ones" if plus_ones > 0 else ""),  fill=(255, 255, 255), font=font)

        st.image(template)

        new_row = {"Initials": initials, "Name": name, "PlusOnes": int(plus_ones), "Checked In": 0, "Unique ID": uid}
        df2 = df.append(new_row, ignore_index=True)
        st.write(df2)
        sheet.write_df(df2)

        st.info(f"If you messed up and want to edit the spreadsheet, click [here]({sheet.url}).")