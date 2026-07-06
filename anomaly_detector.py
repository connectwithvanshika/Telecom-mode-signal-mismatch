import pandas as pd


class AnomalyDetector:

    def __init__(self, config):
        self.config = config
        self.rules = config["mode_signal_mismatch"]

    def detect(self, row):

        triggered_rules = []
        reasons = []

        if not self.rules["enabled"]:
            return {
                "Triggered Rules": "",
                "Reason": ""
            }

        mode = str(row[self.rules["network_mode_column"]]).upper()

        rsrp = float(str(row[self.rules["rsrp_column"]]).replace("dBm", "").strip())

        rsrq = float(str(row[self.rules["rsrq_column"]]).replace("dB", "").strip())

        sinr = float(str(row[self.rules["sinr_column"]]).replace("dB", "").strip())

        signal_quality = float(row[self.rules["signal_quality_column"]])

        thresholds = self.rules["thresholds"]

        # ---------------- LTE ---------------- #

        if "LTE" in mode:

            lte = thresholds["LTE"]

            if (
                rsrp < lte["rsrp_min"] or
                rsrq < lte["rsrq_min"] or
                sinr < lte["sinr_min"] or
                signal_quality < lte["signal_quality_min"]
            ):

                triggered_rules.append(
                    self.rules["anomaly_name"]
                )

                reasons.append(
                    "Poor signal quality for LTE mode."
                )

        # ---------------- 5G ---------------- #

        elif "5G" in mode or "NR" in mode:

            nr5g = thresholds["NR5G"]

            if (
                rsrp < nr5g["rsrp_min"] or
                sinr < nr5g["sinr_min"] or
                signal_quality < nr5g["signal_quality_min"]
            ):

                triggered_rules.append(
                    self.rules["anomaly_name"]
                )

                reasons.append(
                    "Poor signal quality for 5G mode."
                )

        return {
            "Triggered Rules": ", ".join(triggered_rules),
            "Reason": ", ".join(reasons)
        }

    def run(self, dataframe):

        results = []

        for _, row in dataframe.iterrows():

            anomaly = self.detect(row)

            output = row.to_dict()

            output["Triggered Rules"] = anomaly["Triggered Rules"]
            output["Reason"] = anomaly["Reason"]

            results.append(output)

        return pd.DataFrame(results)