#!/usr/bin/env python
import webbrowser
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from random import randint
import time 
import os



userNamePasswordFile = './redditNameList.txt'
createdUserNamePasswordFile = './createdNames.txt'


def create_account(username, password):
    try:
        print('[+] restarting tor for a new ip address...')
        os.system('taskkill /IM tor.exe /F')
        torexe = os.popen(r'C:\Users\ '.removesuffix(' ') + os.environ.get( "USERNAME" ) + r'\Desktop\Tor Browser\Browser\TorBrowser\Tor\tor.exe')

        profile = FirefoxProfile(r'C:\Users\ '.removesuffix(' ') + os.environ.get( "USERNAME" ) + r'\Desktop\Tor Browser\Browser\TorBrowser\Data\Browser\profile.default')
        profile.set_preference('network.proxy.type', 1)
        profile.set_preference('network.proxy.socks', '127.0.0.1')
        profile.set_preference('network.proxy.socks_port', 9050)
        profile.set_preference("network.proxy.socks_remote_dns", False)
        profile.update_preferences()
        browser = webdriver.Firefox(firefox_profile= profile, executable_path=r'.\geckodriver.exe')

        #get reddit account creation page
        browser.set_window_size(683, 744)
        browser.get('http://old.reddit.com/login')
        #insert username
        time.sleep(randint(1,5))
        browser.find_element_by_id('user_reg').click()
        browser.find_element_by_id('user_reg').send_keys(username)
        #insert password
        time.sleep(randint(1,5))
        browser.find_element_by_id('passwd_reg').click()
        browser.find_element_by_id('passwd_reg').send_keys(password)
        time.sleep(randint(1,5))
        browser.find_element_by_id('passwd2_reg').click()
        browser.find_element_by_id('passwd2_reg').send_keys(password)

        #open captcha
        WebDriverWait(browser, 120).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@title='reCAPTCHA']")))
        WebDriverWait(browser, 120).until(EC.presence_of_element_located((By.XPATH, "//*[@id='recaptcha-anchor']")))
        browser.find_element_by_xpath("//*[@id='recaptcha-anchor']").click()
        browser.switch_to.default_content()

        print("[+] Please complete the captcha, then click sign up")
        WebDriverWait(browser, 240).until(EC.title_is("reddit: the front page of the internet"))
        browser.quit()
    except:
        os.system('cls')
        print('[+] Timeout reached, restarting browser to try again')
        browser.quit()
        create_account(username,password)





def main():
    os.system('cls')
    #run account generator for each user in list
    created = open(createdUserNamePasswordFile, 'a')
    creds = [cred.strip() for cred in open(userNamePasswordFile).readlines()]
    for cred in creds:
        username, password = cred.split(':')
        print('[+] creating account for %s with password %s' % (username,password))
        create_account(username, password)
            
        print('[+] writing name:password to created names...')
        created.write(username + ':' + password + '\n')
        print('[+] deleting name:password from original file...')
        lines = [line.strip() for line in open(userNamePasswordFile).readlines()]
        f = open(userNamePasswordFile, 'w')
        for line in lines:
            if (line != cred):
                f.write(line + "\n")
        f.close()
        time.sleep(2)
        os.system('cls')
    created.close()

    
main()
