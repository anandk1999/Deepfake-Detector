import cv2
import torch

from torchvision import transforms

def extract_frames(video_path, num_frames=40):

    cap = cv2.VideoCapture(video_path)
    frames = []
    while len(frames) < num_frames:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()

    return frames

def preprocess_frames(frames):

    transform = transforms.Compose([transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])

    processed_frames = []
    
    for frame in frames:
        # Resize frame to (299, 299)
        frame = cv2.resize(frame, (299, 299))
        frame_tensor = torch.tensor(frame).permute(2, 0, 1).float()
        # Apply normalization
        frame_tensor = transform(frame_tensor)
        processed_frames.append(frame_tensor)
    
    # Stack all frames into a single tensor
    return torch.stack(processed_frames)