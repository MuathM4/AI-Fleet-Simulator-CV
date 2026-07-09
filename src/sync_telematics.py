import os
import glob
import pandas as pd

def print_summary(df, total_frames):
    # just some quick stats to see how well the matching worked
    total_rows = len(df)
    matched = df['frame_filename'].notna().sum()

    coverage = (matched / total_rows) * 100
    used = (matched / total_frames) * 100 if total_frames > 0 else 0

    print("\n---- Sync Summary ----")
    print(f"Telematics rows: {total_rows}")
    print(f"Frames found:    {total_frames}")
    print(f"Frames matched:  {matched}")
    print(f"Coverage:  {coverage:.2f}%")
    print(f"Frame use: {used:.2f}%")
    print("-----------------------\n")


def time_to_seconds(ts):
    # turns "MM:SS" or "HH:MM:SS" into plain seconds
    # returns None if it can't figure it out
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
    # basic check first
    if not os.path.exists(telematics_csv):
        print("Can't find the telematics file.")
        return

    data = pd.read_csv(telematics_csv)

    # grab all the extracted frame images
    frame_paths = glob.glob(os.path.join(frames_folder, "frame_sec_*.jpg"))
    if len(frame_paths) == 0:
        print(f"No frames found in {frames_folder}")
        return

    # figure out which column has the timestamps
    time_col = 'Timestamp' if 'Timestamp' in data.columns else data.columns[0]

    # convert timestamps to seconds
    data['seconds'] = data[time_col].apply(time_to_seconds)

    # the clock sometimes "rolls over" (like resets after an hour)
    # so instead of trusting the raw seconds, we look at the difference
    # between each row and the one before it, and fix any big negative jumps
    time_diffs = data['seconds'].diff().fillna(0)
    time_diffs[time_diffs < -1000] += 3600  # fix rollover

    # add up the differences to get a clean, always-increasing time
    data['clean_time'] = time_diffs.cumsum()

    # these will hold the matched frame info
    data['frame_filename'] = None
    data['frame_path'] = None

    print("Matching frames to closest telematics timestamp...")

    for path in frame_paths:
        filename = os.path.basename(path)

        # pull the seconds value out of the filename, e.g. frame_sec_12.5.jpg -> 12.5
        try:
            frame_time = float(filename.replace("frame_sec_", "").replace(".jpg", ""))
        except ValueError:
            continue  # skip files that don't match the expected naming

        # find the row whose time is closest to this frame's time
        closest_row = (data['clean_time'] - frame_time).abs().idxmin()

        data.at[closest_row, 'frame_filename'] = filename
        data.at[closest_row, 'frame_path'] = path

    # drop the helper columns we don't need in the final file
    data = data.drop(columns=['seconds', 'clean_time'])

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    data.to_csv(output_csv, index=False)

    print(f"Saved result to '{output_csv}'")
    print_summary(data, len(frame_paths))


if __name__ == "__main__":
    frames_dir = "data/extracted_frames/Job1"
    telematics_csv = "data/telematics/job1_logger_transport_ground_truth1.csv"
    output_csv = "data/processed/Job1_synced_clean.csv"

    sync_frames_with_telematics(frames_dir, telematics_csv, output_csv)