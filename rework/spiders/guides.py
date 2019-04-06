import scrapy
from w3lib.html import remove_tags
        
class GuidesSpider(scrapy.Spider):
    name = "guides"
    
    def start_requests(self):
        urls = [ 'https://rework.withgoogle.com/guides/' ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_top)

    def parse_top(self, response):
    
        links = response.css(".rw-card__title > a::attr(href)").getall()
        
        titles = list(map(lambda e: e.strip(), response.css(".rw-card__title > a::text").getall()))
        
        categories = list(map(lambda e: e.strip(), response.css(".rw-card__actions > a::text").getall()))
        
        for (link, title, category) in zip(links, titles, categories):
            
            guide = {'guide': title, 'category': category, "steps": [] }
            
            yield response.follow(link, callback=self.parse_guide, meta={"item": guide})
            
    def parse_guide(self,response):        
        
        guide = response.meta["item"]

        navigation = response.css('.nav__body')[0] # it's duplicated, only consider the first
        
        links = list(map(lambda x: remove_tags(x).strip().replace('\n',''), response.css('a.step-link::attr(href)').getall()))

        for i, link in enumerate(links):
        
            last = (i == (len(links) - 1))
            
            item = {"item": guide, "last": last}
            
            yield response.follow(link, callback=self.parse_step, meta=item)
        
        yield guide
                
    def parse_step(self,response):

        guide = response.meta["item"]
           
        title = remove_tags(response.css('.step__title').get()).strip().replace('\n','')
            
        content = remove_tags(response.css('.step__body').get()).strip().replace('\n','')
        
        step = { 'title': title, 'content': content }
        
        guide["steps"].append(step)        
