import re

class QuizariumGameInstance:
    def __init__(self):
        self.curQuestion = None

    async def parse(self, message, store, messageObj):
        QUESTION = "question"
        ANSWER = "answer"
        startOfQnRegEx = f"Round [\\d]+\/.+\\n▶️ QUESTION.+(?:\\[.+\\])?\\n(?P<{QUESTION}>.+)\\n\[.+\\]$"
        middleOfQnRegEx = f"(?P<{QUESTION}>[\\w?., '!]+)\\nHint:[ \\w]+\\n\\[.+\\]$"
        nobodyGuessed = f"⛔️ Nobody guessed\\. The correct answer was (?P<{ANSWER}>[\\w\\d ]+)\\n\\n"
        somebodyGuessed = f"✅ Yes, (?P<{ANSWER}>[\\w\\d ]+)!\\n\\n(?:.+\\n)+\\n"

        result = re.match(startOfQnRegEx, message)
        if result:
            self.curQuestion = result.group(QUESTION)
            if store.exists(self.curQuestion):
                answer = store.get(self.curQuestion)
                print(f"Answering {self.curQuestion}: {answer}")
                await messageObj.reply(answer)
            return
        
        result = re.match(middleOfQnRegEx, message)
        if result:
            self.curQuestion = result.group(QUESTION)
            if store.exists(self.curQuestion):
                answer = store.get(self.curQuestion)
                print(f"Answering {self.curQuestion}: {answer}")
                await messageObj.reply(answer)
            return

        result = re.match(nobodyGuessed, message)
        if result:
            answer = result.group(ANSWER)
            if self.curQuestion != None:
                store.add(self.curQuestion, answer)
            self.curQuestion = None
            return

        result = re.match(somebodyGuessed, message)
        if result:
            answer = result.group(ANSWER)
            if self.curQuestion != None:
                if not store.exists(self.curQuestion):
                    store.add(self.curQuestion, answer)
            return
