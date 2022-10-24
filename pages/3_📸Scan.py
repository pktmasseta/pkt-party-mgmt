import cv2
import numpy as np
import streamlit as st
from util import *

if check_password():
    df = sheet.get_df()
    image = st.camera_input("Show QR code")
    # image = st.file_uploader("Show QR Code")

    if image is not None:
        bytes_data = image.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        detector = cv2.QRCodeDetector()

        data, bbox, straight_qrcode = detector.detectAndDecode(cv2_img)

        if df['Unique ID'].str.contains(data).any() and data != "":
            st.success("You're on the list!")
        else:
            st.error("You're not in!")