import dateparser

from datetime import datetime
from scrapy import Request, Spider
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

class SpOsascoSpider(BaseGazetteSpider):
    MUNICIPALITY_ID = '3534401'
    PDF_URL = 'https://www.joinville.sc.gov.br'

    DATE_CSS = 'ul li span::text'
    ACTUAL_PAGE = 'div.c-pagination li.m-active a::text'
    NEXT_PAGE_CSS = 'http://www.osasco.sp.gov.br/imprensa-oficial?page={}'
    PDF_HREF_CSS = 'h4 a::attr(href)'
    GAZETTE_CSS = 'ul.document-list li'

    allowed_domains = ['osasco.sp.gov.br']
    name = 'sp_osasco'
    start_urls = ['http://www.osasco.sp.gov.br/imprensa-oficial?page=1']

    def parse(self, response):
        """
        @url http://www.osasco.sp.gov.br/imprensa-oficial?page=1
        @returns requests 1
        @scrapes date file_urls is_extra_edition municipality_id power scraped_at
        """

        for element in response.css(self.GAZETTE_CSS):
            url = self.extract_url(element)
            date = self.extract_date(element)

            yield Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition=False,
                municipality_id=self.MUNICIPALITY_ID,
                power='executive_legislature',
                scraped_at=datetime.utcnow(),
            )

        while(self.NEXT_PAGE_CSS.format(int(self.ACTUAL_PAGE) + 1) != ""):
            url = self.NEXT_PAGE_CSS.format(int(self.ACTUAL_PAGE) + 1)
            yield Request(url)

    def extract_url(self, element):
        href = element.css(self.PDF_HREF_CSS).extract_first()
        return href

    def extract_date(self, element):
        date = element.css(self.DATE_CSS)
        return dateparser.parse(date, languages=['pt']).date()
