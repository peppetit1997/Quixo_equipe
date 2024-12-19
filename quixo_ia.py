from quixo import Quixo
from quixo_error import QuixoError
import random

class QuixoIA(Quixo):
    def __init__(self, joueurs):
        super().__init__(joueurs)


    def lister_les_coups_possibles(self, plateau, cube):
        """Liste tous les coups possibles pour le joueur.

        Args:
            plateau (list[list[str]]): Le plateau de jeu sous forme de grille 5x5.
            cube (str): Le symbole du joueur ('X' ou 'O').

        Returns:
            list[dict]: Une liste de dictionnaires représentant les coups possibles.
        """
        # Créer la liste des coups possibles
        Coups_possibles = []
    
        # Créer une liste pour les coordonnées disponibles sur les bords
        Coordonnees_disponibles = []

        # Parcourir les bords pour trouver les cubes jouables
        for x in range(4):
            for y in range(4):
                # Vérifier si la case est sur un bord
                if x in [1, 5] or y in [1, 5]:
                    # Ajouter la case si elle est vide ou contient le symbole du joueur
                    if plateau[x][y] == "" or plateau[x][y] == cube:
                        Coordonnees_disponibles.append((x, y))

        # Générer les coups possibles pour chaque coordonnée disponible
        for (x, y) in Coordonnees_disponibles:
            # Vérifier les directions possibles selon la position
            if x > 0:  # Peut aller vers le haut
                Coups_possibles.append({"origine": [x, y], "direction": "haut"})
            if x < 5:  # Peut aller vers le bas
                Coups_possibles.append({"origine": [x, y], "direction": "bas"})
            if y > 0:  # Peut aller à gauche
                Coups_possibles.append({"origine": [x, y], "direction": "gauche"})
            if y < 5:  # Peut aller à droite
                Coups_possibles.append({"origine": [x, y], "direction": "droite"})

        return Coups_possibles

        
    def analyser_le_plateau(plateau):
        """Analyse l'état actuel du plateau, incluant lignes, colonnes et diagonales."""
        resultats = {
            "X": {2: 0, 3: 0, 4: 0},
            "O": {2: 0, 3: 0, 4: 0}
        }

        # Analyse des lignes
        for x in range(4):
            compteur_x = 0
            compteur_o = 0
            for y in range(4):
                if plateau[x][y] == "x":
                    compteur_x += 1
                    compteur_o = 0
                elif plateau[x][y] == "O":
                    compteur_o += 1
                    compteur_x = 0
                else:
                    compteur_x = 0
                    compteur_o = 0
                if 2 <= compteur_x <= 4:
                    resultats["X"][compteur_x] += 1
                if 2 <= compteur_o <= 4:
                    resultats["O"][compteur_o] += 1

        # Analyse des colonnes
        for y in range(4):
            compteur_x = 0
            compteur_o = 0
            for x in range(4):
                if plateau[x][y] == "x":
                    compteur_x += 1
                    compteur_o = 0
                elif plateau[x][y] == "O":
                    compteur_o += 1
                    compteur_x = 0
                else:
                    compteur_x = 0
                    compteur_o = 0
                if 2 <= compteur_x <= 4:
                    resultats["X"][compteur_x] += 1
                if 2 <= compteur_o <= 4:
                    resultats["O"][compteur_o] += 1

        # Analyse des diagonales principales
        compteur_x = 0
        compteur_o = 0
        for i in range(4):
            if plateau[i][i] == "x":
                compteur_x += 1
                compteur_o = 0
            elif plateau[i][i] == "O":
                compteur_o += 1
                compteur_x = 0
            else:
                compteur_x = 0
                compteur_o = 0
            if 2 <= compteur_x <= 4:
                resultats["X"][compteur_x] += 1
            if 2 <= compteur_o <= 4:
                resultats["O"][compteur_o] += 1

        # Analyse des diagonales secondaires
        compteur_x = 0
        compteur_o = 0
        for i in range(4):
            if plateau[i][3 - i] == "x":
                compteur_x += 1
                compteur_o = 0
            elif plateau[i][3 - i] == "O":
                compteur_o += 1
                compteur_x = 0
            else:
                compteur_x = 0
                compteur_o = 0
            if 2 <= compteur_x <= 4:
                resultats["X"][compteur_x] += 1
            if 2 <= compteur_o <= 4:
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
        """Trouve un coup gagnant pour le joueur donné.

        Args:
            symbole (str): Le symbole du joueur ('X' ou 'O').

        Returns:
            dict | None: Un dictionnaire représentant un coup gagnant ou None si aucun coup gagnant n'est possible.
        """
        # Obtenir les coups possibles
        coups_possibles = self.lister_les_coups_possibles(self.plateau, symbole)

        for coup in coups_possibles:
            # Créer une copie du plateau pour simuler le coup
            nouveau_plateau = [row[:] for row in self.plateau]
            origine_x, origine_y = coup["origine"]
            direction = coup["direction"]

            # Simuler le déplacement
            nouveau_plateau[origine_x][origine_y] = ""
            if direction == "haut":
                nouveau_plateau[0][origine_y] = symbole
            elif direction == "bas":
                nouveau_plateau[4][origine_y] = symbole
            elif direction == "gauche":
                nouveau_plateau[origine_x][0] = symbole
            elif direction == "droite":
                nouveau_plateau[origine_x][4] = symbole

            # Vérifier si le coup permet de compléter une ligne de 5
            analyse = self.analyser_le_plateau(nouveau_plateau)
            if analyse[symbole][5] > 0:  # Une ligne de 5 est formée
                return coup  # Retourner immédiatement le coup gagnant

        return None  # Aucun coup gagnant trouvé

    def trouver_un_coup_bloquant(self, symbole):
        """Trouve un coup bloquant pour empêcher l'adversaire de gagner.

        Args:
            symbole (str): Le symbole du joueur ('X' ou 'O').

        Returns:
            dict | None: Un dictionnaire représentant un coup bloquant ou None si aucun coup bloquant n'est possible.
        """
        # Identifier le symbole de l'adversaire
        symbole_adversaire = "X" if symbole == "O" else "O"

        # Rechercher un coup vainqueur pour l'adversaire
        coup_vainqueur_adversaire = self.trouver_un_coup_vainqueur(symbole_adversaire)

        # Si un coup vainqueur existe pour l'adversaire, agir pour le bloquer
        if coup_vainqueur_adversaire:
            return coup_vainqueur_adversaire

        # Sinon, aucun coup bloquant n'est nécessaire
        return None

class QuixoIA(Quixo):
    def __init__(self, joueurs, plateau=None):
        super().__init__(joueurs, plateau)

    def jouer_un_coup(self, symbole):
        """Joue un coup valide pour le joueur donné.

        Args:
            symbole (str): Le symbole du joueur ('X' ou 'O').

        Returns:
            dict: Le coup joué sous la forme {"origine": [x, y], "direction": direction}.

        Raises:
            QuixoError: Si la partie est terminée ou si le symbole est invalide.
        """
        # Vérifier si la partie est terminée
        if self.plateau.vérifier_gagnant() is not None:
            raise QuixoError("La partie est déjà terminée.")

        # Vérifier si le symbole est valide
        if symbole not in ["X", "O"]:
            raise QuixoError('Le symbole doit être "X" ou "O".')

        # Chercher un coup vainqueur
        coup_vainqueur = self.trouver_un_coup_vainqueur(symbole)
        if coup_vainqueur:
            self.déplacer_pion(symbole, coup_vainqueur["origine"], coup_vainqueur["direction"])
            return coup_vainqueur

        # Chercher un coup bloquant
        coup_bloquant = self.trouver_un_coup_bloquant(symbole)
        if coup_bloquant:
            self.déplacer_pion(symbole, coup_bloquant["origine"], coup_bloquant["direction"])
            return coup_bloquant

        # Liste des coups possibles
        coups_possibles = self.lister_les_coups_possibles(self.plateau.état_plateau(), symbole)

        # Choisir un coup aléatoire parmi les coups possibles
        coup_aleatoire = random.choice(coups_possibles)
        self.déplacer_pion(symbole, coup_aleatoire["origine"], coup_aleatoire["direction"])
        return coup_aleatoire