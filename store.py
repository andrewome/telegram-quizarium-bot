import os
import json

class Store:
    def __init__(self, filePath):
        self.filePath = filePath 
        self.answers = {}

    def load(self):
        print("Loading answers from: ", self.filePath)
        with open(self.filePath, 'r') as saveFile:
            self.answers = json.load(saveFile)

    def save(self):
        print("Answers saved to: ", self.filePath)
        with open(self.filePath, 'w') as saveFile:
            json.dump(self.answers, saveFile)

    def add(self, question, answer):
        self.answers[question] = answer

            
    


    



