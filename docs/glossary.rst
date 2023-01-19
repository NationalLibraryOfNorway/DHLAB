Glossary
----------

.. glossary::

   IDE
      Integrated Development Environment. Read more on `wikipedia <https://en.wikipedia.org/wiki/Integrated_development_environment>`_.

   API
      Application Programming Interface. Read more on `wikipedia <https://en.wikipedia.org/wiki/API>`_.

   n-gram
      An n-gram is a sequence of linguistic units, typically words or characters.

      Depending on the length n of the 'gram' sequence, we call them unigrams for single tokens, bigrams
      for sequences of two, trigrams for three, etc.

      As we count the occurrences of these n-grams across a large body of text, called a corpus,
      we can view patterns of the rhetoric in that corpus. If we additionally can spread samples of the corpus
      over time, we can see how the use of language develops in that time frame.

      The `NB N-gram app <https://www.nb.no/ngram/#1_1_1__1_1_3_1810%2C2022_2_2_2_12_2>`_ offers a visual graph of all uni-, bi-, and trigrams in
      the `digital collection <https://www.nb.no/search/>`_ of all Norwegian published textual material (books,
      newspapers, magazines) between 1810 and 2021.

      The :py:class:`~dhlab.ngram.Ngram`, :py:class:`~dhlab.ngram.NgramBook`, :py:class:`~dhlab.ngram.NgramNews` classes
      extract ngrams and their frequency lists.

