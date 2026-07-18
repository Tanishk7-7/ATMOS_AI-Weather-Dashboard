import streamlit as st
import plotly.express as px
from back import get_data
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from datetime import datetime
import os


load_dotenv()

api = os.getenv("GROQ_API_KEY")

model = init_chat_model(
    model="llama-3.1-8b-instant",
    model_provider="groq",
    api_key=api
)


st.set_page_config(
    page_title="Atmos | Live Weather Intelligence",
    page_icon="⛅",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
        :root {
            --surface: #1d2422;
            --surface-2: #252e2b;
            --border: rgba(220, 225, 214, 0.12);
            --muted: #aab4ad;
            --text: #f3f1eb;
            --blue: #90aa99;
        }
        .stApp {
            background:
                radial-gradient(circle at 92% 0%, rgba(124, 150, 128, 0.13), transparent 27%),
                radial-gradient(circle at 4% 46%, rgba(180, 150, 103, 0.08), transparent 24%),
                #161a19;
            color: var(--text);
        }
        #MainMenu, footer, header { visibility: hidden; }
        .block-container { max-width: 1440px; padding: 2.15rem 3rem 4rem; }
        [data-testid="stSidebar"] {
            background: rgba(28, 34, 32, 0.97);
            border-right: 1px solid var(--border);
        }
        [data-testid="stSidebar"] > div:first-child { padding-top: 1.8rem; }
        .brand { display:flex; align-items:center; gap:.65rem; font-weight:700; font-size:1.2rem; margin:.25rem 0 2rem; }
        .brand-mark { display:grid; place-items:center; width:35px; height:35px; border-radius:12px; background:#708b78; box-shadow:0 8px 20px rgba(28,37,32,.28); }
        .side-label { font-size:.74rem; font-weight:700; letter-spacing:.11em; color:#9ba69e; margin:1.7rem 0 .6rem; }
        .topbar { display:flex; justify-content:space-between; align-items:center; margin:0 0 2rem; }
        .topbar-title { font-size:1.85rem; font-weight:700; letter-spacing:-.045em; margin:0; }
        .topbar-copy { color:var(--muted); margin:.28rem 0 0; }
        .live-pill { display:inline-flex; align-items:center; gap:.45rem; background:rgba(123, 151, 129, .14); color:#c9dccb; border:1px solid rgba(145,172,150,.24); padding:.42rem .72rem; border-radius:999px; font-size:.78rem; font-weight:600; }
        .live-dot { width:7px; height:7px; border-radius:50%; background:#9fbe9c; box-shadow:0 0 8px rgba(159,190,156,.45); }
        .hero { border:1px solid rgba(216,221,209,.14); border-radius:26px; padding:2rem; background:linear-gradient(120deg,rgba(83,105,91,.38),rgba(46,57,53,.56) 57%,rgba(31,38,35,.8)); box-shadow:0 22px 60px rgba(0,0,0,.17); margin-bottom:1.35rem; }
        .hero-kicker { font-size:.73rem; font-weight:700; letter-spacing:.11em; color:#c9d9c9; }
        .hero h1 { font-size:2.35rem; line-height:1.1; letter-spacing:-.055em; margin:.65rem 0 .65rem; }
        .hero p { color:#d5dbd1; max-width:630px; margin:0; font-size:1.02rem; }
        .weather-card { min-height:300px; color:#f8f6ef; border-radius:23px; padding:1.65rem 1.75rem; background:linear-gradient(140deg,#566c60,#3d5149 58%,#293630); box-shadow:0 22px 52px rgba(18,24,21,.26); }
        .weather-heading { display:flex; justify-content:space-between; gap:1rem; align-items:flex-start; }
        .weather-heading h2 { font-size:1.22rem; margin:0; }
        .weather-heading p { margin:.25rem 0 0; color:rgba(255,255,255,.76); font-size:.84rem; }
        .weather-reading { display:flex; gap:1rem; align-items:center; margin:2rem 0 1.3rem; }
        .weather-icon { font-size:3.45rem; line-height:1; }
        .weather-temperature { font-size:4.4rem; line-height:.85; font-weight:700; letter-spacing:-.08em; }
        .weather-description { font-size:1rem; color:rgba(255,255,255,.9); }
        .weather-footer { display:flex; gap:1.65rem; flex-wrap:wrap; margin-top:1.35rem; }
        .weather-footer span { display:block; color:rgba(255,255,255,.68); font-size:.74rem; margin-bottom:.15rem; }
        .weather-footer strong { font-weight:600; }
        .section-card { background:rgba(34,42,39,.9); border:1px solid var(--border); border-radius:22px; padding:1.5rem; height:100%; }
        .section-title { font-weight:700; font-size:1.05rem; margin:0 0 .3rem; }
        .section-copy { color:var(--muted); font-size:.85rem; margin:0 0 1.25rem; }
        .metric-box { background:rgba(38,47,43,.88); border:1px solid var(--border); border-radius:16px; padding:1.05rem 1.15rem; min-height:115px; }
        .metric-icon { font-size:1.08rem; }
        .metric-label { color:#b4beb5; font-size:.79rem; margin:.42rem 0; }
        .metric-value { font-weight:700; font-size:1.48rem; letter-spacing:-.04em; }
        .metric-note { color:#8f9c91; font-size:.75rem; margin-top:.38rem; }
        .insight-card { background:linear-gradient(135deg,rgba(93,117,95,.23),rgba(65,76,68,.35)); border:1px solid rgba(152,174,151,.2); border-radius:22px; padding:1.45rem; }
        .insight-card h2 { font-size:1.12rem; margin:0 0 .35rem; }
        .insight-card p { color:#c0c9be; margin:0 0 1rem; font-size:.9rem; }
        .forecast-card { background:rgba(34,42,39,.9); border:1px solid var(--border); border-radius:22px; padding:1.5rem; margin-top:1.35rem; }
        .forecast-card h2 { margin:0; font-size:1.15rem; }
        .forecast-card p { color:var(--muted); font-size:.84rem; margin:.35rem 0 1rem; }
        .sky-card { background:rgba(38,47,43,.88); border:1px solid var(--border); border-radius:18px; padding:1rem; text-align:center; min-height:205px; }
        .sky-temp { font-size:1.45rem; font-weight:700; margin:.35rem 0 .2rem; }
        .sky-condition { color:#d0d7cc; font-size:.86rem; font-weight:600; }
        .sky-time { color:#9da99f; font-size:.75rem; margin-top:.45rem; }
        [data-testid="stTextInput"] input, [data-testid="stSelectbox"] div[data-baseweb="select"] > div, [data-testid="stSlider"] div[role="slider"] {
            border-radius:11px !important;
        }
        [data-testid="stTextInput"] input, [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            background:#29332f !important; border:1px solid rgba(215,223,209,.16) !important; color:#f3f1eb !important;
        }
        [data-testid="stTextInput"] label, [data-testid="stSlider"] label, [data-testid="stSelectbox"] label { color:#d0d7cc !important; font-weight:600 !important; font-size:.87rem !important; }
        .stButton > button { background:#738d79; color:#f7f5ee; border:0; border-radius:11px; font-weight:700; min-height:43px; box-shadow:0 10px 22px rgba(19,27,23,.24); }
        .stButton > button:hover { border:0; color:#f7f5ee; filter:brightness(1.08); }
        [data-testid="stPlotlyChart"] { border-radius:15px; overflow:hidden; }
        .stAlert { border-radius:13px; }
        .stDivider { border-color:var(--border); }
        @media (max-width: 750px) { .block-container { padding:1.2rem 1rem 2.5rem; } .hero { padding:1.4rem; } .hero h1 { font-size:1.85rem; } .weather-temperature { font-size:3.6rem; } }
    </style>
    """,
    unsafe_allow_html=True,
)


def weather_emoji(condition):
    return {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Snow": "❄️",
        "Thunderstorm": "⛈️",
        "Drizzle": "🌦️",
        "Mist": "🌫️",
    }.get(condition, "⛅")


def metric_card(icon, label, value, note):
    st.markdown(
        f'''<div class="metric-box">
            <div class="metric-icon">{icon}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>''',
        unsafe_allow_html=True,
    )


with st.sidebar:
    st.markdown('<div class="brand"><span class="brand-mark">⛅</span> Atmos</div>', unsafe_allow_html=True)
    st.markdown('<div class="side-label">LOCATION</div>', unsafe_allow_html=True)
    place = st.text_input(
        "City search",
        placeholder="Jaipur, London, New York...",
        label_visibility="visible",
    )
    st.markdown('<div class="side-label">FORECAST RANGE</div>', unsafe_allow_html=True)
    days = st.slider(
        "Forecast days",
        min_value=1,
        max_value=5,
        value=3,
        help="Select the number of forecAast days",
    )
    st.markdown('<div class="side-label">INFO</div>', unsafe_allow_html=True)
    st.caption("Search a city to explore live weather.")


st.markdown(
    '''<div class="topbar">
        <div><h1 class="topbar-title">Atmospheric Intel</h1><p class="topbar-copy">Live conditions and thoughtful planning guidance, all in one place.</p></div>
        <div class="live-pill"><span class="live-dot"></span> Live data</div>
    </div>''',
    unsafe_allow_html=True,
)

if not place:
    st.markdown(
        '''<section class="hero">
            <div class="hero-kicker">CLIMATE OVERVIEW</div>
            <h1>Actionable weather data at your fingertips.</h1>
            <p>Search for any city from the sidebar to explore current conditions, interactive forecasts, a visual sky timeline, and AI-powered weather advice.</p>
        </section>''',
        unsafe_allow_html=True,
    )
    st.markdown(
            """
            <div style="
                background-color: rgba(213, 228, 205, 0.05); 
                border: 1px dashed rgba(220, 225, 214, 0.2); 
                padding: 1rem 1.25rem; 
                border-radius: 12px; 
                color: #aab4ad; 
                font-size: 0.9rem;
            ">
                ✨ Enter a city in the sidebar to start your weather briefing.
            </div>
            """, 
            unsafe_allow_html=True
        )
else:
    try:
        filtered_data, info = get_data(place, days)

        current_time = datetime.now().strftime("%d %b %Y · %I:%M %p")
        current = st.container()

        st.markdown(f"### {place.title()}\n<small style='color:#aab4ad'>Updated {current_time} • {info['condition']} • Feels like {info['feels_like']:.1f}°C</small>", unsafe_allow_html=True)

        with current:
            st.markdown(
                f'''<section class="weather-card">
                    <div class="weather-heading"><div><h2>{place.title()}</h2><p>{info['condition']} · {info['description'].title()}</p></div><span>Now</span></div>
                    <div class="weather-reading"><span class="weather-icon">{weather_emoji(info['condition'])}</span><span class="weather-temperature">{info['temp']:.1f}°</span></div>
                    <div class="weather-description">Feels like {info['feels_like']:.1f}°C · {info['description'].title()}</div>
                    <div class="weather-footer"><div><span>Humidity</span><strong>{info['humidity']}%</strong></div><div><span>Wind</span><strong>{info['wind_speed']:.1f} m/s</strong></div><div><span>Rain chance</span><strong>{info['rain_probability']:.0f}%</strong></div></div>
                </section>''',
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height:1.35rem'></div>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">Today’s conditions</div><p class="section-copy">A detailed view of the current observation from OpenWeather.</p>', unsafe_allow_html=True)

        metrics = st.columns(6, gap="small")
        metric_data = [
            ("🌡️", "Temperature", f"{info['temp']:.1f} °C", "Current reading"),
            ("🥵", "Feels like", f"{info['feels_like']:.1f} °C", "Perceived temperature"),
            ("💧", "Humidity", f"{info['humidity']}%", "Moisture in the air"),
            ("🌬️", "Wind speed", f"{info['wind_speed']:.1f} m/s", "Current breeze"),
            ("☁️", "Cloud cover", f"{info['clouds']}%", "Sky coverage"),
            ("👁️", "Visibility", f"{info['visibility']/1000:.1f} km", "Viewing distance"),
        ]
        for column, values in zip(metrics, metric_data):
            with column:
                metric_card(*values)

        prompt = f"""
You are a professional weather assistant.

Based on the following weather information, generate a concise and user-friendly weather summary.

Current Weather:
- City: {place.title()}
- Temperature: {info['temp']}°C
- Feels Like: {info['feels_like']}°C
- Humidity: {info['humidity']}%
- Wind Speed: {info['wind_speed']} m/s
- Cloud Cover: {info['clouds']}%
- Visibility: {info['visibility']/1000:.1f} km
- Weather: {info['condition']}
- Description: {info['description']}
- Chance of Rain: {info['rain_probability']}%

Instructions:
- Write in 4-6 sentences.
- Explain how the weather feels.
- Mention whether it is suitable for outdoor activities.
- Mention if the user should carry an umbrella, sunscreen, or a jacket if appropriate.
- Use a friendly and natural tone.
- Do not mention that you are an AI.
- Do not repeat the raw values unnecessarily.
"""

        st.markdown("<div style='height:1.35rem'></div>", unsafe_allow_html=True)
        st.markdown('<section class="insight-card"><h2>✨ Smart weather insight</h2><p>Get a practical, human-friendly weather briefing based on the live conditions above.</p></section>', unsafe_allow_html=True)
        if st.button("Analyze today’s weather", use_container_width=True):
            with st.spinner("Preparing your weather briefing..."):
                response = model.invoke(prompt)
                st.info(response.content)

        st.markdown('<section class="forecast-card">', unsafe_allow_html=True)
        temp_tab, sky_tab = st.tabs(["🌡 Temperature","☁ Sky"])

        with temp_tab:
            temp = [forecast["main"]["temp"] for forecast in filtered_data]
            dates = [forecast["dt_txt"] for forecast in filtered_data]

            figure = px.line(
                x=dates,
                y=temp,
                markers=True,
                labels={"x": "Date & time", "y": "Temperature (°C)"},
            )
            figure.update_traces(
                line={"color": "#a8c49f", "width": 3},
                marker={"size": 7, "color": "#d5e4cd", "line": {"color": "#27322d", "width": 2}},
                fill="tozeroy",
                fillcolor="rgba(151, 184, 145, 0.14)",
            )
            figure.update_layout(
                title=f"Temperature forecast · {place.title()}",
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(244, 244, 232, 0.025)",
                font={"color": "#e1e5da"},
                title_font={"size": 18},
                margin={"l": 10, "r": 10, "t": 58, "b": 10},
                xaxis={"gridcolor": "rgba(216,224,210,0.10)", "showline": False},
                yaxis={"gridcolor": "rgba(216,224,210,0.10)", "zeroline": False},
            )
            st.plotly_chart(figure, use_container_width=True)
        with sky_tab:
            st.markdown(f"<h2>Sky forecast · {place.title()}</h2><p>Weather conditions at three-hour intervals.</p>", unsafe_allow_html=True)
            
            images = {
                    "Clear": "images/clear.png",
                    "Clouds": "images/cloud.png",
                    "Rain": "images/rain.png",
                    "Snow": "images/snow.png",
                }

            for i in range(0, len(filtered_data), 4):

                cols = st.columns(4, gap="small")

                for col, forecast in zip(cols, filtered_data[i:i+4]):

                    condition = forecast["weather"][0]["main"]

                    image_path = images.get(condition, "images/cloud.png")

                    temperature = forecast["main"]["temp"]

                    forecast_date, forecast_time = forecast["dt_txt"].split(" ")

                    with col:

                        with st.container(border=True):

                            st.image(image_path, width=60)

                            st.markdown(f"### {temperature:.1f}°C")

                            st.markdown(f"**{condition}**")

                            st.caption(forecast_time[:5])

                            st.caption(forecast_date)
                                    

    except Exception:
        st.error("City not found. Please check the spelling and try again.")


st.markdown("---")
st.caption("Powered by OpenWeather • Groq • LangChain • Streamlit")
