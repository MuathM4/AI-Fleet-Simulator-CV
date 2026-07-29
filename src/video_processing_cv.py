import os
import cv2


def inspect_and_extract_frames(
    video_path, output_folder, sample_rate_seconds=1.0
):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    # Extract video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_sec = total_frames / fps
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print("Video Metadata:")
    print(f"Resolution: {width}x{height}")
    print(f"FPS: {fps:.2f}")
    print(f"Total Frames: {total_frames}")
    print(f"Duration: {duration_sec:.2f} seconds ({duration_sec / 60:.2f} mins)")
    print("-" * 40)

    # Frame interval for 1 frame per sample_rate_seconds
    frame_interval = int(fps * sample_rate_seconds)
    frame_count = 0
    saved_count = 0

    print(f"Extracting 1 frame every {sample_rate_seconds} second(s)...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            timestamp_sec = frame_count / fps
            # Added zero-padding (frame_000000_) so your OS keeps files in exact order
            frame_name = f"frame_{saved_count:06d}_sec_{timestamp_sec:.2f}.jpg"
            out_path = os.path.join(output_folder, frame_name)

            cv2.imwrite(out_path, frame)
            saved_count += 1

        frame_count += 1

    cap.release()
    print(
        f"\nSuccess: Extracted {saved_count} frames into '{output_folder}'"
    )


# Execution
if __name__ == "__main__":
    # Update video path if your file is inside a subfolder (e.g., "data/raw_videos/Job1.mp4")
    video_file = "data/raw_videos/Job3.mp4"
    output_dir = "data/extracted_frames/Job3"

    # Extract 1 frame per 1 second
    inspect_and_extract_frames(video_file, output_dir, sample_rate_seconds=1.0)
