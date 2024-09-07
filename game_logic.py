import numpy as np

COLORS = ["red", "orange", "yellow", "green"]


GRID_HEIGHT = 9  
GRID_WIDTH = 12  

def PlaceGhost():
    return np.random.choice(GRID_HEIGHT), np.random.choice(GRID_WIDTH)

# Initialize probabilities
probabilities = np.full((GRID_HEIGHT, GRID_WIDTH), 1.0 / (GRID_WIDTH * GRID_HEIGHT))



def distance(loc1, loc2):
    return max(abs(loc1[0] - loc2[0]), abs(loc1[1] - loc2[1]))

def ComputeInitialPriorProbabilities():
    global probabilities
    probabilities = np.full((GRID_HEIGHT, GRID_WIDTH), 1.0 / (GRID_WIDTH * GRID_HEIGHT))

def conditional_prob_color_given_distance(dist):
    # Conditional probabilities of sensing each color given a distance
    if dist == 0:
        return {'red': 0.9, 'orange': 0.1, 'yellow': 0, 'green': 0}
    elif dist in [1, 2]:
        return {'red': 0.1, 'orange': 0.8, 'yellow': 0.1, 'green': 0}
    elif dist in [3, 4]:
        return {'red': 0, 'orange': 0.1, 'yellow': 0.8, 'green': 0.1}
    else:
        return {'red': 0, 'orange': 0, 'yellow': 0.1, 'green': 0.9}

def DistanceSense(xclk, yclk, gx, gy):
    dist = distance((xclk, yclk), (gx, gy))
    color_probabilities = conditional_prob_color_given_distance(dist)
    
    # Instead of selecting the color with the highest probability,
    # we now sample based on the conditional probabilities.
    # This introduces variability and makes sensor readings more realistic.
    colors, probs = zip(*color_probabilities.items())
    color = np.random.choice(colors, p=probs)
    
    return color

def update_probabilities(sensor_color, xclk, yclk):
    global probabilities
    new_probabilities = np.zeros_like(probabilities)
    
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            dist = distance((i, j), (xclk, yclk))
            prob_color_given_dist = conditional_prob_color_given_distance(dist)[sensor_color]
            
            # Bayesian update: P(H|E) = P(E|H) * P(H) / P(E)
            # P(H) is the current probability of the ghost being at (i, j).
            # P(E|H) is the probability of sensing the color given the ghost is at (i, j).
            # Since P(E) is not calculated directly (the sum of all P(E|H) * P(H) for all H),
            # normalization is necessary to ensure probabilities sum to 1.
            new_probabilities[i][j] = prob_color_given_dist * probabilities[i][j]
    
    # Normalize to ensure the sum of probabilities equals 1.
    total_probability = np.sum(new_probabilities)
    if total_probability > 0:
        probabilities = new_probabilities / total_probability

def get_probabilities():
    global probabilities
    return probabilities

def bust(x, y, gx, gy):
    if (x, y) == (gx, gy):
        return True, "Congratulations! You've busted the ghost!"
    else:
        return False, "Sorry, the ghost is not here."
