import dateparser

from datetime import datetime
from scrapy import Request
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

now = datetime.now()

class SpBauruSpider(BaseGazetteSpider):

    MUNICIPALITY_ID = '3506003'
    PAGES_URL = 'http://www.bauru.sp.gov.br/juridico/diariooficial.aspx?a={}&m={}'
    PDF_URL = 'http://www.bauru.sp.gov.br{}'
    MONTHS = [str(x).zfill(2) for x in range(1,13)]
    YEARS = range(2015,now.year+1)

    DATE_CSS = 'main div.container ul ul ul li b::text'
    PDF_HREF_CSS = 'main div.container ul ul ul li a::attr(href)'

    allowed_domains = ['bauru.sp.gov.br']
    name = 'sp_bauru'
    start_urls = ['http://www.bauru.sp.gov.br/juridico/diariooficial.aspx']

    def date_parse(self, dates):
        for date in range(len(dates)):
            dates[date] = dateparser.parse(dates[date][0:10],languages=['pt']).date()
        return dates

    def pdf_link(self, links):
        for link in range(len(links)):
            links[link] = self.PDF_URL.format(links[link])
        return links

    def parse(self, response):
        for year in self.YEARS:
            for month in self.MONTHS:
                page_url = self.PAGES_URL.format(year, month)
                #Request(url=page_url)
                #sudo docker-compose run --rm processing scrapy shell page_url # Como fazer isso?
                url = self.pdf_link(response.css(self.PDF_HREF_CSS).extract())
                date = self.date_parse(response.css(self.DATE_CSS).extract())
                print(date)
                '''
                for day in range(len(date)):
                    print(date[day])

                    yield Gazette(
                        date=date[day],
                        file_urls=[url[day]],
                        is_extra_edition=False,
                        municipality_id=self.MUNICIPALITY_ID,
                        power='executive_legislature',
                        scraped_at=datetime.utcnow(),
                    )
                    '''
