from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
import os
import socket

timeout = 20
socket.setdefaulttimeout(timeout)

driver = webdriver.Chrome('./chromedriver')
opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

def download_manga(url = '', V = False):
    driver.get(url)
    while(True):
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        #제목 찾기
        #사용할 웹 페이지에 따라 수정하셔야 합니다.
        title = soup.find('meta', attrs={'name': 'title'})
        title = title.get('content')
        try:
            os.mkdir('./Result/' + title)
        except FileExistsError:
            pass

        #이미지가 있는 클래스 찾기
        #사용할 웹 페이지에 따라 수정하셔야 합니다.
        tag = soup.find('div', attrs={'class': 'view-content scroll-viewer'})
        images = tag.find_all('img')
        if V:
            print(title + ' '+ str(len(images)) + '장')
        for i, img in enumerate(images):
            img_src = img.get('src')
            
            loop = 5
            while(loop > 0):
                try:
                    urllib.request.urlretrieve(img_src, './' + title + '/' + str(i) + '.jpg')
                except Exception as e:
                    print(e)
                    loop -= 1
                    continue
                else:
                    break
        
        #다음 화 버튼 찾기
        #사용할 웹 페이지에 따라 수정하셔야 합니다.
        try:
            driver.find_element_by_xpath('//a[@class="chapter_next"]').click()
        except ElementNotInteractableException:
            break
        except Exception as e:
            print(e)
    
    print(title + " done!")

if __name__ == "__main__":
    download_manga(input(), True)