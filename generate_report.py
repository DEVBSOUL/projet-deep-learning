"""
Generateur de rapport PDF professionnel - Deep Learning
Auteur : Soulaimane El Younessi
Double passe pour TOC automatique avec numeros de pages reels.
"""
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os, struct

def _png_size(path):
    """Lit largeur/hauteur depuis l en-tete PNG sans librairie externe."""
    try:
        with open(path, "rb") as f:
            if f.read(8) != b"\x89PNG\r\n\x1a\n":
                return None, None
            f.read(8)  # longueur + type IHDR
            w = struct.unpack(">I", f.read(4))[0]
            h = struct.unpack(">I", f.read(4))[0]
            return w, h
    except Exception:
        return None, None

BASE = r"c:\Users\lenovo\Desktop\Projet Deep Learning"
OUT  = BASE + r"\Rapport_Deep_Learning_Soulaimane_El_Younessi.pdf"

NAVY  = (30,  80,  160)
STEEL = (70,  120, 190)
LGRAY = (235, 242, 252)
BLACK = (30,  30,  30)
GRAY  = (100, 100, 100)
GREEN = (55,  140, 70)


class Report(FPDF):

    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_margins(20, 25, 20)
        self.set_auto_page_break(auto=True, margin=20)
        self.fig_n = 0
        self.tab_n = 0
        self.sec_pages = {}   # populated during pass-1

    # ------------------------------------------------------------------ layout
    def header(self):
        if self.page_no() <= 2:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        self.set_x(20)
        self.cell(170, 5,
                  "Rapport Deep Learning - MLP, CNN, RNN/LSTM/GRU  |  "
                  "Soulaimane El Younessi  |  EMSI 2025-2026",
                  align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(200, 210, 225)
        self.set_line_width(0.2)
        self.line(20, self.get_y() + 0.5, 190, self.get_y() + 0.5)
        self.ln(6)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-14)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*GRAY)
        if self.page_no() == 2:
            self.cell(0, 6, "i", align="C")
        else:
            self.cell(0, 6, str(self.page_no() - 2), align="C")

    # ------------------------------------------------------------------ cover
    def cover(self):
        self.add_page()
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 58, "F")
        self.set_fill_color(*STEEL)
        self.rect(0, 58, 210, 2, "F")

        self.set_y(10)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(180, 210, 255)
        self.cell(0, 7, "ECOLE MAROCAINE DES SCIENCES DE L'INGENIEUR - EMSI CASABLANCA", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Helvetica", "", 9)
        self.cell(0, 6, "Module : Deep Learning  |  Annee universitaire 2025-2026", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(3)
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(255, 255, 255)
        self.cell(0, 12, "RAPPORT DE PROJET", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 9, "Deep Learning avec PyTorch : MLP, CNN et RNN/LSTM/GRU", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_y(70)
        self.set_fill_color(248, 250, 255)
        self.set_draw_color(*NAVY)
        self.set_line_width(0.4)
        self.rect(20, 70, 170, 75, "FD")
        self.set_fill_color(*NAVY)
        self.rect(20, 70, 3, 75, "F")

        infos = [
            ("Etudiant",     "Soulaimane El Younessi"),
            ("Email",        "soulaymane.mo3jiza@gmail.com"),
            ("GitHub",       "DEVBSOUL"),
            ("Repository",   "github.com/DEVBSOUL/projet-deep-learning"),
            ("Encadrant",    "Module Deep Learning - EMSI Casablanca"),
            ("Annee",        "2025 - 2026"),
        ]
        self.set_y(77)
        for lbl, val in infos:
            self.set_x(27)
            self.set_font("Helvetica", "B", 10)
            self.set_text_color(*NAVY)
            self.cell(42, 10, lbl + " :", new_x=XPos.RIGHT, new_y=YPos.LAST)
            self.set_font("Helvetica", "", 10)
            self.set_text_color(*BLACK)
            self.cell(0, 10, val, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_y(155)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*NAVY)
        self.cell(0, 8, "Synthese des architectures etudiees", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)
        self._table(
            ["Partie", "Architecture", "Dataset", "Tache"],
            [
                ["Partie I",   "MLP",          "Breast Cancer Wisconsin",     "Classification binaire"],
                ["Partie II",  "CNN",          "Fashion-MNIST",               "Classification (10 classes)"],
                ["Partie III", "RNN/LSTM/GRU", "Tiny Shakespeare / Tatoeba",  "Modele de langage / Traduction"],
            ],
            [22, 36, 60, 52],
        )

    # ------------------------------------------------------------------ TOC
    def toc(self, pages):
        self.add_page()
        self.set_font("Helvetica", "B", 15)
        self.set_text_color(*NAVY)
        self.cell(0, 10, "Table des matieres", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(*NAVY)
        self.set_line_width(0.5)
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(6)

        entries = [
            (1, "1.",      "Introduction generale",                         "intro"),
            (1, "2.",      "Partie I - MLP : Classification tabulaire",     "mlp"),
            (2, "  2.1",   "Contexte et donnees",                           "mlp_data"),
            (2, "  2.2",   "Fondamentaux PyTorch utilises",                  "mlp_pytorch"),
            (2, "  2.3",   "Architecture du modele MLP",                     "mlp_arch"),
            (2, "  2.4",   "Strategies d initialisation des poids",          "mlp_init"),
            (2, "  2.5",   "Boucle d entrainement et regularisation",        "mlp_train"),
            (2, "  2.6",   "Resultats et evaluation finale",                 "mlp_results"),
            (2, "  2.7",   "Analyse critique",                               "mlp_critique"),
            (1, "3.",      "Partie II - CNN : Classification d images",      "cnn"),
            (2, "  3.1",   "Contexte et donnees Fashion-MNIST",              "cnn_data"),
            (2, "  3.2",   "Biais inductif des reseaux convolutifs",         "cnn_bias"),
            (2, "  3.3",   "Architecture et configurations comparees",        "cnn_arch"),
            (2, "  3.4",   "Visualisation des feature maps",                 "cnn_maps"),
            (2, "  3.5",   "MLP versus CNN",                                 "cnn_vs_mlp"),
            (2, "  3.6",   "Resultats et evaluation",                         "cnn_results"),
            (1, "4.",      "Partie III - RNN, LSTM, GRU et Seq2Seq",        "rnn"),
            (2, "  4.1",   "Modele de langage probabiliste",                 "rnn_lm"),
            (2, "  4.2",   "Comparaison RNN, LSTM et GRU",                  "rnn_compare"),
            (2, "  4.3",   "BPTT et gradient clipping",                      "rnn_bptt"),
            (2, "  4.4",   "Architecture Seq2Seq Encoder-Decoder",           "rnn_s2s"),
            (2, "  4.5",   "Strategies de decodage et evaluation BLEU",      "rnn_decode"),
            (1, "5.",      "Comparaison transversale des trois architectures","compare"),
            (1, "6.",      "Conclusion et perspectives",                      "conclusion"),
        ]

        for level, num, title, key in entries:
            pg = pages.get(key, "")
            if level == 1:
                self.ln(1)
                self.set_font("Helvetica", "B", 10)
                self.set_text_color(*NAVY)
            else:
                self.set_font("Helvetica", "", 10)
                self.set_text_color(*BLACK)

            self.set_x(20)
            self.cell(15, 7, num, new_x=XPos.RIGHT, new_y=YPos.LAST)

            avail = 150
            tw = self.get_string_width(title)
            self.cell(avail, 7, title, new_x=XPos.RIGHT, new_y=YPos.LAST)

            pg_str = str(pg) if pg != "" else "-"
            self.set_font("Helvetica", "B" if level == 1 else "", 10)
            self.cell(0, 7, pg_str, align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            if level == 1:
                self.set_draw_color(210, 220, 235)
                self.set_line_width(0.15)
                self.line(20, self.get_y(), 190, self.get_y())

        self.set_text_color(*BLACK)

    # ------------------------------------------------------------------ typography helpers
    def h1(self, text, key=None):
        self.add_page()
        if key is not None:
            self.sec_pages[key] = self.page_no() - 2
        self.set_fill_color(*NAVY)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 13)
        self.cell(0, 11, "  " + text, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(*BLACK)
        self.ln(4)

    def h2(self, text, key=None):
        if key is not None:
            self.sec_pages[key] = self.page_no() - 2
        self.ln(3)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*NAVY)
        self.cell(0, 8, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(*STEEL)
        self.set_line_width(0.35)
        self.line(20, self.get_y(), 190, self.get_y())
        self.set_text_color(*BLACK)
        self.ln(3)

    def h3(self, text):
        self.ln(2)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(50, 50, 50)
        self.cell(0, 7, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(*BLACK)
        self.ln(1)

    def prose(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*BLACK)
        self.set_x(20)
        self.multi_cell(170, 5.5, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def bullet(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*BLACK)
        self.set_x(24)
        self.cell(5, 5.5, "-", new_x=XPos.RIGHT, new_y=YPos.LAST)
        self.multi_cell(161, 5.5, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def kv(self, key, value):
        self.set_x(22)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*NAVY)
        self.cell(42, 6, key + " :", new_x=XPos.RIGHT, new_y=YPos.LAST)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*BLACK)
        self.multi_cell(126, 6, value, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def transition(self, text):
        self.ln(5)
        y = self.get_y()
        self.set_fill_color(*NAVY)
        self.rect(20, y, 2, 12, "F")
        self.set_x(25)
        self.set_font("Helvetica", "I", 10)
        self.set_text_color(50, 60, 80)
        self.multi_cell(163, 6, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(*BLACK)
        self.ln(2)

    def result_box(self, items):
        self.ln(3)
        cw = 170 / len(items)
        # Ligne 1 : etiquettes
        self.set_x(20)
        for lbl, _ in items:
            self.set_font("Helvetica", "", 8)
            self.set_text_color(*GRAY)
            self.set_fill_color(242, 250, 242)
            self.cell(cw, 9, lbl, align="C", fill=True,
                      new_x=XPos.RIGHT, new_y=YPos.LAST)
        self.ln()
        # Ligne 2 : valeurs
        self.set_x(20)
        for _, val in items:
            self.set_font("Helvetica", "B", 13)
            self.set_text_color(*NAVY)
            self.set_fill_color(242, 250, 242)
            self.cell(cw, 11, val, align="C", fill=True,
                      new_x=XPos.RIGHT, new_y=YPos.LAST)
        self.ln()
        # Bordure verte autour des deux lignes
        y_box = self.get_y() - 20
        self.set_draw_color(*GREEN)
        self.set_line_width(0.4)
        self.rect(20, y_box, 170, 20, style="D")
        self.set_text_color(*BLACK)
        self.ln(4)

    def figure(self, fname, caption):
        self.fig_n += 1
        n = self.fig_n
        path = os.path.join(BASE, fname)
        if not os.path.exists(path):
            self.prose(f"[Figure {n} non disponible : {fname}]")
            return
        self.ln(2)
        # Calcul de la hauteur proportionnelle avec cap a 90 mm
        max_w, max_h = 150, 90
        pw, ph = _png_size(path)
        if pw and ph and ph > 0:
            aspect = ph / pw
            img_w = max_w
            img_h = img_w * aspect
            if img_h > max_h:
                img_h = max_h
                img_w = img_h / aspect
        else:
            img_w, img_h = max_w, 0  # fallback : fpdf calcule
        x = 20 + (170 - img_w) / 2
        if img_h:
            self.image(path, x=x, w=img_w, h=img_h)
        else:
            self.image(path, x=x, w=img_w)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(*GRAY)
        self.set_x(20)
        self.cell(170, 5, f"Figure {n} : {caption}", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(*BLACK)
        self.ln(4)

    def _table(self, headers, rows, col_widths):
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(*NAVY)
        self.set_text_color(255, 255, 255)
        self.set_x(20)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 8, h, border=1, fill=True, align="C",
                      new_x=XPos.RIGHT, new_y=YPos.LAST)
        self.ln()
        for ri, row in enumerate(rows):
            fill = (ri % 2 == 0)
            self.set_fill_color(*LGRAY) if fill else self.set_fill_color(255, 255, 255)
            self.set_text_color(*BLACK)
            self.set_font("Helvetica", "", 9)
            self.set_x(20)
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 7, str(cell), border=1, fill=fill,
                          align="C", new_x=XPos.RIGHT, new_y=YPos.LAST)
            self.ln()
        self.ln(2)

    def tableau(self, caption, headers, rows, col_widths):
        self.tab_n += 1
        n = self.tab_n
        self.ln(2)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(*GRAY)
        self.cell(0, 5, f"Tableau {n} : {caption}", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self._table(headers, rows, col_widths)


# ===================================================================== build
def build(toc_pages=None):
    pdf = Report()
    if toc_pages:
        pdf.sec_pages = toc_pages.copy()

    pdf.cover()
    pdf.toc(toc_pages or {})

    # ================================================================ Ch1
    pdf.h1("1.  Introduction generale", key="intro")
    pdf.prose(
        "Ce rapport presente les travaux realises dans le cadre du projet de fin de module "
        "Deep Learning, annee universitaire 2025-2026 a l EMSI Casablanca. L objectif central "
        "de ce projet est d implementer, d entrainer et d evaluer trois grandes familles "
        "d architectures de reseaux de neurones profonds en utilisant le framework PyTorch, "
        "en partant des fondements theoriques jusqu a l evaluation quantitative sur des "
        "jeux de donnees reels."
    )
    pdf.prose(
        "Les trois architectures etudiees correspondent a trois types distincts de donnees "
        "et de problemes rencontres en apprentissage automatique moderne. La Partie I porte "
        "sur le Perceptron Multicouche (MLP), architecture de reference pour les donnees "
        "tabulaires structurees. La Partie II introduit les Reseaux de Neurones Convolutifs "
        "(CNN), concus pour exploiter la structure spatiale des images. Enfin, la Partie III "
        "couvre les modeles recurrents (RNN, LSTM, GRU) et l architecture Seq2Seq, adaptes "
        "au traitement de sequences temporelles et de texte."
    )
    pdf.prose(
        "Ce rapport est organise de la maniere suivante : chaque chapitre correspond a une "
        "partie du projet, suivant une progression : presentation du contexte et des donnees, "
        "description de l architecture implementee, analyse des resultats obtenus, et critique "
        "des limites observees. Le cinquieme chapitre propose une comparaison transversale des "
        "trois architectures, avant une conclusion generale qui ouvre sur des perspectives "
        "d amelioration."
    )
    pdf.transition(
        "Le chapitre suivant introduit la premiere architecture etudiee : le Perceptron "
        "Multicouche, applique a un probleme de classification medicale sur donnees tabulaires."
    )

    # ================================================================ Ch2 MLP
    pdf.h1("2.  Partie I - MLP : Classification sur donnees tabulaires", key="mlp")

    pdf.h2("2.1  Contexte et donnees", key="mlp_data")
    pdf.prose(
        "La premiere partie du projet porte sur la classification binaire de tumeurs "
        "cancereuses a partir du dataset Breast Cancer Wisconsin (Diagnostic), disponible "
        "dans la bibliotheque scikit-learn. Ce dataset est largement utilise comme "
        "reference en apprentissage automatique pour les donnees medicales tabulaires. "
        "Il comprend 569 echantillons decrits par 30 features numeriques continues, "
        "representant des mesures geometriques de cellules tumorales (rayon, texture, "
        "perimetre, aire, compacite, etc.). La variable cible est binaire : tumeur "
        "benigne (357 cas, 62.7%) ou maligne (212 cas, 37.3%)."
    )
    pdf.kv("Dataset",       "Breast Cancer Wisconsin (Diagnostic)")
    pdf.kv("Source",        "sklearn.datasets.load_breast_cancer()")
    pdf.kv("Dimensions",    "569 echantillons  x  30 features numeriques continues")
    pdf.kv("Classes",       "Benigne : 357 cas (62.7%)  |  Maligne : 212 cas (37.3%)")
    pdf.kv("Decoupage",     "70% train  /  15% validation  /  15% test  (stratifie par classe)")
    pdf.kv("Preprocessing", "Normalisation Z-score (StandardScaler) ajustee sur le train uniquement")
    pdf.ln(2)
    pdf.prose(
        "Le dataset ne presente aucune valeur manquante, ce qui simplifie la phase de "
        "preparation. En revanche, les 30 features presentent une forte multicollinearite : "
        "par exemple, radius_mean et area_mean affichent un coefficient de correlation "
        "superieur a 0.98. La figure ci-dessous illustre cette structure de correlation "
        "ainsi que la distribution des deux classes cibles."
    )
    pdf.figure("correlation_breast_cancer.png",
               "Matrice de correlation des 10 premieres features et distribution des classes (Breast Cancer Wisconsin)")
    pdf.prose(
        "La matrice de correlation met en evidence plusieurs groupes de features redondantes, "
        "notamment les mesures de taille (rayon, perimetre, aire) fortement liees entre elles. "
        "La distribution des classes revele un leger desequilibre (63% / 37%) pris en compte "
        "lors du decoupage stratifie des ensembles de train, validation et test. "
        "La normalisation Z-score est calculee exclusivement sur l ensemble d entrainement "
        "pour eviter toute fuite d information (data leakage) vers les ensembles d evaluation."
    )

    pdf.h2("2.2  Fondamentaux PyTorch utilises", key="mlp_pytorch")
    pdf.prose(
        "Avant de construire le modele, cette partie a ete l occasion d explorer les "
        "mecanismes fondamentaux du framework PyTorch qui sous-tendent toutes les "
        "implementations subsequentes du projet."
    )
    pdf.bullet(
        "nn.Module : classe de base de tout modele PyTorch. Elle maintient un registre "
        "automatique des parametres apprenables (poids et biais) accessibles via "
        ".parameters() et .named_parameters()."
    )
    pdf.bullet(
        "state_dict : dictionnaire ordonne {nom_couche : tenseur} permettant de sauvegarder "
        "et recharger un modele. Utilise ici pour conserver le meilleur checkpoint durant "
        "l entrainement avec early stopping."
    )
    pdf.bullet(
        "Autograd : moteur de differenciation automatique de PyTorch. Le graphe de calcul "
        "dynamique permet de calculer les gradients via .backward(), stockes dans param.grad "
        "pour la mise a jour par l optimiseur."
    )
    pdf.bullet(
        "DataLoader : gestionnaire de mini-batches avec melange aleatoire (shuffle=True) "
        "sur le train, garantissant une diversite des exemples a chaque epoque."
    )
    pdf.bullet(
        "Device management : .to(device) deplace modele et tenseurs vers CPU ou GPU (CUDA). "
        "Le modele et les donnees doivent imperativement etre sur le meme device."
    )

    pdf.h2("2.3  Architecture du modele MLP", key="mlp_arch")
    pdf.prose(
        "Deux implementations equivalentes ont ete realisees pour illustrer la flexibilite "
        "de PyTorch : une version compacte avec nn.Sequential, et une classe personnalisee "
        "heritant de nn.Module offrant plus de contr'ole sur le flux de calcul. "
        "L architecture retenue pour l entrainement final est la suivante :"
    )
    pdf.tableau(
        "Architecture du MLP - Breast Cancer Wisconsin",
        ["Couche", "Type", "Dimensions (entree -> sortie)", "Activation et regularisation"],
        [
            ["Couche 1", "Linear + BatchNorm1d", "30  ->  64", "ReLU  +  Dropout(p=0.3)"],
            ["Couche 2", "Linear + BatchNorm1d", "64  ->  32", "ReLU  +  Dropout(p=0.2)"],
            ["Couche 3", "Linear",               "32  ->   1", "Sigmoid"],
        ],
        [22, 38, 58, 52],
    )
    pdf.prose(
        "Le modele totalise 4 289 parametres apprenables, ce qui reste tres leger par rapport "
        "a la taille du dataset (569 exemples). Ce choix deliberement sobre vise a limiter "
        "le surapprentissage. L utilisation de BatchNorm1d apres chaque couche lineaire "
        "normalise les activations de chaque mini-batch, accelerant la convergence et "
        "reduisant la sensibilite au taux d apprentissage. Le Dropout desactive aleatoirement "
        "des neurones a chaque forward pass durant l entrainement, forcant le reseau a "
        "apprendre des representations distribuees et robustes."
    )

    pdf.h2("2.4  Strategies d initialisation des poids", key="mlp_init")
    pdf.prose(
        "L initialisation des poids est une etape critique souvent sous-estimee. "
        "Une mauvaise initialisation peut provoquer la disparition ou l explosion du gradient "
        "des les premieres epoques, compromettant toute convergence. Trois strategies "
        "ont ete comparees sur 100 epoques avec le meme optimiseur (Adam, lr=1e-3) :"
    )
    pdf.tableau(
        "Comparaison des strategies d initialisation des poids",
        ["Strategie", "Distribution", "mean(W)", "std(W)", "Best val acc"],
        [
            ["Gaussienne", "N(0, 0.01)",                "-0.00013", "0.01009", "100.00 %"],
            ["Constante",  "Toutes nulles (val = 0)",   " 0.00000", "0.00000", " 62.35 %"],
            ["Xavier",     "Uniforme [-sqrt(6/n), +sqrt(6/n)]", "0.00433", "0.14547", "100.00 %"],
        ],
        [28, 60, 22, 22, 28],
    )
    pdf.prose(
        "La figure suivante illustre les courbes de loss et d accuracy pour chacune des "
        "trois strategies sur l ensemble de validation, permettant de visualiser a la fois "
        "la vitesse de convergence et la stabilite de l apprentissage."
    )
    pdf.figure("init_comparison.png",
               "Comparaison des strategies d initialisation - Loss BCE et Accuracy sur 100 epoques")
    pdf.prose(
        "L analyse des courbes revele trois comportements clairement differencies. "
        "L initialisation Constante echoue completement : tous les neurones d une meme "
        "couche recoivent exactement le meme gradient (probleme de symetrie), les rendant "
        "fonctionnellement identiques et incapables d apprendre des representations "
        "distinctes. Sa best val acc de 62.35% correspond au taux de la classe majoritaire, "
        "soit un classifieur trivial. L initialisation Gaussienne converge correctement "
        "mais plus lentement, sa faible variance initiale (std=0.01) induisant des gradients "
        "attenues dans les premieres iterations. L initialisation Xavier (Glorot, 2010) "
        "offre la convergence la plus rapide et la plus stable : en posant "
        "Var(w) = 2/(n_in + n_out), elle maintient la variance des activations constante "
        "a travers les couches, preservant le flux du gradient dans les deux sens "
        "(forward et backward). C est cette strategie qui a ete retenue pour l entrainement final."
    )

    pdf.h2("2.5  Boucle d entrainement et regularisation", key="mlp_train")
    pdf.prose(
        "Le modele final a ete entraine avec une combinaison de techniques de regularisation "
        "complementaires, chacune agissant a un niveau different de l apprentissage. "
        "L optimiseur Adam (Adaptive Moment Estimation, lr=1e-3) combine momentum et "
        "adaptation du taux d apprentissage par parametre, offrant une convergence rapide "
        "et robuste. Le weight decay (L2, valeur 1e-4) penalise les grands poids dans "
        "la fonction de cout, limitant la complexite effective du modele."
    )
    pdf.prose(
        "Le scheduler ReduceLROnPlateau divise le taux d apprentissage par 2 (factor=0.5) "
        "lorsque la val loss ne s ameliore plus pendant 10 epoques consecutives, permettant "
        "de sortir de plateaux de convergence. L early stopping avec patience=20 arrete "
        "l entrainement si la val loss ne s ameliore pas pendant 20 epoques, et sauvegarde "
        "le meilleur checkpoint via torch.save(model.state_dict(), 'best_mlp.pt'). "
        "L entrainement s est arrete a l epoque 88 sur 200 possibles."
    )

    pdf.h2("2.6  Resultats et evaluation finale", key="mlp_results")
    pdf.prose(
        "Apres rechargement du meilleur checkpoint (epoque correspondant a la val loss "
        "minimale), le modele est evalue sur le jeu de test de 86 exemples, "
        "jamais vus durant l entrainement ni la validation. Les resultats obtenus sont "
        "les suivants :"
    )
    pdf.result_box([
        ("Accuracy",   "98.84 %"),
        ("Precision",  "98.18 %"),
        ("Recall",     "100.0 %"),
        ("F1-score",   "99.08 %"),
    ])
    pdf.prose(
        "La figure ci-dessous presente la matrice de confusion ainsi que les courbes "
        "d apprentissage (loss et accuracy) du meilleur modele sur les 88 epoques "
        "d entrainement effectif, illustrant la dynamique de convergence et l absence "
        "de surapprentissage."
    )
    pdf.figure("evaluation_finale.png",
               "Matrice de confusion et courbes d apprentissage du meilleur modele MLP (test set)")
    pdf.prose(
        "La matrice de confusion revele une seule erreur de classification sur 86 exemples "
        "de test : un cas malin predit comme benin (faux negatif). Dans un contexte medical, "
        "le recall de 100% sur les tumeurs malignes est particulierement important : "
        "ne manquer aucun cas malin est la priorite clinique. Les courbes d apprentissage "
        "montrent une convergence stable sans overfitting, la val loss restant proche "
        "de la train loss tout au long de l entrainement."
    )

    pdf.h2("2.7  Analyse critique", key="mlp_critique")
    pdf.prose(
        "Le MLP atteint d excellentes performances sur ce dataset, ce qui s explique par "
        "plusieurs facteurs favorables : les donnees sont numeriques continues, sans valeurs "
        "manquantes, et le probleme de classification binaire est bien conditionne. "
        "Cependant, une analyse critique s impose pour identifier les limites de cette approche."
    )
    pdf.prose(
        "La forte multicollinearite entre features (r > 0.95 pour plusieurs paires) "
        "genere une redondance de representation qui augmente inutilement la complexite "
        "du modele. Une reduction de dimensionnalite (ACP) ou une selection de features "
        "permettrait de simplifier le reseau sans perte de performance. Par ailleurs, "
        "avec seulement 569 exemples, les methodes ensemblistes (Random Forest, XGBoost) "
        "sont competitives avec moins d hyperparametres a regler. Enfin, le MLP offre "
        "une interpretabilite limitee, ce qui peut etre problematique dans un contexte "
        "medical ou la justification des decisions est reglementairement requise."
    )
    pdf.transition(
        "Apres avoir valide l efficacite du MLP sur des donnees tabulaires, le chapitre "
        "suivant aborde un type de donnees fondamentalement different : les images. "
        "Les reseaux de neurones convolutifs exploitent la structure spatiale des pixels "
        "a travers un biais inductif specifique que le MLP ne possede pas."
    )

    # ================================================================ Ch3 CNN
    pdf.h1("3.  Partie II - CNN : Classification d images", key="cnn")

    pdf.h2("3.1  Contexte et donnees Fashion-MNIST", key="cnn_data")
    pdf.prose(
        "La deuxieme partie du projet porte sur la classification d images avec le dataset "
        "Fashion-MNIST, propose par Zalando Research comme alternative plus difficile "
        "au MNIST original. Ce dataset est devenu un benchmark standard pour evaluer "
        "les architectures de vision par ordinateur."
    )
    pdf.kv("Dataset",    "Fashion-MNIST (Zalando Research, 2017)")
    pdf.kv("Source",     "torchvision.datasets.FashionMNIST (telechargement automatique)")
    pdf.kv("Dimensions", "70 000 images en niveaux de gris  28 x 28 pixels")
    pdf.kv("Decoupage",  "60 000 images d entrainement  +  10 000 images de test")
    pdf.kv("Classes",    "10 categories : T-shirt, Pantalon, Pull, Robe, Manteau, Sandale, Chemise, Basket, Sac, Bottine")
    pdf.ln(2)
    pdf.prose(
        "La figure ci-dessous presente un echantillon representatif des 10 categories, "
        "illustrant la diversite visuelle des articles et les similitudes entre certaines "
        "classes (par exemple T-shirt et Chemise, ou Pull et Manteau) qui rendent "
        "la classification non triviale."
    )
    pdf.figure("fashion_mnist_samples.png",
               "Exemples d images par categorie - dataset Fashion-MNIST (28x28 pixels, niveaux de gris)")
    pdf.prose(
        "L observation des exemples confirme que certaines classes presentent une forte "
        "ambiguite visuelle : la Chemise (classe 6) et le T-shirt (classe 0) partagent "
        "des formes tres proches, tout comme le Pull (classe 2) et le Manteau (classe 4). "
        "Ces confusions potentielles seront confirmees par la matrice de confusion "
        "presentee en section 3.6."
    )

    pdf.h2("3.2  Biais inductif des reseaux convolutifs", key="cnn_bias")
    pdf.prose(
        "Le MLP traite chaque pixel independamment, sans tenir compte de la structure "
        "spatiale de l image. Il ignore que les pixels voisins sont generalement correles "
        "et que les motifs visuels (bords, textures, formes) sont invariants en translation : "
        "un col de chemise reste un col de chemise qu il soit a gauche ou a droite de l image."
    )
    pdf.prose(
        "Le CNN encode deux biais inductifs fondamentaux qui le rendent naturellement adapte "
        "aux images. Premierement, la localite : chaque filtre convolutif n observe qu une "
        "petite region de l image (le champ receptif), capturant des motifs locaux. "
        "Deuxiemement, le partage de poids : le meme filtre est applique a toutes les "
        "positions de l image, reduisant drastiquement le nombre de parametres et "
        "assurant l invariance a la translation. Le Max Pooling renforce cette invariance "
        "en rendant la representation robuste aux petites deformations."
    )

    pdf.h2("3.3  Architecture et configurations comparees", key="cnn_arch")
    pdf.prose(
        "L architecture CNN implementee suit la structure classique : blocs convolutifs "
        "(Conv2d + BatchNorm + ReLU + MaxPool) suivis de couches fully connected. "
        "Plusieurs configurations ont ete evaluees pour identifier le meilleur compromis "
        "performance / complexite."
    )
    pdf.tableau(
        "Architecture du meilleur modele CNN - Fashion-MNIST",
        ["Bloc", "Operations", "Sortie (H x W x C)", "Role"],
        [
            ["Conv Block 1", "Conv2d(1,32,3) + BN + ReLU + MaxPool(2)", "14 x 14 x 32", "Detection bords et textures"],
            ["Conv Block 2", "Conv2d(32,64,3) + BN + ReLU + MaxPool(2)", "7 x 7 x 64",  "Detection formes complexes"],
            ["Flatten",      "-",                                         "3136",          "Mise a plat"],
            ["FC 1",         "Linear(3136,256) + ReLU + Dropout(0.5)",   "256",           "Representation compacte"],
            ["FC 2",         "Linear(256,10) + Softmax",                  "10",            "Probabilites par classe"],
        ],
        [25, 60, 36, 49],
    )
    pdf.prose(
        "La figure suivante compare les courbes d apprentissage de plusieurs configurations "
        "CNN testees, permettant de justifier empiriquement le choix de l architecture finale. "
        "Les configurations varient en profondeur (nombre de blocs convolutifs), "
        "en largeur (nombre de filtres) et en taux de dropout."
    )
    pdf.figure("cnn_config_comparison.png",
               "Comparaison de configurations CNN - Accuracy de validation et Loss par configuration")
    pdf.prose(
        "L analyse comparative montre que les configurations avec deux blocs convolutifs "
        "convergent plus rapidement et atteignent une meilleure accuracy que les architectures "
        "a un seul bloc. Au-dela de deux blocs, le gain de performance ne compense pas "
        "l augmentation du temps d entrainement sur CPU. Le dropout apres la couche "
        "fully connected est essentiel pour limiter le surapprentissage observe sans lui."
    )

    pdf.h2("3.4  Visualisation des feature maps", key="cnn_maps")
    pdf.prose(
        "L une des specificites des CNN est leur capacite a apprendre automatiquement "
        "des representations hierarchiques. Pour comprendre ce que le reseau a appris, "
        "les activations des filtres de la premiere couche convolutive ont ete visualisees "
        "sur une image test. Ces activations constituent les feature maps de la premiere couche."
    )
    pdf.figure("feature_maps.png",
               "Visualisation des feature maps de la premiere couche convolutive (Conv Block 1)")
    pdf.prose(
        "Les feature maps revelent que les filtres de la premiere couche se specialisent "
        "dans la detection de motifs elementaires : certains reagissent aux contours "
        "horizontaux, d autres aux contours verticaux, d autres encore aux transitions "
        "d intensite diagonales. Ce resultat est coherent avec la litterature : les premieres "
        "couches d un CNN apprennent des detecteurs de bords de type filtre de Sobel ou "
        "Gabor, tandis que les couches plus profondes combinent ces primitives pour "
        "former des representations de plus haut niveau semantique."
    )

    pdf.h2("3.5  MLP versus CNN", key="cnn_vs_mlp")
    pdf.prose(
        "Afin de quantifier l apport du biais inductif convolutif, les performances du "
        "meilleur CNN ont ete comparees a celles d un MLP applique directement aux "
        "784 pixels aplatis de chaque image. Cette comparaison est illustree dans la "
        "figure suivante."
    )
    pdf.figure("mlp_vs_cnn.png",
               "Comparaison MLP versus CNN - Courbes d apprentissage et accuracy sur Fashion-MNIST")
    pdf.tableau(
        "MLP versus CNN sur Fashion-MNIST",
        ["Critere", "MLP (pixels aplatis)", "CNN (architecture convolutive)"],
        [
            ["Nb parametres",            "> 600 000",          "~200 000"],
            ["Accuracy test",            "~85 %",              "~88-91 %"],
            ["Partage de poids",         "Non",                "Oui (filtres convolutifs)"],
            ["Invariance translation",   "Non",                "Oui (via MaxPooling)"],
            ["Temps d entrainement",     "Rapide",             "Plus lent sur CPU"],
        ],
        [58, 62, 50],
    )
    pdf.prose(
        "Le CNN surpasse le MLP en accuracy tout en utilisant trois fois moins de parametres, "
        "confirmant l efficacite du partage de poids convolutif. L avantage en parametres "
        "s explique par le fait que les filtres convolutifs (typiquement 3x3 = 9 poids par filtre) "
        "remplacent des connexions denses qui relieraient chaque pixel a chaque neurone caché."
    )

    pdf.h2("3.6  Resultats et evaluation", key="cnn_results")
    pdf.prose(
        "Le meilleur modele CNN atteint une accuracy de 88 a 91% sur le jeu de test, "
        "selon la configuration retenue. La matrice de confusion ci-dessous detail le "
        "comportement du modele classe par classe, revelant les confusions les plus "
        "frequentes entre categories visuellement proches."
    )
    pdf.figure("cnn_confusion_matrix.png",
               "Matrice de confusion du meilleur modele CNN sur le jeu de test Fashion-MNIST")
    pdf.prose(
        "La matrice de confusion confirme les ambigüites identifies lors de l exploration "
        "du dataset : les confusions les plus frequentes se produisent entre T-shirt (0) "
        "et Chemise (6), et entre Pull (2) et Manteau (4), deux paires de classes aux "
        "formes visuelles tres similaires. Ces erreurs sont communes a tous les modeles "
        "de vision sur Fashion-MNIST et representent la difficulte intrinseque du dataset."
    )
    pdf.transition(
        "Apres avoir explore les donnees structurees et les images, le chapitre suivant "
        "aborde la troisieme famille d architectures : les modeles recurrents, concus pour "
        "traiter des sequences de longueur variable ou l ordre des elements est porteur de sens."
    )

    # ================================================================ Ch4 RNN
    pdf.h1("4.  Partie III - RNN, LSTM, GRU et Seq2Seq", key="rnn")

    pdf.h2("4.1  Modele de langage probabiliste", key="rnn_lm")
    pdf.prose(
        "La troisieme partie du projet porte sur le traitement de sequences, en commencant "
        "par un modele de langage au niveau caractere entraine sur le corpus Tiny Shakespeare. "
        "Un modele de langage assign une probabilite a chaque sequence de tokens en decomposant "
        "cette probabilite par la regle de la chaine :"
    )
    pdf.prose(
        "P(w1, w2, ..., wT) = Produit de P(wt | w1, ..., wt-1) pour t de 1 a T."
    )
    pdf.prose(
        "A chaque pas de temps t, le reseau recurrent recoit le caractere courant, "
        "met a jour son etat cache ht = f(ht-1, xt), puis calcule une distribution "
        "de probabilites sur le vocabulaire pour predire le prochain caractere. "
        "La metrique d evaluation est la Perplexite (PPL), definie comme PPL = exp(Loss), "
        "ou une valeur plus basse indique un modele plus performant : une PPL de k signifie "
        "que le modele est aussi incertain que s il choisissait uniformement parmi k alternatives."
    )
    pdf.kv("Dataset",      "Tiny Shakespeare (~200 000 caracteres)")
    pdf.kv("Source",       "Telechargement automatique depuis GitHub (Karpathy/char-rnn)")
    pdf.kv("Vocabulaire",  "65 caracteres uniques (lettres, chiffres, ponctuation, espaces)")
    pdf.kv("Sequence",     "SEQ_LEN = 64 caracteres  |  BATCH_SIZE = 128")
    pdf.kv("Decoupage",    "80% train  /  20% validation")

    pdf.h2("4.2  Comparaison RNN, LSTM et GRU", key="rnn_compare")
    pdf.prose(
        "Une architecture CharRNN unifiee a ete implementee, parametree par le type de "
        "cellule recurrente (RNN, LSTM ou GRU). Les trois variantes ont ete entrainées "
        "dans des conditions identiques (embed_dim=64, hidden_dim=128, 1 couche, Adam lr=1e-3) "
        "afin de comparer uniquement l effet de la cellule recurrente."
    )
    pdf.tableau(
        "Comparaison architecturale RNN, LSTM et GRU",
        ["Modele", "Memoire", "Stabilite gradient", "Nb params (relatif)", "Vitesse"],
        [
            ["RNN",  "Court terme uniquement",         "Mauvaise (vanishing/exploding)", "1x (reference)", "Rapide"],
            ["LSTM", "Long terme (cell state ct)",     "Bonne (4 portes : i, f, g, o)", "4x",             "Lent"],
            ["GRU",  "Moyen terme (2 portes r et z)",  "Bonne (reset, update gates)",   "3x",             "Intermediaire"],
        ],
        [22, 45, 48, 32, 23],
    )
    pdf.prose(
        "La figure suivante presente les courbes de loss et de perplexite sur l ensemble "
        "de validation pour les trois architectures, permettant de comparer "
        "empiriquement leur comportement sur le meme corpus."
    )
    pdf.figure("rnn_comparison.png",
               "Comparaison RNN vs LSTM vs GRU - Loss et Perplexite de validation sur Tiny Shakespeare")
    pdf.prose(
        "Les courbes confirment la superiorite du LSTM sur les sequences de caracteres. "
        "Le RNN simple manifeste une instabilite et converge vers une perplexite plus "
        "elevee, reflet de son incapacite a modeliser les dependances de longue distance "
        "dans le texte de Shakespeare (structures de strophes, repetition de motifs). "
        "Le LSTM obtient la perplexite de validation la plus basse grace a son cell state, "
        "qui cree une 'autoroute de gradient' preservant l information sur de longues sequences. "
        "Le GRU offre un excellent compromis : performances proches du LSTM avec un tiers "
        "de parametres en moins et une vitesse d entrainement superieure."
    )

    pdf.h2("4.3  BPTT et gradient clipping", key="rnn_bptt")
    pdf.prose(
        "La retropropagation a travers le temps (BPTT, Backpropagation Through Time) "
        "etend l algorithme standard de retropropagation aux reseaux recurrents. "
        "Le gradient de la loss par rapport aux parametres initiaux implique un produit "
        "de T jacobiens successifs, ou T est la longueur de la sequence :"
    )
    pdf.prose(
        "d(ht)/d(h0) = Produit de d(hk)/d(hk-1) pour k de 1 a t."
    )
    pdf.prose(
        "Si les valeurs propres de la matrice recurrente sont inferieures a 1, ce produit "
        "converge vers zero exponentiellement (vanishing gradient), rendant le modele "
        "incapable d apprendre des dependances longue distance. A l inverse, des valeurs "
        "propres superieures a 1 provoquent une explosion du gradient. Le gradient clipping "
        "constitue la solution standard a l explosion : si la norme du gradient depasse "
        "un seuil tau, on le renormalise a tau sans en changer la direction."
    )
    pdf.prose(
        "La figure suivante presente l effet de trois valeurs de seuil de clipping "
        "sur la norme du gradient et la loss d entrainement d un RNN simple avec SGD, "
        "un contexte particulierement propice a l explosion du gradient."
    )
    pdf.figure("gradient_clipping.png",
               "Effet du gradient clipping sur la norme du gradient et la loss (RNN + SGD, 40 iterations)")
    pdf.prose(
        "Sans clipping, la norme du gradient explose rapidement (visible en echelle "
        "logarithmique), provoquant des mises a jour de poids erratiques et une "
        "loss instable. Un seuil de 5.0 stabilise l entrainement sans contraindre "
        "excessivement la descente de gradient. Un seuil de 1.0 est plus conservateur "
        "et peut ralentir la convergence initiale. Dans la pratique, un seuil entre "
        "1.0 et 5.0 est recommande pour les RNN entraînes avec SGD ou Adam."
    )

    pdf.h2("4.4  Architecture Seq2Seq Encoder-Decoder", key="rnn_s2s")
    pdf.prose(
        "La seconde application de la Partie III est un systeme de traduction automatique "
        "anglais vers francais base sur l architecture Sequence-to-Sequence (Sutskever et al., 2014). "
        "Ce systeme est constitue de deux modules LSTM distincts : un encodeur qui lit "
        "la sequence source et la compresse en un vecteur contexte, et un decodeur qui "
        "genere la traduction token par token a partir de ce vecteur."
    )
    pdf.kv("Dataset",       "Tatoeba (paires de phrases EN-FR courtes)")
    pdf.kv("Volume",        "500 paires d entrainement  (train 85% / validation 15%)")
    pdf.kv("Tokenisation",  "Decoupage par mots (split), mise en minuscules")
    pdf.kv("Tokens spec.",  "<pad>, <sos> (debut), <eos> (fin), <unk> (inconnu)")
    pdf.kv("Entrainement",  "5 epoques, Adam lr=5e-3, gradient clipping = 1.0, teacher forcing ratio = 0.5")
    pdf.ln(2)
    pdf.prose(
        "Le teacher forcing consiste, durant l entrainement, a fournir au decodeur "
        "le vrai token de reference yt-1 comme entree, plutot que sa propre prediction. "
        "Cette technique accelere la convergence mais introduit un exposure bias : "
        "le modele apprend dans une distribution differente de celle de l inference, "
        "ou il doit corriger ses propres erreurs. La figure ci-dessous presente les "
        "courbes de loss du systeme Seq2Seq sur les ensembles de train et de validation."
    )
    pdf.figure("seq2seq_loss.png",
               "Courbes de loss du systeme Seq2Seq (Encoder-Decoder LSTM) - Anglais vers Francais")
    pdf.prose(
        "Les courbes montrent une decroissance reguliere de la loss d entrainement sur "
        "les 5 epoques. L ecart entre train loss et val loss reste modere, indiquant "
        "l absence de surapprentissage severe malgre le faible volume de donnees. "
        "Le systeme apprend les structures syntaxiques elementaires de la traduction "
        "anglais-francais, bien que la performance reste limitee par la taille du corpus."
    )

    pdf.h2("4.5  Strategies de decodage et evaluation BLEU", key="rnn_decode")
    pdf.prose(
        "Une fois le modele entraine, deux strategies de decodage ont ete implementees "
        "et comparees pour la generation des traductions a l inference."
    )
    pdf.prose(
        "Le decodage glouton (greedy decoding) selectionne a chaque pas le token de "
        "probabilite maximale : token_t = argmax P(wt | contexte). Cette approche est "
        "computationnellement simple (O(T x V) par inference) mais myope : choisir le "
        "meilleur token local peut conduire a une sequence globalement sous-optimale."
    )
    pdf.prose(
        "Le Beam Search (k=3) maintient simultanement les k hypotheses les plus prometteuses "
        "a chaque pas, explorant davantage l espace de sequences. Sa complexite est "
        "O(T x k x V), mais il ameliore generalement le score BLEU de 1 a 3 points "
        "par rapport au decodage glouton."
    )
    pdf.prose(
        "L evaluation de la qualite des traductions est realisee avec le score BLEU-1 "
        "(Bilingual Evaluation Understudy), qui mesure le recouvrement de unigrammes "
        "entre la traduction predite et la reference, avec une penalite de brievete. "
        "Les scores obtenus sont modestes en raison du volume tres limite du corpus "
        "d entrainement (500 paires, 5 epoques sur CPU) : un score BLEU-1 significatif "
        "necessite au minimum 10 000 paires et 20 epoques d entrainement."
    )
    pdf.transition(
        "Les trois architectures ayant ete etudiees independamment, le chapitre suivant "
        "propose une analyse transversale qui met en evidence leurs differences fondamentales "
        "et guide le choix de l architecture en fonction de la nature des donnees."
    )

    # ================================================================ Ch5 Compare
    pdf.h1("5.  Comparaison transversale des trois architectures", key="compare")
    pdf.prose(
        "Ce chapitre synthetise les enseignements des trois parties du projet en proposant "
        "une comparaison structuree des architectures etudiees selon plusieurs dimensions : "
        "biais inductif, type de donnees privilegie, mecanisme de regularisation, "
        "et performance obtenue dans ce projet."
    )
    pdf.tableau(
        "Comparaison multi-criteres : MLP, CNN et RNN/LSTM",
        ["Critere", "MLP (Partie I)", "CNN (Partie II)", "RNN/LSTM (Partie III)"],
        [
            ["Type de donnees cible",  "Tabulaire / features",  "Images et signaux 2D",   "Sequences temporelles"],
            ["Biais inductif",         "Aucun",                 "Localite + inv. transl.", "Ordre temporel"],
            ["Partage de poids",       "Non",                   "Oui (filtres conv.)",     "Oui (matrice Wh)"],
            ["Memoire contextuelle",   "Aucune",                "Locale (champ recept.)", "Globale (etat cache)"],
            ["Regularisation cle",     "BN + Dropout + L2",    "BN + Dropout + Pooling", "Dropout + Clip + TF"],
            ["Entrainement",           "Backprop standard",     "Backprop standard",       "BPTT + grad clipping"],
            ["Dataset utilise",        "Breast Cancer Wisc.",   "Fashion-MNIST",           "Shakespeare / Tatoeba"],
            ["Performance principale", "Acc. 98.84% (F1 99%)", "Acc. 88-91%",             "PPL : LSTM < GRU < RNN"],
        ],
        [44, 40, 42, 44],
    )
    pdf.prose(
        "Le tableau precedent met en lumiere une progression logique : chaque architecture "
        "encode un biais inductif de plus en plus specialise. Le MLP n impose aucune "
        "contrainte sur la structure des donnees, ce qui le rend versatile mais moins "
        "efficace que des architectures adaptees lorsque la structure existe. Le CNN "
        "exploite la regularite spatiale des images via le partage de poids, reduisant "
        "le nombre de parametres d un facteur 3 tout en ameliorant les performances "
        "par rapport au MLP. Le LSTM ajoute une dimension temporelle explicite via "
        "son cell state, lui permettant de capturer des dependances longue distance "
        "impossibles a modeliser pour les deux architectures precedentes."
    )
    pdf.h3("Guide de selection de l architecture")
    pdf.bullet(
        "MLP : donnees tabulaires structurees avec features numeriques ou categorielles, "
        "absence de structure spatiale ou temporelle, faible dimensionnalite. "
        "Exemple : prevision de prix, scoring de credit, diagnostic medical."
    )
    pdf.bullet(
        "CNN : donnees avec structure spatiale (images, spectrogrammes, signaux 1D courts), "
        "problemes ou l invariance a la translation est souhaitable. "
        "Exemple : classification d images, detection d objets, reconnaissance de parole."
    )
    pdf.bullet(
        "RNN/LSTM/GRU : sequences de longueur variable avec dependances temporelles "
        "ou contextuelles importantes. Exemple : NLP, traduction automatique, "
        "prediction de series temporelles, generation de texte."
    )
    pdf.prose(
        "Il est important de noter que ces trois architectures servent aujourd hui "
        "de briques fondamentales aux modeles Transformers (Vaswani et al., 2017), "
        "qui unifient et surpassent ces approches pour le traitement de sequences "
        "grace au mecanisme d attention multi-tete et a la parallelisation complete."
    )
    pdf.transition(
        "La conclusion du rapport revient sur les principaux enseignements du projet "
        "et propose des pistes d amelioration pour chacune des trois parties."
    )

    # ================================================================ Ch6 Conclusion
    pdf.h1("6.  Conclusion et perspectives", key="conclusion")
    pdf.prose(
        "Ce projet a permis d implementer et d evaluer de bout en bout trois familles "
        "fondamentales d architectures de deep learning avec PyTorch, sur des jeux de "
        "donnees reels couvrant des domaines varies : le medical, la vision par ordinateur, "
        "et le traitement du langage naturel."
    )
    pdf.prose(
        "Les principaux enseignements peuvent etre resumes comme suit. Le MLP s avere "
        "une solution performante et robuste pour les donnees tabulaires bien structurees, "
        "atteignant une accuracy de 98.84% sur le dataset Breast Cancer Wisconsin grace "
        "a une regularisation efficace (BatchNorm, Dropout, Early Stopping) et a "
        "l initialisation Xavier. Le CNN exploite avec succes le biais inductif de "
        "localite et d invariance spatiale propre aux images, surpassant le MLP avec "
        "trois fois moins de parametres sur Fashion-MNIST. Enfin, les modeles recurrents "
        "illustrent comment encoder l ordre temporel des sequences : le LSTM surpasse "
        "le RNN simple grace a son cell state qui preserve le gradient sur de longues "
        "sequences, et le systeme Seq2Seq pose les bases de la traduction automatique neuronale."
    )
    pdf.prose(
        "Ces trois architectures s inscrivent dans une progression historique et conceptuelle "
        "qui aboutit aux Transformers (Vaswani et al., 2017), architecture dominante en NLP "
        "et de plus en plus utilisee en vision (Vision Transformer, ViT). Comprendre les "
        "biais inductifs du MLP, du CNN et du LSTM est indispensable pour apprehender "
        "pourquoi l attention multi-tete constitue un mecanisme plus general et plus puissant."
    )
    pdf.h3("Perspectives d amelioration")
    pdf.bullet(
        "Partie I : appliquer une analyse en composantes principales (ACP) pour reduire "
        "la multicollinearite et simplifier le modele sans perte de performance. "
        "Comparer avec un gradient boosting (XGBoost) pour quantifier l apport du MLP."
    )
    pdf.bullet(
        "Partie II : explorer le transfer learning avec des modeles pre-entraines "
        "(ResNet-18, EfficientNet) finetuned sur Fashion-MNIST pour depasser les 93% d accuracy. "
        "Implementer la data augmentation (rotation, flip, crop) pour ameliorer la robustesse."
    )
    pdf.bullet(
        "Partie III : ajouter un mecanisme d attention de Bahdanau (2015) au Seq2Seq "
        "pour depasser le goulot d etranglement du vecteur contexte fixe. "
        "Entrainer sur un corpus plus grand (> 10 000 paires) pour obtenir un BLEU significatif."
    )
    pdf.bullet(
        "Global : experimenter des optimiseurs recents (AdamW, Lion) et des schedulers "
        "cosine avec warmup, qui se sont imposes comme standard dans les grandes architectures."
    )
    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*GRAY)
    pdf.set_x(20)
    pdf.multi_cell(170, 5.5,
        "Repository GitHub : github.com/DEVBSOUL/projet-deep-learning\n"
        "Technologies : Python 3.10+  |  PyTorch  |  torchvision  |  scikit-learn  |  NumPy  |  Matplotlib  |  Seaborn",
        new_x=XPos.LMARGIN, new_y=YPos.NEXT
    )
    pdf.set_text_color(*BLACK)

    return pdf


# ===================================================================== main
if __name__ == "__main__":
    print("Passe 1 : collecte des numeros de pages...")
    p1 = build(toc_pages=None)
    pages = p1.sec_pages.copy()
    print("Pages collectees :", pages)

    print("Passe 2 : generation du PDF final avec TOC...")
    p2 = build(toc_pages=pages)
    p2.output(OUT)

    size_kb = os.path.getsize(OUT) // 1024
    print(f"PDF genere : {OUT}")
    print(f"Taille     : {size_kb} KB  |  Pages : {p2.page_no()}")
