!cp /usr/lib/chromium-browser/chromedriver /usr/bin

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import base64
from IPython.display import HTML, display

# Chiedi input all'utente
targa = input("Inserisci la targa: ")
km = input("Inserisci i chilometri: ")

# Configura Chrome
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')

# Inizializza il driver
driver = webdriver.Chrome(options=options)

# Visita il sito
print("Visitando il sito di autoscout24...")
driver.get("https://www.autoscout24.it/valutazione-auto/")
time.sleep(5)  # Attendi il caricamento della pagina

# Prova ad accettare i cookie
try:
    print("Cercando di accettare i cookie...")
    cookie_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Accetta')]")
    if cookie_buttons:
        cookie_buttons[0].click()
    time.sleep(2)
except Exception as e:
    print(f"Errore cookie: {str(e)}")

# Verifica se ci sono i campi per la targa e i km
print("Cercando i campi per targa e chilometri...")

# Stampa la struttura HTML per debug
print("Struttura della pagina:")
print(driver.page_source[:1000])  # Stampa i primi 1000 caratteri per debug

try:
    # Prova diversi selettori per il campo targa
    selettori_targa = ["#license-plate", "input[name='licensePlate']", "input[placeholder*='targ']", 
                      "//input[contains(@placeholder, 'targ')]"]
    
    for selettore in selettori_targa:
        try:
            print(f"Provando selettore targa: {selettore}")
            if selettore.startswith("//"):
                targa_input = driver.find_element(By.XPATH, selettore)
            elif selettore.startswith("#"):
                targa_input = driver.find_element(By.CSS_SELECTOR, selettore)
            else:
                targa_input = driver.find_element(By.CSS_SELECTOR, selettore)
                
            targa_input.clear()
            targa_input.send_keys(targa)
            print("Campo targa trovato e compilato!")
            break
        except:
            continue
            
    # Prova diversi selettori per il campo km
    selettori_km = ["#mileage", "input[name='mileage']", "input[placeholder*='chilo']", 
                   "//input[contains(@placeholder, 'chilo')]"]
    
    for selettore in selettori_km:
        try:
            print(f"Provando selettore km: {selettore}")
            if selettore.startswith("//"):
                km_input = driver.find_element(By.XPATH, selettore)
            elif selettore.startswith("#"):
                km_input = driver.find_element(By.CSS_SELECTOR, selettore)
            else:
                km_input = driver.find_element(By.CSS_SELECTOR, selettore)
                
            km_input.clear()
            km_input.send_keys(km)
            print("Campo km trovato e compilato!")
            break
        except:
            continue
            
    # Cerca il pulsante di invio
    selettori_bottone = ["button[type='submit']", "button.primary", "//button[contains(text(), 'Valu')]"]
    
    for selettore in selettori_bottone:
        try:
            print(f"Provando selettore bottone: {selettore}")
            if selettore.startswith("//"):
                bottone = driver.find_element(By.XPATH, selettore)
            else:
                bottone = driver.find_element(By.CSS_SELECTOR, selettore)
                
            bottone.click()
            print("Bottone cliccato!")
            break
        except:
            continue
            
    # Aspetta che la pagina carichi
    print("Attendendo i risultati...")
    time.sleep(10)
    
    # Salva screenshot
    print("Salvando screenshot...")
    screenshot = driver.get_screenshot_as_base64()
    
    # Mostra lo screenshot
    display(HTML(f'<img src="data:image/png;base64,{screenshot}" width="800"/>'))
    
    # Salva lo screenshot come file
    with open("valutazione.png", "wb") as fh:
        fh.write(base64.b64decode(screenshot))
    
    print("Screenshot salvato come 'valutazione.png'")
    
except Exception as e:
    print(f"Errore durante l'automazione: {str(e)}")
    
finally:
    # Chiudi il browser
    driver.quit()
    print("Browser chiuso")
