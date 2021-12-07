from word_definition import WordDefinition
from sentence_ranker import RankedSentences


class WordResult(object):
    def __init__(
            self,
            word: str,
            definition: WordDefinition,
            ranked_sentences: []
    ):
        self.word = word
        self.definition = definition
        self.ranked_sentences = ranked_sentences

    def to_html(self):
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <body>
        <h2><span style="color: darkblue;"><strong>{self.word}</strong></span></h2>
        {self.definition_html()}
        {self.example_html()}
        </body>
        </html>
        """

    def definition_html(self):
        if self.definition.not_empty():
            items = "".join([
                f"""<li>[<strong><span style="color: darkgreen;">{d.pos}</span></strong>] {d.desc}</li>"""
                for d in self.definition.definitions
            ])

            return f"""
            <p><strong>Definitions</strong></p>
            <ol>
                {items}
            </ol>
            """
        else:
            return ""

    def example_html(self):
        if self.ranked_sentences:
            items = "".join([
                f"""<li>{str(s)}</li>"""
                for s in self.ranked_sentences
            ])

            return f"""
            <p><strong>Examples</strong></p>
            <ol>
                {items}
            </ol>
            """
        else:
            return ""
