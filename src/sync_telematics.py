import os
import glob
import pandas as pd

def print_summary(df, total_frames):
    # Stats on the active matched range
    total_rows = len(df)
    matched = df['frame_filename'].notna().sum()
    coverage = (matched / total_rows) * 100 if total_rows > 0 else 0
    used = (matched / total_frames) * 100 if total_frames > 0 else 0

    print("\n---- Sync Summary ----")
    print(f"Telematics rows (Active): {total_rows}")
    print(f"Frames found:            {total_frames}")
    print(f"Frames matched:          {matched}")
    print(f"Coverage:                {coverage:.2f}%")
    print(f"Frame use:               {used:.2f}%")
    print("-----------------------\n")

def time_to_seconds(ts):
    try:
        parts = str(ts).split(':')
        if len(parts) == 2:
            minutes, seconds = parts
            return float(minutes) * 60 + float(seconds)
        elif len(parts) == 3:
            hours, minutes, seconds = parts
            return float(hours) * 3600 + float(minutes) * 60 + float(seconds)
        else:
            return float(ts)
    except:
        return None

def sync_frames_with_telematics(frames_folder, telematics_csv, output_csv):
    if not os.path.exists(telematics_csv):
        print("Can't find the telematics file.")
        return
    data = pd.read_csv(telematics_csv)

    frame_paths = glob.glob(os.path.join(frames_folder, "frame_*_sec_*.jpg"))
    if len(frame_paths) == 0:
        print(f"No frames found in {frames_folder}")
        return

    time_col = 'Timestamp' if 'Timestamp' in data.columns else data.columns[0]
    data['seconds'] = data[time_col].apply(time_to_seconds)

    time_diffs = data['seconds'].diff().fillna(0)
    time_diffs[time_diffs < -1000] += 3600  # fix rollover
    data['clean_time'] = time_diffs.cumsum()

    data['frame_filename'] = None
    data['frame_path'] = None

    print("Matching frames to closest telematics timestamp...")

    extracted_times = []
    for path in frame_paths:
        filename = os.path.basename(path)
        try:
            time_str = filename.split('_sec_')[1].replace('.jpg', '')
            frame_time = float(time_str)
            extracted_times.append(frame_time)
        except (ValueError, IndexError):
            continue

        closest_row = (data['clean_time'] - frame_time).abs().idxmin()
        data.at[closest_row, 'frame_filename'] = filename
        data.at[closest_row, 'frame_path'] = path

    # =========================================================
    # 📍 ADDED: TRIM TRAILING TELEMETRY AFTER VIDEO ENDS
    # =========================================================
    if extracted_times:
        max_frame_time = max(extracted_times)
        # Keep only telematics rows recorded while video was running
        data = data[data['clean_time'] <= max_frame_time].copy()
    # =========================================================

    data = data.drop(columns=['seconds', 'clean_time'])

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    data.to_csv(output_csv, index=False)

    print(f"Saved result to '{output_csv}'")
    print_summary(data, len(frame_paths))

if __name__ == "__main__":
    frames_dir = "data/extracted_frames/Job3"
    telematics_csv = "data/telematics/job3_logger_transport_ground_truth.csv"
    output_csv = "data/processed/Job3_synced_clean.csv"
    sync_frames_with_telematics(frames_dir, telematics_csv, output_csv)
