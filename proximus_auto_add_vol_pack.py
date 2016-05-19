#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright (C) 2016   Tuxicoman & shakasan

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

Link to the post on Tuxicoman website : https://tuxicoman.jesuislibre.net/2016/05/internet-vraiment-illimite-chez-belgacomproximus.html

Link to the Github of shakasan : https://github.com/shakasan/bgc_add_vol_pack

---

Script modified by :
  Nicolas DE VOS (dz0org)

Github :
  https://github.com/shakasan/bgc_add_vol_pack

Changelog :
    - Create of object classes
    - Use chromedriver instead of firefox, see the variable path_browser
    - Random pause of some seconds between the queries
    - Check the amount of the invoice is equal to ' 0,00'
    - Add a cron job at the crontab

 Please before running, check if the depends below are installed :
 sudo aptitude install chromedriver xvfb python-selenium python-crontab
"""


from argparse import ArgumentParser
from sys import exit, argv
from os import path

from random import randint
from time import sleep

from pyvirtualdisplay import Display
from crontab import CronTab

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class VolumePack:
    """ Add a free volume pack for Proxmius FAI """

    path_browser = "/usr/lib/chromium/chromedriver"

    def __init__(self, user, pwd, debug):

        self.debug = debug
        self.user = user
        self.pwd = pwd

        self.set_debug()        # if self.debug = yes view procedure step by step in the browser
        self.browser = webdriver.Chrome(self.path_browser)
        self.login()
        self.select()
        self.confirmed()

    def login(self):

        self.browser.get('https://www.belgacom.be/login/fr/?ru=https%3A%2F%2Fadmit.belgacom.be%2F&pv=fls')

        try:
            self.browser.switch_to_frame(self.browser.find_element_by_xpath('//iframe[@name="loginIframe"]'))
            self.browser.switch_to_frame(self.browser.find_element_by_xpath('//iframe[@name="frame"]'))

            self.browser.find_element_by_xpath('//input[@id="loginForm:userName"]').send_keys(self.user)
            self.browser.find_element_by_xpath('//input[@id="loginForm:password"]').send_keys(self.pwd)

            self.browser.find_element_by_xpath('//input[@id="loginForm:continue"]').click()

        except:
            self.error_take_screenshot('to login procedure')
            exit(2)

    def select(self):

        self.wait_before_continue('ns_7_7OGJPDU518D6A0ACILTFQT2004_myBillAndProducts')

        try:

            self.browser.find_element_by_xpath('//i[contains(@class, "icon-Internetlaptop")]').click()
            self.wait_before_continue("ns_7_7OGJPDU51OKG60I9TQGKIB1004_myInternetServicesContent")

            self.browser.find_element_by_xpath('//a[@href="#pb-tabs-notActivated"]').click()
            services = self.browser.find_elements_by_xpath('//a[contains(@class, "pb-ico-plus")]')

        except:
            self.error_take_screenshot('to go on the service page')
            exit(3)

        # choice among the services availables
        try:
            for service in services:
                extraVol = "Extra Volume 20 GB"
                if extraVol in service.get_attribute("innerHTML"):
                    service.click()
                    break

        except:
            self.error_take_screenshot('to select the service pack')
            exit(3)

    def confirmed(self):

        # auto find url
        bt_link_order = "/eservices/wps/myportal/myProducts/myOrder?selectedOption=hbs_volume_pack_20_free"
        print self.browser.find_element_by_xpath('//a[contains(@href,"' + bt_link_order + '")]').text

        try:
            self.browser.find_element_by_xpath('//a[contains(@href,"' + bt_link_order + '")]').click()
            self.wait_before_continue("ns_7_7OGJPDU51OKOF0I9LM7HMQ30K5_")

            self.browser.find_element_by_xpath('//a[contains(@class,"pcp-order-next")]').click()
            self.wait_before_continue("ns_7_7OGJPDU51OKOF0I9LM7HMQ30K5_")

        except:
            self.error_take_screenshot('the order of the volume pack')
            exit(4)

        price = self.browser.find_element_by_xpath('//tr[contains(@class, "pb-table-total")]').find_element_by_class_name('pb-textAlignCenter').text

        if price.find(' 0,00') == -1:
            self.error_take_screenshot("the checking of invoice")
            exit(4)

        try:
            self.browser.find_element_by_xpath('//input[@id="generalTerms"]').click()

        except:
            self.error_take_screenshot("the accepted of general terms")
            exit(4)
        try:
            self.browser.find_element_by_xpath('//a[@eventdetail="confirmOrderLink"]').click()

        except:
            self.error_take_screenshot('the finalization of the order')
            exit(4)

        self.browser.find_element_by_xpath('//a[@href="/eservices/wps/myportal/myProducts"]').click()

    def wait_before_continue(self, id):

        WebDriverWait(self.browser, 60).until(
            EC.presence_of_element_located((By.ID, id))
        )

        # wait some seconds before continue
        sleep(randint(2, 10))

    def error_take_screenshot(self, txt):

            path_screenshot = '/tmp/proximus_add_vol_pack.png'
            print 'Error during ' + txt + ', please show the screenshot : ' + path_screenshot
            self.browser.get_screenshot_as_file(path_screenshot)

    def set_debug(self):

        if self.debug == 'yes':
            value = 1
        else:
            value = 0       # not display window browser

        self.display = Display(visible=value, size=(1440, 900)).start()

    def __del__(self):

        self.browser.quit()

        if self.debug == 'yes':
            self.display.stop()
        #    import os
        #    os.system("killall chromedriver && killall chrome-sandbox")


class Crontab:
    """ Add a cron job """

    def __init__(self, user, pwd):

        self.cron = CronTab(user=True)
        self.cmd = '`/usr/bin/python ' + path.realpath('') + '/' + path.basename(__file__) + ' ' + user + ' \"' + pwd + '\"`'

        if self.is_no_exist() is not True:
            self.add_job()

    def add_job(self):

        self.job = self.cron.new(command=self.cmd, comment='Proximus add a volume pack every 4 days')
        self.job.setall(0, 20, '*/4', '*', '*')

        self.cron.write_to_user(user=True)
        print 'Add the cron job at your crontab done'

    def is_no_exist(self):

        for job in self.cron.commands:
            if job == self.cmd:
                return True

    # def del_job(self):
    #     self.cron.remove_all(command=self.cmd)


if __name__ == "__main__":

    parser = ArgumentParser(description='Add a free extra data volume pack to Proximus FAI', usage='python ' + argv[0] + ' \"toto@proximus.be\" \"monSuperPwd\" --debug=yes --add_cron_job=yes')
    parser.add_argument('user', type=str, help='User proximus email')
    parser.add_argument('pwd', type=str, help='Password proximus')
    parser.add_argument('--add_cron_job', default='no', help='Add a job at crontab, use \'yes\' or \'no\' (default: no)')
    parser.add_argument('--debug', default='no', help='Use Xvfb to view step by step in your browser, use \'yes\' or \'no\' (default: no)')

    if len(argv) < 3:
        print parser.print_help()

    args = parser.parse_args()
    user = args.user
    pwd = args.pwd

    # VolumePack(user, pwd, args.debug)

    if args.add_cron_job == 'yes':
        Crontab(user, pwd)

    exit(0)
