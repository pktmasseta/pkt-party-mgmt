import cv2
import numpy as np
import streamlit as st
from util import *

df = sheet.get_df()
image = st.camera_input("Show QR code")

if image is not None:
    bytes_data = image.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    detector = cv2.QRCodeDetector()

    data, bbox, straight_qrcode = detector.detectAndDecode(cv2_img)


    if df['Unique ID'].str.contains(data).any() and data != "":
        inv = df.loc[df['Unique ID'] == data].iloc[0]

        if inv['Checked In'] == 0:
            st.success(f"{inv['Name']} + {inv['PlusOnes']} by {inv['Initials']} checked in for first time!")
        else:
            st.warning(f"{inv['Name']} + {inv['PlusOnes']} by {inv['Initials']} checked in for #{inv['Checked In'] +1} time!")
    else:
        st.error("You're not in!")


    df2 = df.copy()
    df2.loc[df2['Unique ID'] == data, 'Checked In'] += 1

    sheet.write_df(df2)