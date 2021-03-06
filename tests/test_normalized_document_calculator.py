import context
from unit_test import *
from scraper.document import *
from scraper.normalized_document_calculator import *

if __name__ == "__main__":

    # Test NormalizedDocumentCalculator initiailzation
    subject = "NormalizedDocumentCalculator.__init__"
    described = Describe(subject)

    # Create initialization of inverse document frequencies.
    N = 100
    term_frequencies = { "foo": 10, "bar": 1 }
    calc = NormalizedDocumentCalculator(term_frequencies, N)
    test = described.it("should properly calculate idf values")
    test.expect(calc.term_idfs["foo"] == 1 and calc.term_idfs["bar"] == 2)


    # Test the normalization of a document
    subject = "NormalizedDocumentCalculator.normalize"
    described = Describe(subject)

    # Set up for test
    N = 100
    term_frequencies = { "foo": 10, "bar": 1 }
    calc = NormalizedDocumentCalculator(term_frequencies, N)
    text = "foo bar foo foo"
    doc = Document(text, None, "09823gaakdf")

    test = described.it("calculates normalized document vectors")
    calc.normalize(doc)
    test.expect(doc.normalized_tf.has_key("foo") and
        doc.normalized_tf.has_key("bar") and
        round(doc.normalized_tf["foo"], 2) == 0.83 and
        round(doc.normalized_tf["bar"], 2) == 0.55)

    # Test the scoring of two documents
    subject = "NormalizedDocumentCalculator.score"
    described = Describe(subject)

    # Set up test
    N = 100
    term_frequencies = { "foo": 10, "bar": 1 }
    calc = NormalizedDocumentCalculator(term_frequencies, N)
    text = "foo bar foo foo"
    doc = Document(text, text, None, "09823gaakdf")
    calc.normalize(doc)
    query = Document("foo bar")
    calc.normalize(query)

    test = described.it("calculates the cosine similarity score")
    score = calc.score(query, doc)
    test.expect(round(score, 2) == 0.87)
