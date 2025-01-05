from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import requests
from bs4 import BeautifulSoup
import os
import re
from typing import List, Tuple

def getPatch() -> str:
    for root, dirs, files in os.walk('Data/'):
        reg = re.compile(r'^\d{1,2}\.\d{1,2}\.\d{1,2}$')
        for dirc in dirs:
            if reg.match(dirc):
                patch = dirc
    return '-'.join(patch.split('.')[:2])

def write(data):
    with open('./Data/changes.json','w', encoding='utf-8') as t:
       json.dump(data, t, ensure_ascii=False, indent=4)
       
def getBanner(url):
    driver = webdriver.Chrome()
    driver.get(url)
    
    try:
        # Wait for the image to be present
        banner_image = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'banner-image'))
        )
        banner_src = banner_image.get_attribute('src')
    except Exception as e:
        print(f"Error: {e}")
        banner_src = None
    finally:
        driver.quit()
    
    return banner_src
    
def getName(x) -> Tuple[bool, str]:
    isName = x.find('h3', class_='change-title') is not None
    isNameMidPatch = x.find('h4', class_='change-detail-title') and x.find('h4', class_='change-detail-title').find_next_sibling(lambda tag: tag.name == 'h3' and 'change-detail-title' in tag.get('class', [])) is not None
    if isName:
        return [isName,False,x.find('h3',class_='change-title').get_text(strip=True)]
    if isNameMidPatch:
        return [False,isNameMidPatch,x.find('h4', class_='change-detail-title').get_text(strip=True)]
    return [False, False]
    
def getSummary(x) -> Tuple[bool, str]:
    isSummary = x.find('p', class_='summary') is not None
    if isSummary:
        return [isSummary,x.find('p', class_='summary').get_text(strip=True)]
    return [False]
    
def getText(x) -> str :
    isText =  x.find('blockquote') is not None
    if isText :
        return [isText,x.find('blockquote').get_text(strip=True)]
    return False
    
def getChanges(x, isName, isNameMidPatch) -> Tuple[bool, List[dict]]:
    isChanges = x.find('li') is not None
    changes = []
    if isName and isChanges:
        isChamp = x.find('h4') is not None
        if isChamp:
            for whatChange in x.find_all('h4'):
                changesTab = []
                change_html = ''
                for sibling in whatChange.find_next_siblings():
                    if sibling.name == 'h4':
                        break
                    change_html += str(sibling)
                change_html = BeautifulSoup(change_html, 'html.parser')
                for li in change_html.find_all('li'):
                    changesTab.append(li.get_text(strip=True))
                changes.append({whatChange.get_text(strip=True): changesTab})
        else:
            for li in x.find_all('li'):
                changes.append(li.get_text(strip=True).splitlines())

    if isNameMidPatch and isChanges:
        isChamp = x.find_all('h3', class_='change-detail-title ability-title')
        if isChamp:
            for champ in isChamp:
                champ_name = champ.get_text(strip=True)
                champ_changes = []
                sibling = champ.find_next_sibling()
                while sibling and sibling.name != 'h3':
                    if sibling.name == 'p' or sibling.name == 'ul':
                        if sibling.name == 'p':
                            category = sibling.get_text(strip=True)
                        elif sibling.name == 'ul':
                            ul_changes = [li.get_text(strip=True) for li in sibling.find_all('li')]
                            champ_changes.append({category: ul_changes})
                    sibling = sibling.find_next_sibling()
                changes.append({champ_name: champ_changes})

    return [isChanges, changes] if isChanges else [False]


def getCorrecBug(soup) -> Tuple[bool,Tuple]:
    correctifs = []
    isCorrectBug = soup.find('h2', id="patch-bugfixes-and-qol-changes") is not None
    if isCorrectBug:
        for whatChange in soup.find('h2', id="patch-bugfixes-and-qol-changes").find_next('div', class_='content-border').find_all('h4'):
            changesTab = []
            change_html = ''
            for sibling in whatChange.find_next_siblings():
                if sibling.name == 'h4':
                    break
                change_html += str(sibling)
            change_html = BeautifulSoup(change_html, 'html.parser')
            for li in change_html.find_all('li'):
                changesTab.append(li.get_text(strip=True))
            correctifs.append({whatChange.get_text(strip=True) : changesTab})
        return [isCorrectBug,correctifs]
    return [False]
    
def getMythicShop(soup) -> Tuple[bool,dict]:
    changes = []
    isMythicShop = soup.find('h2',id="patch-mythic-shop-update") is not None
    if isMythicShop:
        div = soup.find('h2',id="patch-mythic-shop-update").find_next('div', class_="content-border")
        for whatChange in div.find_all('h4'):
                changesTab = []
                change_html = ''
                for sibling in whatChange.find_next_siblings():
                    if sibling.name == 'h4':
                        break
                    change_html += str(sibling)
                change_html = BeautifulSoup(change_html, 'html.parser')
                for li in change_html.find_all('li'):
                    changesTab.append(li.get_text(strip=True))
                changes.append({whatChange.get_text(strip=True) : changesTab})
        return [isMythicShop,changes]
    return [False]
    
def getBazarEssences(soup) -> Tuple[bool,str]:
    isBazar = soup.find('h2',id="patch-essence-emporium-is-back!") is not None
    if isBazar:
        div = soup.find('h2',id="patch-essence-emporium-is-back!").find_next('div', class_="content-border")
        return [isBazar,getText(div)[1]]
    return [False]

def getSkins(soup) -> Tuple[bool,Tuple]:
    tab = []
    isSkins = soup.find('h2',id="patch-upcoming-skins,-chromas,-and-finishers") is not None
    if isSkins:
        div = soup.find('h2',id="patch-upcoming-skins,-chromas,-and-finishers").find_next('div', class_='content-border')
        for skin in div.find_all('a'):
            tab.append(skin.get_text(strip=True)) if skin.get_text(strip=True) != "" else None
        return [isSkins,tab]
    return [False]

def getWeb() -> BeautifulSoup:
    url = f"https://www.leagueoflegends.com/fr-fr/news/game-updates/patch-{getPatch()}-notes/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def getUrl():
    return f"https://www.leagueoflegends.com/fr-fr/news/game-updates/patch-{getPatch()}-notes/"

def main():
    print("running patch.py")
    data = {}
    soup = getWeb()
    tabUpdate = soup.find_all('div', class_='content-border')
    tabUpdate = [div for div in tabUpdate if not div.find_parent('div', class_='content-border')]
    
    correctifs = getCorrecBug(soup)
    mythicShop = getMythicShop(soup)
    bazarEssences = getBazarEssences(soup)
    skins = getSkins(soup)
    image_link = getBanner(getUrl())

    tabChampMidPatch = []
    tabChamp = []
    tabSum = []

    for x in tabUpdate:
        
        name = getName(x)
        summary = getSummary(x)
        text = getText(x)
        changes = getChanges(x,name[0], name[1])
        
        if summary[0]:
            tabChamp.append({name[2] : {'résumé': summary[1], 'text': text[1], 'changes': changes[1]}})
        elif name[0]:
            tabSum.append({name[2] : {'text': text[1], 'changes': changes[1]}})
        elif name[1]:
            tabChampMidPatch.append({name[2] : {'changes': changes[1]}})
            
    data['patch'] = getPatch()
    data['banner'] = image_link
    data['Champions Mid Patch'] = tabChampMidPatch
    data['Champions'] = tabChamp
    data['Summoners/items'] = tabSum
            
    if correctifs[0]:
        data['correctif'] = correctifs[1]
    if mythicShop[0]:
        data['mythicShop'] = mythicShop[1]
    if bazarEssences[0]:
        data['Bazar des essences'] = bazarEssences[1]
    if skins[0]:
        data['skins'] = skins[1]
            
    write(data)
    print("\033[32mDone\033[0m")
    
if __name__ == "__main__" or __name__ == "patch":
    main()