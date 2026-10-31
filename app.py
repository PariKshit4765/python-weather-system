"""
Weather Data Analysis System - Interactive Streamlit Dashboard
==============================================================
An interactive, clickable web application to visualize, analyze, simulate,
and edit daily weather records. Built with Python, Pandas, Matplotlib, and Streamlit.

Author: Antigravity
"""

import os
import pandas as pd
import streamlit as st

from weather_analysis import (
    load_weather_data,
    calculate_temperature_stats,
    calculate_humidity_stats,
    calculate_rainfall_stats,
    calculate_wind_stats,
    generate_weather_summary,
    plot_temperature_trend,
    plot_daily_rainfall,
    plot_humidity_trend,
    evaluate_weather_condition,
    calculate_feels_like,
)

# ---------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="Weather Data Analysis System",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom styling for dashboard
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1e3a8a;
        margin-bottom: 0px;
    }
    .metric-container {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 14px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .summary-card {
        background-color: #f0fdf4;
        border-left: 5px solid #22c55e;
        padding: 14px 18px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    .chart-box {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def init_session_state(default_csv):
    """Initializes and manages session state for interactive editing."""
    if "weather_df" not in st.session_state:
        if os.path.exists(default_csv):
            st.session_state.weather_df = load_weather_data(default_csv)
            st.session_state.original_df = st.session_state.weather_df.copy()
        else:
            st.session_state.weather_df = pd.DataFrame()
            st.session_state.original_df = pd.DataFrame()

    if "quick_filter" not in st.session_state:
        st.session_state.quick_filter = "All"


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    default_csv = os.path.join(base_dir, "weather_data.csv")
    init_session_state(default_csv)

    # ---------------------------------------------------------
    # Header Section
    # ---------------------------------------------------------
    st.markdown("<h1 class='main-title'>🌤️ Weather Data Analysis System</h1>", unsafe_allow_html=True)
    st.markdown(
        "An **interactive, visual** weather analytics dashboard. "
        "Explore daily temperature, rainfall, and humidity graphs, run weather simulations, and edit data in real time."
    )
    st.divider()

    # ---------------------------------------------------------
    # Sidebar: Data Source & Filtering
    # ---------------------------------------------------------
    st.sidebar.header("⚙️ Controls & Settings")

    data_source = st.sidebar.radio(
        "Select Data Source:",
        ("Active Dataset (Session Data)", "Upload Custom CSV", "Reset to Default Sample"),
    )

    if data_source == "Reset to Default Sample":
        if st.sidebar.button("🔄 Confirm Reset to Default Sample"):
            st.session_state.weather_df = load_weather_data(default_csv)
            st.session_state.original_df = st.session_state.weather_df.copy()
            st.sidebar.success("Reset to default 30-day dataset!")
            st.rerun()

    elif data_source == "Upload Custom CSV":
        uploaded_file = st.sidebar.file_uploader(
            "Upload CSV (Date, Temperature, Humidity, Rainfall, Wind_Speed):",
            type=["csv"],
        )
        if uploaded_file is not None:
            temp_path = os.path.join(base_dir, "_temp_upload.csv")
            try:
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                uploaded_df = load_weather_data(temp_path)
                st.session_state.weather_df = uploaded_df
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                st.sidebar.success(f"Loaded {len(uploaded_df)} custom rows!")
            except Exception as e:
                st.sidebar.error(f"Error parsing file: {e}")

    df_current = st.session_state.weather_df

    if df_current.empty:
        st.error("No weather data available. Please upload a file or reset to the sample dataset.")
        return

    # Date Range Filter in Sidebar
    min_date = df_current["Date"].min().date()
    max_date = df_current["Date"].max().date()

    st.sidebar.subheader("📅 Date Range Filter")
    selected_dates = st.sidebar.date_input(
        "Pick Date Range:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    # Apply date range
    if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
        start_d, end_d = selected_dates
        filtered_df = df_current.loc[
            (df_current["Date"].dt.date >= start_d) & (df_current["Date"].dt.date <= end_d)
        ].copy()
    else:
        filtered_df = df_current.copy()

    # ---------------------------------------------------------
    # Clickable Quick-Filter Buttons
    # ---------------------------------------------------------
    st.subheader("🎯 Quick Interactive Filters")
    st.caption("Click any button below to immediately isolate specific weather conditions:")

    qcol1, qcol2, qcol3, qcol4, qcol5 = st.columns(5)

    if qcol1.button("🌐 All Days", use_container_width=True):
        st.session_state.quick_filter = "All"
    if qcol2.button("🌧️ Rainy Days Only", use_container_width=True):
        st.session_state.quick_filter = "Rain"
    if qcol3.button("☀️ Hot Days (>28°C)", use_container_width=True):
        st.session_state.quick_filter = "Hot"
    if qcol4.button("❄️ Cool Days (<23°C)", use_container_width=True):
        st.session_state.quick_filter = "Cool"
    if qcol5.button("💨 High Wind (>18 km/h)", use_container_width=True):
        st.session_state.quick_filter = "Wind"

    # Apply Quick Filter
    q_filter = st.session_state.quick_filter
    if q_filter == "Rain":
        active_df = filtered_df[filtered_df["Rainfall"] > 0].copy()
        st.info("Showing **Rainy Days Only** (Rainfall > 0 mm).")
    elif q_filter == "Hot":
        active_df = filtered_df[filtered_df["Temperature"] > 28.0].copy()
        st.info("Showing **Hot Days Only** (Temperature > 28°C).")
    elif q_filter == "Cool":
        active_df = filtered_df[filtered_df["Temperature"] < 23.0].copy()
        st.info("Showing **Cool Days Only** (Temperature < 23°C).")
    elif q_filter == "Wind":
        active_df = filtered_df[filtered_df["Wind_Speed"] > 18.0].copy()
        st.info("Showing **Breezy / High Wind Days Only** (Wind Speed > 18 km/h).")
    else:
        active_df = filtered_df.copy()

    if active_df.empty:
        st.warning("No records matched the selected quick filter in this date range.")
        return

    # Recalculate stats on the active filtered dataframe
    t_stats = calculate_temperature_stats(active_df)
    h_stats = calculate_humidity_stats(active_df)
    r_stats = calculate_rainfall_stats(active_df)
    w_stats = calculate_wind_stats(active_df)

    # ---------------------------------------------------------
    # Top KPI Metrics Row
    # ---------------------------------------------------------
    st.write("")
    mcol1, mcol2, mcol3, mcol4, mcol5 = st.columns(5)

    with mcol1:
        st.metric(label="🌡️ Avg Temperature", value=f"{t_stats['avg_temp']} °C")
    with mcol2:
        st.metric(label="🔥 Max Temperature", value=f"{t_stats['max_temp']} °C", delta=f"{t_stats['hottest_date']}")
    with mcol3:
        st.metric(label="❄️ Min Temperature", value=f"{t_stats['min_temp']} °C", delta=f"{t_stats['coldest_date']}", delta_color="inverse")
    with mcol4:
        st.metric(label="💧 Avg Humidity", value=f"{h_stats['avg_humidity']} %")
    with mcol5:
        st.metric(label="🌧️ Total Rainfall", value=f"{r_stats['total_rainfall']} mm", delta=f"{r_stats['rainy_days_count']} wet days")

    st.write("")

    # ---------------------------------------------------------
    # Main Tabs: CHARTS ARE NOW TAB 1 (FRONT & CENTER!)
    # ---------------------------------------------------------
    tab_charts, tab_overview, tab_simulator, tab_compare, tab_data = st.tabs([
        "📊 Weather Charts & Graphs",
        "📋 Observations & Summary",
        "🔮 Weather Simulator & Advisory",
        "⚖️ Compare Any 2 Days",
        "✏️ Live Editable Dataset",
    ])

    # ---------------------------------------------------------
    # TAB 1: Visualizations & Graphs (Prominently Displayed!)
    # ---------------------------------------------------------
    with tab_charts:
        st.subheader("📊 Meteorological Charts & Visualizations")

        chart_layout_col1, chart_layout_col2 = st.columns([2, 1])
        with chart_layout_col1:
            chart_style = st.radio(
                "Select Graph Engine:",
                ("Interactive Hover/Zoom Charts (Streamlit)", "Publication Figures (Matplotlib)"),
                horizontal=True,
            )
        with chart_layout_col2:
            display_view = st.radio(
                "Layout View:",
                ("All 3 Graphs Together (Scroll to view)", "Tabbed Single View"),
                horizontal=True,
            )

        chart_df = active_df.copy()
        chart_df["DateStr"] = chart_df["Date"].dt.strftime("%b %d")
        chart_df = chart_df.set_index("DateStr")

        if display_view == "All 3 Graphs Together (Scroll to view)":
            st.markdown("---")

            # 1. Temperature Line Chart
            st.markdown("### 🌡️ 1. Daily Temperature Trend (°C)")
            st.caption("Shows temperature variations across days, highlighting warm spells and cool days.")
            if chart_style == "Interactive Hover/Zoom Charts (Streamlit)":
                st.line_chart(chart_df[["Temperature"]], color="#e65100", height=320)
            else:
                fig1 = plot_temperature_trend(active_df)
                st.pyplot(fig1, use_container_width=True)

            st.write("")

            # 2. Rainfall Bar Chart
            st.markdown("### 🌧️ 2. Daily Rainfall Distribution (mm)")
            st.caption(f"Total precipitation: **{r_stats['total_rainfall']} mm** across **{r_stats['rainy_days_count']} rainy days** (Max: {r_stats['max_rainfall']} mm on {r_stats['max_rain_date']}).")
            if chart_style == "Interactive Hover/Zoom Charts (Streamlit)":
                st.bar_chart(chart_df[["Rainfall"]], color="#0288d1", height=320)
            else:
                fig2 = plot_daily_rainfall(active_df)
                st.pyplot(fig2, use_container_width=True)

            st.write("")

            # 3. Humidity Area Chart
            st.markdown("### 💧 3. Daily Relative Humidity Variation (%)")
            st.caption(f"Relative humidity averages **{h_stats['avg_humidity']}%** (Range: {h_stats['min_humidity']}% to {h_stats['max_humidity']}%).")
            if chart_style == "Interactive Hover/Zoom Charts (Streamlit)":
                st.area_chart(chart_df[["Humidity"]], color="#00897b", height=320)
            else:
                fig3 = plot_humidity_trend(active_df)
                st.pyplot(fig3, use_container_width=True)

        else:
            # Tabbed View
            sub1, sub2, sub3 = st.tabs(["🌡️ Temperature Line Chart", "🌧️ Rainfall Bar Chart", "💧 Humidity Curve"])

            with sub1:
                st.markdown("#### Daily Temperature Trend (°C)")
                if chart_style == "Interactive Hover/Zoom Charts (Streamlit)":
                    st.caption("💡 *Hover over data points to see exact temperature values; scroll or drag to zoom.*")
                    st.line_chart(chart_df[["Temperature"]], color="#e65100", height=380)
                else:
                    fig1 = plot_temperature_trend(active_df)
                    st.pyplot(fig1, use_container_width=True)

            with sub2:
                st.markdown("#### Daily Rainfall Distribution (mm)")
                if chart_style == "Interactive Hover/Zoom Charts (Streamlit)":
                    st.caption(f"Total rainfall: **{r_stats['total_rainfall']} mm** across **{r_stats['rainy_days_count']} rainy days**.")
                    st.bar_chart(chart_df[["Rainfall"]], color="#0288d1", height=380)
                else:
                    fig2 = plot_daily_rainfall(active_df)
                    st.pyplot(fig2, use_container_width=True)

            with sub3:
                st.markdown("#### Relative Humidity Curve (%)")
                if chart_style == "Interactive Hover/Zoom Charts (Streamlit)":
                    st.caption(f"Average humidity: **{h_stats['avg_humidity']}%**.")
                    st.area_chart(chart_df[["Humidity"]], color="#00897b", height=380)
                else:
                    fig3 = plot_humidity_trend(active_df)
                    st.pyplot(fig3, use_container_width=True)

    # ---------------------------------------------------------
    # TAB 2: Observations & Summary
    # ---------------------------------------------------------
    with tab_overview:
        st.subheader("📋 Key Meteorological Observations")
        bullets = generate_weather_summary(active_df)

        col_sum1, col_sum2 = st.columns([2, 1])
        with col_sum1:
            box_html = "<div class='summary-card'><strong>Automated Weather Insights:</strong><ul style='margin-bottom:0; padding-left:20px;'>"
            for b in bullets:
                box_html += f"<li>{b}</li>"
            box_html += "</ul></div>"
            st.markdown(box_html, unsafe_allow_html=True)

        with col_sum2:
            st.success(
                f"**🔥 Peak Hottest Day**\n\n"
                f"**Date:** {t_stats['hottest_date']}\n\n"
                f"**Temperature:** {t_stats['hottest_temp']} °C"
            )
            st.info(
                f"**❄️ Lowest Coldest Day**\n\n"
                f"**Date:** {t_stats['coldest_date']}\n\n"
                f"**Temperature:** {t_stats['coldest_temp']} °C"
            )

    # ---------------------------------------------------------
    # TAB 3: Interactive Weather Simulator & Advisory (Clickable Tool)
    # ---------------------------------------------------------
    with tab_simulator:
        st.subheader("🔮 Interactive Weather Condition Simulator")
        st.markdown(
            "Adjust meteorological inputs using the sliders below and click **'Analyze Weather Condition'** "
            "to calculate the apparent 'Feels Like' temperature, comfort category, and activity advisory."
        )

        with st.form("weather_simulator_form"):
            sim_col1, sim_col2 = st.columns(2)
            with sim_col1:
                sim_temp = st.slider("Ambient Temperature (°C):", min_value=10.0, max_value=45.0, value=28.0, step=0.5)
                sim_humidity = st.slider("Relative Humidity (%):", min_value=10, max_value=100, value=65, step=1)

            with sim_col2:
                sim_rain = st.slider("Rainfall (mm):", min_value=0.0, max_value=60.0, value=0.0, step=0.5)
                sim_wind = st.slider("Wind Speed (km/h):", min_value=0.0, max_value=50.0, value=15.0, step=0.5)

            submitted = st.form_submit_button("🔍 Click to Analyze Weather Condition", use_container_width=True)

        if submitted:
            result = evaluate_weather_condition(sim_temp, sim_humidity, sim_rain, sim_wind)

            st.write("---")
            st.markdown("### 🎯 Simulation Analysis Result:")

            res_c1, res_c2, res_c3 = st.columns(3)
            with res_c1:
                st.metric(label="Calculated Condition", value=result["condition"])
            with res_c2:
                st.metric(label="Calculated 'Feels Like'", value=f"{result['feels_like']} °C", delta=f"{round(result['feels_like'] - sim_temp, 1)} °C vs actual")
            with res_c3:
                st.metric(label="Air Comfort Level", value=result["comfort"])

            st.info(f"**💡 Daily Outdoor Advisory:** {result['advisory']}")

    # ---------------------------------------------------------
    # TAB 4: Interactive Day Comparison Tool (Clickable Comparison)
    # ---------------------------------------------------------
    with tab_compare:
        st.subheader("⚖️ Compare Any Two Days Side-by-Side")
        st.markdown("Select two observation dates from the dataset and click **'Compare Days'** to evaluate how conditions shifted.")

        all_dates = [d.strftime("%Y-%m-%d") for d in df_current["Date"]]

        if len(all_dates) >= 2:
            ccol1, ccol2 = st.columns(2)
            with ccol1:
                day_1_str = st.selectbox("Select First Day (Day A):", all_dates, index=0)
            with ccol2:
                day_2_str = st.selectbox("Select Second Day (Day B):", all_dates, index=min(15, len(all_dates) - 1))

            if st.button("⚖️ Click to Compare Selected Days", use_container_width=True):
                row1 = df_current[df_current["Date"].dt.strftime("%Y-%m-%d") == day_1_str].iloc[0]
                row2 = df_current[df_current["Date"].dt.strftime("%Y-%m-%d") == day_2_str].iloc[0]

                diff_temp = round(row2["Temperature"] - row1["Temperature"], 1)
                diff_hum = round(row2["Humidity"] - row1["Humidity"], 1)
                diff_rain = round(row2["Rainfall"] - row1["Rainfall"], 1)
                diff_wind = round(row2["Wind_Speed"] - row1["Wind_Speed"], 1)

                st.write("")
                st.markdown(f"#### 📊 Comparison: **{day_1_str}** vs **{day_2_str}**")

                cmp_col1, cmp_col2, cmp_col3, cmp_col4 = st.columns(4)
                cmp_col1.metric("Temperature", f"{row2['Temperature']} °C", delta=f"{diff_temp:+} °C")
                cmp_col2.metric("Humidity", f"{row2['Humidity']} %", delta=f"{diff_hum:+} %")
                cmp_col3.metric("Rainfall", f"{row2['Rainfall']} mm", delta=f"{diff_rain:+} mm")
                cmp_col4.metric("Wind Speed", f"{row2['Wind_Speed']} km/h", delta=f"{diff_wind:+} km/h")
        else:
            st.info("At least two days of data are needed for side-by-side comparison.")

    # ---------------------------------------------------------
    # TAB 5: Live Editable Dataset (Click to Edit / Add / Save)
    # ---------------------------------------------------------
    with tab_data:
        st.subheader("✏️ Live Editable Weather Dataset")
        st.markdown(
            "Click on **any cell** in the table below to edit numbers directly! "
            "You can also check boxes, add rows, or delete rows. Click **'Save Edits'** to apply changes to the whole system."
        )

        editable_display = active_df.copy()
        editable_display["Date"] = editable_display["Date"].dt.strftime("%Y-%m-%d")

        edited_data = st.data_editor(
            editable_display,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            key="weather_editor",
        )

        save_col1, save_col2, save_col3 = st.columns([1, 1, 2])

        with save_col1:
            if st.button("💾 Save Edits to Session"):
                try:
                    reconstructed = edited_data.copy()
                    reconstructed["Date"] = pd.to_datetime(reconstructed["Date"])
                    st.session_state.weather_df = reconstructed
                    st.success("Changes saved! All metrics and charts updated.")
                    st.rerun()
                except Exception as err:
                    st.error(f"Failed to apply edits: {err}")

        with save_col2:
            if st.button("🔄 Discard Edits"):
                st.session_state.weather_df = st.session_state.original_df.copy()
                st.warning("Reverted changes to original dataset.")
                st.rerun()

        with save_col3:
            # Download button
            csv_bytes = st.session_state.weather_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Current Dataset (CSV)",
                data=csv_bytes,
                file_name="weather_data_updated.csv",
                mime="text/csv",
                use_container_width=True,
            )

        # Expandable Add Record Form
        with st.expander("➕ Click to Add a Single New Daily Record"):
            with st.form("add_record_form"):
                add_col1, add_col2 = st.columns(2)
                with add_col1:
                    new_date = st.date_input("Date:")
                    new_temp = st.number_input("Temperature (°C):", value=27.5, step=0.1)
                    new_humidity = st.number_input("Humidity (%):", value=60.0, step=1.0)
                with add_col2:
                    new_rain = st.number_input("Rainfall (mm):", value=0.0, step=0.1)
                    new_wind = st.number_input("Wind Speed (km/h):", value=14.0, step=0.1)

                add_submitted = st.form_submit_button("➕ Append Record to Dataset")

                if add_submitted:
                    new_row = pd.DataFrame([{
                        "Date": pd.to_datetime(new_date),
                        "Temperature": float(new_temp),
                        "Humidity": float(new_humidity),
                        "Rainfall": float(new_rain),
                        "Wind_Speed": float(new_wind),
                    }])
                    st.session_state.weather_df = pd.concat([st.session_state.weather_df, new_row], ignore_index=True)
                    st.session_state.weather_df = st.session_state.weather_df.sort_values(by="Date").reset_index(drop=True)
                    st.balloons()
                    st.success(f"Added record for {new_date}! Charts and metrics updated.")
                    st.rerun()


if __name__ == "__main__":
    main()
