import json

class Store:
    def __init__(self, filePath):
        self.filePath = filePath 
        self.answers = {}

    def load(self):
        print(f"Loading answers from: {self.filePath}")
        with open(self.filePath, 'r') as saveFile:
            self.answers = json.load(saveFile)

    def save(self):
        print(f"Answers saved to: {self.filePath}")
        with open(self.filePath, 'w') as saveFile:
            json.dump(self.answers, saveFile)

    def add(self, question, answer):
        self.answers[question] = answer
        print(f"Added {question}: {answer}")
        self.save()

    def exists(self, question):
        if question in self.answers:
            return True
        else:
            return False

    def get(self, question):
        return self.answers[question]
