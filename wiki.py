# https://github.com/greeneyedsoandso/chewie
"""wikia access utilities"""
import wikia


def wikia_summary(page_name):
    return wikia.summary('starwars', page_name)


def wikia_link(page_name):
    url = 'https://starwars.fandom.com/wiki/' + page_name
    return url

