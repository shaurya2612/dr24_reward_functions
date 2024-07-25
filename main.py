import math

def reward_function(params):
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed']
    all_wheels_on_track = params['all_wheels_on_track']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    progress = params['progress']
    steps = params['steps']
    is_left_of_center = params['is_left_of_center']
    steering_angle = params['steering_angle']

    # Initialize the reward
    reward = 1.0

    # Penalize if the car is off track
    if not all_wheels_on_track:
        return 1e-3

    # Reward for keeping the car near the center of the track
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    if distance_from_center <= marker_1:
        reward += 1.0
    elif distance_from_center <= marker_2:
        reward += 0.5
    elif distance_from_center <= marker_3:
        reward += 0.1
    else:
        reward += 1e-3  # likely crashed/close to off track

    # Reward for speed with dynamic threshold
    SPEED_THRESHOLD = 2.0  # Base threshold speed
    MAX_SPEED = 4.0  # Max speed for full reward
    speed_reward = max(0.0, (speed - SPEED_THRESHOLD) / (MAX_SPEED - SPEED_THRESHOLD))
    reward += speed_reward

    # Calculate the direction of the center line based on the closest waypoints
    next_waypoint = waypoints[closest_waypoints[1]]
    prev_waypoint = waypoints[closest_waypoints[0]]

    # Calculate the direction of the track (radians to degrees)
    track_direction = math.atan2(
        next_waypoint[1] - prev_waypoint[1],
        next_waypoint[0] - prev_waypoint[0]
    )
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)

    # Penalize if the difference in direction is too large
    DIRECTION_THRESHOLD = 10.0
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.5

    # Reward for smooth steering (penalize zigzag)
    if abs(steering_angle) < 15.0:
        reward += 0.5

    # Reward for progress and fewer steps
    if steps > 0:
        progress_reward = (progress / 100) * (100 / steps)
        reward += progress_reward

    # Additional reward for completing the lap
    if progress == 100:
        reward += 10.0  # Large reward for finishing the lap

    return float(reward)