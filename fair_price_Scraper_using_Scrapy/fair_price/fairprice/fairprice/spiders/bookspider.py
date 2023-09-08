import scrapy
import datetime

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["www.fairpricegroup.com.sg"]
    start_urls = [
        "https://www.fairpricegroup.com.sg/media-and-reports/press-releases/"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapers.pipelines.ScrapersMongoDBPipeline': 300
        }
    }
    count = 0

    def parse(self, response):
        articles = response.css("div.col-12")
        for article in articles:
            url = article.css("div.col-12::attr(data-url)").get()
            if url:
                self.count += 1
                yield response.follow(url, callback=self.parse_article_page)
                if self.count >= 3:
                    break

    def parse_article_page(self, response):
        thumbnail = response.css("img::attr(src)").get()
        yield {
            'url': response.url,
            "title": response.css("h3.font-weight-bold ::text").get(),
            "date": response.css("h6.font-weight-normal ::text").get(),
            "description": response.css("em ::text").getall(),
            "category": "Press Releases",
            'categoryId': 'Uncategorized',
            "content": response.css("div.cnt-wrapper-sm p ::text").getall(),
            "source": "fairpricegroup.com.sg",
            "source_url": "https://www.fairpricegroup.com.sg/media-and-reports/press-releases/",
            'countries': ['sg'],
            'createdAt': datetime.datetime.utcnow(),
            'updatedAt': datetime.datetime.utcnow(),
            'thumbnail': thumbnail,
        }
