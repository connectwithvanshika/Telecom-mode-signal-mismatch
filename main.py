import pandas as pd
import yaml

from anomaly_detector import AnomalyDetector


def load_config():

    with open("config/config.yaml", "r") as file:
        return yaml.safe_load(file)


def main():

    config = load_config()

    input_file = config["dataset"]["input_file"]
    output_file = config["dataset"]["output_file"]

    print("Loading dataset...")

    df = pd.read_csv(input_file)

    print(f"Total records: {len(df)}")

    detector = AnomalyDetector(config)

    print("Running anomaly detection...")

    result = detector.run(df)

    result.to_csv(output_file, index=False)

    total_anomalies = result["Triggered Rules"].astype(bool).sum()

    print("Detection completed successfully!")
    print(f"Total anomalies detected: {total_anomalies}")
    print(f"Output saved to: {output_file}")


if __name__ == "__main__":
    main()