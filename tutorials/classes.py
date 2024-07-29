class Circle:
    def __str__(self):
        return f"A circle with a radius of {self.radius}."

    def __init__(self, radius):
        self.radius = radius

    def calc_area(self):
        return 3.14159 * self.radius**2

    def calc_circumference(self):
        return 2 * 3.14159 * self.radius


my_circle = Circle(5)

print(my_circle)
