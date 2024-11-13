from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from time import sleep

def procurar_mod():
    service = Service(executable_path="geckodriver.exe")
    options = Options()
    #options.add_argument('--headless')

    driver = webdriver.Firefox(service=service, options=options)
    nomes = []
    try:
        for i in range(5):
            driver.get(f"https://www.curseforge.com/minecraft/search?page={i+1}&pageSize=20&sortBy=total+downloads&class=modpacks")
            sleep(1)
            modpacks = driver.find_elements(By.CLASS_NAME, "project-card")
            links = []
            for modpack in modpacks:
                linha = modpack.find_element(By.TAG_NAME, "a")
                links.append(linha.get_attribute("href"))
            for link in links:
                driver.get(link +"/relations/dependencies?page=1&search=MineColonies")
                sleep(1)
                try:
                    verificar = driver.find_element(By.CSS_SELECTOR, "a.related-project-card")
                    linkDep = verificar.get_attribute("href")
                    nomeDiv = driver.find_element(By.CLASS_NAME, "name-container")
                    nome = nomeDiv.find_element(By.TAG_NAME, "h1")
                    nomes.append(nome.text)
                except:
                    print("Nao achou!")

                
    except:
        print("Erro ao abrir pagina de Total downloads")
    finally:
        print("Lista de modpacks com o mod")
        for elemento in nomes:
            print(elemento)
        driver.quit()