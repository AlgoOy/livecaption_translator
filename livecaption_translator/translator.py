from googletrans import Translator


class Trans:
    def __init__(self, source_lang: str = 'auto', dest_lang: str = 'zh-CN'):
        self.translator = Translator()
        self.source_lang = source_lang
        self.dest_lang = dest_lang

    def translate(self, text: str):
        return self.translator.translate(text, src=self.source_lang, dest=self.dest_lang).text
