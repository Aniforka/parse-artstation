from undetected_selenium_base import *
from time import perf_counter
import requests
import json
import os    

user_url = ""

time_begin = perf_counter()

nick = user_url.split('/')[-1]
count_of_pictures = 0

try:
    os.mkdir(nick)
except Exception: pass


driver = create_driver(headless=True)
driver.get(f"https://www.artstation.com/users/{nick}/projects.json")
content = driver.find_element("xpath", "//body").text
parsed_json = json.loads(content)

for data in parsed_json["data"]:
    if int(data["assets_count"]) == 1:
        title = data["title"].replace('/', '-')
        img = data["cover"]["small_square_url"].replace("small_square", "large").split('?')[0]

        if img.count('/') > 11:
            new_img = ''
            count = 0

            for s in img:
                if s == '/': count += 1
                if count != 10: new_img += s

            img = new_img

        p = requests.get(img)
        out = open(f"./{nick}/{title}.jpg", "wb")
        out.write(p.content)
        out.close()
        count_of_pictures += 1
    else:
        try:
            os.mkdir(f"./{nick}/{title}")
        except Exception: pass

        driver.get(data["permalink"])
        pictures = driver.find_elements("xpath", "//div[@class='project-assets-list multiple-images']/project-asset")

        index = 1
        for picture in pictures:
            img = picture.find_element("xpath", "./div/div/picture/source").get_attribute("srcset").split('?')[0]
            p = requests.get(img)
            out = open(f"./{nick}/{title}/{index}.jpg", "wb")
            out.write(p.content)
            out.close()
            count_of_pictures += 1

            index += 1

delete_driver(driver)

time_end = perf_counter()

print(f"Скачано артов: {count_of_pictures}")
print(f"Затрачено, с: {round(time_end - time_begin, 2)}\n")