import csv
import urllib.request

import pandas as pd
import plotly.express as px


URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSC4KusfFzvOsr8WJRgozzsCxrELW4G4PopUkiDbvrrV2lg0S19-zeryp02MC9WYSVBuzGCUtn8ucZW/pub?output=csv"


df = pd.read_csv(URL)
df["ca"] = df["prix"] * df["qte"]

ca_total = df["ca"].sum()

ventes_par_produit = (
    df.groupby("produit", as_index=False)["qte"]
    .sum()
    .sort_values("qte", ascending=False)
)

ca_par_produit = (
    df.groupby("produit", as_index=False)["ca"]
    .sum()
    .sort_values("ca", ascending=False)
)

ventes_par_region = (
    df.groupby("region", as_index=False)["qte"]
    .sum()
    .sort_values("qte", ascending=False)
)

ca_par_region = (
    df.groupby("region", as_index=False)["ca"]
    .sum()
    .sort_values("ca", ascending=False)
)

stats = df.groupby("produit").agg(
    moyenne_ca=("ca", "mean"),
    mediane_ca=("ca", "median"),
    moyenne_qte=("qte", "mean"),
    mediane_qte=("qte", "median"),
    ecart_type_qte=("qte", "std"),
    variance_qte=("qte", "var")
).round(2)



print("Chiffre d'affaires total :", ca_total)
print("\nVentes par produit :")
print(ventes_par_produit.to_string(index=False))
print("\nChiffre d'affaires par produit :")
print(ca_par_produit.to_string(index=False))
print("\nVentes par région :")
print(ventes_par_region.to_string(index=False))
print("\nChiffre d'affaires par région :")
print(ca_par_region.to_string(index=False))
print(stats)
ventes_natives = {}

with urllib.request.urlopen(URL) as response:
    lignes = response.read().decode("utf-8").splitlines()
    lecteur = csv.DictReader(lignes)

    for ligne in lecteur:
        produit = ligne["produit"]
        qte = int(ligne["qte"])
        ventes_natives[produit] = ventes_natives.get(produit, 0) + qte

produit_plus_vendu = max(ventes_natives, key=ventes_natives.get)
produit_moins_vendu = min(ventes_natives, key=ventes_natives.get)

print("\nProduit le plus vendu :", produit_plus_vendu, "-", ventes_natives[produit_plus_vendu], "unités")
print("Produit le moins vendu :", produit_moins_vendu, "-", ventes_natives[produit_moins_vendu], "unités")

fig_ventes_produit = px.bar(
    ventes_par_produit,
    x="produit",
    y="qte",
    title="Ventes par produit",
    labels={"produit": "Produit", "qte": "Quantité vendue"},
    text="qte",
)

fig_ventes_produit.update_traces(textposition="outside")
fig_ventes_produit.write_html("ventes-par-produit.html")

fig_ca_produit = px.bar(
    ca_par_produit,
    x="produit",
    y="ca",
    title="Chiffre d'affaires par produit",
    labels={"produit": "Produit", "ca": "Chiffre d'affaires"},
    text="ca",
)

fig_ca_produit.update_traces(textposition="outside")
fig_ca_produit.write_html("ca-par-produit.html")

print("\nFichiers générés :")
print("- ventes-par-produit.html")
print("- ca-par-produit.html")
