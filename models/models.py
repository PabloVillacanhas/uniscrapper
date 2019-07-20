class Faculty:
    def __init__(self, name):
        self.name = name


class Subject:
    def __init__(self, name, credits, course):
        self.name = name
        self.credits = credits
        self.course = course

    def __str__(self):
        return "Name: " + self.name + ", credits " + self.credits


class University:
    def __init__(self, name):
        self.name = name
