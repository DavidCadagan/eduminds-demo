import streamlit as st
import hashlib
import hmac
import time

# --- STREAMLIT UI SETUP ---
st.set_page_config(page_title="EduMinds Middleware Engine", layout="wide")

st.title("🧠 EduMinds: B2B Behavioral Telemetry & Health-Routing Infrastructure")
st.subheader("Closed-Loop RVO Compliance & Middleware Demonstration Sandbox")

st.markdown("""
This functional prototype demonstrates how our core architecture sits invisibly between a university's **LMS (Canvas / Brightspace)** and its **Student Well-Being Infrastructure**, executing a strict cryptographic privacy wall to enforce GDPR/AVG Article 9 and SURF compliance.
""")

# --- SESSION STATE ---
if "peer_requested" not in st.session_state:
    st.session_state.peer_requested = False
if "decaan_notified" not in st.session_state:
    st.session_state.decaan_notified = False
if "pomo_running" not in st.session_state:
    st.session_state.pomo_running = False
if "pomo_seconds_left" not in st.session_state:
    st.session_state.pomo_seconds_left = 300
if "pomo_total_seconds" not in st.session_state:
    st.session_state.pomo_total_seconds = 300
if "pomo_completed" not in st.session_state:
    st.session_state.pomo_completed = False
if "show_grounding" not in st.session_state:
    st.session_state.show_grounding = False
if "show_distraction_nudge" not in st.session_state:
    st.session_state.show_distraction_nudge = False

# --- SIDEBAR: LIVE THRESHOLD CONTROLS ---
st.sidebar.header("⚙️ Algorithmic Controller Settings")
st.sidebar.caption("Calibrate institutional sensitivity live during a demo without altering core engine code.")
VELOCITY_THRESHOLD = st.sidebar.slider("Activity Velocity Drop Threshold (%)", 10, 95, 70) / 100.0
ASSIGNMENT_THRESHOLD = st.sidebar.slider("Overdue Assignments Threshold", 1, 5, 2)
LATE_NIGHT_THRESHOLD = st.sidebar.slider("Late-Night Login Anomaly Threshold", 1, 10, 4)

st.sidebar.divider()
force_preview = st.sidebar.checkbox("👁️ Always show Student LTI Widget Preview", value=True)
demo_fast_clock = st.sidebar.checkbox("⏩ Fast-Forward Pomodoro Clock (10x for Live Demo)", value=True)

# --- STEP 1: INGESTION ENGINE ---
st.header("1. Ingestion Layer (IMS Caliper & LTI 1.3 Webhook Streams)")
st.caption("Simulating real-time student activity tracking events ingested from Canvas / Brightspace and Osiris SIS.")

mock_students = {
    "Student B (High Stress - Triggers Loop)": {
        "real_student_id": "UT_STUDENT_89324",
        "name": "Jan Janssen",
        "velocity_drop": 0.78,
        "overdue_assignments": 3,
        "late_night_logins": 6
    },
    "Student A (Normal Baseline)": {
        "real_student_id": "UT_STUDENT_48291",
        "name": "Alex de Jong",
        "velocity_drop": 0.15,
        "overdue_assignments": 0,
        "late_night_logins": 1
    },
    "Student C (Mild Academic Friction)": {
        "real_student_id": "UT_STUDENT_11029",
        "name": "Emma Bakker",
        "velocity_drop": 0.45,
        "overdue_assignments": 1,
        "late_night_logins": 2
    },
    "Custom Sandbox Student (Adjust Live)": {
        "real_student_id": "UT_STUDENT_99402",
        "name": "Sanne Visser",
        "velocity_drop": 0.50,
        "overdue_assignments": 2,
        "late_night_logins": 4
    }
}

selected_profile = st.selectbox("Select an incoming student telemetry stream to test:", list(mock_students.keys()))
data = mock_students[selected_profile].copy()

if selected_profile == "Custom Sandbox Student (Adjust Live)":
    st.info("🎚️ **Live Pitch Mode:** Adjust this student's incoming telemetry below to test boundary conditions.")
    c1, c2, c3 = st.columns(3)
    data["velocity_drop"] = c1.slider("Simulated Velocity Drop (%)", 0, 100, 50) / 100.0
    data["overdue_assignments"] = c2.number_input("Simulated Overdue Assignments", 0, 10, 2)
    data["late_night_logins"] = c3.number_input("Simulated Late-Night Logins", 0, 14, 4)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Raw Institutional ID", data["real_student_id"])
col2.metric("LMS Activity Velocity Drop", f"{int(data['velocity_drop'] * 100)}%")
col3.metric("Overdue Assignments", data["overdue_assignments"])
col4.metric("Nocturnal Session Flags (01:00–05:30)", data["late_night_logins"])

# --- STEP 2: PRIVACY WALL ---
st.header("2. Security Layer (GDPR/AVG Article 9 & SURF Compliance Privacy Wall)")
st.caption("Stripping institutional identifiers via institution-held HMAC-SHA256 cryptographic hashing before behavioral scoring.")

institution_kms_key = b"UniversityOfTwente_HSM_SecretKey_2026"
hashed_token = hmac.new(
    institution_kms_key,
    data["real_student_id"].encode("utf-8"),
    hashlib.sha256
).hexdigest()

st.warning(f"🔒 **Privacy Enforcement Protocol Active:** Raw ID `{data['real_student_id']}` purged from processing memory prior to analytics.")
st.info(f"**Generated Zero-Knowledge Telemetry Token (HMAC-SHA256):** `{hashed_token}`")

# --- STEP 3: ALGORITHMIC CONTROLLER ---
st.header("3. Processing Layer (Deterministic Closed-Loop Controller)")
st.caption(
    f"Evaluating individualized baseline drift against calibrated thresholds "
    f"(≥{int(VELOCITY_THRESHOLD * 100)}% velocity drop & ≥{ASSIGNMENT_THRESHOLD} overdue assignments, "
    f"or ≥{LATE_NIGHT_THRESHOLD} nocturnal session flags)."
)

is_breached = (
    (data["velocity_drop"] >= VELOCITY_THRESHOLD and data["overdue_assignments"] >= ASSIGNMENT_THRESHOLD)
    or data["late_night_logins"] >= LATE_NIGHT_THRESHOLD
)

if is_breached:
    st.error("🚨 **THRESHOLD BREACHED:** Behavioral drift indicates elevated executive-function strain. Triggering low-friction support loop.")
else:
    st.success("✅ **STABLE BASELINE:** Behavioral telemetry remains within normal student margins. Zero alerts generated.")

# --- STEP 4: INTERVENTION ENGINE ---
st.header("4. Delivery Edge (Zero-Install LTI 1.3 Side-Panel & Clinical Routing)")
st.caption("Replacing passive university directories with immediate micro-scaffolding and unidirectional health routing.")

if is_breached or force_preview:
    left_col, right_col = st.columns([1.25, 1])

    with left_col:
        st.subheader("🎓 Student-Facing Canvas LTI 1.3 Drawer")
        st.caption(f"Rendered natively inside Canvas LMS for {data['name']} — zero separate apps or logins required.")

        with st.container(border=True):
            first_name = data["name"].split()
            st.markdown("#### 🌿 EduMinds Study Companion • *Quick Reset*")
            st.write(f"Hi **{first_name}**, we noticed your study rhythm slowed down this week. Let's break the overwhelm into one tiny, doable step.")

            tab1, tab2, tab3 = st.tabs(["2️⃣ Live CBT Pomodoro", "1️⃣ 60s CBT Reframe", "3️⃣ Low-Friction Support"])

            # TAB 1: LIVE CBT POMODORO WIDGET
            with tab1:
                sprint_map = {
                    "5-Min Starter Sprint (Low Friction)": 300,
                    "15-Min Momentum Block": 900,
                    "25-Min Classic Pomodoro": 1500
                }
                selected_sprint = st.select_slider(
                    "1. Choose an executive-function-friendly sprint:",
                    options=list(sprint_map.keys()),
                    value="5-Min Starter Sprint (Low Friction)",
                    disabled=st.session_state.pomo_running
                )

                if not st.session_state.pomo_running and not st.session_state.pomo_completed:
                    if st.session_state.pomo_total_seconds != sprint_map[selected_sprint]:
                        st.session_state.pomo_total_seconds = sprint_map[selected_sprint]
                        st.session_state.pomo_seconds_left = sprint_map[selected_sprint]

                micro_goal = st.text_input(
                    "2. Define ONE tiny micro-goal (no perfectionism):",
                    value="Open assignment PDF & write 3 rough bullet points",
                    disabled=st.session_state.pomo_running
                )

                if st.button("🫁 10s Somatic Calm Reset (Before Starting)", use_container_width=True):
                    st.session_state.show_grounding = not st.session_state.show_grounding

                if st.session_state.show_grounding:
                    st.info("🌬️ **Vagal Down-Regulation:** Inhale slowly for **4 seconds**... Hold **2 seconds**... Exhale gently for **6 seconds**.")

                st.divider()

                mins, secs = divmod(st.session_state.pomo_seconds_left, 60)
                progress_ratio = 1.0 - (st.session_state.pomo_seconds_left / max(1, st.session_state.pomo_total_seconds))

                t_col1, t_col2 = st.columns([1, 1.5])
                t_col1.metric(
                    label="Active Focus Timer",
                    value=f"{mins:02d}:{secs:02d}",
                    delta="Running" if st.session_state.pomo_running else ("Done!" if st.session_state.pomo_completed else "Ready")
                )
                t_col2.write(f"**Current Anchor:** *{micro_goal}*")
                t_col2.progress(min(1.0, max(0.0, progress_ratio)))

                ctrl1, ctrl2, ctrl3 = st.columns(3)
                start_label = "⏸️ Pause" if st.session_state.pomo_running else "▶️ Start Sprint"
                if ctrl1.button(start_label, type="primary", use_container_width=True):
                    st.session_state.pomo_running = not st.session_state.pomo_running
                    if st.session_state.pomo_running:
                        st.session_state.pomo_completed = False
                    st.rerun()

                if ctrl2.button("🔄 Reset", use_container_width=True):
                    st.session_state.pomo_running = False
                    st.session_state.pomo_completed = False
                    st.session_state.pomo_seconds_left = sprint_map[selected_sprint]
                    st.session_state.pomo_total_seconds = sprint_map[selected_sprint]
                    st.session_state.show_distraction_nudge = False
                    st.rerun()

