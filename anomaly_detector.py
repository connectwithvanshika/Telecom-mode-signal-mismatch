import pandas as pd


class AnomalyDetector:

    def __init__(self, config):
        self.config = config
        self.rules = config["mode_signal_mismatch"]

    def detect(self, row):

        triggered_rules = []
        reasons = []
        severity = "None"

        if not self.rules["enabled"]:
            return {
                "Is Anomaly": "No",
                "Triggered Rules": "",
                "Severity": "None",
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

            failed_conditions = 0
            issue_list = []

            if rsrp < lte["rsrp_min"]:
                failed_conditions += 1
                issue_list.append(
                    f"RSRP ({rsrp} dBm) is below the LTE threshold ({lte['rsrp_min']} dBm)"
                )

            if rsrq < lte["rsrq_min"]:
                failed_conditions += 1
                issue_list.append(
                    f"RSRQ ({rsrq} dB) is below the LTE threshold ({lte['rsrq_min']} dB)"
                )

            if sinr < lte["sinr_min"]:
                failed_conditions += 1
                issue_list.append(
                    f"SINR ({sinr} dB) is below the LTE threshold ({lte['sinr_min']} dB)"
                )

            if signal_quality < lte["signal_quality_min"]:
                failed_conditions += 1
                issue_list.append(
                    f"Signal Quality ({signal_quality}) is below the LTE threshold ({lte['signal_quality_min']})"
                )

            if failed_conditions > 0:

                triggered_rules.append(self.rules["anomaly_name"])

                reasons.append(
                    "The device is operating in LTE mode, but the following signal metrics indicate degraded network performance: "
                    + "; ".join(issue_list)
                    + "."
                )

                if failed_conditions == 1:
                    severity = "Low"

                elif failed_conditions == 2:
                    severity = "Medium"

                else:
                    severity = "High"

        # ---------------- 5G ---------------- #

        elif "5G" in mode or "NR" in mode:

            nr5g = thresholds["NR5G"]

            failed_conditions = 0
            issue_list = []

            if rsrp < nr5g["rsrp_min"]:
                failed_conditions += 1
                issue_list.append(
                    f"RSRP ({rsrp} dBm) is below the 5G threshold ({nr5g['rsrp_min']} dBm)"
                )

            if sinr < nr5g["sinr_min"]:
                failed_conditions += 1
                issue_list.append(
                    f"SINR ({sinr} dB) is below the 5G threshold ({nr5g['sinr_min']} dB)"
                )

            if signal_quality < nr5g["signal_quality_min"]:
                failed_conditions += 1
                issue_list.append(
                    f"Signal Quality ({signal_quality}) is below the 5G threshold ({nr5g['signal_quality_min']})"
                )

            if failed_conditions > 0:

                triggered_rules.append(self.rules["anomaly_name"])

                reasons.append(
                    "The device is operating in 5G mode, but the following signal metrics indicate degraded network performance: "
                    + "; ".join(issue_list)
                    + "."
                )

                if failed_conditions == 1:
                    severity = "Low"

                elif failed_conditions == 2:
                    severity = "Medium"

                else:
                    severity = "High"

        return {
            "Is Anomaly": "Yes" if triggered_rules else "No",
            "Triggered Rules": ", ".join(triggered_rules),
            "Severity": severity,
            "Reason": " ".join(reasons)
        }

    def run(self, dataframe):

        results = []

        for _, row in dataframe.iterrows():

            anomaly = self.detect(row)

            output = row.to_dict()

            output["Is Anomaly"] = anomaly["Is Anomaly"]
            output["Triggered Rules"] = anomaly["Triggered Rules"]
            output["Severity"] = anomaly["Severity"]
            output["Reason"] = anomaly["Reason"]

            results.append(output)

        return pd.DataFrame(results)