from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
import os
import socket
import time
import sys
from PIL import Image

SPIN_BAR = '-\\|/'
timeout = 20
socket.setdefaulttimeout(timeout)

options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('window-size=1920x1080')
# options.add_argument("disable-gpu")
#options.add_argument("--disable-gpu")

driver = webdriver.Chrome('./chromedriver', chrome_options=options)

driver.set_page_load_timeout(30)
opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

def parse_name(name = ''):
    name = name.replace('\\', '￦')
    name = name.replace('/', '／')
    name = name.replace(':', '：')
    name = name.replace('*', '＊')
    name = name.replace('?', '？')
    name = name.replace('"', '＂')
    name = name.replace('<', '＜')
    name = name.replace('>', '＞')
    name = name.replace('|', '｜')
    name = name.replace('.', '．')
    return name

def download_manga(url = '', V = False):
    driver.get(url)
    while(True):
        #제목 찾기
        #사용할 웹 페이지에 따라 수정하셔야 합니다.
        while True:
            try:
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                title = soup.find('meta', attrs={'name': 'title'})
                title = title.get('content')
            except Exception as e:
                print(e)
                time.sleep(5)
                for i in range(3):
                    try:
                        driver.refresh()
                    except Exception as ex:
                        print(ex)
                    else:
                        break
            else:
                break

        title = parse_name(title)
        try:
            os.mkdir('./Result/' + title)
        except FileExistsError:
            pass

        #이미지가 있는 클래스 찾기
        #사용할 웹 페이지에 따라 수정하셔야 합니다.
        tag = soup.find('div', attrs={'class': 'view-content scroll-viewer'})
        images = tag.find_all('img')
        if len(images) != 0:
            for i, img in enumerate(images):
                if V:
                    sys.stdout.write('\r' + title + ' ' + str(i + 1) + '/' + str(len(images)) + '장 ')
                    sys.stdout.flush()
                img_src = img.get('src')
                if img_src is None:
                    img_src = img.get('lazy-src')

                result = driver.execute_script("return img_list")

                loop = 5
                while(loop > 0):
                    try:
                        urllib.request.urlretrieve(result[i], './Result/' + title + '/' + str(i + 1) + '.jpg')
                    except Exception as e:
                        print(e)
                        loop -= 1
                        continue
                    else:
                        break
                    print(i)

        #캔버스인 경우
        else:
            images_container = driver.find_element_by_css_selector('div.view-content.scroll-viewer')
            images = images_container.find_elements_by_tag_name('canvas')

            js_script = '''\
            bottom_navi = document.getElementsByClassName('manga-bottom-navi');
            bottom_navi[0].style.display = 'none';
            '''
            driver.execute_script(js_script)

            for i, img in enumerate(images):
                if V:
                    sys.stdout.write('\r' + title + ' ' + str(i) + '/' + str(len(images)) + '장 ')
                    sys.stdout.flush()
                img.screenshot('./Result/' + title + '/' + str(i) + '.png')
            images[0].screenshot('./Result/' + title + '/0.png')

            #합치기
            i = 0
            while True:
                if os.path.exists('./Result/' + title + '/' + str(2 * i) + '.png'):
                    up_image = Image.open('./Result/' + title + '/' + str(2 * i) + '.png')
                    down_image = Image.open('./Result/' + title + '/' + str(2 * i + 1) + '.png')
                    new_image = Image.new('RGB', (up_image.size[0], up_image.size[1] + down_image.size[1]))
                    new_image.paste(up_image, (0,0))
                    new_image.paste(down_image, (0, up_image.size[1]))
                    up_image.close()
                    down_image.close()
                    os.remove('./Result/' + title + '/' + str(2 * i) + '.png')
                    os.remove('./Result/' + title + '/' + str(2 * i + 1) + '.png')
                    new_image.save('./Result/' + title + '/' + str(i) + '.png')
                    i += 1
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
    
    print('\n' + title + " done!")

if __name__ == "__main__":
    download_manga(input(), True)