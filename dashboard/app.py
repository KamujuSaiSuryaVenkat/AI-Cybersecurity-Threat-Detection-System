import streamlit as st
import requests
import pandas as pd
import os
import random
import datetime
import plotly.express as px

# UI Configuration
st.set_page_config(page_title="AI Threat Shield", page_icon="🛡️", layout="wide")

def generate_fake_ip():
    return f"192.168.{random.randint(10, 50)}.{random.randint(1, 254)}"

st.title("🔐 AI Cybersecurity SOC Dashboard")

mode = st.sidebar.radio("Select Input Mode", ["Manual Entry", "Bulk CSV Audit"])

if mode == "Manual Entry":
    st.subheader("Single Connection Analysis")
    col1, col2 = st.columns(2)
    with col1:
        duration = st.number_input("Duration", 0)
        protocol_type = st.selectbox("Protocol Type", [0, 1, 2], help="0:icmp, 1:tcp, 2:udp")
        service = st.number_input("Service ID", 0)
        src_bytes = st.number_input("Source Bytes", 0)
        dst_bytes = st.number_input("Destination Bytes", 0)
    with col2:
        count = st.number_input("Connection Count", 0)
        srv_count = st.number_input("Service Count", 0)
        serror_rate = st.slider("Serror Rate", 0.0, 1.0)
        srv_serror_rate = st.slider("Srv Serror Rate", 0.0, 1.0)
        same_srv_rate = st.slider("Same Service Rate", 0.0, 1.0)

    if st.button("RUN SECURITY SCAN"):
        payload = {"duration":duration, "protocol_type":protocol_type, "service":service, "src_bytes":src_bytes, 
                   "dst_bytes":dst_bytes, "count":count, "srv_count":srv_count, "serror_rate":serror_rate, 
                   "srv_serror_rate":srv_serror_rate, "same_srv_rate":same_srv_rate}
        try:
            res = requests.post("http://127.0.0.1:5000/predict", json=payload).json()
            if "ATTACK" in res['result']:
                st.error(f"### {res['result']} | Severity: {res['severity']}")
            else:
                st.success(f"### {res['result']}")
            st.info(f"**Analysis:** {res['reason']}")
        except:
            st.error("API Error: Ensure api/app.py is running.")

else:
    st.subheader("📂 Bulk Forensic Analysis")
    uploaded_file = st.file_uploader("Upload Network Traffic CSV", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        if st.button("🚀 EXECUTE SOC AUDIT"):
            results = []
            progress = st.progress(0)
            
            p_map = {"tcp": 1, "udp": 2, "icmp": 0}
            s_map = {"http": 1, "private": 2, "ftp_data": 3, "other": 0}

            for i, row in df.iterrows():
                payload = row.to_dict()
                payload["protocol_type"] = p_map.get(str(payload.get("protocol_type")).lower(), 0)
                payload["service"] = s_map.get(str(payload.get("service")).lower(), 0)

                try:
                    res = requests.post("http://127.0.0.1:5000/predict", json=payload).json()
                    results.append(res)
                except:
                    results.append({"result":"Error", "severity":"N/A", "attack_type":"Error", "timestamp":"N/A", "reason":"API Offline"})
                progress.progress((i + 1) / len(df))
            
            # --- Build SOC Dataframe ---
            df['TIMESTAMP'] = [r.get('timestamp') for r in results]
            df['SOURCE_IP'] = [generate_fake_ip() for _ in range(len(df))]
            df['ATTACK_TYPE'] = [r.get('attack_type') for r in results]
            df['SEVERITY'] = [r.get('severity') for r in results]
            df['DECISION'] = [r.get('result') for r in results]
            df['REASONING'] = [r.get('reason') for r in results]

            # Reorder for "Forensic" look
            report_df = df[['TIMESTAMP', 'SOURCE_IP', 'ATTACK_TYPE', 'SEVERITY', 'DECISION', 'REASONING']]

            # Visuals
            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(px.pie(report_df, names='ATTACK_TYPE', title="Incident Classification", hole=.4), use_container_width=True)
            with c2:
                st.plotly_chart(px.bar(report_df, x='SEVERITY', color='SEVERITY', title="Alert Priority Levels", 
                                       color_discrete_map={'HIGH':'#ff4b4b', 'MEDIUM':'#ffa500', 'LOW':'#28a745'}), use_container_width=True)

            # Styled Table
            st.subheader("🕵️ Investigation Log")
            st.dataframe(report_df.style.map(lambda v: f"color: {'#ff4b4b' if v=='HIGH' else '#ffa500' if v=='MEDIUM' else '#28a745'}; font-weight:bold", subset=['SEVERITY']))
            
            # Export
            st.download_button("📥 DOWNLOAD COMPREHENSIVE SOC REPORT", report_df.to_csv(index=False), "soc_report.csv", "text/csv")

# Sidebar Cleanup
st.sidebar.divider()
if st.sidebar.button("Flush System Logs"):
    if os.path.exists("logs/detections.log"):
        os.remove("logs/detections.log")
        st.sidebar.success("Logs Flushed")