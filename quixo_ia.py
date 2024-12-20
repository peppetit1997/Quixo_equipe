from quixo import Quixo
from quixo_error import QuixoError
import random

class QuixoIA(Quixo):
    def __init__(self, joueurs, plateau=None):
        super().__init__(joueurs, plateau)
        self.resultats = {
            "X": {2: 0, 3: 0, 4: 0, 5: 0},
            "O": {2: 0, 3: 0, 4: 0, 5: 0}
        }

    def lister_les_coups_possibles(self, plateau, cube):
        """Retourne une liste des coups possibles pour le cube donné."""
        Coups_possibles = []
        Coordonnees_disponibles = []

        # Modifier les bornes de 0-4 à 1-5 pour respecter la validation des coordonnées
        for x in range(1, 6):  # Limiter x de 1 à 5
            for y in range(1, 6):  # Limiter y de 1 à 5
                if (x == 1 or x == 5 or y == 1 or y == 5):  # Bords du plateau
                    if plateau[x-1][y-1] == " " or plateau[x-1][y-1] == cube:  # Ajuster l'indexation
                        Coordonnees_disponibles.append((x, y))

        for (x, y) in Coordonnees_disponibles:
            # Vérification des bords du plateau pour éviter les déplacements hors des limites
            if x == 1:
                Coups_possibles.append({"origine": (x, y), "direction": "haut"})
            if x == 5:
                Coups_possibles.append({"origine": (x, y), "direction": "bas"})
            if y == 1:
                Coups_possibles.append({"origine": (x, y), "direction": "gauche"})
            if y == 5:
                Coups_possibles.append({"origine": (x, y), "direction": "droite"})

        return Coups_possibles

    def analyser_le_plateau(self, plateau):
        """Analyse le plateau et retourne les résultats de l'analyse."""
        resultats = {
            "X": {2: 0, 3: 0, 4: 0, 5: 0},
            "O": {2: 0, 3: 0, 4: 0, 5: 0}
        }

        # Analyse des lignes
        for x in range(5):
            compteur_x = 0
            compteur_o = 0
            for y in range(5):
                if plateau[x][y] == "X":
                    compteur_x += 1
                    compteur_o = 0
                elif plateau[x][y] == "O":
                    compteur_o += 1
                    compteur_x = 0
                else:
                    compteur_x = 0
                    compteur_o = 0
                if 2 <= compteur_x <= 5:
                    resultats["X"][compteur_x] += 1
                if 2 <= compteur_o <= 5:
                    resultats["O"][compteur_o] += 1

        # Analyse des colonnes
        for y in range(5):
            compteur_x = 0
            compteur_o = 0
            for x in range(5):
                if plateau[x][y] == "X":
                    compteur_x += 1
                    compteur_o = 0
                elif plateau[x][y] == "O":
                    compteur_o += 1
                    compteur_x = 0
                else:
                    compteur_x = 0
                    compteur_o = 0
                if 2 <= compteur_x <= 5:
                    resultats["X"][compteur_x] += 1
                if 2 <= compteur_o <= 5:
                    resultats["O"][compteur_o] += 1

        # Analyse des diagonales principales
        compteur_x = 0
        compteur_o = 0
        for i in range(5):
            if plateau[i][i] == "X":
                compteur_x += 1
                compteur_o = 0
            elif plateau[i][i] == "O":
                compteur_o += 1
                compteur_x = 0
            else:
                compteur_x = 0
                compteur_o = 0
            if 2 <= compteur_x <= 5:
                resultats["X"][compteur_x] += 1
            if 2 <= compteur_o <= 5:
                resultats["O"][compteur_o] += 1

        # Analyse des diagonales secondaires
        compteur_x = 0
        compteur_o = 0
        for i in range(5):
            if plateau[i][4 - i] == "X":
                compteur_x += 1
                compteur_o = 0
            elif plateau[i][4 - i] == "O":
                compteur_o += 1
                compteur_x = 0
            else:
                compteur_x = 0
                compteur_o = 0
            if 2 <= compteur_x <= 5:
                resultats["X"][compteur_x] += 1
            if 2 <= compteur_o <= 5:
                resultats["O"][compteur_o] += 1

        return resultats

    def partie_terminée(self):
        """Détermine si la partie est terminée et retourne le résultat."""
        if self.resultats["X"][5] != 0:
            return self.joueurs[0]
        if self.resultats["O"][5] != 0:
            return self.joueurs[1]
        else:
            return None

    def trouver_un_coup_vainqueur(self, symbole):
        """Trouve un coup gagnant pour le joueur donné."""
        coups_possibles = self.lister_les_coups_possibles(self.plateau.état_plateau(), symbole)

        for coup in coups_possibles:
            # Créer une copie de l'état du plateau
            nouveau_plateau = [row[:] for row in self.plateau.état_plateau()]

            origine_x, origine_y = coup["origine"]
            direction = coup["direction"]

            # Vérification que le coup n'est pas en dehors des limites
            if direction == "bas" and origine_x == 5:
                continue  # Impossible de déplacer un cube de la dernière ligne vers le bas

            # Vérification que le coup est sur un cube du joueur
            if nouveau_plateau[origine_x-1][origine_y-1] != symbole and nouveau_plateau[origine_x-1][origine_y-1] != " ":
                continue  # Passer ce coup si ce n'est pas un cube du joueur

            # Effectuer le coup sur une copie du plateau
            nouveau_plateau[origine_x-1][origine_y-1] = ""
            if direction == "haut":
                nouveau_plateau[0][origine_y-1] = symbole
            elif direction == "bas":
                nouveau_plateau[4][origine_y-1] = symbole
            elif direction == "gauche":
                nouveau_plateau[origine_x-1][0] = symbole
            elif direction == "droite":
                nouveau_plateau[origine_x-1][4] = symbole

            # Analyser l'état du plateau modifié
            analyse = self.analyser_le_plateau(nouveau_plateau)
            if analyse[symbole][5] > 0:
                return coup

        return None

    def trouver_un_coup_bloquant(self, symbole):
        """Trouve un coup bloquant pour empêcher l'adversaire de gagner."""
        symbole_adversaire = "X" if symbole == "O" else "O"
        coup_vainqueur_adversaire = self.trouver_un_coup_vainqueur(symbole_adversaire)

        if coup_vainqueur_adversaire:
            return coup_vainqueur_adversaire

        return None

    def jouer_un_coup(self, symbole):
        """Joue un coup pour le joueur spécifié (X ou O)."""
        if self.partie_terminée() is not None:
            raise QuixoError("La partie est déjà terminée.")
        if symbole not in ["X", "O"]:
            raise QuixoError('Le symbole doit être "X" ou "O".')

        # Trouver un coup gagnant
        coup_vainqueur = self.trouver_un_coup_vainqueur(symbole)
        if coup_vainqueur:
            return coup_vainqueur["origine"], coup_vainqueur["direction"]

        # Trouver un coup bloquant
        coup_bloquant = self.trouver_un_coup_bloquant(symbole)
        if coup_bloquant:
            return coup_bloquant["origine"], coup_bloquant["direction"]

        # Choisir un coup aléatoire parmi les coups possibles
        coups_possibles = self.lister_les_coups_possibles(self.plateau.état_plateau(), symbole)
        if not coups_possibles:
            raise QuixoError("Aucun coup possible.")
        coup_aleatoire = random.choice(coups_possibles)
        return coup_aleatoire["origine"], coup_aleatoire["direction"]
