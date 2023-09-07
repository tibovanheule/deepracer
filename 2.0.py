
import math

def reward_function(params):
    is_offtrack = params['is_offtrack']
    if is_offtrack:
        return -1e5
    
    # Read input parameters
    distance_from_center = params['distance_from_center']
    reward = math.exp(-6*distance_from_center)
    
    progress = params['progress']/100.0 #scale to 0...1
    waypoints = params['waypoints']
    throttle = params['speed']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    
    if progress == 1:
        reward = 1e5
    else:
        reward *= progress

    waypoint_yaw = waypoints[closest_waypoints[1]][-1]
    if abs(heading - waypoint_yaw) >= math.radians(10):
        reward *= 0.25
    else:
        reward *= 1.25

    # Gotta go fast
    if throttle < 1.5:
        reward *= 0.5
    else:
        reward *= (1 + throttle/5)

    # min max
    if reward < -1e5:
        return float(-1e5)
    elif reward > 1e5:
        return float(1e5)
    
    return float(reward)
