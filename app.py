import streamlit as st
import pandas as pd

# Charger les données depuis le fichier Excel
file_path = "exemple_2_antibio.xlsx"  # Assurez-vous que le fichier est dans le même répertoire que le script
data = pd.read_excel(file_path, engine='openpyxl')

# Vérifier que les colonnes attendues sont présentes
required_columns = ['Spécialité chirurgicale', 'Chirurgie Spécifique', 'Antibioprophylaxie']
for col in required_columns:
    if col not in data.columns:
        st.error(f"La colonne '{col}' est manquante dans le fichier Excel.")
        st.stop()

# Nettoyer les données pour enlever les lignes avec des valeurs manquantes
data.dropna(subset=required_columns, inplace=True)

# Ajouter du CSS pour améliorer la lisibilité des menus déroulants et cacher l'élément spécifique
st.markdown("""
    <style>
    .stSelectbox div[role='listbox'] ul {
        max-height: 200px;
        overflow-y: auto;
    }
    .stSelectbox label {
        font-size: 1.2rem;
    }
    .stSelectbox div[role='combobox'] input {
        height: 2.5rem;
        font-size: 1rem;
        width: 100%;
    }
    .stSelectbox div[role='combobox'] {
        width: 100%;
    }
    .stSelectbox div[role='listbox'] {
        width: 100%;
    }
    /* Augmenter la hauteur du menu déroulant pour la chirurgie spécifique */
    .stSelectbox:nth-of-type(2) div[role='combobox'] {
        height: 7.5rem; /* Augmenter la hauteur par 3 */
    }
    .stSelectbox:nth-of-type(2) div[role='listbox'] ul {
        max-height: 600px; /* Augmenter la hauteur par 3 */
    }
    /* Cacher le selectbox de la recherche globale */
    #recherche_globale {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Titre de l'application
st.title("Application d'Antibioprophylaxie Chirurgicale")

# Fonction de recherche
def search_in_list(search_term, options):
    return [option for option in options if search_term.lower() in option.lower()]

# Recherche globale pour la chirurgie spécifique
chirurgie_specifique_search = st.text_input("Recherche", key="global_search")
chirurgies_specifiques = data['Chirurgie Spécifique'].unique()
filtered_chirurgies_specifiques = search_in_list(chirurgie_specifique_search, chirurgies_specifiques)

# Sélection de la chirurgie spécifique avec recherche (caché avec CSS)
chirurgie_specifique = st.selectbox("Chirurgie Spécifique", filtered_chirurgies_specifiques, key="recherche_globale")

# Obtenir la spécialité chirurgicale correspondant à la chirurgie spécifique sélectionnée
if chirurgie_specifique:
    type_chirurgie = data[data['Chirurgie Spécifique'] == chirurgie_specifique]['Spécialité chirurgicale'].values[0]
    st.markdown(f"### Spécialité Chirurgicale: {type_chirurgie}")

# Sélection du type de chirurgie avec menu déroulant
type_chirurgie_selection = st.selectbox("Type de Chirurgie", data['Spécialité chirurgicale'].unique())

# Filtrer les chirurgies spécifiques basées sur le type de chirurgie sélectionné
chirurgies_specifiques_selection = data[data['Spécialité chirurgicale'] == type_chirurgie_selection]['Chirurgie Spécifique'].unique()

# Sélection de la chirurgie spécifique avec menu déroulant
chirurgie_specifique_selection = st.selectbox("Chirurgie Spécifique (sélection par spécialité)", chirurgies_specifiques_selection)

# Indiquer si le patient a une allergie
allergie = st.checkbox("Le patient a-t-il une allergie aux antibiotiques ?")

# Filtrer les données pour obtenir l'antibioprophylaxie correspondante
result = data[(data['Spécialité chirurgicale'] == type_chirurgie_selection) & (data['Chirurgie Spécifique'] == chirurgie_specifique_selection)]

# Fonction pour déterminer l'antibioprophylaxie alternative en cas d'allergie
def get_alternative_antibioprophylaxie(antibioprophylaxie):
    if "céfazoline" in antibioprophylaxie.lower():
        return "Clindamycine 900mg IV"
    elif "amoxicilline/clavulanate" in antibioprophylaxie.lower():
        return "Bactrim 800/160 sans réinjection"
    elif "céfazoline" in antibioprophylaxie.lower() and "amoxicilline/clavulanate" in antibioprophylaxie.lower():
        return "Clindamycine 900mg IV si Céfazoline ou Bactrim 800/160 si Augmentin"
    return None

# Afficher le résultat avec une mise en forme optimisée
if not result.empty:
    antibioprophylaxie = result.iloc[0]['Antibioprophylaxie']
    if allergie:
        alternative_antibioprophylaxie = get_alternative_antibioprophylaxie(antibioprophylaxie)
        if alternative_antibioprophylaxie:
            st.markdown(f"<span style='color: red; font-size: 20px;'>Le patient est allergique. Antibioprophylaxie alternative recommandée : {alternative_antibioprophylaxie}</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span style='color: red; font-size: 20px;'>Le patient est allergique, mais aucune alternative spécifique n'est recommandée.</span>", unsafe_allow_html=True)
    else:
        st.markdown(f"<span style='color: green; font-size: 20px;'>Antibioprophylaxie recommandée : {antibioprophylaxie}</span>", unsafe_allow_html=True)
else:
    st.markdown("<span style='color: red; font-size: 20px;'>Aucune antibioprophylaxie recommandée trouvée pour cette combinaison.</span>", unsafe_allow_html=True)

# Ajouter la mention en bas de l'écran
st.markdown("<div style='position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px 0; background-color: #f8f9fa; color: #333; font-size: 14px;'>Recommandations d'antibioprophylaxie de la SFAR, au jour du 13/06/2024</div>", unsafe_allow_html=True)
