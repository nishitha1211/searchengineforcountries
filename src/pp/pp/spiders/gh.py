# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import json

class GhSpider(CrawlSpider):
    name = 'gh'
    #allowed_domains = ['']
    start_urls = ['https://simple.wikipedia.org/wiki/List_of_countries','https://en.wikipedia.org/wiki/Main_Page','https://www.britannica.com/topic/list-of-countries-1993160','https://www.infoplease.com/world/countries']
    
    rules = (Rule(LinkExtractor(), callback='parse_item', follow=True),)

    def parse_item(self, response):
        #self.log('Visited:'+response.url)
        llist = LinkExtractor(unique=True).extract_links(response)
        alllinks = []
        for link in llist:
            alllinks.append(link.url)
        data = {}
        data['url'] = response.url
        data['totallinks'] = alllinks
        with open('links.txt', 'a') as outfile:  
            json.dump(data, outfile)
            outfile.write("\n")
        word_list = ['afghanistan','albania','algeria','andorra','angola','antigua','deps','argentina','armenia','australia','austria','azerbaijan','bahamas','bahrain','bangladesh','barbados','belarus','belgium','belize','benin','bhutan','bolivia','bosnia','herzegovina','botswana','brazil','brunei','bulgaria','burkina','burundi','capital','cambodia','cameroon','canada','cape' ,'verde','central','african','rep','chad','chile','china','colombia','comoros','congo','democratic','costa','rica','croatia','country','countries','cuba','cyprus','czech','republic','denmark','djibouti','dominica','dominican','east','timor','ecuador','egypt','el','salvador','equatorial','guinea','eritrea','estonia','ethiopia','fiji','finland','france','gabon','gambia','georgia','germany','ghana','greece','grenada','guatemala','guinea-bissau','guyana','haiti','honduras','hungary','iceland','india','indonesia','iran','iraq','ireland','israel','italy','ivory','coast','jamaica','japan','jordan','kazakhstan','kenya','kiribati','korea','north','south','kosovo','kuwait','kyrgyzstan','laos','latvia','lebanon','lesotho','liberia','libya','liechtenstein','lithuania','luxembourg','macedonia','madagascar','malawi','malaysia','maldives','mali','malta','marshall','islands','mauritania','mauritius','mexico','micronesia','moldova','monaco','mongolia','montenegro','morocco','mozambique','myanmar','burma','namibia','nauru','nepal','netherlands','new','zealand','nicaragua','niger','nigeria','norway','oman','pakistan','palau','panama','papua','guinea','paraguay','peru','philippines','poland','portugal','qatar','romania','russian','federation','rwanda','st','kitts','nevis','lucia','saint','vincent','grenadines','samoa','san','marino','sao','tome','principe','saudi','arabia','senegal','serbia','seychelles','sierra','leone','singapore','slovakia','slovenia','solomon','somalia','africa','sudan','spain','sri','lanka','sudan','suriname','swaziland','sweden','switzerland','syria','taiwan','tajikistan','tanzania','thailand','territory','territories','togo','tonga','trinidad' ,'tobago','tunisia','turkey','turkmenistan','tuvalu','uganda','ukraine','united','union','arab','emirates','kingdom','states','state','uruguay','uzbekistan','vanuatu','vatican','city','venezuela','vietnam','yemen','zambia','zimbabwe']
        status = 1
        if response.xpath("boolean(//meta[@name='description']/@content)")[0].extract() == '1':
            if any(key in response.css('title::text')[0].extract().lower() for key in word_list):
                status = 0
                yield {
                'url': response.url,
                'title': response.css('title::text')[0].extract().lower(),
                'description': response.xpath("//meta[@name='description']/@content")[0].extract().lower()
                }
            elif status == 1:
                if any(key in response.xpath("//meta[@name='description']/@content")[0].extract().lower() for key in word_list):
                    yield {
                    'url': response.url,
                    'title': response.css('title::text')[0].extract().lower(),
                    'description': response.xpath("//meta[@name='description']/@content")[0].extract().lower()
                    }
        else:
            if any(key in response.css('title::text')[0].extract().lower() for key in word_list):
                yield {
                'url': response.url,
                'title': response.css('title::text')[0].extract().lower()
                }
