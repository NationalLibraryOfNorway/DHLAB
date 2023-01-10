import json
import matplotlib.pyplot as plt
from collections import Counter

try:
    from wordcloud import WordCloud
except BaseException:
    print("wordcloud er ikke installert, kan ikke lage ordskyer")


def make_cloud(json_text, top=100, background='white',
               stretch=lambda x: 2 ** (10 * x), width=500, height=500,
               font_path=None):
    """Create a word cloud from a frequency list."""
    pairs0 = Counter(json_text).most_common(top)
    pairs = {x[0]: stretch(x[1]) for x in pairs0}
    wc = WordCloud(
        font_path=font_path,
        background_color=background,
        width=width,
        # color_func=my_colorfunc,
        ranks_only=True,
        height=height).generate_from_frequencies(pairs)
    return wc


def draw_cloud(sky, width=20, height=20, fil=''):
    """Draw a word cloud produced by :func:`make_cloud`."""
    plt.figure(figsize=(width, height))
    plt.imshow(sky, interpolation='bilinear')
    figplot = plt.gcf()
    if fil != '':
        figplot.savefig(fil, format='png')


def cloud(df, column='', top=200, width=1000, height=1000, background='black',
          file='', stretch=10, font_path=None):
    """Make and draw a cloud from a pandas dataframe, using :func:`make_cloud` and
    :func:`draw_cloud`."""
    if column == '':
        column = df.columns[0]
    data = json.loads(df[column].to_json())
    a_cloud = make_cloud(data, top=top,
                         background=background, font_path=font_path,
                         stretch=lambda x: 2 ** (stretch * x), width=width,
                         height=height)
    draw_cloud(a_cloud, fil=file)