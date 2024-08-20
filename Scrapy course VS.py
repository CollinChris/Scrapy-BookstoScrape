#!/usr/bin/env python
# coding: utf-8

# In[1]:


import scrapy


# In[2]:


class bookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            relative_url = book.css('h3 a ::attr(href)').get()

            if 'catalogue/' in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url
            yield response.follow(book_url, callback = self.parse_book_page)

        next_page = response.css('li.next a ::attr(href)').get()
        if next_page != None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback = self.parse)

    def parse_book_page(self, response):

        table_rows = response.css('table tr')

        yield{'url': response.url,
              'title': response.css('.product_main h1::text').get(),
              'tag': response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
              'descript' : response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
              'product_type' : table_rows[1].css('td ::text').get(),
              'price_exc_tax' : table_rows[2].css('td ::text').get(),
              'tax' : table_rows[4].css('td ::text').get(),
              'in_stock' : table_rows[5].css('td ::text').get(),
              'reviews' : table_rows[6].css('td ::text').get(),
              'stars' : response.css("p.star-rating").attrib['class'],
              }


# In[3]:


from scrapy.crawler import CrawlerProcess


# In[ ]:


process = CrawlerProcess(settings = {'FEEDS':{'books.csv':{'format':'csv'}}})
process.crawl(bookSpider)
process.start()


# In[5]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




