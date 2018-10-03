"""
User Defined Selenium Browser
"""

import json, datetime, csv, logging, sys, time
import ftfy, os, requests, tldextract

from urllib.parse import urlencode, urlparse, urlunparse, parse_qs
from sys import platform

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.common.action_chains import ActionChains

from src import app
from src.models import Proxy, Store, StoreStatus, Coupon, db, session
from .wordai import WordAI

class Browser:
    def __init__(self, *args, **kwargs):
        self.driver = None
        self.init_timer = 0
        self.click_counter = 0
        self.proxy = None
        self.base_url = ""
        self.start_point = ""
        self.coupons = list()
        self.source = kwargs.get('source', 'groupon')

        if platform != 'win32':
            self.display = Display(visible=0, size=(1200, 900))
            self.display.start()

        if self.start_browser():
            print("A browser instance created Successfully.")
        else:
            print("Something went wrong with brower instance creation.")
    
    def get_browser(self):
        return self.driver
    
    def open(self, url, **kwargs):
        try:
            self.driver.get(url)
            if kwargs.get('wait_for'):
                time.sleep(int(kwargs.get('wait_for')))
            return True
        except Exception as e:
            print("Exception occurred in open method of browser class")
            print(str(e))
            print("----------------------------------")
            return False
    
    def click(self, element):
        if self.click_counter > 5:
            return False
        else:
            self.click_counter += 1
        
        try:
            self.wait_for(1)
            self.move_to(element)
            element.click()
            return True
        except Exception as e:
            print(str(e))
            print("Element not found...{0}".format(self.click_counter))
            return self.click(element)
    
    def move_to(self, element):
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

    def get_new_credential(self):
        with app.app_context():
            self.proxy = Proxy.last()
            if self.proxy:
                return self.proxy.name
            else:
                return None

    def write_coupons_to_db(self, id):
        # self.process_wordai()
        with app.app_context():
            for row in self.coupons:
                coupon = Coupon(
                    original_title=row.get('original_title'), 
                    title=row.get('original_title'), 
                    original_description=row.get('original_description'), 
                    description=row.get('original_description'), 
                    price=row.get('price'), 
                    expiry_date=row.get('expiry_date'), 
                    url=row.get('url'), 
                    code=row.get('code'),
                    store_id=id
                )
                session.add(coupon)
            
            try:
                session.commit()
            except Exception as e:
                print(str(e))
                session.rollback()

            store = Store.query.get(id)
            store.status = StoreStatus.done
            store.job_uid = None

            try:
                session.commit()
                return True
            except Exception as e:
                print(str(e))
                session.rollback()
                return False

    def wait_for(self, period=1):
        time.sleep(period)
    
    def get_promo_code(self):
        """This should be implemented/overrided later to get the correct code from the layout.
        So this should be depends on layout of source website.
        """
        pass

    def start_browser(self):
        """
        cross platform browser initiation
        :param proxy: proxy binded to specific account
        :return: chrome webdriver
        """
        print("Preparing selenium browser instance...\nGetting proxy instance.")
        print(self.get_new_credential())

        with app.app_context():
            if self.driver:
                self.close()

            if platform == 'darwin':
                chromedriver = os.path.join(app.config.get('BASE_DIR'), 'storage/chromedriver_mac')
            elif platform == 'win32':
                chromedriver = os.path.join(app.config.get('BASE_DIR'), 'storage/chromedriver.exe')
            else:
                chromedriver = os.path.join(app.config.get('BASE_DIR'), 'storage/chromedriver_linux')

            options = webdriver.ChromeOptions()
            # options.add_argument("--headless")
            options.add_argument("--window-size=1200,900")
            options.add_argument('--dns-prefetch-disable')
            options.add_argument('--js-flags="--max_old_space_size=4096"')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')

            if not self.proxy:
                self.get_new_credential()

            # if self.proxy and self.proxy.name:
            #     options.add_argument("--proxy-server=" + self.proxy.name)
            prefs = {"profile.managed_default_content_settings.images":2}
            options.add_experimental_option("prefs",prefs)
        
            try:
                self.driver = webdriver.Chrome(chromedriver, chrome_options=options)
                return True

            except Exception as e:
                print("Got an error in starting browser.")
                print(str(e))

                if self.driver:
                    print("Quiting the driver...")
                    self.close()
                
                return False

    def prepare(self, task=None, total=1):
        if self.init_timer > 10:
            return None, None
        else:
            self.init_timer += 1

        if not self.driver:
            self.start_browser()

            if task:
                task.update_state(state='PROGRESS',
                        meta={'current': 1, 'total': total,
                        'status': "Retrying to start browser because an unexpected exception raised."})
            return self.prepare(task, total)

        return True

    def open_list_url(self):
        self.coupons.clear()
        try:
            self.driver.get("{0}{1}".format(self.base_url, self.start_point))
            time.sleep(1)
            return True
        except Exception as e:
            print(str(e))
            return False


    def mark_credential_as_dead(self, **kwargs):
        with app.app_context():
            return Proxy.mark_as(self.proxy.id, **kwargs)

    def close(self):
        if self.driver:
            print("Closing chrome driver...")
            self.driver.quit()
            self.driver = None

            if platform != 'win32':
                self.display.stop()

    def run(self):
        print("Starting the default method...")

    def process_wordai(self):
        wai = WordAI()
        for c in self.coupons:
            original_title = c.get('original_title')
            original_description = c.get('original_description')

            c['title'] = c['original_title']
            c['description'] = c['original_description']
            c['title_changed'] = False
            c['description_changed'] = False

            try:
                title = wai.unique_variation(original_title)

                if not original_title in title:
                    print("Title Changed from \"{0}\" to \"{1}\"".format(original_title, title))
                    c['title'] = title
                    c['title_changed'] = True
                    
            except Exception as e:
                print(str(e))

            try:
                description = wai.unique_variation(original_description)

                if not original_description in description:
                    print("Description Changed from \n\"{0}\" \nto\n \"{1}\"".format(original_description, description))
                    c['description'] = description
                    c['description_changed'] = True
            except Exception as e:
                print(str(e))
                
    def rebuild_url(self):
        pass

