import bs4, requests, sys, os, time, urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
songs = []

path = os.getcwd() + "/songs"
try:
    for file in os.listdir(path):
        if file.endswith(".crdownload"):
            os.remove(path+"/"+file)
            break
except:
    pass
if len(sys.argv)>1:
    songs = songs + [" ".join(sys.argv[1:])]
else:
    print("Enter the song you want to download. Leave the input empty when you are done.")
    while True:
        song = input("Enter the song: ")
        if len(song)==0:
            break
        songs = songs+[song]
print("For video input '720p' or '360p'. For audio, type '320kbps', '192kbps' or '128kbps'")
format = input("Enter the format you want to download: ")
print('\n')

options = webdriver.ChromeOptions()
options.add_experimental_option("prefs",{
    "download.default_directory": os.getcwd()+"\songs",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True
})
# options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=options)
browser.set_window_position(-2000,0)

def findsong(s):
    elem = browser.find_element_by_class_name(s)
    elem.click()
    time.sleep(2)
    wait = WebDriverWait(browser, 100)
    time.sleep(3)
    browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "a")))
    elem = browser.find_elements_by_tag_name("a")
    print("[@] Downloading song: " + song)
    time.sleep(2)
    return elem

def closeWindow():
    if len(browser.window_handles) > 1:
        time.sleep(1)
        current = browser.window_handles[0]
        handles = browser.window_handles
        for handle in handles[1:]:
            browser.switch_to_window(handle)
            browser.close()
        browser.switch_to_window(current)

def waitForFinish():
    path = os.getcwd() + "/songs"
    out = True
    time.sleep(3)
    while out:
        time.sleep(1)
        out = False
        for file in os.listdir(path):
            if file.endswith(".crdownload"):
                out = True



for song in songs:
    try:
        req = requests.get("https://www.emp3c.co/mp3/"+song)
        req.raise_for_status()
        soup = bs4.BeautifulSoup(req.text, "html.parser")
        elems = soup.find_all(class_="mp3-dl")
    except:
        print("Error downloading song: " + song+ ". Invalid song name or the song may be removed.")
        continue
    link = "https://www.emp3c.co"+elems[1].a.get('href')
    if (format=='128kbps' or format=="256kbps" or format=="192kbps" or format=="320kbps"):
        browser.get(link)
        try:
            elem = findsong("download_now2")
        except:
            print("Error downloading song: " + song)
            continue
        elem[0].click()
        closeWindow()
        browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))
        elem = browser.find_elements_by_tag_name("a")

        if (format == '320kbps'):
            element = elem[0]
        elif (format == '256kbps'):
            element = elem[1]
        elif (format == '192kbps'):
            element = elem[2]
        elif (format == '128kbps'):
            element = elem[3]
        element.click()
        waitForFinish()

    elif (format!='720p' and format!='360p'):
        print("Enter a valid input.")
    else:
        browser.get(link)
        try:
            elem = findsong("download_now3")
        except:
            print("Error Downloading song: "+ song)
            continue
        if(format =='720p'):
            element = elem[0]
        else:
            element = elem[2]
        url = element.click()
        closeWindow()
        waitForFinish()

handles = browser.window_handles
for handle in handles:
    browser.switch_to_window(handle)
    browser.close()

print("All songs downloaded!")