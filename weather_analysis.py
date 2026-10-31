"""
Weather Data Analysis Module
============================
This module provides functions to load, validate, clean, and analyze daily
weather data from a CSV file. It calculates key statistics such as temperature
extremes, rainfall totals, and humidity averages, and generates informative
visualizations using Matplotlib.

Author: Antigravity
Project: Weather Data Analysis System
"""

import os
import pandas as pd
import matplotlib.pyplot as plt


# Expected columns in the weather dataset
REQUIRED_COLUMNS = ["Date", "Temperature", "Humidity", "Rainfall", "Wind_Speed"]


def load_weather_data(filepath="weather_data.csv"):
    """
    Loads weather data from a CSV file, validates required columns,
    cleans missing or invalid values, and parses dates.

    Parameters:
        filepath (str): Relative or absolute path to the CSV file.

    Returns:
        pd.DataFrame: Cleaned and formatted weather DataFrame.

    Raises:
        FileNotFoundError: If the CSV file cannot be located.
        ValueError: If required columns are missing or the file is empty.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Weather dataset not found at '{filepath}'. Please ensure the file exists.")

    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        raise ValueError(f"Unable to read the CSV file: {e}")

    if df.empty:
        raise ValueError("The provided CSV file is empty.")

    # Check for required columns
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Dataset is missing required columns: {', '.join(missing_cols)}")

    # Clean and convert data types
    df = df.copy()

    # Parse Date column
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])

    # Convert numerical columns to numeric types, coercing invalid values to NaN
    numeric_cols = ["Temperature", "Humidity", "Rainfall", "Wind_Speed"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Handle missing values gracefully
    # If rainfall is missing, assume 0.0 mm
    if df["Rainfall"].isnull().any():
        df["Rainfall"] = df["Rainfall"].fillna(0.0)

    # For other numerical columns, fill with the column mean
    for col in ["Temperature", "Humidity", "Wind_Speed"]:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].mean())

    # Sort sequentially by date
    df = df.sort_values(by="Date").reset_index(drop=True)

    return df


def calculate_temperature_stats(df):
    """
    Calculates average, maximum, and minimum temperatures,
    as well as the specific hottest and coldest days.

    Returns:
        dict: Temperature metrics and extreme day records.
    """
    avg_temp = df["Temperature"].mean()
    max_temp = df["Temperature"].max()
    min_temp = df["Temperature"].min()

    # Find rows for hottest and coldest days
    hottest_row = df.loc[df["Temperature"].idxmax()]
    coldest_row = df.loc[df["Temperature"].idxmin()]

    return {
        "avg_temp": round(float(avg_temp), 2),
        "max_temp": round(float(max_temp), 2),
        "min_temp": round(float(min_temp), 2),
        "hottest_date": hottest_row["Date"].strftime("%Y-%m-%d"),
        "hottest_temp": round(float(hottest_row["Temperature"]), 2),
        "coldest_date": coldest_row["Date"].strftime("%Y-%m-%d"),
        "coldest_temp": round(float(coldest_row["Temperature"]), 2),
    }


def calculate_humidity_stats(df):
    """
    Calculates average, maximum, and minimum humidity percentages.

    Returns:
        dict: Humidity summary statistics.
    """
    avg_humidity = df["Humidity"].mean()
    max_humidity = df["Humidity"].max()
    min_humidity = df["Humidity"].min()

    return {
        "avg_humidity": round(float(avg_humidity), 2),
        "max_humidity": round(float(max_humidity), 2),
        "min_humidity": round(float(min_humidity), 2),
    }


def calculate_rainfall_stats(df):
    """
    Calculates total rainfall, average rainfall across all days,
    count of rainy days, and peak rainfall day.

    Returns:
        dict: Rainfall summary statistics.
    """
    total_rainfall = df["Rainfall"].sum()
    avg_rainfall = df["Rainfall"].mean()
    rainy_days_count = int((df["Rainfall"] > 0).sum())

    max_rain_row = df.loc[df["Rainfall"].idxmax()]

    return {
        "total_rainfall": round(float(total_rainfall), 2),
        "avg_rainfall": round(float(avg_rainfall), 2),
        "rainy_days_count": rainy_days_count,
        "max_rainfall": round(float(max_rain_row["Rainfall"]), 2),
        "max_rain_date": max_rain_row["Date"].strftime("%Y-%m-%d"),
    }


def calculate_wind_stats(df):
    """
    Calculates average and maximum wind speed in km/h.

    Returns:
        dict: Wind speed statistics.
    """
    avg_wind = df["Wind_Speed"].mean()
    max_wind = df["Wind_Speed"].max()

    return {
        "avg_wind": round(float(avg_wind), 2),
        "max_wind": round(float(max_wind), 2),
    }


def generate_weather_summary(df):
    """
    Synthesizes the dataset into readable, human-friendly observations.

    Returns:
        list of str: Summary bullet points.
    """
    temp_stats = calculate_temperature_stats(df)
    hum_stats = calculate_humidity_stats(df)
    rain_stats = calculate_rainfall_stats(df)
    total_days = len(df)

    observations = [
        f"The dataset covers {total_days} consecutive days of recorded weather.",
        f"Temperatures averaged {temp_stats['avg_temp']}°C, fluctuating between {temp_stats['min_temp']}°C and {temp_stats['max_temp']}°C.",
        f"The peak temperature of {temp_stats['hottest_temp']}°C occurred on {temp_stats['hottest_date']}.",
        f"The lowest temperature recorded was {temp_stats['coldest_temp']}°C on {temp_stats['coldest_date']}.",
        f"Precipitation was observed on {rain_stats['rainy_days_count']} out of {total_days} days, totaling {rain_stats['total_rainfall']} mm.",
        f"The highest daily precipitation reached {rain_stats['max_rainfall']} mm on {rain_stats['max_rain_date']}.",
        f"Relative humidity averaged {hum_stats['avg_humidity']}%, spanning from {hum_stats['min_humidity']}% to {hum_stats['max_humidity']}%.",
    ]

    return observations


def calculate_feels_like(temp_c, humidity_pct):
    """
    Computes an estimated 'Feels Like' apparent temperature
    based on ambient temperature and relative humidity.
    """
    # Simplified apparent temperature approximation formula
    e = (humidity_pct / 100.0) * 6.105 * (2.71828 ** ((17.27 * temp_c) / (237.7 + temp_c)))
    feels_like = temp_c + 0.33 * e - 0.70 * 2.0 - 4.0
    return round(float(feels_like), 1)


def evaluate_weather_condition(temp, humidity, rainfall, wind):
    """
    Evaluates weather factors and returns an intuitive condition label,
    comfort category, and practical daily advisory.
    """
    if rainfall >= 15.0:
        condition = "🌧️ Heavy Rainfall / Stormy"
        advisory = "Expect heavy downpours. Carry an umbrella and avoid waterlogged routes."
    elif rainfall > 0.0:
        condition = "🌦️ Light Rain / Drizzle"
        advisory = "Intermittent rain showers. Keep rain gear handy."
    elif temp >= 32.0 and humidity >= 60:
        condition = "☀️ Very Hot & Muggy"
        advisory = "High heat and humidity. Stay hydrated and avoid strenuous midday sun."
    elif temp >= 30.0:
        condition = "☀️ Warm & Sunny"
        advisory = "Warm sunshine throughout the day. Suitable for normal outdoor plans."
    elif temp <= 21.0:
        condition = "🌤️ Cool & Breezy"
        advisory = "Crisp, cooler conditions. A light jacket or sweater may be comfortable."
    else:
        condition = "⛅ Pleasant & Mild"
        advisory = "Optimal temperate weather. Ideal for outdoor sports and travel."

    # Comfort assessment
    if humidity > 75:
        comfort = "High Moisture / Sticky"
    elif humidity < 40:
        comfort = "Dry Air"
    else:
        comfort = "Comfortable"

    feels_like = calculate_feels_like(temp, humidity)

    return {
        "condition": condition,
        "comfort": comfort,
        "advisory": advisory,
        "feels_like": feels_like,
    }


# =====================================================================
# Visualization Functions (Matplotlib)
# =====================================================================

def plot_temperature_trend(df):
    """
    Generates a line chart showing daily temperature changes over time.

    Returns:
        matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=(10, 4.5))
    date_labels = df["Date"].dt.strftime("%b %d")

    ax.plot(
        date_labels,
        df["Temperature"],
        color="#e65100",
        marker="o",
        linewidth=2,
        markersize=5,
        label="Daily Temperature (°C)",
    )

    # Highlight average line
    avg_temp = df["Temperature"].mean()
    ax.axhline(avg_temp, color="#bf360c", linestyle="--", alpha=0.7, label=f"Average ({avg_temp:.1f}°C)")

    ax.set_title("Daily Temperature Trend", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Date", fontsize=11, fontweight="normal")
    ax.set_ylabel("Temperature (°C)", fontsize=11, fontweight="normal")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper left")
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.tight_layout()

    return fig


def plot_daily_rainfall(df):
    """
    Generates a bar chart showing daily rainfall in millimeters.

    Returns:
        matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=(10, 4.5))
    date_labels = df["Date"].dt.strftime("%b %d")

    colors = ["#0288d1" if val > 0 else "#cfd8dc" for val in df["Rainfall"]]

    bars = ax.bar(
        date_labels,
        df["Rainfall"],
        color=colors,
        edgecolor="#01579b",
        linewidth=0.8,
        label="Rainfall (mm)",
    )

    ax.set_title("Daily Rainfall Distribution", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Date", fontsize=11, fontweight="normal")
    ax.set_ylabel("Rainfall (mm)", fontsize=11, fontweight="normal")
    ax.grid(axis="y", linestyle=":", alpha=0.6)
    ax.legend(loc="upper right")
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.tight_layout()

    return fig


def plot_humidity_trend(df):
    """
    Generates an area/line chart showing daily relative humidity levels.

    Returns:
        matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=(10, 4.5))
    date_labels = df["Date"].dt.strftime("%b %d")

    ax.plot(
        date_labels,
        df["Humidity"],
        color="#00897b",
        marker="s",
        linewidth=2,
        markersize=4,
        label="Humidity (%)",
    )
    ax.fill_between(date_labels, df["Humidity"], color="#80cbc4", alpha=0.35)

    ax.set_title("Daily Humidity Variation", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Date", fontsize=11, fontweight="normal")
    ax.set_ylabel("Humidity (%)", fontsize=11, fontweight="normal")
    ax.set_ylim(0, 100)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper left")
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.tight_layout()

    return fig


# =====================================================================
# Standalone CLI / Terminal Testing
# =====================================================================

def main():
    """
    Runs a terminal demonstration of the weather data analysis.
    Useful for testing the module independently of Streamlit.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "weather_data.csv")

    print("\n" + "=" * 60)
    print("      WEATHER DATA ANALYSIS SYSTEM - CLI REPORT")
    print("=" * 60)

    try:
        df = load_weather_data(csv_path)
    except Exception as err:
        print(f"Error loading data: {err}")
        return

    print(f"\n[+] Successfully loaded {len(df)} rows from {csv_path}\n")

    # Display dataset sample
    print("Dataset Sample (First 5 Days):")
    print("-" * 60)
    print(df.head().to_string(index=False))
    print("-" * 60)

    # Compute statistics
    t_stats = calculate_temperature_stats(df)
    h_stats = calculate_humidity_stats(df)
    r_stats = calculate_rainfall_stats(df)
    w_stats = calculate_wind_stats(df)

    print("\n--- Key Weather Metrics ---")
    print(f"  * Temperature: Avg = {t_stats['avg_temp']}°C | Min = {t_stats['min_temp']}°C | Max = {t_stats['max_temp']}°C")
    print(f"  * Hottest Day: {t_stats['hottest_date']} ({t_stats['hottest_temp']}°C)")
    print(f"  * Coldest Day: {t_stats['coldest_date']} ({t_stats['coldest_temp']}°C)")
    print(f"  * Humidity:    Avg = {h_stats['avg_humidity']}% | Min = {h_stats['min_humidity']}% | Max = {h_stats['max_humidity']}%")
    print(f"  * Rainfall:    Total = {r_stats['total_rainfall']} mm | Rainy Days = {r_stats['rainy_days_count']} days")
    print(f"  * Wind Speed:  Avg = {w_stats['avg_wind']} km/h | Max = {w_stats['max_wind']} km/h")

    print("\n--- Weather Observations ---")
    for bullet in generate_weather_summary(df):
        print(f"  - {bullet}")

    print("\n" + "=" * 60)
    print(" Analysis complete. Run 'streamlit run app.py' for interactive UI.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
