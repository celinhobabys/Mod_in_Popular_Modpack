from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import tkinter as tk
from time import sleep
import threading
from queue import Queue

def centralize_Window(root,width = None,height = None):
    
    if width is None:
        width = 1280
    if height is None:
        height = 720

    widthW = root.winfo_screenwidth()
    heightW = root.winfo_screenheight()
    
    pos_x = (widthW - width) // 2
    pos_y = (heightW - height) // 2
    
    root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

def procurar_mod_thread(page, res):
    service = Service(executable_path="resources/apps/geckodriver.exe")
    options = Options()
    options.add_argument('--headless')

    driver = webdriver.Firefox(service=service, options=options)
    nomes = []
    try:
        driver.get(f"https://www.curseforge.com/minecraft/search?page={page}&pageSize=20&sortBy=total+downloads&class=modpacks")
        verificador = 0
        while True:
            verificador += 1
            if verificador > 200:
                print(f"problema no loop 1 da thread {page}")
            sleep(0.1)
            try:
                modpacks = driver.find_elements(By.CLASS_NAME, "project-card")
                if len(modpacks) < 20:
                    continue
                break
            except:
                continue
        links = []
        for modpack in modpacks:
            linha = modpack.find_element(By.TAG_NAME, "a")
            links.append(linha.get_attribute("href"))
        for link in links:
            driver.get(link +"/relations/dependencies?page=1&search=MineColonies")
            print(f"Verifying {link}")
            verificador2 = 0
            while True:
                verificador2 += 1
                if verificador2 > 200:
                    print(f"problema no loop 2 da thread {page}")
                sleep(0.1)
                try:
                    driver.find_element(By.CSS_SELECTOR, "a.related-project-card")
                    nomeDiv = driver.find_element(By.CLASS_NAME, "name-container")
                    nome = nomeDiv.find_element(By.TAG_NAME, "h1")
                    nomes.append(nome.text)
                    break
                except:
                    pass
                try:
                    driver.find_element(By.CLASS_NAME, "no-results")
                    break
                except:
                    pass
    except:
        print("Error in getting modpack list page")
    finally:
        for elemento in nomes:
            res.put(elemento)
            print(f"foi terminado a thread {page}")
        driver.quit()

def iniciar_Busca():
    result_queue = Queue()
    threads = []
    for i in range(5):
        thread = threading.Thread(target=procurar_mod_thread, args=(i+1,result_queue))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    
    nomes = []
    while not result_queue.empty():
        nomes.append(result_queue.get())
    
    print("\nModpacks with the mod:")
    for nome in nomes:
        print(nome)


def janela_Principal():
    root = tk.Tk()    
    root.configure(bg='#252525')
    root.title("Mod Searcher")
    root.resizable(False, False)

    icon_path = "resources/media/icon.ico"
    root.iconbitmap(icon_path)

    centralize_Window(root)

    root.mainloop()