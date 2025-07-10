from abc import ABC, abstractmethod
import math

class Student:


  def __init__(self, name, ID):
    self.name = name
    self.ID = ID
    self.scores = {}


  def add_score(self, subject, score):
    self.scores[subject] = score


  def get_average(self):
    if not self.scores:
      return 0
    return sum(self.scores.values()) / len(self.scores)


  def display_info(self):
    average = self.get_average()
    return f'{self.name}, {self.ID}, {self.scores}, {average:.2f}'


"""student = Student("John", "12345")
student.add_score("Maths", 5)
student.add_score("Physics", 4)

print(student.display_info())"""


class Shape(ABC):

  @abstractmethod
  def area(self):
    pass

  @abstractmethod
  def perimeter(self):
    pass

  def display(self):
    return f'{self.area()}, {self.perimeter()}'


class Circle(Shape):
  def __init__(self, radius):
    self.radius = radius

  def area(self):
    return math.pi * self.radius * self.radius

  def perimeter(self):
    return 2 * math.pi * self.radius

  def display(self):
    return f'{self.area()}, {self.perimeter()}'

  def __eq__(self, other):
    if isinstance(other, Circle):
      return self.radius == other.radius
    return False


class Rectangle(Shape):
  def __init__(self, width, height):
    self.width = width
    self.height = height

  def area(self):
    return self.width * self.height

  def perimeter(self):
    return 2 * (self.width + self.height)

  def display(self):
    return f'{self.area()}, {self.perimeter()}'

  def __eq__(self, other):
    if isinstance(other, Rectangle):
      return self.width == other.width and self.height == other.height
    return False


class Triangle(Shape):
  def __init__(self, base, height):
    self.base = base
    self.height = height

  def area(self):
    return self.base * self.height * 0.5

  def perimeter(self):
    pass

"""circle = Circle(5)
rectangle = Rectangle(4, 6)  # ширина 4, высота 6
triangle = Triangle(3, 4)  # основание 3, высота 4

print("Circle:")
print("Area:", circle.area())  # Ожидаем ~78.54
print("Perimeter:", circle.perimeter())  # Ожидаем ~31.42
print("Display:", circle.display())
print("Equality:", circle == Circle(5))  # True
print("Equality:", circle == Circle(3))  # False
print()

print("Rectangle:")
print("Area:", rectangle.area())
print("Perimeter:", rectangle.perimeter())
print("Display:", rectangle.display())
print("Equality:", rectangle == Rectangle(4, 6))
print("Equality:", rectangle == Rectangle(2, 3))
print()

print("Triangle:")
print("Area:", triangle.area())
print("Perimeter:", triangle.perimeter())
print("Display:", triangle.display())"""


from datasets import load_dataset
from itertools import islice

dataset = load_dataset('ddrg/named_math_formulas', split='train', streaming=True)

subset = list(islice(dataset, 10))

for example in subset:
    print(example)

