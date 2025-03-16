import streamlit as st
import requests
from bs4 import BeautifulSoup
import io
from PIL import Image

st.set_page_config(page_title="Valutazione Auto AutoScout24", layout="wide")
st.title("Valutazione Auto AutoScout24")

def valuta_auto(targa, km):
    st.info("Avvio valutazione...")
    try:
        url = f"https://www.autoscout24.it/valutazione-auto/?licensePlate={targa}&mileage={km}" #Modifica se necessario
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        # Trova i dati di valutazione (dovrai adattare questi selettori)
        # Esempio:
        valutazione = soup.find("div", class_="cldt-price-suggestion-average").text.strip()
        dettagli = soup.find("div", class_="cldt-price-suggestion-details").text.strip()

        st.success("Valutazione completata!")
        st.write(f"Valutazione media: {valutazione}")
        st.write(f"Dettagli: {dettagli}")

        # Creazione di un'immagine con i risultati (esempio)
        img = Image.new('RGB', (400, 200), color = (255, 255, 255))
        d = ImageDraw.Draw(img)
        d.text((20, 20), f"Valutazione: {valutazione}\nDettagli: {dettagli}", fill=(0, 0, 0))

        st.image(img, caption="Risultato valutazione", use_column_width=True)

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        btn = st.download_button(
            label="Scarica valutazione come immagine",
            data=byte_im,
            file_name=f"valutazione_{targa}_{km}.png",
            mime="image/png"
        )

        return img

    except requests.exceptions.RequestException as e:
        st.error(f"Errore di richiesta: {e}")
        return None
    except AttributeError:
        st.error("Valutazione non trovata. Controlla i dati inseriti.")
        return None
    except Exception as e:
        st.error(f"Si è verificato un errore: {e}")
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

# Istruzioni
with st.expander("Istruzioni"):
    st.write("""
    1. Inserisci la targa del veicolo (es. AB123CD)
    2. Inserisci i chilometri percorsi (es. 50000)
    3. Clicca su "Valuta veicolo"
    4. Attendi il completamento dell'operazione
    5. Scarica l'immagine con il risultato
    """)
