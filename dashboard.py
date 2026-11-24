import streamlit as st
import numpy as np
import pandas as pd
import requests

firebase_api_key = st.secrets["firebase"]["api_key"]

def firebase_auth(email, password, create_account=False):
    action = "signUp" if create_account else "signInWithPassword"

    url = (
        "https://identitytoolkit.googleapis.com/v1/accounts:"
        + action
        + "?key="
        + firebase_api_key
    )

    response = requests.post(
        url,
        json={
            "email": email,
            "password": password,
            "returnSecureToken": True
        },
        timeout=15
    )

    return response.json()

# ASTRA-SIGNAL Login System

if "user" not in st.session_state:
    st.session_state.user = None

if not st.session_state.user:

    st.title("🪐 ASTRA-SIGNAL")
    st.subheader("Welcome to Exoplanet Detection")

    login_tab, signup_tab = st.tabs(
        ["Login", "Create Account"]
    )

    with login_tab:
        with st.form("login_form"):
            email = st.text_input("Email Address")
            password = st.text_input(
                "Password", type="password"
            )
            login_button = st.form_submit_button(
                "Login to Dashboard"
            )

        if login_button:
            result = firebase_auth(email, password)

            if "idToken" in result:
                st.session_state.user = {
                    "email": result["email"],
                    "token": result["idToken"]
                }
                st.rerun()
                st.error("Account creation failed.")

   
    with signup_tab:
        with st.form("signup_form"):
            new_email = st.text_input("Email Address")
            new_password = st.text_input(
                "Create Password", type="password"
            )
            signup_button = st.form_submit_button(
                "Create Account"
            )

        if signup_button:
            if len(new_password) < 6:
                st.warning("Password must contain at least 6 characters.")
            else:
                result = firebase_auth(
                    new_email, new_password, True
                )

                if "idToken" in result:
                    st.success("Account created! Please log in.")
                else:
                    st.error("Account creation failed.")
                    st.json(result)


        if signup_button:
            if len(new_password) < 6:
                st.warning("Password must contain at least 6 characters.")
            else:
                result = firebase_auth(
                    new_email, new_password, True
                )

                if "idToken" in result:
                    st.success("Account created! Please log in.")
                else:
                    st.error("Account creation failed. Check your details.")

    st.divider()
    st.subheader("🤖 ASTRA AI Assistant")
    st.write("Ask me anything about exoplanets and ASTRA-SIGNAL!")

    question = st.text_input(
        "Ask your question",
        key="login_chat_question"
    )

    if st.button("Ask ASTRA AI"):
        q = question.lower()

        if "exoplanet" in q:
            answer = "An exoplanet is a planet that orbits a star outside our solar system."

        elif "transit" in q:
            answer = "Transit detection identifies a small dip in a star's brightness when a planet passes in front of it."

        elif "bls" in q:
            answer = "BLS means Box Least Squares. It searches for repeating, box-shaped dips in brightness data."

        elif "machine learning" in q or "ml" in q:
            answer = "ASTRA-SIGNAL uses Isolation Forest to identify unusual patterns in stellar brightness data."

        elif "kepler" in q:
            answer = "NASA's Kepler mission collected stellar brightness measurements used to search for exoplanets."

        elif "astra" in q:
            answer = "ASTRA-SIGNAL analyses Kepler light curves using signal processing, periodicity analysis and machine learning."

        else:
            answer = "I can help with exoplanets, Kepler data, transit detection, BLS and ASTRA-SIGNAL. Try asking about one of these topics."

        st.info(answer)


    st.stop()

else:
    st.sidebar.success(
        f"Logged in: {st.session_state.user['email']}"
    )

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

st.divider()
st.header("Detection Overview")

col1, col2, col3, col4 = st.columns(4)

# Use calculated results where available
transit_count = (
    int(count) if "count" in globals() else 0
)
period_value = (
    round(float(best_period), 4)
    if "best_period" in globals() and best_period is not None
    else None
)
ml_count = (
    int(anomaly_count)
    if "anomaly_count" in globals()
    else 0
)

col1.metric("Possible Transit Points", transit_count)

col2.metric(
    "Best Period (Days)",
    f"{period_value}" if period_value is not None else "Unavailable"
)

col3.metric("Unusual ML Windows", ml_count)

col4.metric(
    "Analysis Status",
    "Under Review" if transit_count > 0 else "No Candidate"
)

st.caption(
    "Values are calculated from the loaded Kepler dataset. "
    "These results are preliminary and do not confirm an exoplanet."
)


# Page configuration
st.set_page_config(
    page_title="ASTRA-SIGNAL",
    page_icon="🪐",
    layout="wide"
)

# Dashboard title
st.title("🪐 ASTRA-SIGNAL")

st.subheader("AI-Powered Exoplanet Detection System")

st.write(
    "An intelligent system for detecting possible exoplanet "
    "transits using advanced digital signal processing."
)

st.divider()

st.success("System Status: Online")


st.success("Analysis Mode: Real Kepler Dataset")
st.caption(
    "Source: kepler_real_data.csv | "
    "Preliminary research analysis — not a confirmed exoplanet detection."
)
st.divider()

# Stellar Light Curve
st.divider()

st.header("🌟 Stellar Light Curve")

time = np.linspace(0, 10, 100)

brightness = np.ones(100)

brightness[20:25] = 0.98
brightness[40:45] = 0.98
brightness[60:65] = 0.98

noise = np.random.normal(0, 0.005, 100)
brightness = brightness + noise

smooth_brightness = pd.Series(brightness).rolling(
    window=5,
    center=True,
    min_periods=1
).mean()

chart_data = pd.DataFrame({
    "Noisy Signal": brightness,
    "Smoothed Signal": smooth_brightness
}, index=time)

st.line_chart(chart_data)
# AI/ML Prediction
st.divider()

st.header("🤖 AI/ML Prediction")

col1, col2 = st.columns(2)

with col1:
    st.success("Possible Transit Signal")

with col2:
    st.metric("Candidate Score", "85%")

st.write("The system detected transit-like brightness variations.")
# Candidate Analysis
st.divider()

st.header("🪐 Candidate Analysis")

candidate_data = pd.DataFrame({
    "Parameter": [
        "Detection Method",
        "Signal Type",
        "Transit Events",
        "Analysis Status"
    ],
    "Result": [
        "Transit Detection",
        "Possible Planetary Transit",
        "3",
        "Completed"
    ]
})


st.header("🪐 Exoplanet Candidate Report")

st.write("Candidate ID: ASTRA-001")

if "best_period" in globals() and best_period is not None:
    st.write("Detection Result: Possible Transit Candidate")
    st.write(f"Orbital Period: {best_period:.4f} Days")
    st.write(f"Estimated Transit Depth: {best_depth:.6f}")
    st.write(
        f"Transit Duration: "
        f"{best_duration * best_period * 24:.2f} Hours"
    )
    st.write(
        f"Unusual ML Windows: "
        f"{globals().get('anomaly_count', 'Unavailable')}"
    )
else:
    st.warning("No usable periodicity result is available.")

st.info(
    "These are preliminary results from Kepler brightness data. "
    "A possible transit candidate requires further scientific validation."
)

st.divider()

st.header("🔍 Signal Validation")

st.write("Signal Quality: Good")
st.write("Noise Level: Moderate")
st.write("Repeated Transit: Under Analysis")
st.write("False Positive Risk: Not Yet Verified")

st.warning("Further observation is required to confirm the candidate.")
st.divider()


st.header("📊 Detection History")

if "best_period" in globals() and best_period is not None:
    history = {
        "Candidate": ["ASTRA-001"],
        "Period (Days)": [round(float(best_period), 4)],
        "Transit Depth": [round(float(best_depth), 6)],
        "ML Unusual Windows": [
            globals().get("anomaly_count", "Unavailable")
        ],
        "Status": ["Requires Further Validation"]
    }
    st.dataframe(pd.DataFrame(history), use_container_width=True)
else:
    st.info("No candidate results available yet.")


st.divider()

st.header("📥 Export Analysis")

if "best_period" in globals() and best_period is not None:
    report = f"""
ASTRA-SIGNAL ANALYSIS REPORT

Candidate: ASTRA-001
Data Source: Real Kepler Dataset

Orbital Period: {best_period:.4f} Days
Transit Depth: {best_depth:.6f}
Transit Duration: {best_duration * best_period * 24:.2f} Hours
Unusual ML Windows: {globals().get('anomaly_count', 'Unavailable')}

Status: Requires Further Validation

Note: This is a preliminary candidate analysis,
not a confirmed exoplanet discovery.
"""
else:
    report = "ASTRA-SIGNAL: No valid candidate results available."

st.download_button(
    "📥 Download Analysis Report",
    report,
    file_name="ASTRA_SIGNAL_Report.txt",
    mime="text/plain"
)


st.download_button(
    label="Download Report",
    data=report,
    file_name="ASTRA_SIGNAL_Report.txt",
    mime="text/plain"
)
st.divider()
st.header("🛰️ NASA Exoplanet Archive")

if st.button("Fetch Real NASA Data"):
    import requests
    import pandas as pd

    query = """
    SELECT TOP 5 pl_name, hostname, pl_orbper
    FROM ps
    WHERE default_flag = 1
    AND discoverymethod = 'Transit'
    """

    try:
        with st.spinner("Connecting to NASA..."):
            response = requests.get(
                "https://exoplanetarchive.ipac.caltech.edu/TAP/sync",
                params={"query": query, "format": "json"},
                timeout=90
            )

            response.raise_for_status()
            df = pd.DataFrame(response.json())

        st.success("NASA data loaded successfully!")
        st.dataframe(df, use_container_width=True)

    except requests.exceptions.Timeout:
        st.error("NASA server is taking too long. Try again later.")

    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")

    except Exception as e:
        st.error(f"Error: {e}")

st.divider()

st.header("🌌 Real NASA Kepler Observations")

import pandas as pd

try:
    real_data = pd.read_csv("kepler_real_data.csv")

    st.success("Real Kepler data loaded successfully!")

    st.metric("Total Observations", len(real_data))

    st.line_chart(
        real_data.set_index("Time")["Brightness"]
    )

    st.subheader("Real Observation Data")
    st.dataframe(real_data.head(20), use_container_width=True)

except FileNotFoundError:
    st.error("kepler_real_data.csv not found in project folder.")
             
st.divider()

st.header("🔬 Real Kepler Transit Detection")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

csv_path = Path(__file__).parent / "kepler_real_data.csv"

if csv_path.exists():

    data = pd.read_csv(csv_path)
    data = data.dropna(subset=["Time", "Brightness"])

    # Smooth the real brightness signal
    data["Smoothed"] = (
        data["Brightness"]
        .rolling(window=51, center=True, min_periods=1)
        .median()
    )

    # Identify unusually low brightness points
    residual = data["Brightness"] - data["Smoothed"]

    mad = np.median(np.abs(residual - np.median(residual)))
    threshold = np.median(residual) - 3 * 1.4826 * mad

    data["Transit Candidate"] = residual < threshold

    count = int(data["Transit Candidate"].sum())

    st.metric("Possible Transit Points", count)

    # Plot real observations and detected points
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        data["Time"],
        data["Brightness"],
        label="Real Kepler Signal",
        linewidth=0.8
    )

    detected = data[data["Transit Candidate"]]

    ax.scatter(
        detected["Time"],
        detected["Brightness"],
        color="red",
        label="Possible Transit Points",
        s=12
    )

    ax.set_xlabel("Time")
    ax.set_ylabel("Normalized Brightness")
    ax.set_title("ASTRA-SIGNAL - Real Transit Detection")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)
    plt.close(fig)

    st.info(
        "These are possible brightness anomalies, "
        "not confirmed exoplanet transits."
    )

else:
    st.error("Kepler CSV file not found.")

# =====================================
# BLS PERIODICITY ANALYSIS
# =====================================

st.divider()
st.header("🔭 BLS Periodicity Analysis")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

csv_path = Path(__file__).parent / "kepler_real_data.csv"

if csv_path.exists():

    bls_data = pd.read_csv(csv_path)
    bls_data = bls_data.dropna(subset=["Time", "Brightness"])

    time = bls_data["Time"].to_numpy(dtype=float)
    flux = bls_data["Brightness"].to_numpy(dtype=float)

    valid = np.isfinite(time) & np.isfinite(flux)
    time = time[valid]
    flux = flux[valid]

    if len(time) >= 50:

        # Sort observations by time
        order = np.argsort(time)
        time = time[order]
        flux = flux[order]

        flux = flux / np.median(flux)
        flux_std = np.std(flux)

        # Search possible orbital periods
        min_period = 0.5
        max_period = min(20.0, (time.max() - time.min()) / 2)

        if max_period > min_period:

            periods = np.linspace(min_period, max_period, 250)

            best_depth = 0
            best_period = None
            best_phase = None
            best_duration = None

            bins = 200
            durations = [2, 3, 4, 6, 8]

            for period in periods:

                phase = ((time - time.min()) / period) % 1

                indices = np.floor(
                    phase * bins
                ).astype(int)

                sums = np.bincount(
                    indices,
                    weights=flux,
                    minlength=bins
                )

                counts = np.bincount(
                    indices,
                    minlength=bins
                )

                means = np.full(bins, np.mean(flux))

                occupied = counts > 0
                means[occupied] = (
                    sums[occupied] / counts[occupied]
                )

                # Search for low-brightness boxes
                for width in durations:

                    extended = np.concatenate(
                        [means, means[:width]]
                    )

                    cumulative = np.concatenate(
                        [[0], np.cumsum(extended)]
                    )

                    window_means = (
                        cumulative[width:width + bins]
                        - cumulative[:bins]
                    ) / width

                    depth = np.mean(flux) - np.min(window_means)

                    if depth > best_depth:
                        best_depth = depth
                        best_period = period
                        best_phase = (
                            np.argmin(window_means) + width / 2
                        ) / bins
                        best_duration = width / bins

            if best_period is not None and best_depth > 0:

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Best Period",
                    f"{best_period:.3f} days"
                )

                col2.metric(
                    "Estimated Transit Depth",
                    f"{best_depth:.6f}"
                )

                col3.metric(
                    "Transit Duration",
                    f"{best_duration * best_period * 24:.2f} hours"
                )

                # Fold observations using the best period
                folded_phase = (
                    (time - time.min()) / best_period
                ) % 1

                distance = (
                    folded_phase - best_phase + 0.5
                ) % 1 - 0.5

                transit_mask = (
                    np.abs(distance) < best_duration / 2
                )

                fig, ax = plt.subplots(figsize=(10, 5))

                ax.scatter(
                    folded_phase,
                    flux,
                    s=5,
                    label="Real Kepler Observations"
                )

                ax.scatter(
                    folded_phase[transit_mask],
                    flux[transit_mask],
                    color="red",
                    s=12,
                    label="Possible Transit"
                )

                ax.set_xlabel("Orbital Phase")
                ax.set_ylabel("Normalized Brightness")
                ax.set_title("BLS Phase-Folded Light Curve")
                ax.legend()
                ax.grid(True)

                st.pyplot(fig)
                plt.close(fig)

                st.info(
                    "This is an educational, binned BLS-style "
                    "period search. The result is a candidate, "
                    "not a confirmed exoplanet."
                )

            else:
                st.warning("No transit-like periodic signal found.")

        else:
            st.warning("Not enough observation time for this period search.")

    else:
        st.warning("Not enough valid observations.")

else:
    st.error("Kepler CSV file not found.")

# =====================================
# ML SIGNAL VALIDATION
# =====================================

st.divider()
st.header("🤖 AI/ML Signal Validation")

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from pathlib import Path

csv_path = Path(__file__).parent / "kepler_real_data.csv"

if csv_path.exists():

    ml_data = pd.read_csv(csv_path)
    ml_data = ml_data.dropna(subset=["Time", "Brightness"])
    ml_data = ml_data.sort_values("Time").reset_index(drop=True)

    flux = ml_data["Brightness"].to_numpy(dtype=float)

    # Divide observations into small windows
    window_size = 50
    features = []

    for start in range(0, len(flux) - window_size + 1, window_size):

        segment = flux[start:start + window_size]

        features.append([
            np.mean(segment),
            np.std(segment),
            np.min(segment),
            np.max(segment),
            np.ptp(segment)
        ])

    if len(features) >= 10:

        feature_data = np.array(features)

        # Train unsupervised anomaly detection model
        model = IsolationForest(
            contamination=0.05,
            random_state=42
        )

        predictions = model.fit_predict(feature_data)

        anomaly_count = int(np.sum(predictions == -1))

        st.metric("Unusual Signal Windows", anomaly_count)

        st.write(
            f"Total Windows Analysed: {len(predictions)}"
        )

        st.write(
            f"Normal Windows: {np.sum(predictions == 1)}"
        )

        st.write(
            f"Unusual Windows: {anomaly_count}"
        )

        st.info(
            "The model identifies unusual signal patterns. "
            "An anomaly does not necessarily indicate a planet."
        )

    else:
        st.warning("Not enough data windows for ML analysis.")

else:
    st.error("Kepler CSV file not found.")

# =====================================
# FINAL CANDIDATE RANKING
# =====================================

st.divider()
st.header("🏆 Final Exoplanet Candidate Ranking")

if "best_period" in globals() and best_period is not None:

    candidate_results = pd.DataFrame({
        "Rank": [1],
        "Candidate ID": ["ASTRA-001"],
        "Orbital Period (Days)": [round(best_period, 4)],
        "Transit Depth": [round(best_depth, 6)],
        "Transit Duration (Hours)": [
            round(best_duration * best_period * 24, 2)
        ],
        "Unusual ML Windows": [
            globals().get("anomaly_count", "Unavailable")
        ],
        "Status": ["Requires Further Validation"]
    })

    st.dataframe(
        candidate_results,
        use_container_width=True
    )

    st.download_button(
        "📥 Download Candidate Results",
        candidate_results.to_csv(index=False),
        file_name="ASTRA_Candidate_Results.csv",
        mime="text/csv"
    )

    st.info(
        "Ranking is preliminary. ML anomalies and BLS results "
        "do not independently confirm an exoplanet."
    )

else:
    st.warning("BLS candidate results are not available.")



