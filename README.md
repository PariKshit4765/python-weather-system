# Weather Data Analysis System 🌤️

A beginner-friendly Python mini project that analyzes historical weather data from a CSV file and presents interactive charts, statistics, and observations through a clean Streamlit dashboard.

---

## 📌 Table of Contents
1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Technologies Used](#technologies-used)
4. [Folder Structure](#folder-structure)
5. [Prerequisites](#prerequisites)
6. [How to Open in VS Code](#how-to-open-in-vs-code)
7. [How to Run the Project](#how-to-run-the-project)
   - [Method 1: One-Click Launcher (Windows)](#method-1-one-click-launcher-windows)
   - [Method 2: Manual Terminal Commands](#method-2-manual-terminal-commands)
   - [Method 3: Standalone CLI Analysis](#method-3-standalone-cli-analysis)
8. [Dataset Description](#dataset-description)
9. [Troubleshooting & Common Questions](#troubleshooting--common-questions)
10. [College Demonstration & Viva Tips](#college-demonstration--viva-tips)

---

## 📖 Project Overview

The **Weather Data Analysis System** is designed as a practical, lightweight college mini project. It reads daily meteorological measurements (temperature, humidity, rainfall, and wind speed) stored in a CSV file and produces:
- Summary metrics (average, maximum, and minimum values)
- Detection of the hottest and coldest days
- Informative visual graphs (temperature line charts, rainfall bar charts, humidity curves)
- A plain-language summary of observations
- A complete interactive data table with CSV export capability

No machine learning models, external paid APIs, or active internet connections are required to run the analysis.

---

## ✨ Key Features

- **Interactive, Clickable Features**:
  - **Quick Filter Action Buttons**: Click one button to isolate `Rainy Days`, `Hot Days (>28°C)`, `Cool Days (<23°C)`, or `High Wind Days (>18 km/h)`.
  - **Interactive Weather Simulator**: Adjust sliders for temperature, humidity, rainfall, and wind speed, then click **"Analyze Weather Condition"** to calculate apparent "Feels Like" temperature, comfort categories, and outdoor activity advisories.
  - **Interactive Day Comparison Tool**: Select any two dates and click **"Compare Selected Days"** to see side-by-side delta variations.
  - **Live Editable Dataset (`st.data_editor`)**: Click directly on any cell to edit data live, add new rows, or delete rows, then click **"Save Edits"** to dynamically update all statistics.
  - **Append Single Record Form**: Form to add an observation day with instant balloon animation and recalculation.
- **Dynamic Visualizations**:
  - Toggle between **Interactive Streamlit Charts** (hover for exact tooltip numbers, zoom, pan) and **Matplotlib Figures**.
- **Automated Data Validation & Cleaning**: Validates CSV schema, handles missing values, and parses dates automatically.
- **Statistical Aggregation**:
  - Calculates average, maximum, and minimum temperatures.
  - Identifies the specific date and temperature for the hottest and coldest days.
  - Computes total precipitation, daily rainfall average, and count of rainy days.
  - Computes average relative humidity and wind speed.
- **Terminal CLI Mode**: `weather_analysis.py` can be executed directly in the terminal to print formatted statistics without launching a web browser.

---

## 🛠️ Technologies Used

| Technology | Purpose |
| :--- | :--- |
| **Python 3.9+** | Core programming language |
| **Pandas** | Data loading, manipulation, cleaning, and aggregation |
| **Matplotlib** | Generating line charts, bar plots, and trend graphs |
| **Streamlit** | Web application framework for the interactive dashboard |

---

## 📁 Folder Structure

```text
Weather_Data_Analysis/
│
├── app.py                  # Main Streamlit web dashboard application
├── weather_analysis.py     # Core data processing, analytics, and plotting functions
├── weather_data.csv        # Realistic 30-day sample meteorological dataset
├── requirements.txt        # Required Python dependencies
├── run_project.bat         # Automated 1-click batch script for Windows
├── .gitignore              # Ignores virtual environment and temporary files
└── README.md               # Complete project documentation and guide
```

---

## 📋 Prerequisites

Make sure you have **Python 3.9 or newer** installed on your system.

### How to Install Python on Windows:
1. Visit the official Python download page: [python.org/downloads](https://www.python.org/downloads/)
2. Download the latest Python installer for Windows.
3. Run the installer and **ensure you check the box that says "Add Python to PATH"** before clicking "Install Now".
4. Open Command Prompt (`cmd`) and verify the installation:
   ```cmd
   python --version
   ```

---

## 💻 How to Open in VS Code

1. Launch **Visual Studio Code**.
2. Click **File** > **Open Folder...** (or press `Ctrl + K, Ctrl + O`).
3. Browse to and select the `Weather_Data_Analysis` folder:
   ```text
   C:\Users\hp\.gemini\antigravity\scratch\Weather_Data_Analysis
   ```
4. Click **Select Folder**.
5. You should now see all project files listed in the VS Code Explorer sidebar on the left.

---

## 🚀 How to Run the Project

### Method 1: One-Click Launcher (Windows)
1. In Windows File Explorer or VS Code, double-click the **`run_project.bat`** file.
2. The batch script will automatically:
   - Verify Python is installed.
   - Create a virtual environment (`.venv`) if one does not exist.
   - Install all required libraries from `requirements.txt`.
   - Launch the Streamlit application and open `http://localhost:8501` in your default web browser.

---

### Method 2: Manual Terminal Commands (VS Code Terminal)

If you prefer using the VS Code integrated terminal:

1. In VS Code, open a new terminal:
   - Press `` Ctrl + ` `` (Backtick) or go to menu **Terminal** > **New Terminal**.
2. Ensure you are in the project folder:
   ```powershell
   cd Weather_Data_Analysis
   ```
3. Create a virtual environment:
   ```powershell
   python -m venv .venv
   ```
4. Activate the virtual environment:
   - On Windows (PowerShell):
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   - On Windows (Command Prompt):
     ```cmd
     .venv\Scripts\activate.bat
     ```
   *(If PowerShell displays a script execution policy error, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and retry)*
5. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
6. Run the Streamlit dashboard:
   ```powershell
   streamlit run app.py
   ```
7. Streamlit will display the local URL (usually `http://localhost:8501`). The browser opens automatically.

To stop the web server at any time, click in the terminal and press `Ctrl + C`.

---

### Method 3: Standalone CLI Analysis (Quick Terminal Test)

You can also run the analytics script directly in the terminal without opening a browser:

```powershell
python weather_analysis.py
```

This will load `weather_data.csv`, compute all summary metrics, and print a formatted console report showing temperatures, rainfall statistics, extreme days, and observations.

---

## 📊 Dataset Description

The sample file `weather_data.csv` contains 30 consecutive daily entries formatted as follows:

| Column | Type | Example | Description |
| :--- | :--- | :--- | :--- |
| `Date` | Date (`YYYY-MM-DD`) | `2026-03-01` | Day of observation |
| `Temperature` | Float | `24.5` | Average daily temperature in °C |
| `Humidity` | Integer/Float | `62` | Relative humidity percentage (%) |
| `Rainfall` | Float | `14.5` | Daily precipitation in millimeters (mm) |
| `Wind_Speed` | Float | `14.2` | Wind speed in kilometers per hour (km/h) |

---

## ❓ Troubleshooting & Common Questions

### 1. `'python' is not recognized as an internal or external command`
- **Cause**: Python was not added to your system environment variables.
- **Fix**: Reinstall Python from [python.org](https://www.python.org/) and make sure to check the box **"Add Python to PATH"**.

### 2. `'streamlit' is not recognized`
- **Cause**: Streamlit was installed inside the virtual environment, but the virtual environment is not activated.
- **Fix**: Run `.\.venv\Scripts\activate` first, then run `streamlit run app.py`.

### 3. `Execution of scripts is disabled on this system` (PowerShell)
- **Cause**: Windows PowerShell security policy restricts unsigned scripts.
- **Fix**: Run this in PowerShell before activating:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  ```
  Or use the Command Prompt (`cmd`) terminal instead.

### 4. Port 8501 is already in use
- **Fix**: Specify another port when launching:
  ```powershell
  streamlit run app.py --server.port 8502
  ```

---

## 🎓 College Demonstration & Viva Tips

When explaining this project to an examiner or instructor:
1. **Explain the Modular Architecture**: Point out the separation of concerns:
   - `weather_analysis.py` handles the pure data processing, statistical computations, and chart rendering logic.
   - `app.py` acts as the presentation layer, consuming the functions from `weather_analysis.py` and rendering them in Streamlit.
2. **Explain Data Cleaning**: Mention how `load_weather_data()` uses `pd.to_datetime` and `pd.to_numeric(..., errors='coerce')` to guarantee missing or corrupted records won't crash the system.
3. **Key Functions to Highlight**:
   - `calculate_temperature_stats()`: Uses `.idxmax()` and `.idxmin()` to identify the exact dates of extreme temperatures.
   - `calculate_rainfall_stats()`: Evaluates condition `(df["Rainfall"] > 0).sum()` to count wet weather days.
4. **Demonstrate Interactivity**: Show the date filter in the sidebar to demonstrate how metrics and charts update dynamically.
