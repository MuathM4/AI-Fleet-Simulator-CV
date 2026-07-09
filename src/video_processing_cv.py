import cv2
import os

def inspect_and_extract_frames(video_path, output_folder, sample_rate_seconds=5):
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
    print(f"Duration: {duration_sec:.2f} seconds")
    print("-" * 40)

    frame_interval = int(fps * sample_rate_seconds)
    frame_count = 0
    saved_count = 0

    print(f"Extracting 1 frame every {sample_rate_seconds} seconds...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            timestamp_sec = frame_count / fps
            frame_name = f"frame_sec_{timestamp_sec:.2f}.jpg"
            out_path = os.path.join(output_folder, frame_name)
            
            cv2.imwrite(out_path, frame)
            saved_count += 1

        frame_count += 1

    cap.release()
    print(f"Success: Extracted {saved_count} frames to '{output_folder}'")

# Example Usage
if __name__ == "__main__":
    video_file = "test_trip.mp4"
    output_dir = "extracted_frames"
    
    # inspect_and_extract_frames(video_file, output_dir, sample_rate_seconds=5)