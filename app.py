import streamlit as st
import pandas as pd

# Charger les données depuis le fichier Excel
file_path = "exemple_2_antibio.xlsx"  # Assurez-vous que le fichier est dans le même répertoire que le script
data = pd.read_excel(file_path, engine='openpyxl')

# Nettoyer les données pour enlever les lignes avec des valeurs manquantes
data.dropna(subset=['Type de Chirurgie', 'Chirurgie Spécifique', 'Antibioprophylaxie'], inplace=True)

# Titre de l'application
st.title("Application d'Antibioprophylaxie Chirurgicale")

# Sélection du type de chirurgie
type_chirurgie = st.selectbox("Type de Chirurgie", data['Type de Chirurgie'].unique())

# Filtrer les chirurgies spécifiques basées sur le type de chirurgie sélectionné
chirurgies_specifiques = data[data['Type de Chirurgie'] == type_chirurgie]['Chirurgie Spécifique'].unique()

# Sélection de la chirurgie spécifique
chirurgie_specifique = st.selectbox("Chirurgie Spécifique", chirurgies_specifiques)

# Indiquer si le patient a une allergie
allergie = st.checkbox("Le patient a-t-il une allergie aux antibiotiques ?")

# Filtrer les données pour obtenir l'antibioprophylaxie correspondante
result = data[(data['Type de Chirurgie'] == type_chirurgie) & (data['Chirurgie Spécifique'] == chirurgie_specifique)]

# Fonction pour déterminer l'antibioprophylaxie alternative en cas d'allergie
def get_alternative_antibioprophylaxie(antibioprophylaxie):
    if "céfazoline" in antibioprophylaxie.lower():
        return "Clindamycine 900mg IV"
    elif "amoxicilline/clavulanate" in antibioprophylaxie.lower():
        return "Bactrim 800/160 sans réinjection"
    elif "céfazoline" in antibioprophylaxie.lower() and "amoxicilline/clavulanate" in antibioprophylaxie.lower():
        return "Clindamycine 900mg IV si Céfazoline ou Bactrim 800/160 si Augmentin"
    return None

# Afficher le résultat
if not result.empty:
    antibioprophylaxie = result.iloc[0]['Antibioprophylaxie']
    if allergie:
        alternative_antibioprophylaxie = get_alternative_antibioprophylaxie(antibioprophylaxie)
        if alternative_antibioprophylaxie:
            st.write(f"Le patient est allergique. Antibioprophylaxie alternative recommandée : {alternative_antibioprophylaxie}")
        else:
            st.write("Le patient est allergique, mais aucune alternative spécifique n'est recommandée.")
    else:
        st.write(f"Antibioprophylaxie recommandée : {antibioprophylaxie}")
else:
    st.write("Aucune antibioprophylaxie recommandée trouvée pour cette combinaison.")
