"""Viz tools for for pandas DataFrame"""
import pandas as pd
import seaborn as sns

def heatmap(df: pd.DataFrame, color='green'):
    """A wrapper for heatmap of a dataframe `df`."""
    return df.fillna(0).style.background_gradient(
        cmap=sns.light_palette(color, as_cmap=True))