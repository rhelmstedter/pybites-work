class Circle:
    def __init__(self, radius):
        self.radius = radius

    def calc_area(self):
        return 3.14159 * self.radius**2  # Area calculation for the circle.

    def calc_circumference(self):
        return 2 * 3.14159 * self.radius  # Circumference calculation for the circle.


my_circle = Circle(3)

print(f"My circle has a radius of {my_circle.radius}.")
print(f"My circle has an area of {my_circle.calc_area()}.")
print(f"My circle has a circumference of {my_circle.calc_circumference()}.")
