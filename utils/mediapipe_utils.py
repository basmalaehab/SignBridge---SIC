import numpy as np

def adjust_landmarks(arr, center):
    arr = arr.reshape(-1, 3)
    center = np.tile(center, (arr.shape[0], 1))
    return (arr - center).reshape(-1)

def extract_keypoints(results):
    pose = np.array([[lm.x, lm.y, lm.z] for lm in results.pose_landmarks.landmark]).flatten() \
        if results.pose_landmarks else np.zeros(33 * 3)

    lh = np.array([[lm.x, lm.y, lm.z] for lm in results.left_hand_landmarks.landmark]).flatten() \
        if results.left_hand_landmarks else np.zeros(21 * 3)

    rh = np.array([[lm.x, lm.y, lm.z] for lm in results.right_hand_landmarks.landmark]).flatten() \
        if results.right_hand_landmarks else np.zeros(21 * 3)

    pose = adjust_landmarks(pose, pose[:3])
    lh   = adjust_landmarks(lh, lh[:3])
    rh   = adjust_landmarks(rh, rh[:3])

    return np.concatenate([pose, lh, rh])

def movement_energy(prev, curr):
    return np.mean(np.abs(curr - prev))
