import sys
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rules.rule_checker import check_network_issue
from ai.prompt import NETSAGE_AI_PROMPT

st.set_page_config(page_title="NetSage AI", page_icon="🌐")

st.title(" NetSage AI")
st.caption("Evidence-based Network Troubleshooting Assistant")

df = pd.read_csv(ROOT / "data" / "cases.csv")

case_id = st.selectbox("Select a case", df.case_id.tolist())
case = df[df.case_id == case_id].iloc[0]

st.write(
    f"**Concept:** {case.concept} | "
    f"**OSI:** {case.osi_layer} | "
    f"**Severity:** {case.severity}"
)

symptom = st.text_area("Network Problem", case.symptom)

evidence = st.text_area(
    "Evidence",
    f"Command: {case.evidence_command}\n"
    f"Output: {case.evidence_output}"
)

if st.button("🔍 ANALYZE", use_container_width=True):

    baseline = check_network_issue(symptom, evidence)

    st.session_state.diagnosis = {
        "root_cause": baseline["root_cause"],
        "confidence": baseline["confidence"],
        "evidence": [case.evidence_output],
        "next_command": case.next_command,
        "fix": [
            x.strip()
            for x in str(case.fix).split(";")
            if x.strip()
        ],
        "verification": case.verification,
    }

    st.session_state.prompt = (
        NETSAGE_AI_PROMPT
        + f"\n\nPROBLEM:\n{symptom}"
        + f"\n\nEVIDENCE:\n{evidence}"
    )

if "diagnosis" in st.session_state:

    d = st.session_state.diagnosis

    st.divider()
    st.subheader("Diagnosis")

    st.metric(
        "Confidence",
        f"{d['confidence'] * 100:.0f}%"
    )

    st.success(d["root_cause"])

    st.write("**Evidence**")

    for e in d["evidence"]:
        st.write("✓", e)

    st.write("**Next Command**")
    st.code(d["next_command"])

    st.write("**Recommended Fix**")

    for step in d["fix"]:
        st.code(step)

    st.write("**Verification**")
    st.info(d["verification"])

    st.warning(
        " Human review is required before applying configuration changes."
    )

    a, b, c = st.columns(3)

    if a.button(" ACCEPT"):
        st.session_state.review = "Accepted"

    if b.button(" EDIT"):
        st.session_state.review = "Edited"

    if c.button(" REJECT"):
        st.session_state.review = "Rejected"

    if "review" in st.session_state:
        st.write(
            "**Human Review:**",
            st.session_state.review
        )

    with st.expander("Show AI Prompt"):
        st.code(st.session_state.prompt)
