import nmap
import pandas as pd
import numpy as np
import joblib
import os
import re

# Load the trained model and encoders
rf_model = joblib.load("rf_model.pkl")
label_encoders = joblib.load("label_encoders.pkl")
target_encoder = joblib.load("target_encoder.pkl")
scaler = joblib.load("scaler.pkl")

FEATURES = ["Encryption", "WPS Status", "Open Ports"]

def get_router_ip():
    """Finds the default gateway IP."""
    try:
        command = "ipconfig" if os.name == "nt" else "route -n"
        result = os.popen(command).read()
        match = re.search(r"Default Gateway[ .]*: ([\d.]+)", result) or re.search(r"0.0.0.0\s+([\d.]+)", result)
        return match.group(1) if match else "192.168.1.1"
    except Exception:
        return "192.168.1.1"

def scan_open_ports(ip):
    """Scans open ports on the given IP."""
    try:
        scanner = nmap.PortScanner()
        scanner.scan(ip, arguments="-p 1-1000")
        return sum(1 for port in scanner[ip]['tcp'] if scanner[ip]['tcp'][port]['state'] == 'open')
    except Exception:
        return 0

def get_wifi_details():
    """Retrieves Wi-Fi security details (replace with real scan if needed)."""
    return {"SSID": "MyNetwork", "Encryption": "WPA2", "WPS Status": "Enabled"}

def prepare_data(wifi_info, open_ports):
    """Formats data for prediction."""
    wifi_info["Open Ports"] = open_ports
    df = pd.DataFrame([wifi_info])

    for col in ["Encryption", "WPS Status"]:
        df[col] = label_encoders[col].transform([df[col][0]])[0]

    df["Open Ports"] = scaler.transform([[df["Open Ports"][0]]])[0][0]
    
    return df[FEATURES]

def predict_risk():
    """Scans network and predicts security risk."""
    wifi_info = get_wifi_details()
    router_ip = get_router_ip()
    open_ports = scan_open_ports(router_ip)

    print(f"\n🔹 Wi-Fi: {wifi_info['SSID']}")
    print(f"🔍 Scanning {router_ip} for open ports...")
    print(f"🛠 Open Ports Found: {open_ports}")

    input_data = prepare_data(wifi_info, open_ports)
    prediction = rf_model.predict_proba(input_data)[0]

    attack = target_encoder.inverse_transform([np.argmax(prediction)])[0]
    risk_score = round(np.max(prediction) * 100, 2)

    print(f"\n Predicted Attack: {attack}")
    print(f" Risk Level: {risk_score}%")

    # Security Recommendations
    tips = []
    if open_ports > 5:
        tips.append("Limit unnecessary open ports on your router.")
    if wifi_info["Encryption"] in ["None", "WEP"]:
        tips.append("Switch to WPA2 or WPA3 encryption.")
    if wifi_info["WPS Status"] == "Enabled":
        tips.append("Turn off WPS to avoid unauthorized access.")

    if tips:
        print("\n Security Tips:")
        for tip in tips:
            print(f" {tip}")
    else:
        print("\n Your network looks secure.")

if __name__ == "__main__":
    predict_risk()
