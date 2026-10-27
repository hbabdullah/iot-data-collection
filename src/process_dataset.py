
from pathlib import Path

import pandas as pd


# Find the main project folder and dataset.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "data" / "fact_energy_15m.parquet"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed_energy.csv"

# Signal IDs from the dataset's signal definitions.
SIGNALS = {
    4: "energy_kwh_15m_total",
    8: "demand_kw_total",
    12: "avg_power_kw_15m_total",
}


def main():
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    print("Reading industrial energy dataset...")

    # Read only the columns and signal types we need.
    df = pd.read_parquet(
        DATASET_PATH,
        columns=[
            "asset_id",
            "signal_id",
            "time",
            "value_float",
        ],
    )

    df = df[df["signal_id"].isin(SIGNALS)].copy()

    # Give each signal a meaningful name.
    df["signal_name"] = df["signal_id"].map(SIGNALS)

    # Convert the long-format data into one row per asset and time.
    processed = df.pivot_table(
        index=["asset_id", "time"],
        columns="signal_name",
        values="value_float",
        aggfunc="mean",
    ).reset_index()

    processed.columns.name = None

    # Save the processed real measurements.
    processed.to_csv(OUTPUT_PATH, index=False)

    print("\nDataset processing completed!")
    print(f"Processed rows: {len(processed):,}")
    print(f"Output file: {OUTPUT_PATH}")
    print("\nFirst five rows:")
    print(processed.head().to_string(index=False))


if __name__ == "__main__":
    main()
