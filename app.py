# ============================================================
# CARE TRANSITION EFFICIENCY & PLACEMENT OUTCOME ANALYTICS
# STREAMLIT DASHBOARD
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Care Transition Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #f5f7fb;
    }

    /* Header */
    .main-header {
        background: linear-gradient(135deg, #0f172a, #1e3a5f);
        padding: 28px 32px;
        border-radius: 16px;
        margin-bottom: 22px;
        color: white;
        box-shadow: 0 6px 20px rgba(15, 23, 42, 0.15);
    }

    .main-header h1 {
        margin: 0;
        font-size: 32px;
        font-weight: 700;
    }

    .main-header p {
        margin: 8px 0 0 0;
        font-size: 15px;
        opacity: 0.85;
    }

    /* Section title */
    .section-title {
        font-size: 23px;
        font-weight: 700;
        color: #0f172a;
        margin-top: 12px;
        margin-bottom: 8px;
    }

    .section-subtitle {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 18px;
    }

    /* KPI card */
    .kpi-card {
        background: white;
        padding: 18px 20px;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.06);
        min-height: 115px;
    }

    .kpi-title {
        color: #64748b;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }

    .kpi-value {
        color: #0f172a;
        font-size: 28px;
        font-weight: 750;
        margin-top: 7px;
    }

    .kpi-description {
        color: #94a3b8;
        font-size: 11px;
        margin-top: 4px;
    }

    /* Alert boxes */
    .alert-warning {
        background: #fff7ed;
        border-left: 5px solid #f97316;
        padding: 13px 16px;
        border-radius: 10px;
        margin-bottom: 10px;
        color: #7c2d12;
    }

    .alert-danger {
        background: #fef2f2;
        border-left: 5px solid #ef4444;
        padding: 13px 16px;
        border-radius: 10px;
        margin-bottom: 10px;
        color: #7f1d1d;
    }

    .alert-success {
        background: #f0fdf4;
        border-left: 5px solid #22c55e;
        padding: 13px 16px;
        border-radius: 10px;
        margin-bottom: 10px;
        color: #14532d;
    }

    /* Info boxes */
    .info-box {
        background: #eff6ff;
        border-left: 5px solid #3b82f6;
        padding: 13px 16px;
        border-radius: 10px;
        margin-bottom: 15px;
        color: #1e3a8a;
        font-size: 13px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 10px 18px;
        border-radius: 8px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 12px;
        margin-top: 35px;
        padding: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    file_path = "final_analytical_dataset.csv"

    df = pd.read_csv(file_path)

    # Convert Date
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Convert numeric columns where available
    numeric_columns = [
        "CBP_Intake",
        "CBP_Custody",
        "CBP_Transfers",
        "HHS_Care",
        "HHS_Discharges",
        "Pipeline_Entries",
        "Pipeline_Exits",
        "Net_Pipeline_Flow",
        "Positive_Accumulation",
        "Negative_Accumulation",
        "Transfer_Efficiency_Ratio",
        "Transfer_Efficiency_Pct",
        "Discharge_Effectiveness_Index",
        "Discharge_Effectiveness_Pct",
        "Daily_Pipeline_Throughput",
        "Pipeline_Throughput_Pct",
        "Exit_to_Entry_Activity_Ratio",
        "CBP_Net_Pressure",
        "CBP_Accumulation",
        "CBP_Accumulation_Rate",
        "CBP_Accumulation_Rate_Pct",
        "HHS_Net_Pressure",
        "HHS_Accumulation",
        "HHS_Accumulation_Rate",
        "HHS_Accumulation_Rate_Pct",
        "Total_Stage_Pressure",
        "Outcome_Stability_Score",
        "Transfer_Efficiency_7Obs_Rolling",
        "Discharge_Effectiveness_7Obs_Rolling",
        "Throughput_7Obs_Rolling"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


# ============================================================
# ERROR HANDLING
# ============================================================

try:
    df = load_data()

except FileNotFoundError:
    st.error(
        "final_analytical_dataset.csv was not found. "
        "Please make sure the CSV file is in the same folder as app.py."
    )
    st.stop()

except Exception as e:
    st.error(f"Unable to load the dataset: {e}")
    st.stop()


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [
    "Date",
    "CBP_Intake",
    "CBP_Custody",
    "CBP_Transfers",
    "HHS_Care",
    "HHS_Discharges"
]

missing_required = [
    col for col in required_columns
    if col not in df.columns
]

if missing_required:
    st.error(
        "The following required columns are missing from "
        "final_analytical_dataset.csv:"
    )

    for col in missing_required:
        st.write(f"- {col}")

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="main-header">
        <h1>Care Transition Efficiency & Placement Outcome Analytics</h1>
        <p>
            Monitoring CBP → HHS care transitions, discharge performance,
            stage pressure and operational outcomes.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("## Dashboard Controls")
st.sidebar.markdown("---")

# Date range
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, tuple) and len(date_range) == 2:

    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1])

else:

    start_date = pd.Timestamp(min_date)
    end_date = pd.Timestamp(max_date)


filtered_df = df[
    (df["Date"] >= start_date) &
    (df["Date"] <= end_date)
].copy()


# ============================================================
# RATIO-BASED METRIC TOGGLE
# ============================================================

st.sidebar.markdown("### Metric View")

metric_mode = st.sidebar.radio(
    "Choose metric format:",
    [
        "Percentage",
        "Ratio"
    ],
    index=0
)


# ============================================================
# THRESHOLD CONTROLS
# ============================================================

st.sidebar.markdown("### Alert Thresholds")

transfer_threshold = st.sidebar.slider(
    "Low Transfer Efficiency (%)",
    min_value=0.0,
    max_value=100.0,
    value=50.0,
    step=1.0
)

discharge_threshold = st.sidebar.slider(
    "Low Discharge Effectiveness (%)",
    min_value=0.0,
    max_value=10.0,
    value=1.0,
    step=0.1
)

pressure_threshold = st.sidebar.number_input(
    "High Total Stage Pressure",
    min_value=0.0,
    value=100.0,
    step=10.0
)


# ============================================================
# SIDEBAR DATA SUMMARY
# ============================================================

st.sidebar.markdown("---")
st.sidebar.markdown("### Current Selection")

st.sidebar.write(
    f"**Start:** {start_date.strftime('%d %b %Y')}"
)

st.sidebar.write(
    f"**End:** {end_date.strftime('%d %b %Y')}"
)

st.sidebar.write(
    f"**Reporting observations:** {len(filtered_df):,}"
)


# ============================================================
# HANDLE EMPTY FILTER
# ============================================================

if filtered_df.empty:

    st.warning(
        "No reporting observations are available for the selected date range."
    )

    st.stop()


# ============================================================
# DERIVE MONTHLY DATA
# ============================================================

filtered_df["Month_Period_Display"] = (
    filtered_df["Date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_df = (
    filtered_df
    .groupby("Month_Period_Display", as_index=False)
    .agg(
        CBP_Intake=("CBP_Intake", "sum"),
        CBP_Transfers=("CBP_Transfers", "sum"),
        HHS_Discharges=("HHS_Discharges", "sum"),
        Avg_CBP_Custody=("CBP_Custody", "mean"),
        Avg_HHS_Care=("HHS_Care", "mean"),
        Avg_Transfer_Efficiency=(
            "Transfer_Efficiency_Pct",
            "mean"
        ),
        Avg_Discharge_Effectiveness=(
            "Discharge_Effectiveness_Pct",
            "mean"
        ),
        Avg_CBP_Accumulation=(
            "CBP_Accumulation",
            "mean"
        ),
        Avg_HHS_Accumulation=(
            "HHS_Accumulation",
            "mean"
        ),
        Avg_Total_Stage_Pressure=(
            "Total_Stage_Pressure",
            "mean"
        ),
        Avg_Outcome_Stability=(
            "Outcome_Stability_Score",
            "mean"
        )
    )
)


# ============================================================
# CALCULATE PERIOD KPIs
# ============================================================

total_intake = filtered_df["CBP_Intake"].sum()
total_transfers = filtered_df["CBP_Transfers"].sum()
total_discharges = filtered_df["HHS_Discharges"].sum()

avg_cbp_custody = filtered_df["CBP_Custody"].mean()
avg_hhs_care = filtered_df["HHS_Care"].mean()

avg_transfer_efficiency = (
    filtered_df["Transfer_Efficiency_Pct"].mean()
)

avg_discharge_effectiveness = (
    filtered_df["Discharge_Effectiveness_Pct"].mean()
)

avg_outcome_stability = (
    filtered_df["Outcome_Stability_Score"].mean()
)

avg_cbp_pressure = (
    filtered_df["CBP_Accumulation"].mean()
)

avg_hhs_pressure = (
    filtered_df["HHS_Accumulation"].mean()
)

avg_total_pressure = (
    filtered_df["Total_Stage_Pressure"].mean()
)


# Activity ratios
transfer_activity_ratio = (
    total_transfers / total_intake
    if total_intake > 0
    else np.nan
)

placement_activity_ratio = (
    total_discharges / total_transfers
    if total_transfers > 0
    else np.nan
)

exit_entry_ratio = (
    total_discharges / total_intake
    if total_intake > 0
    else np.nan
)


# ============================================================
# MAIN OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">Executive Overview</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Key operational indicators for the selected reporting period.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# KPI CARDS
# ============================================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Transfer Efficiency</div>
            <div class="kpi-value">{avg_transfer_efficiency:.2f}%</div>
            <div class="kpi-description">
                Average CBP → HHS transfer efficiency
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with kpi2:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Discharge Effectiveness</div>
            <div class="kpi-value">{avg_discharge_effectiveness:.2f}%</div>
            <div class="kpi-description">
                Average HHS discharge effectiveness
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with kpi3:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Outcome Stability</div>
            <div class="kpi-value">{avg_outcome_stability:.1f}/100</div>
            <div class="kpi-description">
                Higher score indicates more consistent outcomes
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with kpi4:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Stage Pressure</div>
            <div class="kpi-value">{avg_total_pressure:,.0f}</div>
            <div class="kpi-description">
                Average observed stage accumulation pressure
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# SECOND KPI ROW
# ============================================================

kpi5, kpi6, kpi7, kpi8 = st.columns(4)

with kpi5:

    st.metric(
        "CBP Intake",
        f"{total_intake:,.0f}"
    )


with kpi6:

    st.metric(
        "CBP Transfers",
        f"{total_transfers:,.0f}"
    )


with kpi7:

    st.metric(
        "HHS Discharges",
        f"{total_discharges:,.0f}"
    )


with kpi8:

    if metric_mode == "Percentage":

        value_text = (
            f"{exit_entry_ratio * 100:.2f}%"
            if not np.isnan(exit_entry_ratio)
            else "N/A"
        )

    else:

        value_text = (
            f"{exit_entry_ratio:.2f}"
            if not np.isnan(exit_entry_ratio)
            else "N/A"
        )

    st.metric(
        "Exit / Entry Activity Ratio",
        value_text
    )


# ============================================================
# INFORMATION NOTE
# ============================================================

st.markdown(
    """
    <div class="info-box">
        <b>Interpretation note:</b>
        Activity ratios compare observed movements between stages and dates.
        They should not be interpreted as individual-level placement or
        cohort success rates because intake, transfer and discharge measures
        can refer to different cohorts and timing windows.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TABS / CORE MODULES
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Pipeline Flow",
        "Efficiency",
        "Bottlenecks",
        "Outcome Trends"
    ]
)


# ============================================================
# TAB 1 — CARE PIPELINE FLOW
# ============================================================

with tab1:

    st.markdown(
        '<div class="section-title">Care Pipeline Flow Visualization</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Observed activity across the major CBP and HHS stages.'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # Flow summary cards
    # --------------------------------------------------------

    flow1, flow2, flow3, flow4 = st.columns(4)

    with flow1:
        st.metric(
            "CBP Intake",
            f"{total_intake:,.0f}"
        )

    with flow2:
        st.metric(
            "Average CBP Custody",
            f"{avg_cbp_custody:,.0f}"
        )

    with flow3:
        st.metric(
            "CBP Transfers",
            f"{total_transfers:,.0f}"
        )

    with flow4:
        st.metric(
            "HHS Discharges",
            f"{total_discharges:,.0f}"
        )


    # --------------------------------------------------------
    # Pipeline activity chart
    # --------------------------------------------------------

    pipeline_chart = pd.DataFrame(
        {
            "Stage": [
                "CBP Intake",
                "CBP Transfers",
                "HHS Discharges"
            ],
            "Observed Activity": [
                total_intake,
                total_transfers,
                total_discharges
            ]
        }
    )

    fig_pipeline = px.bar(
        pipeline_chart,
        x="Stage",
        y="Observed Activity",
        text="Observed Activity",
        title="Observed Pipeline Activity"
    )

    fig_pipeline.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside"
    )

    fig_pipeline.update_layout(
        height=450,
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=30, r=30, t=70, b=30)
    )

    st.plotly_chart(
        fig_pipeline,
        use_container_width=True
    )


    # --------------------------------------------------------
    # Stock indicators
    # --------------------------------------------------------

    st.markdown(
        "### Average Stage Stock Indicators"
    )

    stock_df = pd.DataFrame(
        {
            "Stage": [
                "CBP Custody",
                "HHS Care"
            ],
            "Average Observed Level": [
                avg_cbp_custody,
                avg_hhs_care
            ]
        }
    )

    fig_stock = px.bar(
        stock_df,
        x="Stage",
        y="Average Observed Level",
        text="Average Observed Level",
        title="Average Reported Population in Stage"
    )

    fig_stock.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside"
    )

    fig_stock.update_layout(
        height=400,
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(
        fig_stock,
        use_container_width=True
    )


    st.markdown(
        """
        <div class="info-box">
            <b>Important:</b>
            CBP Custody and HHS Care are stage stock measures, while Intake,
            Transfers and Discharges are movement measures. Therefore,
            the chart is a monitoring view of observed activity and should
            not be treated as a cohort-level funnel.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# TAB 2 — TRANSFER & DISCHARGE EFFICIENCY
# ============================================================

with tab2:

    st.markdown(
        '<div class="section-title">Transfer & Discharge Efficiency</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Track operational efficiency using ratio-based metrics.'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # Efficiency cards
    # --------------------------------------------------------

    e1, e2, e3, e4 = st.columns(4)

    with e1:

        st.metric(
            "Transfer Efficiency",
            f"{avg_transfer_efficiency:.2f}%"
        )

    with e2:

        st.metric(
            "Discharge Effectiveness",
            f"{avg_discharge_effectiveness:.2f}%"
        )

    with e3:

        st.metric(
            "Transfer Activity Ratio",
            f"{transfer_activity_ratio:.2f}"
        )

    with e4:

        st.metric(
            "Placement Activity Ratio",
            f"{placement_activity_ratio:.2f}"
        )


    # --------------------------------------------------------
    # Ratio toggle
    # --------------------------------------------------------

    st.markdown("### Efficiency Trend")

    trend_metric = st.selectbox(
        "Select efficiency metric",
        [
            "Transfer Efficiency",
            "Discharge Effectiveness",
            "Transfer Activity Ratio",
            "Placement Activity Ratio"
        ]
    )


    # --------------------------------------------------------
    # Trend calculation
    # --------------------------------------------------------

    monthly_trend = (
        filtered_df
        .groupby(
            filtered_df["Date"].dt.to_period("M")
        )
        .agg(
            CBP_Intake=("CBP_Intake", "sum"),
            CBP_Transfers=("CBP_Transfers", "sum"),
            HHS_Discharges=("HHS_Discharges", "sum"),
            Transfer_Efficiency=(
                "Transfer_Efficiency_Ratio",
                "mean"
            ),
            Discharge_Effectiveness=(
                "Discharge_Effectiveness_Index",
                "mean"
            )
        )
        .reset_index()
    )

    monthly_trend["Month"] = (
        monthly_trend["Date"]
        .astype(str)
    )

    # Calculate ratios from monthly totals
    monthly_trend["Transfer_Activity_Ratio"] = np.where(
        monthly_trend["CBP_Intake"] > 0,
        monthly_trend["CBP_Transfers"] /
        monthly_trend["CBP_Intake"],
        np.nan
    )

    monthly_trend["Placement_Activity_Ratio"] = np.where(
        monthly_trend["CBP_Transfers"] > 0,
        monthly_trend["HHS_Discharges"] /
        monthly_trend["CBP_Transfers"],
        np.nan
    )


    if trend_metric == "Transfer Efficiency":

        y_column = "Transfer_Efficiency"

        if metric_mode == "Percentage":
            chart_values = (
                monthly_trend[y_column] * 100
            )
        else:
            chart_values = monthly_trend[y_column]

        y_title = (
            "Transfer Efficiency (%)"
            if metric_mode == "Percentage"
            else "Transfer Efficiency Ratio"
        )

    elif trend_metric == "Discharge Effectiveness":

        y_column = "Discharge_Effectiveness"

        if metric_mode == "Percentage":
            chart_values = (
                monthly_trend[y_column] * 100
            )
        else:
            chart_values = monthly_trend[y_column]

        y_title = (
            "Discharge Effectiveness (%)"
            if metric_mode == "Percentage"
            else "Discharge Effectiveness Ratio"
        )

    elif trend_metric == "Transfer Activity Ratio":

        y_column = "Transfer_Activity_Ratio"

        if metric_mode == "Percentage":
            chart_values = (
                monthly_trend[y_column] * 100
            )
        else:
            chart_values = monthly_trend[y_column]

        y_title = (
            "Transfer Activity Ratio (%)"
            if metric_mode == "Percentage"
            else "Transfer Activity Ratio"
        )

    else:

        y_column = "Placement_Activity_Ratio"

        if metric_mode == "Percentage":
            chart_values = (
                monthly_trend[y_column] * 100
            )
        else:
            chart_values = monthly_trend[y_column]

        y_title = (
            "Placement Activity Ratio (%)"
            if metric_mode == "Percentage"
            else "Placement Activity Ratio"
        )


    trend_plot_df = pd.DataFrame(
        {
            "Month": monthly_trend["Month"],
            "Value": chart_values
        }
    )


    fig_efficiency = px.line(
        trend_plot_df,
        x="Month",
        y="Value",
        markers=True,
        title=f"Monthly {trend_metric}"
    )

    fig_efficiency.update_layout(
        height=450,
        xaxis_title="Month",
        yaxis_title=y_title,
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(
        fig_efficiency,
        use_container_width=True
    )


    # --------------------------------------------------------
    # Volume comparison
    # --------------------------------------------------------

    st.markdown("### Monthly Transfer and Discharge Activity")

    volume_plot_df = monthly_trend[
        [
            "Month",
            "CBP_Transfers",
            "HHS_Discharges"
        ]
    ].melt(
        id_vars="Month",
        var_name="Metric",
        value_name="Volume"
    )

    volume_plot_df["Metric"] = (
        volume_plot_df["Metric"]
        .replace(
            {
                "CBP_Transfers": "CBP Transfers",
                "HHS_Discharges": "HHS Discharges"
            }
        )
    )

    fig_volume = px.line(
        volume_plot_df,
        x="Month",
        y="Volume",
        color="Metric",
        markers=True,
        title="Monthly Transfers vs Discharges"
    )

    fig_volume.update_layout(
        height=450,
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(
        fig_volume,
        use_container_width=True
    )


# ============================================================
# TAB 3 — BOTTLENECK DETECTION
# ============================================================

with tab3:

    st.markdown(
        '<div class="section-title">Bottleneck Detection & Stage Pressure</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Identify periods of low transition performance and elevated '
        'stage accumulation pressure.'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # Apply user thresholds
    # --------------------------------------------------------

    bottleneck_df = filtered_df.copy()

    bottleneck_df["Low_Transfer_Alert"] = (
        bottleneck_df["Transfer_Efficiency_Pct"]
        <= transfer_threshold
    )

    bottleneck_df["Low_Discharge_Alert"] = (
        bottleneck_df["Discharge_Effectiveness_Pct"]
        <= discharge_threshold
    )

    bottleneck_df["High_Pressure_Alert"] = (
        bottleneck_df["Total_Stage_Pressure"]
        >= pressure_threshold
    )

    bottleneck_df["Custom_Bottleneck"] = (
        bottleneck_df["Low_Transfer_Alert"]
        & bottleneck_df["High_Pressure_Alert"]
    ) | (
        bottleneck_df["Low_Discharge_Alert"]
        & bottleneck_df["High_Pressure_Alert"]
    )


    # --------------------------------------------------------
    # Alert summary
    # --------------------------------------------------------

    transfer_alerts = (
        bottleneck_df["Low_Transfer_Alert"].sum()
    )

    discharge_alerts = (
        bottleneck_df["Low_Discharge_Alert"].sum()
    )

    pressure_alerts = (
        bottleneck_df["High_Pressure_Alert"].sum()
    )

    custom_bottlenecks = (
        bottleneck_df["Custom_Bottleneck"].sum()
    )


    a1, a2, a3, a4 = st.columns(4)

    with a1:
        st.metric(
            "Low Transfer Alerts",
            f"{transfer_alerts:,}"
        )

    with a2:
        st.metric(
            "Low Discharge Alerts",
            f"{discharge_alerts:,}"
        )

    with a3:
        st.metric(
            "High Pressure Alerts",
            f"{pressure_alerts:,}"
        )

    with a4:
        st.metric(
            "Combined Bottleneck Alerts",
            f"{custom_bottlenecks:,}"
        )


    # --------------------------------------------------------
    # Visual alerts
    # --------------------------------------------------------

    if custom_bottlenecks > 0:

        st.markdown(
            f"""
            <div class="alert-danger">
                <b>Attention:</b>
                {custom_bottlenecks:,} reporting observations meet the
                configured bottleneck conditions.
            </div>
            """,
            unsafe_allow_html=True
        )

    elif pressure_alerts > 0:

        st.markdown(
            f"""
            <div class="alert-warning">
                <b>Pressure Warning:</b>
                {pressure_alerts:,} observations exceed the selected
                total stage pressure threshold.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="alert-success">
                <b>No active combined bottleneck alert</b>
                was detected under the selected thresholds.
            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # Stage pressure chart
    # --------------------------------------------------------

    pressure_trend = (
        filtered_df
        .groupby(
            filtered_df["Date"].dt.to_period("M")
        )
        .agg(
            CBP_Pressure=("CBP_Accumulation", "mean"),
            HHS_Pressure=("HHS_Accumulation", "mean"),
            Total_Pressure=("Total_Stage_Pressure", "mean")
        )
        .reset_index()
    )

    pressure_trend["Month"] = (
        pressure_trend["Date"].astype(str)
    )

    pressure_plot_df = pressure_trend[
        [
            "Month",
            "CBP_Pressure",
            "HHS_Pressure",
            "Total_Pressure"
        ]
    ].melt(
        id_vars="Month",
        var_name="Stage",
        value_name="Pressure"
    )

    pressure_plot_df["Stage"] = (
        pressure_plot_df["Stage"]
        .replace(
            {
                "CBP_Pressure": "CBP Accumulation",
                "HHS_Pressure": "HHS Accumulation",
                "Total_Pressure": "Total Stage Pressure"
            }
        )
    )

    fig_pressure = px.line(
        pressure_plot_df,
        x="Month",
        y="Pressure",
        color="Stage",
        markers=True,
        title="Monthly Stage Pressure"
    )

    fig_pressure.add_hline(
        y=pressure_threshold,
        line_dash="dash",
        annotation_text="Configured pressure threshold",
        annotation_position="top left"
    )

    fig_pressure.update_layout(
        height=480,
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(
        fig_pressure,
        use_container_width=True
    )


    # --------------------------------------------------------
    # Top bottleneck periods
    # --------------------------------------------------------

    st.markdown(
        "### Highest Pressure Reporting Periods"
    )

    top_pressure = (
        filtered_df[
            [
                "Date",
                "CBP_Accumulation",
                "HHS_Accumulation",
                "Total_Stage_Pressure",
                "Transfer_Efficiency_Pct",
                "Discharge_Effectiveness_Pct"
            ]
        ]
        .sort_values(
            "Total_Stage_Pressure",
            ascending=False
        )
        .head(15)
        .copy()
    )

    top_pressure["Date"] = (
        top_pressure["Date"]
        .dt.strftime("%Y-%m-%d")
    )

    top_pressure = top_pressure.rename(
        columns={
            "Date": "Date",
            "CBP_Accumulation": "CBP Accumulation",
            "HHS_Accumulation": "HHS Accumulation",
            "Total_Stage_Pressure": "Total Stage Pressure",
            "Transfer_Efficiency_Pct": "Transfer Efficiency %",
            "Discharge_Effectiveness_Pct":
                "Discharge Effectiveness %"
        }
    )

    st.dataframe(
        top_pressure,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # Bottleneck scatter plot
    # --------------------------------------------------------

    fig_scatter = px.scatter(
        filtered_df,
        x="Transfer_Efficiency_Pct",
        y="Total_Stage_Pressure",
        size="HHS_Care",
        hover_data=[
            "Date",
            "CBP_Custody",
            "CBP_Transfers",
            "HHS_Discharges"
        ],
        title="Transfer Efficiency vs Total Stage Pressure"
    )

    fig_scatter.add_vline(
        x=transfer_threshold,
        line_dash="dash",
        annotation_text="Transfer threshold"
    )

    fig_scatter.add_hline(
        y=pressure_threshold,
        line_dash="dash",
        annotation_text="Pressure threshold"
    )

    fig_scatter.update_layout(
        height=500,
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis_title="Transfer Efficiency (%)",
        yaxis_title="Total Stage Pressure"
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )


    # --------------------------------------------------------
    # Existing model flags
    # --------------------------------------------------------

    flag_columns = [
        "CBP_Transfer_Bottleneck_Flag",
        "HHS_Discharge_Bottleneck_Flag",
        "Any_Bottleneck_Flag",
        "Transfer_Stagnation_Flag",
        "Discharge_Stagnation_Flag",
        "Operational_Anomaly_Flag",
        "HHS_Performance_Deterioration_Flag"
    ]

    available_flags = [
        c for c in flag_columns
        if c in filtered_df.columns
    ]

    if available_flags:

        st.markdown(
            "### Existing Analytical Flags"
        )

        flag_summary = []

        for col in available_flags:

            count = filtered_df[col].fillna(False).sum()

            flag_summary.append(
                {
                    "Flag": col.replace("_", " "),
                    "Observations": int(count)
                }
            )

        flag_summary_df = pd.DataFrame(
            flag_summary
        )

        fig_flags = px.bar(
            flag_summary_df,
            x="Flag",
            y="Observations",
            text="Observations",
            title="Existing Analytical Alerts"
        )

        fig_flags.update_traces(
            textposition="outside"
        )

        fig_flags.update_layout(
            height=450,
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis_tickangle=-35
        )

        st.plotly_chart(
            fig_flags,
            use_container_width=True
        )


# ============================================================
# TAB 4 — OUTCOME TREND ANALYSIS
# ============================================================

with tab4:

    st.markdown(
        '<div class="section-title">Outcome Trend Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Monitor discharge performance, stability and year-over-year '
        'changes in observed outcomes.'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # Outcome cards
    # --------------------------------------------------------

    o1, o2, o3, o4 = st.columns(4)

    with o1:

        st.metric(
            "Avg Discharge Effectiveness",
            f"{avg_discharge_effectiveness:.2f}%"
        )

    with o2:

        st.metric(
            "Outcome Stability",
            f"{avg_outcome_stability:.1f}/100"
        )

    with o3:

        st.metric(
            "Average HHS Care",
            f"{avg_hhs_care:,.0f}"
        )

    with o4:

        st.metric(
            "Average HHS Pressure",
            f"{avg_hhs_pressure:,.0f}"
        )


    # --------------------------------------------------------
    # Outcome trend
    # --------------------------------------------------------

    outcome_trend = (
        filtered_df
        .groupby(
            filtered_df["Date"].dt.to_period("M")
        )
        .agg(
            Discharge_Effectiveness=(
                "Discharge_Effectiveness_Pct",
                "mean"
            ),
            Outcome_Stability=(
                "Outcome_Stability_Score",
                "mean"
            ),
            Avg_HHS_Care=(
                "HHS_Care",
                "mean"
            ),
            Total_Discharges=(
                "HHS_Discharges",
                "sum"
            )
        )
        .reset_index()
    )

    outcome_trend["Month"] = (
        outcome_trend["Date"]
        .astype(str)
    )


    outcome_metric = st.selectbox(
        "Select outcome metric",
        [
            "Discharge Effectiveness",
            "Outcome Stability",
            "Average HHS Care",
            "Total HHS Discharges"
        ]
    )


    if outcome_metric == "Discharge Effectiveness":

        outcome_y = "Discharge_Effectiveness"

        outcome_title = (
            "Monthly Discharge Effectiveness"
        )

    elif outcome_metric == "Outcome Stability":

        outcome_y = "Outcome_Stability"

        outcome_title = (
            "Monthly Outcome Stability Score"
        )

    elif outcome_metric == "Average HHS Care":

        outcome_y = "Avg_HHS_Care"

        outcome_title = (
            "Monthly Average HHS Care"
        )

    else:

        outcome_y = "Total_Discharges"

        outcome_title = (
            "Monthly HHS Discharges"
        )


    fig_outcome = px.line(
        outcome_trend,
        x="Month",
        y=outcome_y,
        markers=True,
        title=outcome_title
    )

    if outcome_metric == "Discharge Effectiveness":

        fig_outcome.add_hline(
            y=discharge_threshold,
            line_dash="dash",
            annotation_text="Configured alert threshold"
        )

    fig_outcome.update_layout(
        height=450,
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(
        fig_outcome,
        use_container_width=True
    )


    # --------------------------------------------------------
    # Yearly comparison
    # --------------------------------------------------------

    st.markdown(
        "### Year-over-Year Outcome Comparison"
    )

    yearly_outcome = (
        filtered_df
        .groupby("Year", as_index=False)
        .agg(
            Total_Intake=(
                "CBP_Intake",
                "sum"
            ),
            Total_Transfers=(
                "CBP_Transfers",
                "sum"
            ),
            Total_Discharges=(
                "HHS_Discharges",
                "sum"
            ),
            Avg_Transfer_Efficiency=(
                "Transfer_Efficiency_Pct",
                "mean"
            ),
            Avg_Discharge_Effectiveness=(
                "Discharge_Effectiveness_Pct",
                "mean"
            ),
            Avg_Outcome_Stability=(
                "Outcome_Stability_Score",
                "mean"
            ),
            Avg_CBP_Pressure=(
                "CBP_Accumulation",
                "mean"
            ),
            Avg_HHS_Pressure=(
                "HHS_Accumulation",
                "mean"
            )
        )
    )


    st.dataframe(
        yearly_outcome.style.format(
            {
                "Total_Intake": "{:,.0f}",
                "Total_Transfers": "{:,.0f}",
                "Total_Discharges": "{:,.0f}",
                "Avg_Transfer_Efficiency": "{:.2f}%",
                "Avg_Discharge_Effectiveness":
                    "{:.2f}%",
                "Avg_Outcome_Stability":
                    "{:.1f}",
                "Avg_CBP_Pressure":
                    "{:,.1f}",
                "Avg_HHS_Pressure":
                    "{:,.1f}"
            }
        ),
        use_container_width=True
    )


    # --------------------------------------------------------
    # Yearly efficiency chart
    # --------------------------------------------------------

    yearly_chart = yearly_outcome[
        [
            "Year",
            "Avg_Transfer_Efficiency",
            "Avg_Discharge_Effectiveness"
        ]
    ].melt(
        id_vars="Year",
        var_name="Metric",
        value_name="Value"
    )

    yearly_chart["Metric"] = (
        yearly_chart["Metric"]
        .replace(
            {
                "Avg_Transfer_Efficiency":
                    "Transfer Efficiency",
                "Avg_Discharge_Effectiveness":
                    "Discharge Effectiveness"
            }
        )
    )

    fig_yearly = px.bar(
        yearly_chart,
        x="Year",
        y="Value",
        color="Metric",
        barmode="group",
        text_auto=".2f",
        title="Yearly Transfer and Discharge Efficiency"
    )

    fig_yearly.update_layout(
        height=450,
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis_title="Percentage"
    )

    st.plotly_chart(
        fig_yearly,
        use_container_width=True
    )


    # --------------------------------------------------------
    # Outcome deterioration detection
    # --------------------------------------------------------

    if "HHS_Performance_Deterioration_Flag" in filtered_df.columns:

        deterioration_count = (
            filtered_df[
                "HHS_Performance_Deterioration_Flag"
            ]
            .fillna(False)
            .sum()
        )

        st.markdown(
            f"""
            <div class="alert-warning">
                <b>HHS Performance Deterioration:</b>
                {deterioration_count:,} reporting observations are
                flagged at or below the analytical lower-quartile
                discharge effectiveness level.
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# DATASET INFORMATION
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">Dataset Information</div>',
    unsafe_allow_html=True
)

d1, d2, d3, d4 = st.columns(4)

with d1:
    st.metric(
        "Reporting Observations",
        f"{len(filtered_df):,}"
    )

with d2:
    st.metric(
        "Date Range",
        f"{(end_date - start_date).days:,} days"
    )

with d3:
    st.metric(
        "Dataset Rows",
        f"{len(df):,}"
    )

with d4:
    st.metric(
        "Dataset Columns",
        f"{len(df.columns):,}"
    )


# ============================================================
# OPTIONAL RAW DATA VIEW
# ============================================================

with st.expander("View Filtered Analytical Dataset"):

    display_df = filtered_df.copy()

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Care Transition Efficiency & Placement Outcome Analytics
        <br>
        Analytical dashboard built using the final project dataset.
    </div>
    """,
    unsafe_allow_html=True
)