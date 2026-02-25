import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import smtplib
from email.message import EmailMessage

# ---------------- EMAIL FUNCTION ----------------
def send_email(pred):
    try:
        msg = EmailMessage()
        msg.set_content(f"Alert! Predicted cloud cost spike: ₹{pred}")
        msg["Subject"] = "Cloud Cost Alert"
        msg["From"] = "YOUR_EMAIL@gmail.com"
        msg["To"] = "RECEIVER_EMAIL@gmail.com"

        server = smtplib.SMTP_SSL("smtp.gmail.com",465)
        server.login("YOUR_EMAIL@gmail.com","YOUR_APP_PASSWORD")
        server.send_message(msg)
        server.quit()
    except:
        pass

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI FinOps Assistant", page_icon="☁️", layout="wide")

# ---------------- STYLISH THEME ----------------
st.markdown("""
<style>
body {background-color:#F4F8FB;}
h1,h2,h3 {color:#2C73D2;}
[data-testid="stMetricValue"] {color:#00C897;font-weight:bold;}
.stButton>button {background:#2C73D2;color:white;border-radius:10px;}
.stDownloadButton>button {background:#00C897;color:white;border-radius:10px;}
</style>
""", unsafe_allow_html=True)

# ---------------- LOGO ----------------
try:
    st.image("logo.png", width=120)
except:
    pass

# ---------------- TITLE ----------------
st.markdown("<h1 style='text-align:center;'>☁️ AI FinOps Assistant Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Smart Cloud Cost Monitoring & Prediction</p>", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.header("Upload Billing CSV")
file = st.sidebar.file_uploader("Upload file", type=["csv"])

# ---------------- MAIN ----------------
if file:

    df = pd.read_csv(file)

    st.subheader("📄 Billing Data")
    st.write(df)

    # -------- METRICS --------
    col1,col2,col3 = st.columns(3)
    col1.metric("Total Spend", f"₹{df['Cost'].sum()}")
    col2.metric("Average Cost", f"₹{int(df['Cost'].mean())}")
    col3.metric("Last Month", f"₹{df['Cost'].iloc[-1]}")

    st.divider()

    # -------- GRAPH --------
    st.subheader("📊 Spending Trend")

    fig, ax = plt.subplots()
    ax.plot(df["Month"], df["Cost"], marker="o")
    ax.set_xlabel("Month")
    ax.set_ylabel("Cost")
    ax.set_title("Monthly Cloud Cost")
    st.pyplot(fig)

    # -------- ML PREDICTION --------
    st.subheader("🤖 AI Cost Prediction")

    X = np.arange(len(df)).reshape(-1,1)
    y = df["Cost"].values

    model = LinearRegression()
    model.fit(X,y)

    next_month = np.array([[len(df)]])
    prediction = int(model.predict(next_month)[0])

    st.success(f"Predicted next month cost: ₹{prediction}")

    # -------- ALERT --------
    if prediction > y[-1]*1.25:
        st.error("⚠️ Cost spike expected! Check unused servers/storage.")
        # send_email(prediction)   # enable if email configured
    else:
        st.info("✅ Cost stable.")

    # -------- DOWNLOAD --------
    st.subheader("⬇ Download Report")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "report.csv", "text/csv")

    # -------- CHATBOT --------
    st.subheader("💬 Ask FinOps Assistant")

    question = st.text_input("Example: why cost high? how reduce cost?")

    if question:
        q = question.lower()

        if "high" in q or "spike" in q:
            st.write("Cost may be high due to unused servers, increased traffic, or large storage usage.")
        elif "reduce" in q or "save" in q:
            st.write("Stop unused VMs, compress storage, enable auto-scaling, or choose cheaper instances.")
        elif "predict" in q:
            st.write(f"AI predicts next month cost around ₹{prediction}")
        else:
            st.write("Monitor usage regularly and optimize unnecessary resources.")

else:
    st.info("👈 Upload billing CSV from sidebar to start.")