from src.models import Coupon, Store, session, StoreStatus

from ..browser import Browser, ElementNotVisibleException, NoSuchElementException, app

class RetailMeNotSpider(Browser):
    """Groupon Spider
    This class will be used to scrape coupons from groupon.com
    """
    def __init__(self, task=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = kwargs.get("base_url", "https://www.retailmenot.com")
        self.start_point = kwargs.get("start_point", "/view/olay.com")
        self.task = task
        self.click_counter = 0

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
            self.driver.find_element_by_css_selector("div#modal div.modal-header span.modal-close").click()
            return True
        except Exception as e:
            print(str(e))
            return False

    def parse_list(self):
        self.open_list_url()
        self.wait_for(0.2)
        self.close_modal()
        self.wait_for(3)
        couponElements = self.driver.find_elements_by_css_selector("ul.offer-list[data-bucket=top-rated] li.offer-list-item, div[data-bucket=unpopular] ul.offer-list li.offer-list-item")
        
        titleEl = couponElements[0].find_element_by_css_selector("div.offer-item-body .offer-item-title a")
        
        self.click_counter = 0
        if self.click(titleEl):
            self.wait_for(1)

        if self.task:
            self.task.update_state(state='PROGRESS',
                            meta={'current': 2, 'total': 2 + len(couponElements),
                            'status': "Init: Grabing coupons list..."})

        count = 0
        couponElements = self.driver.find_elements_by_css_selector("ul.offer-list[data-bucket=top-rated] li.offer-list-item, div[data-bucket=unpopular] ul.offer-list li.offer-list-item")

        while len(self.coupons) < len(couponElements) and count < 200:
            count += 1

            self.close_modal()
            self.wait_for(1)

            if self.task:
                self.task.update_state(state='PROGRESS',
                            meta={'current': 2 + len(self.coupons), 'total': 2 + len(couponElements),
                            'status': "Init: Grabing coupons list..."})

            couponEl = couponElements[len(self.coupons)]
            coupon = dict()

            priceEl = couponEl.find_element_by_css_selector(".offer-type-sale.offer-anchor, .offer-type-code.offer-anchor")
            coupon['price'] = priceEl.text

            typeEl = couponEl.find_element_by_css_selector(".offer-item-head .offer-item-label")
            coupon['type'] = typeEl.text

            titleEl = couponEl.find_element_by_css_selector("div.offer-item-body .offer-item-title a")
            coupon['original_title'] = titleEl.text[:100]

            actionButton = couponEl.find_element_by_css_selector("div.offer-item-actions a.offer-button")
            if "button-show-code-revealed" in actionButton.get_attribute("class").split("\t"):
                coupon['code'] = actionButton.text

            seeDetailLink = couponEl.find_element_by_css_selector("div.offer-item-details a.offer-item-details-link")
            # seeDetailLink.click()
            self.driver.execute_script("arguments[0].click();", seeDetailLink)
            self.wait_for(1)

            detailTabLlink = couponEl.find_element_by_css_selector("li.offer-item-tabs-header-item a.offer-item-tabs-header-item-link")
            self.driver.execute_script("arguments[0].click();", detailTabLlink)
            self.wait_for(1)

            detailEls = couponEl.find_elements_by_css_selector(".offer-item-tabs div.offer-item-tabs-content-details p")
            if len(detailEls) == 1 and "details: " in detailEls[0].text.lower():
                coupon['original_description'] = detailEls[0].text[len("details: "):]
            elif len(detailEls) == 2:
                coupon['expiry_date'] = detailEls[0].text[len("ends: "):] if "ends: " in detailEls[0].text.lower() else None
                coupon['original_description'] = detailEls[1].text[len("details: "):] if "details: " in detailEls[1].text.lower() else None
            
            if len(self.driver.window_handles) > 1:
                self.driver.switch_to.window(self.driver.window_handles[1])
                coupon['url'] = self.driver.current_url
                self.driver.close()

            self.driver.switch_to.window(self.driver.window_handles[0])

            self.coupons.append(coupon)

            try:
                self.driver.find_element_by_css_selector("div.modal-backdrop fade").click()
                self.click_counter = 0

                if self.click(titleEl):
                    self.wait_for(1)
            except Exception as e:
                print(str(e))

            couponElements = self.driver.find_elements_by_css_selector("ul.offer-list[data-bucket=top-rated] li.offer-list-item, div[data-bucket=unpopular] ul.offer-list li.offer-list-item")
        
        return self.coupons
