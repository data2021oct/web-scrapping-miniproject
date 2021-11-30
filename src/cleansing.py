import requests
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager



#driver configuration
opciones=Options()

opciones.add_experimental_option('excludeSwitches', ['enable-automation'])
opciones.add_experimental_option('useAutomationExtension', False)
opciones.headless=False    # si True, no aperece la ventana (headless=no visible)
opciones.add_argument('--start-maximized')         # comienza maximizado
#opciones.add_argument('user-data-dir=selenium')    # mantiene las cookies
#opciones.add_extension('driver_folder/adblock.crx')       # adblocker
opciones.add_argument('--incognito') 



def driver_blospot(url_blog,pages,posts):
    """
    recibe la url de un blog de blogspot
        - el número de páginas de este blog = pages
        - el número de posts que hay por página = posts
    conceta selenium con el driver de selenium
    devuelve una lista de dos listas. La primera es el título de cada post, y la segunda es el contenido
    
    """
    driver = "./chromedriver.exe"
    driver = webdriver.Chrome(driver,options = opciones)

    url2 = url_blog
    driver.get(url2)
    driver.implicitly_wait(2)
    driver.find_element_by_css_selector("#cookieChoiceDismiss").click()

    tit = []
    texto = []

    for i in range(1,pages): 
        try:
            for p in range(1,posts):
                tit.append(driver.find_element_by_css_selector(f"#Blog1 > div.blog-posts.hfeed > div:nth-child({p}) > div > div.post-outer > div > h3 > a").text)
                
                texto.append(driver.find_element_by_css_selector(f"#Blog1 > div.blog-posts.hfeed > div:nth-child({p}) > div > div.post-outer > div").text)
            driver.find_element_by_css_selector("#blog-pager-older-link").click()

        except:
            texto.append("no data")
    driver.quit()
    
    return [tit,texto]


def cleaning_texts(lista,indexando,firmando):
    """
    recibe la lista de los textos que queremos limpiar
        - indexando = el texto final que no queremos que aparezca en nuestro string que corresponde al cajón de reacciones de blogspot
        - firmando = la frima que no queremos que aparezca en nuestro string
    devuelve el texto puro sin firmas en un listado
    """
    textos = []
    for t in lista[:-1]:
        s = t.split("\n")
        ind = s.index(indexando)
        firma = s[1:ind-1] #quitamos el título
        if firmando in firma:
            inddos = firma.index(firmando)
            text_def = firma[1:inddos]
            textos.append(" ".join(text_def).strip())
        else:
            textos.append(" ".join(firma).strip())
    return textos



    