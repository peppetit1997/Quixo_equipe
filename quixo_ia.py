from quixo import Quixo
from quixo_error import QuixoError

class QuixoIA(Quixo):
    def __init__(self):
        super().__init__()

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
# ajout d'une méthode
    def déterminer_coup(self, plateau):
        """Détermine le coup à jouer pour l'IA.
        
        Args:
            plateau (list[list[str]]): Le plateau de jeu sous forme de grille 5x5
            
        Returns:
            tuple: Tuple de 2 éléments composé de l'origine du bloc à déplacer et de sa direction.
        
        """

        cube = "X"
        coups_possibles = self.lister_les_coups_possibles(plateau, cube)

        if coups_possibles:
            coup = coups_possibles[0]
            return coup["origine"], coup["direction"]
        else:
            raise QuixoError("Aucun coup possible.")

    def partie_terminée(self):
        """Détermine si la partie est terminée et retourne le résultat."""
        if self.resultats["X"][5] != 0:
            return self.joueurs[0]
        if self.resultats["O"][5] != 0:
            return self.joueurs[1]
        else:
            return None

    def trouver_un_coup_vainqueur(self, symbole):
        """Trouve un coup permettant de gagner la partie."""
        pass

    def trouver_un_coup_bloquant(self):
        """Trouve un coup permettant de bloquer l'adversaire."""
        pass

    def jouer_un_coup(self):
        """Joue un coup en fonction de la stratégie."""
        pass
