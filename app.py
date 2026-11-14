
import streamlit as st
import streamlit.components.v1 as components
import base64
import json
import io
from PIL import Image

st.set_page_config(
    page_title="PhotoStream",
    page_icon="📸",
    layout="wide"
)

st.title("📸 PhotoStream")
st.subheader("Your personal photo slideshow")

st.write(
    "Upload your favourite pictures and enjoy them "
    "as an automatic slideshow."
)

# Sidebar settings
st.sidebar.header("Slideshow Settings")

duration = st.sidebar.slider(
    "Time per picture (seconds)",
    min_value=1,
    max_value=20,
    value=4
)

autoplay = st.sidebar.checkbox(
    "Start slideshow automatically",
    value=True
)

loop = st.sidebar.checkbox(
    "Repeat slideshow",
    value=True
)

# Upload pictures
st.header("Upload your pictures")

uploaded_files = st.file_uploader(
    "Select multiple pictures",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True
)

if uploaded_files:
    # Validate actual image files before embedding them in the slideshow.
    pictures = []
    rejected_files = []

    for file in uploaded_files:
        image_bytes = file.getvalue()

        try:
            with Image.open(io.BytesIO(image_bytes)) as image:
                image.verify()
        except Exception:
            rejected_files.append(file.name)
            continue

        encoded = base64.b64encode(image_bytes).decode("utf-8")
        mime = file.type or "image/jpeg"

        pictures.append({
            "name": file.name,
            "src": f"data:{mime};base64,{encoded}"
        })

    if rejected_files:
        st.warning(
            "Skipped invalid image files: "
            + ", ".join(rejected_files)
            + ". Please upload valid JPG, PNG, or WEBP images."
        )

    if not pictures:
        st.error("No valid images were uploaded. Please try again with valid picture files.")
        st.stop()

    st.success(f"{len(pictures)} valid pictures uploaded!")

    st.header("Your Photo Gallery")

    # Thumbnail gallery
    columns = st.columns(4)

    for index, picture in enumerate(pictures):
        with columns[index % 4]:
            st.image(
                picture["src"],
                caption=picture["name"],
                use_container_width=True
            )

    st.divider()
    st.header("▶ Photo Slideshow")

    # Pass uploaded photos to the browser player
    pictures_json = json.dumps(pictures)

    player_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #111827;
            color: white;
            text-align: center;
        }

        .player {
            padding: 15px;
        }

        #photo {
            width: 100%;
            height: 430px;
            object-fit: contain;
            border-radius: 10px;
            background: #000;
        }

        #caption {
            padding: 12px;
            font-size: 16px;
        }

        button {
            padding: 11px 18px;
            margin: 5px;
            border: none;
            border-radius: 7px;
            cursor: pointer;
            background: #2563eb;
            color: white;
            font-size: 14px;
        }

        button:hover {
            background: #1d4ed8;
        }

        #counter {
            margin: 12px;
            color: #d1d5db;
        }
    </style>
    </head>

    <body>
    <div class="player">
        <img id="photo" src="" alt="Slideshow picture">
        <div id="caption"></div>
        <div id="counter"></div>

        <button onclick="previous()">⏮ Previous</button>
        <button id="playButton" onclick="togglePlay()">⏸ Pause</button>
        <button onclick="next()">Next ⏭</button>
    </div>

    <script>
        const pictures = PICTURES || [];
        const delay = DELAY * 1000;
        const autoplay = AUTOPLAY;
        const loop = LOOP;

        let current = 0;
        let playing = autoplay;
        let timer = null;

        function display() {
            if (!pictures.length) {
                return;
            }

            document.getElementById("photo").src =
                pictures[current].src;

            document.getElementById("caption").textContent =
                pictures[current].name;

            document.getElementById("counter").textContent =
                "Picture " + (current + 1) +
                " of " + pictures.length;

            document.getElementById("playButton").textContent =
                playing ? "⏸ Pause" : "▶ Play";
        }

        function next() {
            if (!pictures.length) {
                return;
            }

            if (current < pictures.length - 1) {
                current++;
            } else if (loop) {
                current = 0;
            } else {
                playing = false;
            }

            display();
            startTimer();
        }

        function previous() {
            if (!pictures.length) {
                return;
            }

            current = (current - 1 + pictures.length)
                % pictures.length;

            display();
            startTimer();
        }

        function togglePlay() {
            if (!pictures.length) {
                return;
            }

            playing = !playing;
            display();
            startTimer();
        }

        function startTimer() {
            clearInterval(timer);

            if (!pictures.length || !playing) {
                return;
            }

            timer = setInterval(() => {
                if (current === pictures.length - 1 && !loop) {
                    playing = false;
                    clearInterval(timer);
                    display();
                    return;
                }

                current = (current + 1) % pictures.length;
                display();
            }, delay);
        }

        display();
        startTimer();
    </script>
    </body>
    </html>
    """

    # Insert settings and uploaded pictures
    player_html = (
        player_html
        .replace("PICTURES", pictures_json)
        .replace("DELAY", str(duration))
        .replace("AUTOPLAY", str(json.dumps(autoplay)))
        .replace("LOOP", str(json.dumps(loop)))
    )

    components.html(
        player_html,
        height=560,
        scrolling=False
    )

else:
    st.info(
        "Please upload multiple pictures to start "
        "your PhotoStream slideshow."
    )

st.divider()

st.caption("PhotoStream | Built with Python and Streamlit")
