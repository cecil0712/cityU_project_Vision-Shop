import streamlit as st
import os
from PIL import Image
from route_planning import get_route, get_map
from database_connect import check_discount, check_exist, get_item_coor, get_region_coor, get_item_list
from text_detection import OCR
from speech import speak_item, play_audio

def main():
    st.set_page_config(page_title="Vision ∞ Shop")
    st.header("Vision ∞ Shop: The Navigation App")

    if "used_images" not in st.session_state:
        st.session_state.used_images = []

    uploaded_image = st.file_uploader(label="Upload/Update Image", type=["png", "jpg", "jpeg"])

    # Store uploaded image into the image list
    if uploaded_image is not None:
        st.image(uploaded_image, use_container_width=True)
        if uploaded_image not in st.session_state.used_images:
            st.session_state.used_images.append(uploaded_image)

    # Display previously used images
    with st.expander("Previously Uploaded Images"):
        if st.session_state.used_images:

            for i in range(0, len(st.session_state.used_images), 3):
                columns = st.columns(3, border=True, vertical_alignment="bottom")
                
                for col_idx, column in enumerate(columns):
                    if i + col_idx < len(st.session_state.used_images):
                        image = st.session_state.used_images[i + col_idx]
                        column.image(image, use_container_width=True, caption=f"Image {i + col_idx + 1}")

    # Button to start navigation
    if st.button("Start Navigation"):
        if uploaded_image is None:
            st.error("Please upload an image first.")
        else:
            # Write uploaded file to a temporary path so OCR can access it
            temp_path = "temp_uploaded_image.jpg"
            with open(temp_path, "wb") as f:
                f.write(uploaded_image.getbuffer())

            start_navigation(temp_path)

def start_navigation(img_path):

    # Initializing an expander to store the logs
    expander = st.expander("Execution Log")

    expander.write("Starting navigation...")

    map = get_map()
    expander.write("Map obtained")

    text = speak_item(get_item_list())
    expander.write(f"Text obtained: {text}")

    if check_discount(text):
        play_audio('audio/discount.wave')

    destination = get_item_coor(text)
    expander.write(f"Destination coordinates: {destination}")

    play_audio('audio/directing.wav')

    current_brand = check_exist(OCR(img_path))
    if current_brand is None:
        st.error("OCR failed to detect text in the image.")
        raise ValueError("OCR failed to detect text in the image.")

    expander.write(f"Current brand: {current_brand}")

    start = get_region_coor(current_brand)
    if start is None:
        st.error(f"Start coordinates for brand {current_brand} not found.")
        raise ValueError(f"Start coordinates for brand {current_brand} not found.")

    expander.write(f"Start coordinates: {start}")

    route = get_route(start, destination)
    expander.write(f"Planned route: {route}")

    current_coor = start
    route_num = 0

    while current_coor != route[-1]:
        get_direction(route[route_num], route[route_num + 1], expander)

        # Confirming the brand
        expander.write("Re-checking brand via OCR...")
        new_brand = check_exist(OCR(img_path))
        if new_brand is None:
            st.error("OCR failed to detect text in the image.")
            raise ValueError("OCR failed to detect text in the image.")
        expander.write(f"Current brand after OCR check: {new_brand}")

        # Convert brand to coordinates
        current_coor = get_region_coor(new_brand)
        expander.write(f"Current coordinates: {current_coor}")

        # Compare location with expected route segment
        if current_coor == route[route_num + 1]:
            route_num += 1
        elif current_coor not in [route[route_num], route[route_num + 1]]:
            play_audio("audio/redirecting.wav")
            route = get_route(current_coor, destination)
            route_num = 0

    # Arrived
    play_audio("audio/arrive.wav")
    expander.write("Arrived at destination.")

def get_direction(start, end, expander):
    delta_row = end[0] - start[0]
    delta_col = end[1] - start[1]

    if delta_row == 1 and delta_col == 0:
        play_audio("./audio/foward.wav")
        expander.write("Moving Forward")
    elif delta_row == -1 and delta_col == 0:
        play_audio("./audio/backward.wav")
        expander.write("Moving Backward")
    elif delta_row == 0 and delta_col == 1:
        play_audio("./audio/right.wav")
        expander.write("Turning Right")
    elif delta_row == 0 and delta_col == -1:
        play_audio("./audio/left.wav")
        expander.write("Turning Left")
        
if __name__ == '__main__':
    main()