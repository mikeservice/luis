"""
Main spiders package
"""
from .groupon import GroupOnSpider
from .retailmenot import RetailMeNotSpider
from .offers import OffersSpider

CouponSpiders = {
    'groupon': GroupOnSpider,
    'retailmenot': RetailMeNotSpider,
    'offers': OffersSpider
}
