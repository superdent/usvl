# Psychische Gesundheit in technologiebezogenen Berufen

Unsupervised-Learning-Analyse von Umfragedaten zur psychischen Gesundheit in der Tech-Branche.

**Kurs:** DLBDSMLUSL01_D – Maschinelles Lernen: Unsupervised Learning und Feature Engineering

## Datensatz

Quelle: [OSMI Mental Health in Tech Survey 2016](https://www.kaggle.com/datasets/osmi/mental-health-in-tech-2016)

Format: CSV. Die Rohdaten sind nicht im Repository enthalten. CSV-Datei herunterladen und unter `data/raw/` ablegen.

## Installation

Python 3.11

```
pip install -r requirements.txt
```

## Verzeichnisstruktur

```
data/raw/                    # Rohdatensatz (CSV)
data/processed/              # Verarbeitete Datensätze
  preprocessed.csv           # Vorverarbeiteter Datensatz
  selected_features.csv      # Datensatz nach Feature-Auswahl
  clustered.csv              # Datensatz mit Cluster-Zuordnungen
documentation/               # Berichte und Abbildungen
  eda_report.md              # Bericht zur explorativen Datenanalyse
  preprocessing_report.md    # Bericht zur Vorverarbeitung
  figures/                   # Alle erzeugten Abbildungen
    eda/                     # Abbildungen aus EDA
    feature_selection/       # Abbildungen aus Feature-Auswahl
    dimension_reduction/     # Abbildungen aus Dimensionsreduktion
    clustering/              # Abbildungen aus Clustering
src/                         # Python-Scripts
```

## Notebooks

| Notebook | Inhalt |
|----------|--------|
| 01_eda.ipynb | Explorative Datenanalyse |
| 02_preprocessing.ipynb | Bereinigung, Kodierung, Standardisierung |
| 03_feature_auswahl.ipynb | Varianz-, Korrelations- und MI-Filter |
| 04_dimensionsreduktion.ipynb | PCA, MDS, LLE |
| 05_clustering.ipynb | k-Means, GMM, Cluster-Interpretation |

## Scripts

| Script | Beschreibung |
|--------|-------------|
| column_aliases.py | Mapping der Fragebogentexte auf kurze Spaltennamen |
