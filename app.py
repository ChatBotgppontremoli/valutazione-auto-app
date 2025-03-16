import streamlit as st
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import base64
from PIL import Image
import io

st.set_page_config(page_title="Valutazione Auto AutoScout24", layout="wide")
st.title("Valutazione Auto AutoScout24")

# Funzione per eseguire lo scraping
def valuta_auto(targa, km):
    st.info("Avvio valutazione...")
    
    # Configura Chrome
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
    
    try:
        # Inizializza il driver con webdriver_manager per gestire automaticamente il driver
        driver = webdriver.Chrome(options=options)
        
        # Visita il sito
        st.write("Visitando il sito di autoscout24...")
        driver.get("https://www.autoscout24.it/valutazione-auto/")
        time.sleep(5)  # Attendi il caricamento della pagina
        
        # Prova ad accettare i cookie
        try:
            st.write("Accettando i cookie...")
            cookie_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Accetta')]")
            if cookie_buttons:
                cookie_buttons[0].click()
            time.sleep(2)
        except Exception as e:
            st.warning(f"Nota sui cookie: {str(e)}")
        
        # Compila il form
        st.write("Compilando i dati del veicolo...")
        
        # Targa
        trovato_targa = False
        selettori_targa = ["#license-plate", "input[name='licensePlate']", "input[placeholder*='targ']", 
                      "//input[contains(@placeholder, 'targ')]"]
        
        for selettore in selettori_targa:
            try:
                if selettore.startswith("//"):
                    targa_input = driver.find_element(By.XPATH, selettore)
                else:
                    targa_input = driver.find_element(By.CSS_SELECTOR, selettore)
                    
                targa_input.clear()
                targa_input.send_keys(targa)
                trovato_targa = True
                break
            except:
                continue
                
        if not trovato_targa:
            st.error("Non è stato possibile trovare il campo per la targa")
            driver.quit()
            return None
            
        # Chilometri
        trovato_km = False
        selettori_km = ["#mileage", "input[name='mileage']", "input[placeholder*='chilo']", 
                       "//input[contains(@placeholder, 'chilo')]"]
        
        for selettore in selettori_km:
            try:
                if selettore.startswith("//"):
                    km_input = driver.find_element(By.XPATH, selettore)
                else:
                    km_input = driver.find_element(By.CSS_SELECTOR, selettore)
                    
                km_input.clear()
                km_input.send_keys(km)
                trovato_km = True
                break
            except:
                continue
                
        if not trovato_km:
            st.error("Non è stato possibile trovare il campo per i chilometri")
            driver.quit()
            return None
        
        # Clicca sul pulsante
        cliccato = False
        selettori_bottone = ["button[type='submit']", "button.primary", "//button[contains(text(), 'Valu')]"]
        
        for selettore in selettori_bottone:
            try:
                if selettore.startswith("//"):
                    bottone = driver.find_element(By.XPATH, selettore)
                else:
                    bottone = driver.find_element(By.CSS_SELECTOR, selettore)
                    
                bottone.click()
                cliccato = True
                break
            except:
                continue
                
        if not cliccato:
            st.error("Non è stato possibile trovare il pulsante di invio")
            driver.quit()
            return None
        
        # Attendi il caricamento dei risultati
        st.write("Attendendo i risultati...")
        progress_bar = st.progress(0)
        for i in range(10):
            time.sleep(1)
            progress_bar.progress((i + 1) * 10)
        
        # Cattura screenshot
        st.write("Catturando i risultati...")
        screenshot = driver.get_screenshot_as_png()
        
        # Converti l'immagine
        image = Image.open(io.BytesIO(screenshot))
        
        # Chiudi il browser
        driver.quit()
        st.success("Valutazione completata!")
        
        return image
        
    except Exception as e:
        st.error(f"Si è verificato un errore: {str(e)}")
        return None

# Interfaccia utente
with st.form("valutazione_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        targa = st.text_input("Inserisci la targa del veicolo")
    
    with col2:
        km = st.text_input("Inserisci i chilometri percorsi")
    
    submitted = st.form_submit_button("Valuta veicolo")
    
    if submitted:
        if not targa or not km:
            st.warning("Per favore inserisci sia la targa che i chilometri")
        else:
            risultato = valuta_auto(targa, km)
            if risultato:
                st.image(risultato, caption="Risultato valutazione", use_column_width=True)
                
                # Opzione per scaricare l'immagine
                buf = io.BytesIO()
                risultato.save(buf, format="PNG")
                byte_im = buf.getvalue()
                btn = st.download_button(
                    label="Scarica valutazione come immagine",
                    data=byte_im,
                    file_name=f"valutazione_{targa}_{km}.png",
                    mime="image/png"
                )

# Istruzioni
with st.expander("Istruzioni"):
    st.write("""
    1. Inserisci la targa del veicolo (es. AB123CD)
    2. Inserisci i chilometri percorsi (es. 50000)
    3. Clicca su "Valuta veicolo"
    4. Attendi il completamento dell'operazione
    5. Scarica l'immagine con il risultato
    """)
