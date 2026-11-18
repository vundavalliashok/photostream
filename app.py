
import streamlit as st
import streamlit.components.v1 as components
import base64
import json

st.set_page_config(
    page_title="PhotoStream",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("📸 PhotoStream")

    st.markdown("---")

    st.subheader("📤 Upload Photos")

    uploaded_files = st.file_uploader(
        "Choose multiple pictures",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True,
        key="photo_upload"
    )

    st.markdown("---")

    st.subheader("⚙️ Slideshow Settings")

    duration = st.slider(
        "Picture duration (seconds)",
        min_value=1,
        max_value=20,
        value=4
    )

    autoplay = st.toggle(
        "Auto Play",
        value=True
    )

    loop = st.toggle(
        "Repeat Slideshow",
        value=True
    )

    st.markdown("---")

    if uploaded_files:
        st.success(
            f"{len(uploaded_files)} photos uploaded"
        )

        with st.expander("Uploaded pictures"):
            for index, file in enumerate(uploaded_files):
                st.caption(f"{index + 1}. {file.name}")

    else:
        st.info("Upload pictures to start the slideshow.")

# ---------------- MAIN WINDOW ----------------

if uploaded_files:

    pictures = []

    for file in uploaded_files:

        encoded = base64.b64encode(
            file.getvalue()
        ).decode("utf-8")

        pictures.append({
            "name": file.name,
            "src": f"data:{file.type};base64,{encoded}"
        })

    pictures_json = json.dumps(pictures)

    player_html = """
    <!DOCTYPE html>
    <html>
    <head>

    <style>

    * {
        box-sizing: border-box;
    }

    body {
        margin: 0;
        padding: 10px;
        background: transparent;
        color: white;
        font-family: Arial, sans-serif;
    }

    .container {
        width: 100%;
        text-align: center;
    }

    .photo-area {
        width: 100%;
        height: 70vh;
        min-height: 350px;
        max-height: 650px;
        background: #111827;
        border-radius: 14px;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
    }

    #photo {
        width: 100%;
        height: 100%;
        object-fit: contain;
    }

    #caption {
        font-size: 18px;
        margin-top: 15px;
        font-weight: bold;
    }

    #counter {
        color: #9ca3af;
        margin-top: 8px;
        font-size: 14px;
    }

    .controls {
        margin-top: 22px;
        display: flex;
        justify-content: center;
        gap: 15px;
    }

    button {
        background: #2563eb;
        color: white;
        border: none;
        border-radius: 9px;
        padding: 12px 22px;
        cursor: pointer;
        font-size: 15px;
    }

    button:hover {
        background: #1d4ed8;
    }

    @media(max-width: 600px) {
        .photo-area {
            height: 55vh;
            min-height: 250px;
        }

        button {
            padding: 10px 13px;
        }
    }

    </style>

    </head>

    <body>

    <div class="container">

        <div class="photo-area">
            <img id="photo" alt="Slideshow image">
        </div>

        <div id="caption"></div>

        <div id="counter"></div>

        <div class="controls">

            <button onclick="previous()">
                ⏮ Previous
            </button>

            <button id="playButton" onclick="togglePlay()">
                ⏸ Pause
            </button>

            <button onclick="next()">
                Next ⏭
            </button>

        </div>

    </div>

    <script>

        const pictures = __PICTURES_JSON__;
        const delay = __DELAY__ * 1000;
        const autoplay = __AUTOPLAY__;
        const loop = __LOOP__;

        let current = 0;
        let playing = autoplay;
        let timer = null;

        function display() {

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

            if (current > 0) {
                current--;
            } else if (loop) {
                current = pictures.length - 1;
            }

            display();
            startTimer();
        }

        function togglePlay() {

            playing = !playing;

            display();
            startTimer();
        }

        function startTimer() {

            clearInterval(timer);

            if (playing) {

                timer = setInterval(function() {

                    if (
                        current === pictures.length - 1
                        && !loop
                    ) {

                        playing = false;

                        clearInterval(timer);

                        display();

                        return;
                    }

                    current = (current + 1) % pictures.length;

                    display();

                }, delay);
            }
        }

        display();
        startTimer();

    </script>

    </body>
    </html>
    """

    player_html = (
        player_html
        .replace("__PICTURES_JSON__", pictures_json)
        .replace("__DELAY__", str(duration))
        .replace("__AUTOPLAY__", json.dumps(autoplay))
        .replace("__LOOP__", json.dumps(loop))
    )

    components.html(
        player_html,
        height=850,
        scrolling=False
    )

else:

    st.markdown(
        """
        <div style="
            height:75vh;
            display:flex;
            align-items:center;
            justify-content:center;
            text-align:center;
            color:gray;
        ">
            <div>
                <h1>📸 PhotoStream</h1>
                <h3>Your slideshow awaits</h3>
                <p>Upload pictures using the left sidebar.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
