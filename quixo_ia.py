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
        print(f"Liste des coups possibles pour le cube {cube} :")
        Coups_possibles = []
        Coordonnees_disponibles = []

        for x in range(1, 6):  # Limiter x de 1 à 5
            for y in range(1, 6):  # Limiter y de 1 à 5
                if (x in [1, 5] or y in [1, 5]) and (0 <= x < len(plateau)) and (0 <= y < len(plateau[x])):
                    if plateau[x][y] == " " or plateau[x][y] == cube:  # Ne pas inclure les cases occupées par l'adversaire
                        Coordonnees_disponibles.append((x, y))

        for (x, y) in Coordonnees_disponibles:
            if x > 1 and x < 5 and y > 1 and y < 5:
                raise RuntimeError("Le joueur ne peut pas déplacer un bloc intérieur, x ou y doit avoir la valeur 1 ou 5.")
            if x == 1:
                Coups_possibles.append({"origine": (x, y), "direction": "haut"})
            if x == 5:
                Coups_possibles.append({"origine": (x, y), "direction": "bas"})
            if y == 1:
                Coups_possibles.append({"origine": (x, y), "direction": "gauche"})
            if y == 5:
                Coups_possibles.append({"origine": (x, y), "direction": "droite"})

        print(f"Coups possibles : {Coups_possibles}")
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

            # Effectuer le coup sur une copie du plateau
            nouveau_plateau[origine_x][origine_y] = ""
            if direction == "haut":
                nouveau_plateau[0][origine_y] = symbole
            elif direction == "bas":
                nouveau_plateau[4][origine_y] = symbole
            elif direction == "gauche":
                nouveau_plateau[origine_x][0] = symbole
            elif direction == "droite":
                nouveau_plateau[origine_x][4] = symbole

            # Analyser l'état du plateau modifié
            analyse = self.analyser_le_plateau(nouveau_plateau)
            if analyse[symbole][5] > 0:
                return coup

        return None

    def trouver_un_coup_bloquant(self, symbole):
        symbole_adversaire = "X" if symbole == "O" else "O"
        coup_vainqueur_adversaire = self.trouver_un_coup_vainqueur(symbole_adversaire)

        if coup_vainqueur_adversaire:
            return coup_vainqueur_adversaire

        return None

    def jouer_un_coup(self, symbole):
        if self.partie_terminée() is not None:
            raise QuixoError("La partie est déjà terminée.")
        if symbole not in ["X", "O"]:
            raise QuixoError('Le symbole doit être "X" ou "O".')

        coup_vainqueur = self.trouver_un_coup_vainqueur(symbole)
        if coup_vainqueur:
            return coup_vainqueur["origine"], coup_vainqueur["direction"]

        coup_bloquant = self.trouver_un_coup_bloquant(symbole)
        if coup_bloquant:
            return coup_bloquant["origine"], coup_bloquant["direction"]

        coups_possibles = self.lister_les_coups_possibles(self.plateau.état_plateau(), symbole)
        coup_aleatoire = random.choice(coups_possibles)
        return coup_aleatoire["origine"], coup_aleatoire["direction"]
