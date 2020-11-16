# https://github.com/greeneyedsoandso/chewie
"""wikia access utilities"""
import wikia


def wikia_summary(page_name):
    return wikia.summary('starwars', page_name)

