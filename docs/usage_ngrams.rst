.. _usage-ngrams:


N-grams
=================

N-grams are sequences of linguistic units, typically words or characters.

Depending on the length N of the 'gram' sequence, we call them unigrams for single tokens, bigrams
for sequences of two, trigrams for three, etc.

As we count the occurrences of these n-grams across a large body of text, called a corpus, we can
view patterns of the rhetoric in that corpus. If we additionally can spread samples of the corpus
over time, we can see how the use of language develops in that time frame.

The `NB N-gram app <nb-ngrams>`_ offers a visual graph of all uni-, bi-, and trigrams in
the `digital collection <NB Digital>`_ of all Norwegian published textual material (books,
newspapers, magazines) between 1810 and 2021.

The  :doc:`dhlab.ngram <generated/ngram>` subpackage provides python classes to extract
and view ngrams and their frequency lists.

Use
-------------------------------------
Import Ngram classes from :doc:`generated/ngram.ngram` like this:

.. code-block:: python

   from dhlab.ngram import ...

--------------------------------------

.. _nb-ngrams: https://www.nb.no/sprakbanken/ngram/?%7B%22graphViewmode%22:%22trendlinjer%22,%22freq%22:%22rel%22,%22corpus%22:%5B%22bok%22%5D,%22searchTerms%22:%5B%5D,%22lang%22:%22nor%22,%22case_sens%22:0,%22smoothing%22:3,%22yearSpan%22:%5B1810,2021%5D,%22leaves%22:0,%22isCumulative%22:false,%22isGrayscale%22:false,%22limit%22:12,%22isEmbedded%22:false%7D
.. _NB Digital: https://www.nb.no/search

