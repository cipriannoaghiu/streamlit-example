import streamlit as st
from openai import OpenAI
import json

# Configuration OpenAI
client = OpenAI(api_key = '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')
client2 = OpenAI(api_key = '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')

# Chargement des catégories
categories = {
  "Alimentation": {
    "Produits Frais": ["Fruits et Légumes", "Viandes et Volailles", "Poissons et Fruits de Mer", "Charcuterie", "Fromages", "Produits Laitiers"],
    "Épicerie": ["Céréales et Petit-Déjeuner", "Conserves et Plats Préparés", "Pâtes, Riz et Légumineuses", "Huiles, Vinaigres et Condiments", "Épices et Herbes", "Sauces et Assaisonnements", "Snacks et Grignotages", "Confiserie et Chocolat", "Produits pour la Boulangerie et la Pâtisserie", "Café, Thé et Boissons Chaudes"],
    "Boissons": ["Eaux et Boissons Gazeuses", "Jus et Nectars", "Bières, Vins et Spiritueux", "Boissons Énergétiques et Sportives"]
  },
  "Produits Surgelés": ["Plats Cuisinés Surgelés", "Légumes et Fruits Surgelés", "Viandes et Poissons Surgelés", "Glaces et Desserts Surgelés"]
  ,
  "Hygiène et Beauté": ["Soins du Corps et du Visage", "Produits Capillaires", "Hygiène Bucco-Dentaire", "Produits pour le Bain et la Douche", "Produits Menstruels et Intimes", "Soins pour Bébé", "Cosmétiques et Maquillage"]
  ,
  "Produits Ménagers": ["Nettoyants et Désinfectants", "Lessive et Soins du Linge", "Papier Ménager", "Produits pour la Vaisselle", "Insecticides et Anti-Nuisibles"]
}

# Fonction pour déterminer le conditionnement
def find_packaging(description):
    result = ""
    try:
        stream = client.chat.completions.create(
            model="gpt-4", 
            messages=[{"role": "user", "content": f"Déterminer le conditionnement pour le produit suivant seulement en se basant sur la description suivante: {description} \nsi ce n'est pas possible répondre None"}],
            stream=True,
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                result += str(chunk.choices[0].delta.content)
        return result
    except Exception as e:
        return str(e)

# Fonction pour catégoriser le produit
def categorize_product(produit):
    result = ""
    try:
        stream = client.chat.completions.create(
            model="gpt-4", 
            messages=[{"role": "user", "content": f"Catégorisez le produit suivant en utilisant ces catégories {json.dumps(categories)}:\nProduit: {produit}\n répondre uniqueme les catégories et sous-catégorie au format json"}],
            stream=True,
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                result += str(chunk.choices[0].delta.content)
        return result
    except Exception as e:
        return str(e)

def main():
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    # Interface Streamlit
    st.set_page_config(page_title="Catégorisateur de Produits", page_icon=":shopping_cart:")
    st.image("https://relevanc.com/hubfs/LOGO-RELEVANC-CLASSIQUE-GRIS%201.svg")

    st.title("Catégorisateur de Produits")
    
    
  
    st.write("Entrez la description du produit pour le catégoriser.")
    with st.form("pack_form"):
        product_description = st.text_input("Entrez le nom du produit à catégoriser")
        submit_button = st.form_submit_button("Analyser")

    if product_description and submit_button:
        packaging = find_packaging(product_description)
        if packaging != "None":
            st.success("Conditionnement identifié.")
        else:
            st.error("Conditionnement non identifié.")
        category = categorize_product(product_description)
        st.success(f"Catégorie : {category}")
        st.session_state['history'].append((product_description, category, packaging))

    st.subheader("Historique de Catégorisation")
    for prod, cat, packing in reversed(st.session_state['history']):
        st.markdown(f"- **{prod}**: {cat}, {packing}")


if __name__ == "__main__":
    main()
