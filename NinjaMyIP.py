from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from time import sleep
from tqdm import tqdm 
from bs4 import BeautifulSoup
import re
import random
import requests
import sys



options = Options()


ip_port = []
#Grab all the avaliable proxies, and store them in a list called ip_port. 
def Proxies():
    options.headless = True
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(executable_path=r'chromedriver.exe', chrome_options=options)
    #url = "https://www.us-proxy.org/"
    #url = "https://www.free-proxy-list.net"
    url = "https://www.sslproxies.org/"
    driver.get(url)
    sleep(1.5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    print("Beginning Extraction...\n")
    for tr in tqdm(soup.find_all("tr",  {"class": ["even", "odd"]})):
        ip = tr.find("td").text
        port = tr.find("td").find_next_sibling("td").text
        ip_port.append(ip + ":" + port)
        #print(ip + ":" + port)
    
    #print()
    #print(ip_port)
    print()
    
    driver.close()

#Here we perform a testing on each proxy. If we recieve a response then we use that proxy.
#Otherwise, we remove that proxy and randomly choose another. 
def TestProxies():
    url = "https://www.icanhazip.com/"
    try:
        if len(ip_port) != 0:
            proxy_element = random.choice(ip_port)
            proxies = {
                "http": "http://"+proxy_element, 
                "https": "http://"+proxy_element
            }
            r = requests.get(url, proxies=proxies)
            #print(r.status_code)
            print(r.text)
            return proxy_element
        else: 
            print("None of the proxies worked, try again with a newer list.")
            sys.exit(1)
    except SystemExit as e:
        sys.exit(e)
    except:
        print("Trying another proxy...")
        ip_port.remove(proxy_element)
        TestProxies()
         
#Applying the proxy that responded to the argument, we are able to open that url.
#Therefore, having a different IP, and we ready to browse the web. 
def OpenUrl(PROXY):
    options.headless = False
    options.add_argument('--proxy-server=%s' % PROXY)
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=r'chromedriver.exe', chrome_options=options)
    #url = "https://www.youtube.com/"
    #url = "https://www.icanhazip.com/"
    url = "https://www.google.com/"
    driver.get(url)
    sleep(1)
    
    
Proxies()
PROXY = TestProxies()
#You can look up a proxy and use it manually like so, EX. PROXY = "136.228.128.6:51114"
OpenUrl(PROXY)



