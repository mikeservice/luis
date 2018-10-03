"""
Groupon.com spider
"""
from src.models import Coupon, Store, session, StoreStatus

from ..browser import Browser, ElementNotVisibleException, NoSuchElementException, app

class GroupOnSpider(Browser):
    """Groupon Spider
    This class will be used to scrape coupons from groupon.com
    """
    def __init__(self, task=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = kwargs.get("base_url", "https://www.groupon.com")
        self.start_point = kwargs.get("start_point", "/coupons/stores/nike.com")
        self.task = task
        
        if self.task:
            self.task.update_state(state='PROGRESS',
                                meta={'current': 0, 'total': 50,
                                'status': "Init: Search page is opening..."})

    def parse_list(self):
        count = 0

        self.open_list_url()

        if self.task:
            self.task.update_state(state='PROGRESS',
                                meta={'current': 2, 'total': 50,
                                'status': "Init: Grabing coupons list..."})
        
        couponElements = self.driver.find_elements_by_css_selector(".nine.columns ol li>div")

        while len(self.coupons) < len(couponElements) and count < 200:
            count += 1

            coupon = dict()
            couponEl = couponElements[len(self.coupons)]

            if self.task:
                self.task.update_state(state='PROGRESS',
                            meta={'current': 2 + len(self.coupons), 'total': 2 + len(couponElements),
                            'status': "Init: Grabing coupons list..."})
            
            priceEl = couponEl.find_element_by_css_selector(".discount.c-txt-black")
            coupon['price'] = priceEl.text

            dataContainer = couponEl.find_element_by_css_selector(".coupon-data")
            typeEl = dataContainer.find_element_by_css_selector("span[itemprop=category]")
            coupon['type'] = typeEl.text

            titleEl = dataContainer.find_element_by_css_selector("h2[itemprop=name]")
            coupon['original_title'] = titleEl.text[:100]

            descEl = dataContainer.find_element_by_css_selector("p span[itemprop=description]")
            coupon['original_description'] = descEl.text

            ButtonsContainer = couponEl.find_element_by_css_selector(".buttons")
            
            try:
                expDateEl = dataContainer.find_element_by_css_selector("meta[itemprop=validThrough]")
                coupon['expiry_date'] = expDateEl.get_attribute('content')
            except NoSuchElementException as e:
                coupon['expiry_date'] = None

            # Code to grab coupon code value
            try:
                urlEl = ButtonsContainer.find_element_by_css_selector("a[data-bhw=ActivateOnlineSaleButton], a[data-bhw=GetOnlinePromoCodeButton], a[data-bhw=GetInstorePromoCodeButton], a[data-bhw=ActivateInstoreSaleButton], a[data-bhw=CustomCouponActionButton]")
                
                coupon['mode'] = urlEl.get_attribute('data-bhw')

                urlEl.click()

                self.wait_for(1)

                coupon['url'] = self.driver.current_url

                if len(self.driver.window_handles) > 1:
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    couponCodeElement = self.driver.find_element_by_css_selector("div.vodal-dialog div.coupon-content div.code span.text-select")

                    coupon['code'] = couponCodeElement.text
            except NoSuchElementException as e:
                print(str(e))
            finally:
                self.coupons.append(coupon)
                if (len(self.driver.window_handles) > 1):
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
            
            try:
                self.driver.find_element_by_css_selector(".vodal-dialog .vodal-close").click()
            except Exception as e:
                print(str(e))
                
            couponElements = self.driver.find_elements_by_css_selector(".nine.columns ol li>div")
        
        return self.coupons

    def run(self, id):
        """Method to execute spider to grab coupons for the store specified by `id`
        > `id`: integer
        """
        self.parse_list()
        
        if not self.write_coupons_to_db(id):
            self.write_coupons_to_db(id)
            
        self.close()


