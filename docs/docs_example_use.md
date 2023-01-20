# Example Use

<!-- start example-use -->

## Build a corpus

You could start by building your own [corpus](https://en.wikipedia.org/wiki/Text_corpus), e.g. of
books published between 1814 and 1905:

```python
import dhlab as dh

book_corpus = dh.Corpus(doctype="digibok", from_year=1814, to_year=1905)
```

You can now use `book_corpus` and to do quantitative text analyses.
`book_corpus.corpus` is a [Pandas dataframe](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html#pandas.DataFrame) with metadata information about the publications in the corpus.

<!-- end example-use -->
