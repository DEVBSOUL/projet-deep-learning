# Projet Deep Learning — MLP, CNN, RNN/LSTM/GRU

**Module :** Deep Learning  
**Année universitaire :** 2025–2026  
**Auteur :** Soulaimane El Younessi

---

## Idée générale

Ce projet explore les trois grandes familles d'architectures de réseaux de neurones profonds à travers des implémentations PyTorch complètes :

| Partie | Architecture | Tâche | Dataset |
|--------|-------------|-------|---------|
| I | MLP | Classification binaire | Breast Cancer Wisconsin |
| II | CNN | Classification d'images (10 classes) | Fashion-MNIST |
| III | RNN / LSTM / GRU + Seq2Seq | Modèle de langage + Traduction EN→FR | Tiny Shakespeare / Tatoeba |

Chaque partie couvre la théorie, l'implémentation from scratch, l'entraînement, l'évaluation et une question de synthèse critique.

---

## Structure du repository

```
Projet Deep Learning/
│
├── Partie_I_MLP.ipynb               # Notebook complet — MLP & ingénierie PyTorch
├── Partie_II_CNN.ipynb              # Notebook complet — Réseaux convolutifs
├── Partie_III_RNN_LSTM_GRU.ipynb    # Notebook complet — RNN, LSTM, GRU, Seq2Seq
│
├── best_mlp.pt                      # Poids du meilleur modèle MLP sauvegardé
│
├── correlation_breast_cancer.png    # Matrice de corrélation & distribution des classes
├── init_comparison.png              # Comparaison des stratégies d'initialisation
├── evaluation_finale.png            # Matrice de confusion + courbes d'apprentissage (MLP)
│
├── fashion_mnist_samples.png        # Exemples d'images Fashion-MNIST
├── cnn_config_comparison.png        # Comparaison des configurations CNN
├── cnn_confusion_matrix.png         # Matrice de confusion (CNN)
├── feature_maps.png                 # Visualisation des feature maps convolutives
├── mlp_vs_cnn.png                   # Comparaison MLP vs CNN sur Fashion-MNIST
│
└── README.md
```

> **Note sur les données :** Le dossier `data/` (FashionMNIST) est exclu du repository car il est téléchargé automatiquement par `torchvision.datasets.FashionMNIST` lors de la première exécution du notebook.

---

## Partie I — MLP (Multilayer Perceptron)

**Fichier :** `Partie_I_MLP.ipynb`

### Objectif
Classification binaire sur le dataset **Breast Cancer Wisconsin** (569 échantillons, 30 features numériques) : distinguer tumeurs bénignes vs. malignes.

### Contenu
- Fondamentaux PyTorch : `nn.Module`, `state_dict`, autograd, device management
- Deux implémentations : `nn.Sequential` et classe personnalisée héritant de `nn.Module`
- Comparaison de 3 stratégies d'initialisation des poids :
  - **Gaussienne** `N(0, 0.01)` → convergence stable mais lente
  - **Constante** `0` → échec (symétrie des neurones, pas d'apprentissage)
  - **Xavier (Glorot)** → convergence rapide, meilleure performance
- Boucle d'entraînement avec Adam, ReduceLROnPlateau et Early Stopping (patience=20)
- Régularisation : BatchNorm1d + Dropout + weight decay (L2)

### Résultats
| Métrique | Score |
|---------|-------|
| Accuracy (test) | **98.84%** |
| Precision | 98.18% |
| Recall | **100%** |
| F1-score | **99.08%** |

Architecture : `MLP 30 → 64 (BN+ReLU+Drop0.3) → 32 (BN+ReLU+Drop0.2) → 1 (Sigmoid)` — 4 289 paramètres

---

## Partie II — CNN (Réseaux de Neurones Convolutifs)

**Fichier :** `Partie_II_CNN.ipynb`

### Objectif
Classification multi-classes (10 catégories de vêtements) sur **Fashion-MNIST** (28×28 pixels, 70 000 images).

### Contenu
- Architecture CNN avec blocs Conv2d + BatchNorm + ReLU + MaxPool
- Visualisation des feature maps appris par les filtres convolutifs
- Comparaison de plusieurs configurations (profondeur, taille des filtres, dropout)
- Comparaison MLP vs CNN : justification du biais inductif convolutif (localité + invariance à la translation)

### Résultats clés
- Accuracy CNN : **~88–91%** sur Fashion-MNIST
- Les feature maps montrent une détection progressive (bords → textures → formes)
- Le CNN surpasse le MLP grâce aux paramètres partagés et à la réduction de dimensionnalité par pooling

---

## Partie III — RNN, LSTM, GRU & Seq2Seq

**Fichier :** `Partie_III_RNN_LSTM_GRU.ipynb`

### Objectif
Deux tâches de traitement de séquences :
1. **Modèle de langage au niveau caractère** sur Tiny Shakespeare
2. **Traduction automatique** anglais → français (Seq2Seq Encoder–Decoder)

### Contenu

#### Section 1 — Modèle de langage probabiliste
- Règle de la chaîne, perplexité (PPL)
- Architecture `CharRNN` unifiée supportant RNN / LSTM / GRU
- BPTT (Backpropagation Through Time) et gradient clipping

#### Section 2 — Comparaison RNN vs LSTM vs GRU
| Modèle | Mémoire | Stabilité gradient | Paramètres |
|--------|---------|-------------------|-----------|
| **RNN** | Court terme | Mauvaise | 1× |
| **LSTM** | Long terme (cell state + 4 portes) | Bonne | 4× |
| **GRU** | Moyen terme (2 portes) | Bonne | 3× |

Le LSTM obtient la **perplexité la plus basse** grâce à son cell state qui crée une autoroute de gradient.

#### Section 3 — Système Seq2Seq (EN→FR)
- Architecture **Encoder–Decoder LSTM** avec teacher forcing
- Décodage **glouton** vs **Beam Search** (k=3)
- Évaluation **BLEU-1**

---

## Prérequis & Installation

```bash
# Cloner le repository
git clone https://github.com/<votre-username>/projet-deep-learning.git
cd projet-deep-learning

# Créer un environnement virtuel
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac

# Installer les dépendances
pip install torch torchvision numpy pandas matplotlib seaborn scikit-learn jupyter
```

> Les données FashionMNIST (~45 MB) sont téléchargées automatiquement dans un dossier `data/` lors de la première exécution de `Partie_II_CNN.ipynb`.

## Lancement

```bash
jupyter notebook
```

Exécuter les notebooks dans l'ordre : Partie I → Partie II → Partie III.

---

## Technologies utilisées

- **Python 3.10+**
- **PyTorch** — construction et entraînement des modèles
- **torchvision** — dataset Fashion-MNIST et transforms
- **scikit-learn** — dataset Breast Cancer, métriques, preprocessing
- **NumPy / Pandas** — manipulation des données
- **Matplotlib / Seaborn** — visualisations

---

## Résumé comparatif final

| Architecture | Biais inductif | Données idéales | Application dans ce projet |
|-------------|---------------|-----------------|---------------------------|
| **MLP** | Aucun | Tabulaire, features numériques | Classification cancer du sein |
| **CNN** | Localité + invariance translation | Images, signaux 2D | Classification Fashion-MNIST |
| **RNN/LSTM/GRU** | Ordre temporel + état caché | Séquences, texte | Modèle de langage + traduction |

Ce projet illustre la **progression naturelle** des architectures : du MLP (représentations brutes), au CNN (structure spatiale), puis au RNN/LSTM (dépendances temporelles), en posant les bases pour comprendre les **Transformers** qui unifient ces approches.
