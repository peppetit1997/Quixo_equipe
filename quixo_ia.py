"""
Module pour implémenter l'IA du jeu Quixo.
Hérite de la classe Quixo et inclut des méthodes pour la prise de décision.
"""

from quixo import Quixo
from quixo_error import QuixoError
import random


class QuixoIA(Quixo):
    """
    Cette classe implémente l'IA du jeu Quixo.
    Elle hérite de la classe Quixo et inclut des méthodes pour évaluer le plateau,
    choisir des coups gagnants ou bloquants, et effectuer des coups aléatoires.
    """
    def __init__(self, joueurs, plateau=None):
        """
        Initialise la classe QuixoIA avec les joueurs et le plateau.

        Arguments:
        joueurs -- Liste des joueurs.
        plateau -- (Optionnel) État initial du plateau.
        """
        super().__init__(joueurs, plateau)
        self.resultats = {
            "X": {2: 0, 3: 0, 4: 0, 5: 0},
            "O": {2: 0, 3: 0, 4: 0, 5: 0}
        }

    def lister_les_coups_possibles(self, plateau, cube):
        """
        Retourne une liste des coups possibles pour le cube donné.

        Arguments:
        plateau -- État actuel du plateau.
        cube -- Symbole du cube pour lequel lister les coups possibles.
        """
        coups_possibles = []
        coordonnees_disponibles = self._get_available_coordinates(plateau, cube)
        for (x, y) in coordonnees_disponibles:
            coups_possibles.extend(self._get_move_directions(x, y))
        return coups_possibles

    def _get_available_coordinates(self, plateau, cube):
        coordonnees_disponibles = []
        for x in range(1, 6):
            for y in range(1, 6):
                if (x == 1 or x == 5 or y == 1 or y == 5):
                    if plateau[x - 1][y - 1] == " " or plateau[x - 1][y - 1] == cube:
                        coordonnees_disponibles.append((x, y))
        return coordonnees_disponibles

    def _get_move_directions(self, x, y):
        coups_possibles = []
        if x == 1:
            coups_possibles.append({"origine": (x, y), "direction": "haut"})
        if x == 5:
            coups_possibles.append({"origine": (x, y), "direction": "bas"})
        if y == 1:
            coups_possibles.append({"origine": (x, y), "direction": "gauche"})
        if y == 5:
            coups_possibles.append({"origine": (x, y), "direction": "droite"})
        return coups_possibles

    def analyser_le_plateau(self, plateau):
        """
        Analyse le plateau et retourne les résultats de l'analyse.

        Arguments:
        plateau -- État actuel du plateau.
        """
        resultats = {
            "X": {2: 0, 3: 0, 4: 0, 5: 0},
            "O": {2: 0, 3: 0, 4: 0, 5: 0}
        }
        self.analyser_lignes(plateau, resultats)
        self.analyser_colonnes(plateau, resultats)
        self.analyser_diagonales(plateau, resultats)
        return resultats

    def analyser_lignes(self, plateau, resultats):
        """
        Analyse les lignes du plateau.

        Arguments:
        plateau -- État actuel du plateau.
        resultats -- Dictionnaire où les résultats seront stockés.
        """
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

    def analyser_colonnes(self, plateau, resultats):
        """
        Analyse les colonnes du plateau.

        Arguments:
        plateau -- État actuel du plateau.
        resultats -- Dictionnaire où les résultats seront stockés.
        """
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

    def analyser_diagonales(self, plateau, resultats):
        """
        Analyse les diagonales du plateau.

        Arguments:
        plateau -- État actuel du plateau.
        resultats -- Dictionnaire où les résultats seront stockés.
        """
        self.analyser_diagonale_principale(plateau, resultats)
        self.analyser_diagonale_secondaire(plateau, resultats)

    def analyser_diagonale_principale(self, plateau, resultats):
        """
        Analyse la diagonale principale du plateau.

        Arguments:
        plateau -- État actuel du plateau.
        resultats -- Dictionnaire où les résultats seront stockés.
        """
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

    def analyser_diagonale_secondaire(self, plateau, resultats):
        """
        Analyse la diagonale secondaire du plateau.

        Arguments:
        plateau -- État actuel du plateau.
        resultats -- Dictionnaire où les résultats seront stockés.
        """
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

    def partie_terminée(self):
        """
        Détermine si la partie est terminée et retourne le résultat.

        Arguments:
        Aucun.
        """
        if self.resultats["X"][5] != 0:
            return self.joueurs[0]
        if self.resultats["O"][5] != 0:
            return self.joueurs[1]
        return None

    def trouver_un_coup_vainqueur(self, symbole):
        """
        Trouve un coup gagnant pour le joueur donné.

        Arguments:
        symbole -- Symbole du joueur (X ou O).
        """
        plateau_etat = self.plateau.état_plateau()
        coups_possibles = self.lister_les_coups_possibles(plateau_etat, symbole)

        for coup in coups_possibles:
            # Créer une copie de l'état du plateau
            nouveau_plateau = [row[:] for row in plateau_etat]

            origine_x, origine_y = coup["origine"]
            direction = coup["direction"]

            # Vérification que le coup n'est pas en dehors des limites
            if direction == "bas" and origine_x == 5:
                continue

            # Vérification que le coup est sur un cube du joueur
            if nouveau_plateau[origine_x - 1][origine_y - 1] != symbole and nouveau_plateau[origine_x - 1][origine_y - 1] != " ":
                continue

            # Effectuer le coup sur une copie du plateau
            nouveau_plateau[origine_x - 1][origine_y - 1] = ""
            if direction == "haut":
                nouveau_plateau[0][origine_y - 1] = symbole
            elif direction == "bas":
                nouveau_plateau[4][origine_y - 1] = symbole
            elif direction == "gauche":
                nouveau_plateau[origine_x - 1][0] = symbole
            elif direction == "droite":
                nouveau_plateau[origine_x - 1][4] = symbole

            # Analyser l'état du plateau modifié
            analyse = self.analyser_le_plateau(nouveau_plateau)
            if analyse[symbole][5] > 0:
                return coup

        return None

    def trouver_un_coup_bloquant(self, symbole):
        """
        Trouve un coup bloquant pour empêcher l'adversaire de gagner.

        Arguments:
        symbole -- Symbole du joueur (X ou O).
        """
        symbole_adversaire = "X" if symbole == "O" else "O"
        coup_vainqueur_adversaire = self.trouver_un_coup_vainqueur(symbole_adversaire)

        if coup_vainqueur_adversaire:
            return coup_vainqueur_adversaire

        return None

    def jouer_un_coup(self, symbole):
        """
        Joue un coup pour le joueur spécifié (X ou O).

        Arguments:
        symbole -- Symbole du joueur (X ou O).
        """
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
        plateau_etat = self.plateau.état_plateau()
        coups_possibles = self.lister_les_coups_possibles(plateau_etat, symbole)
        if not coups_possibles:
            raise QuixoError("Aucun coup possible.")
        coup_aleatoire = random.choice(coups_possibles)
        return coup_aleatoire["origine"], coup_aleatoire["direction"]
