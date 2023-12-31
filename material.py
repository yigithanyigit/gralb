class Material:
    def __init__(self, shininess = 1):
        self.shininess = float(shininess)

    def set_shininess(self, value):
        self.shininess = float(value)
