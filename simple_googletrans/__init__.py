#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
import sys
import json

import click
import googletrans
import prettytable
from simple_loggers import SimpleLogger


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
version_info = json.load(open(os.path.join(BASE_DIR, 'version.json')))

__version__ = version_info['version']
__author__ = version_info['author']
__author_email__ = version_info['author_email']


class GoogleTrans(object):
    """
    >>> from simple_googletrans import GoogleTrans
    >>> t = GoogleTrans()
    >>> t.translate('hello world')
    >>>
    >>> t.show_languages()
    """
    logger = SimpleLogger('GoogleTrans')

    def __init__(self, url='translate.google.cn', proxies=None, timeout=None):
        self.url = url
        self.translator = googletrans.Translator(service_urls=[url], proxies=proxies, timeout=timeout)
        self.check_service()
        self.nltk_checked = False

    def translate(self, text, dest='zh-cn', **kwargs):
        if os.path.isfile(text):
            text = open(text).read()

        texts = self.split_text(text)

        result = []
        for text in texts:
            text = self.translator.translate(text, dest=dest, **kwargs).text
            result.append(text)
        result = ''.join(result)

        return result

    def check_service(self):
        try:
            self.translator.detect('hello world')
        except Exception as e:
            self.logger.error('service not avaiable: {}'.format(self.url))
            exit(1)

    def check_nltk(self):
        """
            - download from Interactive Python
            >>> import nltk
            >>> nltk.download('punkt')

            - download from command line
            $ python -m nltk.downloader punkt

            - more: http://www.nltk.org/data.html
        """
        try:
            import nltk
        except SyntaxError:
            self.logger.warning('nltk is not available for Python2, use Python3 please.')
            exit(1)

        try:
            nltk.sent_tokenize('hello world')
            self.logger.info('nltk is ok!')
        except Exception:
            self.logger.warning('nltk_data not found! downloading start ...')
            try:
                nltk.download('punkt')
                self.nltk_checked = True
            except:
                self.logger.error('nltk_data download failed! you can also try: python -m nltk.downloader punkt')
                exit(1)

    def split_text(self, text, max_len=5000):
        """
            googletrans limits 5000 characters

            split text with nltk.sent_tokenize

            >>> nltk.sent_tokenize('hello world!')
        """
        if len(text) <= max_len:
            return [text]

        if not self.nltk_checked:
            self.check_nltk()

        self.logger.info('split text with nltk')

        texts = []
        for sent in nltk.sent_tokenize(text):
            if (not texts) or (len(texts[-1]) + len(sent) > max_len):
                texts.append(sent)
            else:
                texts[-1] += ' ' + sent
        return texts

    def show_languages(self):
        data = googletrans.LANGCODES
        table = prettytable.PrettyTable(['Index', 'Abbr', 'Language'])
        for n, (lang, abbr) in enumerate(sorted(data.items(), key=lambda x: x[1]), 1):
            table.add_row([n, abbr, lang])
        table.align['Abbr'] = 'l'
        table.align['Language'] = 'l'
        click.secho(str(table), fg='cyan')


__epilog__ = 'contact: {__author__} <{__author_email__}>'.format(**locals())

@click.command(epilog=__epilog__)
@click.version_option(version=__version__, prog_name='simple_googletrans')
@click.argument('text', nargs=-1)
@click.option('-u', '--url', help='the url of google', default='translate.google.cn', show_default=True)
@click.option('-d', '--dest', help='the dest language', default='zh-cn', show_default=True)
@click.option('-o', '--output', help='the output of result [stdout]')
@click.option('-l', '--list', help='list the available languages', is_flag=True)
@click.option('-p', '--proxy', help='use a proxy if you want')
@click.option('-t', '--timeout', help='the timeout for translating', type=click.FLOAT)
def main(**kwargs):
    proxies = None
    if kwargs['proxy']:
        proxy = kwargs['proxy']
        protocol = proxy.split('://')[0] if '://' in proxy else 'http'
        host = proxy.split('://')[-1]
        proxies = {protocol: '{protocol}://{host}'.format(**locals())}
        click.secho('use proxies: {protocol}://{host}'.format(**locals()), fg='yellow')

    t = GoogleTrans(kwargs['url'], proxies=proxies, timeout=kwargs['timeout'])
    if kwargs['list']:
        t.show_languages()
    else:
        text = ' '.join(kwargs['text']) or click.prompt('Please input a string or a file')
        out = open(kwargs['output'], 'w') if kwargs['output'] else sys.stdout
        with out:
            res = t.translate(text, dest=kwargs['dest'])
            out.write(res + '\n')


if __name__ == '__main__':
    main()
    