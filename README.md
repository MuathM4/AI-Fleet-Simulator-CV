# 🚘 AI-Fleet-Simulator-CV: Vision-Based Driver Behavior Analytics (Phase 2)

**Jul 2026 – Present** *Building on Phase 1’s IoT Telematics Framework by integrating real-time Computer Vision and Sensor Fusion.*

---

## 📌 Executive Summary

**AI-Fleet-Simulator Phase 2** extends the original [AI-Fleet-Simulator (Phase 1)](https://github.com/MuathM4/AI-Fleet-Simulator) telemetry data collection pipeline by adding a computer vision analytics layer. 

Using **11.5 hours of continuous simulation footage** across 10 transport missions, this project synchronizes image frames extracted from camera streams with logged physical telematics ground truth (speed, steering, RPM, G-force). The objective is **sensor fusion validation**: comparing visual observations (object & lane detection) against IoT telematics data and calculating percentage discrepancies to identify where vision models excel versus where physical sensors lack environmental context.

* **🎥 Dataset & Demo Footage:** [11.5 Hours Driving Dataset Video](https://youtu.be/aWDoQomXQu8)
* **💻 Phase 1 Repository:** [MuathM4/AI-Fleet-Simulator](https://github.com/MuathM4/AI-Fleet-Simulator)
* **💻 Phase 2 Repository:** [MuathM4/AI-Fleet-Simulator-CV](https://github.com/MuathM4/AI-Fleet-Simulator-CV)

---

## 🛠️ Tech Stack & Skills

* **Core Computer Vision:** OpenCV, YOLO (You Only Look Once)
* **Data Engineering & Processing:** Python, Pandas, NumPy, Glob
* **Machine Learning & Analytics:** Scikit-Learn, Sensor Fusion, Temporal Alignment
* **Simulation & Logging:** Euro Truck Simulator 2 (ETS2), IoT Telemetry Logging

---

## 📊 Telematics & Video Synchronization Performance

Before passing visual data to detection models, video frames were sampled, compressed, and time-aligned with ground-truth sensor rows using custom nearest-neighbor timestamp matching and clock-rollover correction logic.

| Transport Mission | Active Telematics Rows | Frames Extracted | Frames Matched | Coverage (%) | Frame Utilization (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Job 1** | 5,540 | 5,395 | 5,240 | **94.58%** | **97.13%** |
| **Job 2** | 5,207 | 7,927 | 5,204 | **99.94%** | **65.65%** |
| **Job 3** | 3,570 | 3,803 | 3,567 | **99.92%** | **93.79%** |

*Note: In Job 2, telematics data was automatically trimmed to match the active duration of the video stream, raising effective temporal coverage to **99.94%**.*

---

## 🖼️ Terminal Synchronization Output Proofs

#### Job 1 Output
![Job 1 Sync Summary](docs/images/job1_sync_summary.png)

#### Job 2 Output
![Job 2 Sync Summary](docs/images/job2_sync_summary.png)

#### Job 3 Output
![Job 3 Sync Summary](docs/images/job3_sync_summary.png)

---

## 🚀 How to Run the Pipeline

### 1. Frame Extraction
Extract frames from video footage into time-indexed JPEG images:
```bash
python src/video_processing_cv.py

2. Synchronization
Align extracted image frames with ground truth CSV telemetry logs:

Bash
python src/sync_telematics.py
🔗 Author
Muath Makhlouf – LinkedIn Profile | GitHub Profile
2. Synchronization
Align extracted image frames with ground truth CSV telemetry logs:

Bash
python src/sync_telematics.py
🔗 Author
Muath Makhlouf – LinkedIn Profile | GitHub Profile
