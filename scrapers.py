from selenium.webdriver.chrome.options import Options
from selenium import webdriver

# the driver created is one and global for all scrapers
try:
    options = Options()
    options.add_argument('--headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    DRIVER = webdriver.Chrome(options=options)
except Exception as e:
    print("The bot was not able to create a webdriver instance. Probably the driver has to be updated")
    input()

def get_immobiliare(comune: str, min: int, max: int, *args) -> list:
    """ Function to get properties from Immobiliare.it """

    # creates the URL for the search
    url = "https://www.immobiliare.it/vendita-case/"
    url += comune + "/?"
    url += "criterio=dataModifica&ordine=desc"
    url += "&prezzoMinimo=" + str(min)
    url += "&prezzoMassimo=" + str(max)
    for a in args:
        url += a


    DRIVER.get(url)
    first_page = DRIVER.find_element_by_class_name("in-realEstateResults").find_elements_by_class_name("in-realEstateResults__item")

    el_list = []

    for el in first_page:

        nome = el.find_element_by_class_name("in-card__title")
        prezzo = el.find_element_by_class_name("in-realEstateListCard__features--main")

        el_list.append([nome.text,
                          prezzo.text,
                          nome.get_attribute("href"),
                          ])

    return el_list


def get_subito(oggetto: str, regione: str, provincia: str, categoria: str, *args) -> list:
    """ Function to get items from Subito.it
        regione='italia'
        categoria='usato' """
    
    # creates the URL for the search
    url = "https://www.subito.it/annunci-{}/vendita/{}/{}/?q={}".format(    regione,
                                                                            categoria,
                                                                            provincia,
                                                                            oggetto)

    for e in args:
        url += "&" + e

    DRIVER.get(url)
    container = DRIVER.find_element_by_css_selector("[class='jsx-4116751698 items visible']")
    first_page = container.find_elements_by_tag_name("a")

    el_list = []

    for el in first_page:
        link = el.get_attribute("href")
        nome = " ".join(link.split("/")[-1].split("-")[:-1]).capitalize()
        el_list.append([nome, link])

    return el_list
