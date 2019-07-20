class Subject:
    def __init__(self, data):
        self.name = data["name"]
        self.credits = data["credits"]
        self.course = data["course"]
        self.period = data["period"]
        self.type = data["type"]

    def __str__(self):
        return ("name: " + self.name
                + " credits: " + str(self.credits)
                + " course: " + str(self.course)
                + " period: " + self.period
                + " type: " + self.type)
