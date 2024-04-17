import glob
import os
import re
from uuid import uuid4

import spacy
import textdistance as td
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer

nlp = spacy.load("en_core_web_md")

REGEX_PATTERNS = {
    "email_pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "phone_pattern": r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
    "link_pattern": r"\b(?:https?://|www\.)\S+\b",
}


class TextCleaner:
    @staticmethod
    def remove_emails_links(text):
        for pattern in REGEX_PATTERNS:
            text = re.sub(REGEX_PATTERNS[pattern], "", text)
        return text

    @staticmethod
    def clean_text(text):
        text = TextCleaner.remove_emails_links(text)
        doc = nlp(text)
        for token in doc:
            if token.pos_ == "PUNCT":
                text = text.replace(token.text, "")
        return text

    @staticmethod
    def remove_stopwords(text):
        doc = nlp(text)
        for token in doc:
            if token.is_stop:
                text = text.replace(token.text, "")
        return text


class CountFrequency:
    def __init__(self, text):
        self.text = text
        self.doc = nlp(text)

    def count_frequency(self):
        pos_freq = {}
        for token in self.doc:
            if token.pos_ in pos_freq:
                pos_freq[token.pos_] += 1
            else:
                pos_freq[token.pos_] = 1
        return pos_freq


class TextUtils:
    @staticmethod
    def generate_unique_id():
        return str(uuid4())

    @staticmethod
    def get_filenames_from_dir(directory_path: str) -> list:
        filenames = [
            f
            for f in os.listdir(directory_path)
            if os.path.isfile(os.path.join(directory_path, f)) and f != ".DS_Store"
        ]
        return filenames

    @staticmethod
    def match(resume, job_des):
        j = td.jaccard.similarity(resume, job_des)
        s = td.sorensen_dice.similarity(resume, job_des)
        c = td.cosine.similarity(resume, job_des)
        o = td.overlap.normalized_similarity(resume, job_des)
        total = (j + s + c + o) / 4
        return total * 100

    @staticmethod
    def do_tfidf(token):
        tfidf = TfidfVectorizer(max_df=0.05, min_df=0.002)
        tfidf.fit_transform(token)
        sentence = " ".join(tfidf.get_feature_names())
        return sentence

    @staticmethod
    def read_multiple_pdf(file_path: str) -> list:
        pdf_files = TextUtils.get_pdf_files(file_path)
        output = []
        for file in pdf_files:
            try:
                with open(file, "rb") as f:
                    pdf_reader = PdfReader(f)
                    count = pdf_reader.getNumPages()
                    for i in range(count):
                        page = pdf_reader.getPage(i)
                        output.append(page.extractText())
            except Exception as e:
                print(f"Error reading file '{file}': {str(e)}")
        return output

    @staticmethod
    def read_single_pdf(file_path: str) -> str:
        output = []
        try:
            with open(file_path, "rb") as f:
                pdf_reader = PdfReader(f)
                count = len(pdf_reader.pages)
                for i in range(count):
                    page = pdf_reader.pages[i]
                    output.append(page.extract_text())
        except Exception as e:
            print(f"Error reading file '{file_path}': {str(e)}")
        return str(" ".join(output))

    @staticmethod
    def get_pdf_files(file_path: str) -> list:
        pdf_files = []
        try:
            pdf_files = glob.glob(os.path.join(file_path, "*.pdf"))
        except Exception as e:
            print(f"Error getting PDF files from '{file_path}': {str(e)}")
        return pdf_files
