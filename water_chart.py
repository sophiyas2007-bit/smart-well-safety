
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("gwl_manual_quarterly_cgwb_tn_2021_2025.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Select required columns
date_col = "Data Acquisition Time"
level_col = "Groundwater Level Quarterly Manual (meter)"

# Convert data
df[date_col] = pd.to_datetime(
    df[date_col], dayfirst=True, errors="coerce"
)
df[level_col] = pd.to_numeric(
    df[level_col], errors="coerce"
)

# Remove missing values
data = df.dropna(subset=[date_col, level_col])

# Calculate average water level by date
chart_data = data.groupby(date_col)[level_col].mean()

# Draw chart
plt.figure(figsize=(10, 5))
plt.plot(chart_data.index, chart_data.values, marker="o")

plt.title("Tamil Nadu Groundwater Level Analysis")
plt.xlabel("Date")
plt.ylabel("Groundwater Level (meter)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
