import dateparser
from datetime import datetime
from scrapy import Request, Spider
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

class SpGuarujaSpider(BaseGazetteSpider):
	MUNICIPALITY_ID = "3518701"
	URL = "http://www.guaruja.sp.gov.br/wp-content/uploads/{}/{}/{}-{}-{}.pdf"

	MONTHS = [str(x).zfill(2) for x in range(1, 13)]
	YEARS = ['2017', '2018']
	DAYS = [str(x).zfill(2) for x in range(1, 25)]

	allowed_domains = ['guaruja.sp.gov.br']
	name = "sp_guaruja"
	start_urls = ['http://www.guaruja.sp.gov.br/index.php/diario-oficial/']

	def parse(self, response):
		"""
        @url http://www.guaruja.sp.gov.br/index.php/diario-oficial/
        @returns requests 1
        @scrapes date file_urls is_extra_edition municipality_id power scraped_at
        """

		for year in self.YEARS:
			for month in self.MONTHS:
				for day in self.DAYS:
					url = self.format_url(year, month, day)
					date = self.format_date(year, month, day)

					yield Gazette(
		                date=date,
		                file_urls=[url],
		                is_extra_edition=False,
		                municipality_id=self.MUNICIPALITY_ID,
		                power='executive_legislature',
		                scraped_at=datetime.utcnow(),
		            )

	def format_url(self, year, month, day):
		if(year == "2016"):
			return self.URL.format("2017", "05", day, month, year)
		else:
			return self.URL.format(year, month, day, month, year)

	def format_date(self, year, month, day):
		date = "{}/{}/{}".format(day, month, year)
		return dateparser.parse(date).date()
