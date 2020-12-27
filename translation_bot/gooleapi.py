from googletrans import Translator

class Googleapi():
    def __init__(self, src):
        self.src = src 

    def detect(self):
        translator = Translator()
        result = translator.detect(self.src).lang
        return result

    def translate(self, tl):
        translator = Translator()
        result = translator.translate(self.src, dest=tl).text
        return result
