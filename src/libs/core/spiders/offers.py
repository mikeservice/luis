"""Offers.com spider
"""

from src.models import Coupon, Store, session, StoreStatus

from ..browser import Browser, ElementNotVisibleException, NoSuchElementException, app


class OffersSpider(Browser):
    """Offers Spider
    This class will be used to scrape coupons from groupon.com
    """
    def __init__(self, task=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = kwargs.get("base_url", "https://www.offers.com")
        self.start_point = kwargs.get("start_point", "/bigceramicstore/")
        self.task = task

        if self.task:
            self.task.update_state(state='PROGRESS',
                                meta={'current': 0, 'total': 50,
                                'status': "Init: Search page is opening..."})

    def run(self, id):
        """Main method to execute RetailMeNot spider.
        > `id` : store_id(number)
        """
        self.parse_list()

        # count = 0
        # for coupon in self.coupons:
        #     if self.task:
        #         self.task.update_state(state='PROGRESS',
        #                         meta={'current': 2 + count, 'total': len(self.coupons) + 2,
        #                         'status': "Main: Getting the destination url..."})
        #     if self.open(coupon.get('url'), wait_for=0.1):
        #         coupon['url'] = self.driver.current_url
        #         count += 1
        
        if not self.write_coupons_to_db(id):
            self.write_coupons_to_db(id)
            
        self.close()
    
    def close_modal(self):
        try:
            self.driver.find_element_by_css_selector("#close-modal").click()
            self.wait_for(1)
            return True
        except Exception as e:
            print(str(e))
            return False

    def parse_list(self):
        self.open_list_url()

        couponElements = self.driver.find_elements_by_css_selector("div.offer-strip-container#offercontainer-1 div.offerstrip, div.offer-strip-container#offercontainer-2 div.offerstrip")

        if self.task:
            self.task.update_state(state='PROGRESS',
                            meta={'current': 2, 'total': 2 + len(couponElements),
                            'status': "Init: Grabing coupons list..."})

        count = 0

        while len(self.coupons) < len(couponElements) and count < 200:
            count += 1
            couponEl = couponElements[len(self.coupons)]
            coupon = dict()

            if self.task:
                self.task.update_state(state='PROGRESS',
                            meta={'current': 2 + len(self.coupons), 'total': 2 + len(couponElements),
                            'status': "Init: Grabing coupons list..."})

            try:
                priceEl = couponEl.find_element_by_css_selector("div.discount")
                coupon['price'] = priceEl.text
            except NoSuchElementException as e:
                coupon['price'] = 'n/a'

            try:
                typeEl = couponEl.find_element_by_css_selector(".dolphin.flag, .badge-text")
                coupon['type'] = typeEl.text
            except NoSuchElementException as e:
                coupon['type'] = ''

            titleEl = couponEl.find_element_by_css_selector("h3.name a")
            coupon['original_title'] = titleEl.text[:100]
            

            coupon['original_description'] = "n/a"

            try:
                cookie_accept_button = self.driver.find_element_by_css_selector("#_evidon-accept-button")
                cookie_accept_button.click()
            except Exception as e:
                print(str(e))

            self.click_counter = 0
            if self.click(titleEl):
                self.wait_for(1)
            
            for handler in self.driver.window_handles:
                self.driver.switch_to.window(handler)
                if "{0}{1}".format(self.base_url, self.start_point) in self.driver.current_url:
                    continue
                else:
                    coupon['url'] = self.driver.current_url
                    self.driver.close()
            
            self.driver.switch_to.window(self.driver.window_handles[0])

            self.wait_for(1)
            try:
                couponCodeEl = self.driver.find_element_by_css_selector("div#modal .coupon-code")
                coupon['code'] = couponCodeEl.text
                
            except Exception as e:
                print(str(e))
                coupon['code'] = ''

            try:
                self.close_modal()
            except Exception as e:
                print(str(e))

            
            self.coupons.append(coupon)
            couponElements = self.driver.find_elements_by_css_selector("div.offer-strip-container#offercontainer-1 div.offerstrip, div.offer-strip-container#offercontainer-2 div.offerstrip")
        
        return self.coupons
