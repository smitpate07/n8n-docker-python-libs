import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import json
import sys
import os
import uuid
import base64

def load_json(path):
    """Load JSON from file and normalize nested payload/data structure"""
    with open(path, "r") as f:
        data = json.load(f)

    # Case 1: unwrap [{...}]
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
        data = data[0]

    # Case 2: unwrap payload
    if isinstance(data, dict) and "payload" in data:
        data = data["payload"]

    # Case 3: unwrap data
    if isinstance(data, list) and len(data) > 0:
        if isinstance(data[0], dict) and "data" in data[0]:
            data = data[0]["data"]

    return data

def safe_to_numeric(df):
    """Try converting object cols to numeric"""
    for col in df.columns:
        if df[col].dtype == "object":
            try:
                df[col] = pd.to_numeric(df[col])
            except Exception:
                pass
    return df

def numeric_eda_charts(df: pd.DataFrame, output_file, json_file):
    df = safe_to_numeric(df)
    num_df = df.select_dtypes(include=[np.number])
    cat_df = df.select_dtypes(exclude=[np.number])

    # Missing values
    missing_pct = df.isnull().mean() * 100
    missing_summary = missing_pct.to_dict()

    # Outliers
    outlier_summary = {}
    for col in num_df.columns:
        Q1 = num_df[col].quantile(0.25)
        Q3 = num_df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = num_df[
            (num_df[col] < Q1 - 1.5 * IQR) | (num_df[col] > Q3 + 1.5 * IQR)
        ]
        outlier_summary[col] = len(outliers)

    # Correlations
    corr = num_df.corr(numeric_only=True)
    corr_summary = {"high": [], "medium": [], "low": []}
    if not corr.empty:
        for i in range(len(corr.columns)):
            for j in range(i + 1, len(corr.columns)):
                val = abs(corr.iloc[i, j])
                pair = f"{corr.columns[i]} vs {corr.columns[j]}"
                if val >= 0.7:
                    corr_summary["high"].append({pair: float(val)})
                elif val >= 0.4:
                    corr_summary["medium"].append({pair: float(val)})
                else:
                    corr_summary["low"].append({pair: float(val)})

    feature_counts = {"categorical": cat_df.shape[1], "numerical": num_df.shape[1]}

    # Plots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("EDA Summary", fontsize=16, fontweight="bold")

    # Missing values
    if missing_pct.sum() == 0:
        axes[0, 0].text(0.5, 0.5, "No missing values", ha="center", va="center", fontsize=14)
        axes[0, 0].set_xticks([])
        axes[0, 0].set_yticks([])
        axes[0, 0].set_title("% Missing Values")
    else:
        sns.barplot(x=missing_pct.index, y=missing_pct.values, ax=axes[0, 0])
        axes[0, 0].set_title("% Missing Values")
        axes[0, 0].tick_params(axis="x", rotation=45)

    # Boxplots
    if not num_df.empty:
        sns.boxplot(data=num_df, orient="h", ax=axes[0, 1])
        axes[0, 1].set_title("Boxplots")
    else:
        axes[0, 1].text(0.5, 0.5, "No numeric data", ha="center", va="center", fontsize=14)
        axes[0, 1].set_xticks([])
        axes[0, 1].set_yticks([])

    # Correlation heatmap
    if not corr.empty:
        sns.heatmap(corr, cmap="coolwarm", annot=True, fmt=".2f", cbar=True, ax=axes[1, 0])
        axes[1, 0].set_title("Correlation Matrix")
    else:
        axes[1, 0].text(0.5, 0.5, "No correlation", ha="center", va="center", fontsize=14)
        axes[1, 0].set_xticks([])
        axes[1, 0].set_yticks([])

    # Feature counts
    sns.barplot(x=list(feature_counts.keys()), y=list(feature_counts.values()), ax=axes[1, 1])
    axes[1, 1].set_title("Feature Counts")
    axes[1, 1].set_ylabel("Count")

    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    plt.close()

    summary = {
        "missing_values_pct": missing_summary,
        "outliers": outlier_summary,
        "correlation_summary": corr_summary,
        "feature_counts": feature_counts,
    }

    with open(json_file, "w") as f:
        json.dump(summary, f, indent=4)

    return output_file, summary

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise RuntimeError("Usage: python3 n_test.py <input.json>")

    input_file = sys.argv[1]
    data = load_json(input_file)
    df = pd.DataFrame(data)

    base_dir = os.path.dirname(input_file)
    chart_file = os.path.join(base_dir, f"eda_chart_{uuid.uuid4().hex}.png")
    summary_file = os.path.join(base_dir, f"eda_summary_{uuid.uuid4().hex}.json")

    output_file, summary = numeric_eda_charts(df, chart_file, summary_file)

    # Encode chart to Base64
    with open(chart_file, "rb") as f:
        chart_base64 = base64.b64encode(f.read()).decode("utf-8")

    # Encode summary JSON as Base64 too (optional)
    with open(summary_file, "rb") as f:
        summary_base64 = base64.b64encode(f.read()).decode("utf-8")

    manifest = {
        "summary": summary,
        "chart": {
            "fileName": "eda_chart.png",
            "mimeType": "image/png",
            "data": chart_base64
        },
        "summary_file": {
            "fileName": "eda_summary.json",
            "mimeType": "application/json",
            "data": summary_base64
        }
    }

    print(json.dumps(manifest, indent=4))