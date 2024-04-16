import textacy
from textacy import extract


class KeytermExtractor:
    def __init__(self, raw_text: str, top_n_values: int = 20):
        self.raw_text = raw_text
        self.text_doc = textacy.make_spacy_doc(self.raw_text, lang="en_core_web_md")
        self.top_n_values = top_n_values

    def get_keyterms_based_on_textrank(self):
        return list(
            extract.keyterms.textrank(
                self.text_doc, normalize="lemma", topn=self.top_n_values
            )
        )

    def get_keyterms_based_on_sgrank(self):
        return list(
            extract.keyterms.sgrank(
                self.text_doc, normalize="lemma", topn=self.top_n_values
            )
        )

    def get_keyterms_based_on_scake(self):
        return list(
            extract.keyterms.scake(
                self.text_doc, normalize="lemma", topn=self.top_n_values
            )
        )

    def get_keyterms_based_on_yake(self):
        return list(
            extract.keyterms.yake(
                self.text_doc, normalize="lemma", topn=self.top_n_values
            )
        )

    def bi_gramchunker(self):
        return list(
            textacy.extract.basics.ngrams(
                self.text_doc,
                n=2,
                filter_stops=True,
                filter_nums=True,
                filter_punct=True,
            )
        )

    def tri_gramchunker(self):
        return list(
            textacy.extract.basics.ngrams(
                self.text_doc,
                n=3,
                filter_stops=True,
                filter_nums=True,
                filter_punct=True,
            )
        )
