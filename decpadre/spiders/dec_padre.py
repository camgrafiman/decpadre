# from scrapy.item import Field
# from scrapy.item import Item
# from scrapy.spiders import Spider
# from scrapy.selector import Selector
# from scrapy.loader import ItemLoader
# from scrapy.exporters import XmlItemExporter
# from scrapy.loader.processors import TakeFirst

import Field
import Item
import Spider
import Selector
import ItemLoader
import XmlItemExporter
import TakeFirst

# construir los campos del archivo:


class Producto(Item):
    imagen = Field(output_processor=TakeFirst())
    id = Field(output_processor=TakeFirst())
    titulo = Field(output_processor=TakeFirst())
    precio = Field(output_processor=TakeFirst())
    precio_a = Field(output_processor=TakeFirst())
    precio_b = Field(output_processor=TakeFirst())
    precio_previo = Field(output_processor=TakeFirst())
    reduccion = Field(output_processor=TakeFirst())
    marca = Field(output_processor=TakeFirst())
    url = Field(output_processor=TakeFirst())
    rating = Field(output_processor=TakeFirst())
    review = Field(output_processor=TakeFirst())


class decSpider(Spider):
    name = "dec_padre"
    #grupoProductos = '?Ndrc=2'
    start_urls = [
        'https://www.decathlon.es/es/browse/c0-hombre/c1-regalos-para-hombre/_/N-9cqwoa'
        # % Descuento
        # 'https://www.decathlon.es/es/special-page/_/N-o51r9u?Ns=sku.discountRate%7C1%7C%7Csku.availability%7C1',
        # valoración:
        # 'https://www.decathlon.es/es/special-page/_/N-o51r9u?Ns=product.averageRating%7C1%7C%7Csku.availability%7C1',
        # precios mayor a menor:
        # 'https://www.decathlon.es/es/special-page/_/N-o51r9u?Ns=sku.modelLowestPrice%7C1%7C%7Csku.activePrice%7C0%7C%7Csku.availability%7C1'
    ]

    def parse(self, response):

        sel = Selector(response)
        productos = sel.xpath('//div[@id="js-product-wrapper"]/article')

        # sel.css también puede ser usado.
        # iterar sobre todos los productos:
        for i, elem in enumerate(productos):
            item = ItemLoader(Producto(), elem)
            item.add_xpath(
                # 'imagen', './div[@class="dkt-product__gallery"]/div/div/div/div/picture/source[5]/@srcset')
                # 'imagen', './div/div/div/div/div/picture/source[position()=4]/@srcset')
                'imagen', './div[@class="dkt-product__gallery"]/div/div/div[position()=1]/div/picture/source/source/source/source/source/@srcset')
            item.add_xpath(
                'titulo', 'div[@class="dkt-product__infos-wrapper"]/div[@class="dkt-product__infos__link"]/div/div/a/h2/text()')
            item.add_xpath(
                # 'precio', './div[@class="dkt-product__infos-wrapper"]/div/div/div[@class="dkt-product__price"]/div/div/@data-price')
                'precio', './div[@class="dkt-product__infos-wrapper"]/div/div/div[@class="dkt-product__price"]/div/div[@class="dkt-price__cartridge"]/@data-price')
            item.add_xpath(
                'precio_a', 'normalize-space(.//div[@class="dkt-price__cartridge"]/text())')
            item.add_xpath(
                'precio_b', 'normalize-space(.//div[@class="dkt-price__cartridge"]/sup/text())')
            item.add_xpath(
                'precio_previo', './div[@class="dkt-product__infos-wrapper"]/div/div/div[@class="dkt-product__price"]/div/span/span[position()=1]/text()')
            item.add_xpath(
                'reduccion', './div[@class="dkt-product__infos-wrapper"]/div/div/div[@class="dkt-product__price"]/div/span/span[position()=2]/text()')
            item.add_xpath(
                'marca', './div[@class="dkt-product__infos-wrapper"]/div/div/div/span/span/text()')
            item.add_xpath(
                'url', './div[@class="dkt-product__infos-wrapper"]/div[@class="dkt-product__infos__link"]/div/div/a/@href')
            item.add_xpath(
                'rating', './div[@class="dkt-product__infos-wrapper"]/div/div/span[@itemprop="ratingValue"]/text()')
            item.add_xpath(
                'review', './div[@class="dkt-product__infos-wrapper"]/div/div/span[@itemprop="reviewCount"]/text()')
            item.add_value('id', i)

            yield item.load_item()

# correr el programa en consola:
# scrapy runspider spider.py -o datos.csv -t csv
