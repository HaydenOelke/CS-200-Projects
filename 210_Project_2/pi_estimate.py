"""Estimate the value of Pi with Monte Carlo simulation.
Author:  Hayden Oelke
Credits:  TBD
"""
import random
import doctest
import points_plot
import math


GOOD_PI = 3.141592653589793 # A very good estimate, from math.pi
SAMPLES = 1000 # More => more precise, but slower

def in_unit_circle(x: float, y: float) -> bool:
    """Returns True if and only if (x,y) lies within the circle
    with origin (0,0) and radius of 1.0.
    
    >>> in_unit_circle(0.0, 0.0)
    True
    
    >>> in_unit_circle(1.0, 1.0)
    False
    
    >>> in_unit_circle(0.5, -0.5)
    True
    
    >>> in_unit_circle(-0.9, -0.5)
    False
    """
    distance_from_origin = math.sqrt(x ** 2 + y ** 2)
    return distance_from_origin <= 1.0


def  rand_point_unit_sq() -> tuple[float, float]:
    """Returns random x,y both in range 0..1.0, 0..1.0."""
    x = random.random()
    y = random.random()
    return x, y

x,y = rand_point_unit_sq()


def plot_random_points(n_points: int = 500):
    """Generate and plot n_points in interval (0,0) to (1,1).
    Creates a window and prompts the user before closing it.
    """
    points_plot.init()
    for i in range(n_points):
        x, y = rand_point_unit_sq()
        
    points_plot.wait_to_close()

    
def relative_error(est: float, expected: float) -> float:
    """Relative error of estimate (est) as non-negative fraction of expected value.
    Note estimate and expected are NOT interchangeable (see test cases).
    For example, if expected value is 5.0 but estimate is 3.0, the
    absolute error is -2.0, but the relative error is 2.0/5.0 = 0.4.
    If the expected value is 3.0 but the estimate is 5.0, the
    absolute error is 2.0, but the relative error is 2.0/3.0 = 0.66.
    >>> round(relative_error(3.0, 5.0), 2)
    0.4
    >>> round(relative_error(5.0, 3.0), 2)
    0.67
    """
    abs_error = est - expected
    rel_error = abs(abs_error / expected)
    return rel_error


def pi_approx() -> float:
    #for approximation, force totals to 0
    total_tried = 0
    total_within_circle = 0
    #for loop for samples
    for i in range(SAMPLES):
        # Generate points
        x = random.random()
        y = random.random()
        total_tried += 1
        #Check if point is in unit circle, if yes add to within circle count
        # add to total_tried always
        if in_unit_circle(x, y):
            total_within_circle += 1
            points_plot.plot(x, y, color_rgb=(255, 20, 20))
        else:
            points_plot.plot(x,y, color_rgb=(240, 240, 240))


    estimate = 4 * (total_within_circle / SAMPLES)
    return estimate





def main():
    doctest.testmod()
    # plot_random_points()
    points_plot.init()
    estimate = pi_approx()
    print(f"Pi is approximately {estimate}")
    points_plot.wait_to_close()
    


if __name__ == "__main__":
    main()
