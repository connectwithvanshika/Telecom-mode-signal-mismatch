# Mode–Signal Mismatch Detector

A simple rule-based telecom anomaly detector that identifies inconsistencies between the reported Network Mode (RAT) and observed signal quality metrics such as RSRP, RSRQ, SINR, RSSI, and Signal Quality.

## Project Structure

- config/
- data/
- output/
- anomaly_detector.py
- main.py

## Output

The detector generates:

output/anomaly_report.csv