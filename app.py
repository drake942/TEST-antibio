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

# Titre de l'application
st.title("Antibioprophylaxie en chirurgie et médecine interventionnelle")

# Page d'accueil
if "page" not in st.session_state:
    st.session_state.page = "Accueil"

if st.session_state.page == "Accueil":
    st.header("Bienvenue")
    if st.button("Recherche par intitulé opératoire"):
        st.session_state.page = "Recherche par intitulé opératoire"
        st.experimental_rerun()
    if st.button("Recherche par catégorie"):
        st.session_state.page = "Recherche par catégorie"
        st.experimental_rerun()

elif st.session_state.page == "Recherche par intitulé opératoire":
    if st.button("Retour"):
        st.session_state.page = "Accueil"
        st.experimental_rerun()

    # Recherche globale pour la chirurgie spécifique
    chirurgie_specifique_search = st.text_input("Recherche", key="global_search")
    chirurgies_specifiques = data['Chirurgie Spécifique'].unique()
    filtered_chirurgies_specifiques = [option for option in chirurgies_specifiques if chirurgie_specifique_search.lower() in option.lower()]

    # Sélection de la chirurgie spécifique avec recherche
    chirurgie_specifique = st.selectbox("Chirurgie Spécifique", filtered_chirurgies_specifiques)

    # Obtenir la spécialité chirurgicale correspondant à la chirurgie spécifique sélectionnée
    if chirurgie_specifique:
        type_chirurgie = data[data['Chirurgie Spécifique'] == chirurgie_specifique]['Spécialité chirurgicale'].values[0]
        st.markdown(f"### Spécialité Chirurgicale: {type_chirurgie}")

    # Indiquer si le patient a une allergie
    allergie = st.checkbox("Le patient a-t-il une allergie aux antibiotiques ?")

    # Filtrer les données pour obtenir l'antibioprophylaxie correspondante
    result = data[(data['Spécialité chirurgicale'] == type_chirurgie) & (data['Chirurgie Spécifique'] == chirurgie_specifique)]

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

elif st.session_state.page == "Recherche par catégorie":
    if st.button("Retour"):
        st.session_state.page = "Accueil"
        st.experimental_rerun()

    # Sélection du type de chirurgie avec menu déroulant
    type_chirurgie_selection = st.selectbox("Type de Chirurgie", data['Spécialité chirurgicale'].unique())

    # Filtrer les chirurgies spécifiques basées sur le type de chirurgie sélectionné
    chirurgies_specifiques_selection = data[data['Spécialité chirurgicale'] == type_chirurgie_selection]['Chirurgie Spécifique'].unique()

    # Sélection de la chirurgie spécifique avec menu déroulant
    chirurgie_specifique_selection = st.selectbox("Chirurgie Spécifique", chirurgies_specifiques_selection)

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
