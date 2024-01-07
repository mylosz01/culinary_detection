from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time
import urllib
import requests
import shutil

# Setup chrome driver
driver = webdriver.Chrome()

# Navigate to the url
driver.get('https://www.google.com/search?q=table+knife&tbm=isch&ved=2ahUKEwj-zKOy_o-DAxUO4bsIHVfXCeIQ2-cCegQIABAA&oq=table+knife&gs_lcp=CgNpbWcQAzIFCAAQgAQyBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB46CggAEIAEEIoFEEM6CAgAEIAEELEDOgsIABCABBCxAxCDAVDSswFY-bsBYJG9AWgAcAB4AIAB-wGIAdUIkgEGMTIuMC4xmAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=LIN7Zf6GC47C7_UP166nkA4&bih=754&biw=1495&client=opera-gx&hs=bsw')



check = input('WAITING....')
# Find all images
images = driver.find_elements(By.TAG_NAME, 'img')

# Print number of images
print(f'There are {len(images)} images.')

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(4)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
    #break #insert press load more
        try:
            print('przycisk')
            element = driver.find_element(By.CLASS_NAME,'LZ4I') #returns list
            element.click()
            time.sleep(6)
        except:
            break

    last_height = new_height

images = driver.find_elements(By.TAG_NAME, 'img')

# Print number of images
print(f'There are {len(images)} images.')

for idx, img in enumerate(images):
    try:
        data_url = img.get_attribute('src')
        response = requests.get(data_url, stream=True)
        with open(f'my_pic{str(idx)}.png', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        time.sleep(0.2)
    except:
        continue

# Close the driver
driver.quit()
driver.close()