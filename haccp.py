# Streamlit HACCP Plan Form for Ice Cream Production
# -------------------------------------------------
# Usage:
#   1) Save this file as `app.py` (or keep the name and run `streamlit run streamlit_haccp_form.py`).
#   2) `pip install streamlit pandas`
#   3) Run: `streamlit run app.py`
#
# Notes:
# - This app builds a structured, fillable HACCP plan aligned with your QA workflow.
# - On submit, it compiles all sections into a single JSON payload and also creates CSVs
#   for key tables. You can download them via buttons.
# - Designed to be used alongside your QA app; this is the policy/documentation side.

from __future__ import annotations
import json
from datetime import datetime, date
from typing import List, Dict

import pandas as pd
import streamlit as st

st.set_page_config(page_title="HACCP Plan – Ice Cream", page_icon="🍦", layout="wide")

# -----------------------------
# Helpers
# -----------------------------

def make_df(rows: List[Dict]) -> pd.DataFrame:
    return pd.DataFrame(rows) if rows else pd.DataFrame()


def download_bytes_label(obj, filename: str, label: str):
    """Render a download button for a bytes-like object."""
    st.download_button(label=label, data=obj, file_name=filename, mime="application/octet-stream")


# -----------------------------
# Sidebar / Header
# -----------------------------
with st.sidebar:
    st.header("📄 HACCP Plan – Ice Cream")
    st.caption("Fill the form, then click **Save / Export** at the bottom.")
    st.markdown("— Built for Lush Gelato QA —")

st.title("🍦 HACCP Food Safety Plan – Ice Cream Production")
st.write("This form generates a HACCP-style plan you can save and print. It mirrors the template we drafted and is designed for inspectors and insurers.")

# Metadata
colm1, colm2, colm3 = st.columns(3)
with colm1:
    business_name = st.text_input("Business Name", value="Lush Gelato")
with colm2:
    location = st.text_input("Location", value="San Francisco, CA")
with colm3:
    plan_date = st.date_input("Plan Date", value=date.today())

st.divider()

# -----------------------------
# 1) Product Information
# -----------------------------
st.subheader("1. Product Information")
pi1, pi2, pi3 = st.columns([1,1,1])
with pi1:
    product_name = st.text_input("Product Name", value="Ice cream mix & frozen batches")
with pi2:
    shelf_life = st.text_input("Shelf Life (frozen)", value="__ months at ≤0°F")
with pi3:
    packaging = st.text_input("Packaging", value="Pints / pans / bulk tubs, food-safe lids")

intended_use = st.text_input("Intended Use", value="Ready-to-eat frozen dessert")
consumers = st.text_input("Consumers", value="General public, including children and elderly")

st.divider()

# -----------------------------
# 2) Process Flow Diagram (free text)
# -----------------------------
st.subheader("2. Process Flow Diagram")
process_flow = st.text_area(
    "Process Steps (free text or arrows)",
    value=(
        "Receiving Ingredients → Cold Storage → Mix Preparation → Pasteurization "
        "→ Cooling → Batch Freezing → Frozen Storage → Retail Service"
    ),
    height=80,
)

st.divider()

# -----------------------------
# 3) Hazard Analysis Table
# -----------------------------
st.subheader("3. Hazard Analysis")

hazard_default = [
    {
        "Step": "Receiving (milk, cream, eggs)",
        "Potential Hazards": "Pathogens, spoilage",
        "Preventive Measures": "Approved suppliers, check expiration dates, temp check"
    },
    {
        "Step": "Storage (raw ingredients)",
        "Potential Hazards": "Pathogen growth",
        "Preventive Measures": "Refrigerate ≤41°F, FIFO rotation"
    },
    {
        "Step": "Mix Preparation",
        "Potential Hazards": "Cross-contamination, expired use",
        "Preventive Measures": "Sanitize equipment, hygiene, QA expiration log"
    },
    {
        "Step": "Pasteurization",
        "Potential Hazards": "Survival of pathogens",
        "Preventive Measures": "≥155°F/30 min or HTST validated"
    },
    {
        "Step": "Cooling",
        "Potential Hazards": "Pathogen growth",
        "Preventive Measures": "Cool ≤41°F within 4 hrs"
    },
    {
        "Step": "Batch Freezing",
        "Potential Hazards": "Cross-contamination",
        "Preventive Measures": "Taste test, second-person verification"
    },
    {
        "Step": "Storage (frozen)",
        "Potential Hazards": "Pathogen survival, quality loss",
        "Preventive Measures": "≤0°F, freezer monitoring"
    },
    {
        "Step": "Retail Service",
        "Potential Hazards": "Cross-contamination, allergens",
        "Preventive Measures": "Hygiene, clean scoops, allergen labeling"
    },
]

st.caption("Edit rows as needed. Use the + button to add more steps.")
rows_hazard = st.number_input("Number of hazard rows", min_value=1, max_value=30, value=len(hazard_default))

hazard_rows: List[Dict] = []
for i in range(int(rows_hazard)):
    # populate defaults where available
    d = hazard_default[i] if i < len(hazard_default) else {"Step": "", "Potential Hazards": "", "Preventive Measures": ""}
    c1, c2, c3 = st.columns([1.1, 1, 1])
    with c1:
        step = st.text_input(f"Step {i+1}", value=d["Step"], key=f"hz_step_{i}")
    with c2:
        haz = st.text_input(f"Potential Hazards {i+1}", value=d["Potential Hazards"], key=f"hz_haz_{i}")
    with c3:
        prev = st.text_input(f"Preventive Measures {i+1}", value=d["Preventive Measures"], key=f"hz_prev_{i}")
    hazard_rows.append({"Step": step, "Potential Hazards": haz, "Preventive Measures": prev})

st.divider()

# -----------------------------
# 4) Critical Control Points (CCPs)
# -----------------------------
st.subheader("4. Critical Control Points (CCPs)")
ccp_default = [
    {
        "CCP": "Pasteurization",
        "Critical Limits": "≥155°F for 30 min OR 175°F for 25 sec",
        "Monitoring": "Chart recorder, thermometer",
        "Corrective Action": "Re-pasteurize or discard batch",
        "Verification": "Manager daily check",
        "Records": "Pasteurization logs"
    },
    {
        "CCP": "Cooling",
        "Critical Limits": "≤41°F within 4 hrs",
        "Monitoring": "Thermometer",
        "Corrective Action": "Discard if limit not met",
        "Verification": "Manager daily check",
        "Records": "Cooling logs"
    },
    {
        "CCP": "Expiration Date Check",
        "Critical Limits": "No expired ingredients used",
        "Monitoring": "QA app logs",
        "Corrective Action": "Discard expired mix",
        "Verification": "Weekly audit",
        "Records": "QA app records"
    },
    {
        "CCP": "Taste Test",
        "Critical Limits": "Final mix & frozen batch taste tested",
        "Monitoring": "Employee check + second verifier",
        "Corrective Action": "Stop freezing, discard if sour/acidic",
        "Verification": "Weekly review",
        "Records": "QA logs"
    },
]

rows_ccp = st.number_input("Number of CCP rows", min_value=1, max_value=20, value=len(ccp_default))
ccp_rows: List[Dict] = []
for i in range(int(rows_ccp)):
    d = ccp_default[i] if i < len(ccp_default) else {
        "CCP": "", "Critical Limits": "", "Monitoring": "", "Corrective Action": "", "Verification": "", "Records": ""
    }
    c1, c2 = st.columns([1, 1])
    with c1:
        ccp = st.text_input(f"CCP {i+1}", value=d["CCP"], key=f"ccp_name_{i}")
        limits = st.text_input(f"Critical Limits {i+1}", value=d["Critical Limits"], key=f"ccp_limits_{i}")
        monitoring = st.text_input(f"Monitoring {i+1}", value=d["Monitoring"], key=f"ccp_monitor_{i}")
    with c2:
        ca = st.text_input(f"Corrective Action {i+1}", value=d["Corrective Action"], key=f"ccp_ca_{i}")
        ver = st.text_input(f"Verification {i+1}", value=d["Verification"], key=f"ccp_ver_{i}")
        rec = st.text_input(f"Records {i+1}", value=d["Records"], key=f"ccp_rec_{i}")
    ccp_rows.append({
        "CCP": ccp,
        "Critical Limits": limits,
        "Monitoring": monitoring,
        "Corrective Action": ca,
        "Verification": ver,
        "Records": rec,
    })

st.divider()

# -----------------------------
# 5) Prerequisite Programs
# -----------------------------
st.subheader("5. Prerequisite Programs")
pp_default = [
    {"Program": "Employee Hygiene", "Description": "Handwashing, gloves, hair restraints", "Responsible Person": ""},
    {"Program": "Sanitation", "Description": "Clean/sanitize equipment each use", "Responsible Person": ""},
    {"Program": "Supplier Approval", "Description": "Purchase only from licensed suppliers", "Responsible Person": ""},
    {"Program": "Training", "Description": "Staff trained in HACCP, QA app, sanitation", "Responsible Person": ""},
    {"Program": "Traceability", "Description": "Lot numbers & employee recorded", "Responsible Person": ""},
    {"Program": "Recall Plan", "Description": "Immediate batch ID + notify authorities", "Responsible Person": ""},
]
rows_pp = st.number_input("Number of prerequisite rows", min_value=1, max_value=30, value=len(pp_default))
pp_rows: List[Dict] = []
for i in range(int(rows_pp)):
    d = pp_default[i] if i < len(pp_default) else {"Program": "", "Description": "", "Responsible Person": ""}
    c1, c2, c3 = st.columns([1, 1.4, 1])
    with c1:
        prog = st.text_input(f"Program {i+1}", value=d["Program"], key=f"pp_prog_{i}")
    with c2:
        desc = st.text_input(f"Description {i+1}", value=d["Description"], key=f"pp_desc_{i}")
    with c3:
        resp = st.text_input(f"Responsible Person {i+1}", value=d["Responsible Person"], key=f"pp_resp_{i}")
    pp_rows.append({"Program": prog, "Description": desc, "Responsible Person": resp})

st.divider()

# -----------------------------
# 6) Verification Schedule
# -----------------------------
st.subheader("6. Verification Schedule")
ver_default = [
    {"Frequency": "Daily", "Activity": "Manager reviews pasteurization & cooling logs", "Responsible Person": ""},
    {"Frequency": "Weekly", "Activity": "Audit QA system (expiration & taste test)", "Responsible Person": ""},
    {"Frequency": "Monthly", "Activity": "Review sanitation records", "Responsible Person": ""},
    {"Frequency": "Annual", "Activity": "HACCP plan review & revalidation", "Responsible Person": ""},
]
rows_ver = st.number_input("Number of verification rows", min_value=1, max_value=30, value=len(ver_default))
ver_rows: List[Dict] = []
for i in range(int(rows_ver)):
    d = ver_default[i] if i < len(ver_default) else {"Frequency": "", "Activity": "", "Responsible Person": ""}
    c1, c2, c3 = st.columns([0.7, 1.5, 1])
    with c1:
        freq = st.text_input(f"Frequency {i+1}", value=d["Frequency"], key=f"ver_freq_{i}")
    with c2:
        act = st.text_input(f"Activity {i+1}", value=d["Activity"], key=f"ver_act_{i}")
    with c3:
        resp = st.text_input(f"Responsible Person {i+1}", value=d["Responsible Person"], key=f"ver_resp_{i}")
    ver_rows.append({"Frequency": freq, "Activity": act, "Responsible Person": resp})

st.divider()

# -----------------------------
# 7) Corrective Action Log (blank table structure)
# -----------------------------
st.subheader("7. Corrective Action Log (Template)")
ca_rows_n = st.number_input("Number of initial blank rows", min_value=1, max_value=50, value=5)
ca_rows: List[Dict] = []
for i in range(int(ca_rows_n)):
    c1, c2, c3, c4, c5 = st.columns([0.7, 1.3, 1.2, 1, 1])
    with c1:
        dte = st.text_input(f"Date {i+1}", value="", key=f"ca_date_{i}")
    with c2:
        issue = st.text_input(f"Issue Identified {i+1}", value="", key=f"ca_issue_{i}")
    with c3:
        act = st.text_input(f"Action Taken {i+1}", value="", key=f"ca_act_{i}")
    with c4:
        resp = st.text_input(f"Responsible Employee {i+1}", value="", key=f"ca_resp_{i}")
    with c5:
        ver = st.text_input(f"Verified By {i+1}", value="", key=f"ca_ver_{i}")
    ca_rows.append({
        "Date": dte, "Issue Identified": issue, "Action Taken": act,
        "Responsible Employee": resp, "Verified By": ver
    })

st.divider()

# -----------------------------
# Submission & Export
# -----------------------------
with st.form("save_export_form"):
    st.subheader("Save / Export")
    notes = st.text_area("Internal Notes (optional)", value="")
    submitted = st.form_submit_button("💾 Generate Files")

if submitted:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    payload = {
        "meta": {
            "business_name": business_name,
            "location": location,
            "plan_date": str(plan_date),
            "generated_at": timestamp,
        },
        "product_information": {
            "product_name": product_name,
            "shelf_life": shelf_life,
            "packaging": packaging,
            "intended_use": intended_use,
            "consumers": consumers,
        },
        "process_flow": process_flow,
        "hazard_analysis": hazard_rows,
        "ccps": ccp_rows,
        "prerequisite_programs": pp_rows,
        "verification_schedule": ver_rows,
        "corrective_action_log_template": ca_rows,
        "notes": notes,
    }

    # JSON export
    json_bytes = json.dumps(payload, indent=2).encode("utf-8")
    st.success("HACCP plan generated. Use the buttons below to download.")
    download_bytes_label(json_bytes, f"haccp_plan_{timestamp}.json", "⬇️ Download HACCP Plan (JSON)")

    # CSV exports for key tables
    df_hazard = make_df(hazard_rows)
    df_ccp = make_df(ccp_rows)
    df_pp = make_df(pp_rows)
    df_ver = make_df(ver_rows)
    df_ca = make_df(ca_rows)

    if not df_hazard.empty:
        download_bytes_label(df_hazard.to_csv(index=False).encode("utf-8"), f"hazard_analysis_{timestamp}.csv", "⬇️ Hazard Analysis (CSV)")
    if not df_ccp.empty:
        download_bytes_label(df_ccp.to_csv(index=False).encode("utf-8"), f"ccps_{timestamp}.csv", "⬇️ CCPs (CSV)")
    if not df_pp.empty:
        download_bytes_label(df_pp.to_csv(index=False).encode("utf-8"), f"prereq_programs_{timestamp}.csv", "⬇️ Prerequisite Programs (CSV)")
    if not df_ver.empty:
        download_bytes_label(df_ver.to_csv(index=False).encode("utf-8"), f"verification_{timestamp}.csv", "⬇️ Verification Schedule (CSV)")
    if not df_ca.empty:
        download_bytes_label(df_ca.to_csv(index=False).encode("utf-8"), f"corrective_actions_template_{timestamp}.csv", "⬇️ Corrective Actions Template (CSV)")

    st.info("Pro tip: Keep JSON in your repo; print and file the CSVs weekly in your HACCP binder.")

st.markdown("---")
st.caption("This template is a first draft. Have a certified HACCP consultant review for regulatory compliance in your jurisdiction.")
