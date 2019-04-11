import scrapy
from w3lib.html import remove_tags


class GuidesSpider(scrapy.Spider):
    name = "guides"

    def start_requests(self):
        urls = ['https://rework.withgoogle.com/guides/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_top)

    def parse_top(self, response):

        links = response.css(".rw-card__title > a::attr(href)").getall()

        titles = list(map(lambda e: e.strip(),
                      response.css(".rw-card__title > a::text").getall()))

        categories = list(map(lambda e: e.strip(),
                          response.css(".rw-card__actions > a::text").getall()))

        for (link, title, category) in zip(links, titles, categories):

            guide = {'guide': title, 'category': category, "steps": []}

            yield response.follow(link,
                                  callback=self.parse_guide,
                                  meta={"item": guide},
                                  dont_filter=True)

    def parse_guide(self, response):

        guide = response.meta["item"]

        # links appear twice, only consider the first occurrence
        navigation = response.css('.nav__body')[0]

        links = list(map(lambda x: remove_tags(x).strip().replace('\n', ''),
                     navigation.css('a.step-link::attr(href)').getall()))

        guide["num_links"] = len(links)

        for i, link in enumerate(links):

            yield response.follow(link, callback=self.parse_step,
                                  meta={"item": guide, "order": i},
                                  dont_filter=True)

    def parse_step(self, response):
        guide = response.meta["item"]

        num_links = guide["num_links"]

        order = response.meta["order"]

        title = remove_tags(
            response.css('.step__title').get()).strip().replace('\n', '')

        content = response.css('.step__body').get().strip().replace('\n', '')

        step = {'order': order, 'title': title, 'content': content}

        guide["steps"].append(step)

        if num_links == 1:
            guide.pop("num_links", None)
            return guide
        else:
            guide["num_links"] = num_links - 1
