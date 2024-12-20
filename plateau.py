"""Module Plateau

Classes:
    * Plateau - Classe principale du plateau de jeu Quixo.
"""

from copy import deepcopy

from quixo_error import QuixoError


class Plateau:
    """Classe principale du plateau de jeu Quixo. 
    
    Cette classe gère les opérations sur le plateau de jeu, 
    
    y compris l'insertion et le déplacement des cubes. 
    """

    def __init__(self, plateau=None):
        """Constructeur de la classe Plateau

        Vous ne devez rien modifier dans cette méthode.

        Args:
            plateau (list[list[str]], optional): La représentation du plateau
                tel que retourné par le serveur de jeu ou la valeur None par défaut.
        """
        self.plateau = self.générer_le_plateau(deepcopy(plateau))

    def état_plateau(self):
        """Retourne une copie du plateau

        Retourne une copie du plateau pour éviter les effets de bord.
        Vous ne devez rien modifier dans cette méthode.

        Returns:
            list[list[str]]: La représentation du plateau
            tel que retourné par le serveur de jeu.
        """
        return deepcopy(self.plateau)

    def __str__(self):
        """Retourne une représentation en chaîne de caractères du plateau

        Déplacer le code de votre fonction formater_plateau ici et ajuster le en conséquence.

        Returns:
            str: Une représentation en chaîne de caractères du plateau.
        """
        plateau_formate = "   -------------------\n"
        for index, ligne in enumerate(self.plateau):
            plateau_formate += f"{index + 1} |"
            for cell in ligne:
                if cell == "X":
                    plateau_formate += " X |"
                elif cell == "O":
                    plateau_formate += " O |"
                else:
                    plateau_formate += "   |"
            if index + 1 < len(self.plateau):
                plateau_formate += "\n  |---|---|---|---|---|\n"
        plateau_formate += "\n--|---|---|---|---|---|\n"
        plateau_formate += "  | 1   2   3   4   5 |\n"
        return plateau_formate


    def __getitem__(self, position):
        """Retourne la valeur à la position donnée

        Args:
            position (tuple[int, int]): La position (x, y) du cube sur le plateau.

        Returns:
            str: La valeur à la position donnée, soit "X", "O" ou " ".

        Raises:
            QuixoError: Les positions x et y doivent être entre 1 et 5 inclusivement.
        """
        x, y = position
        if not (1 <= x <= 5 and 1 <= y <= 5):
            raise QuixoError("Les positions x et y doivent être entre 1 et 5 inclusivement.")

        return self.plateau[x-1][y-1]


    def __setitem__(self, position, valeur):
        """Modifie la valeur à la position donnée

        Args:
            position (tuple[int, int]): La position (x, y) du cube sur le plateau.
            value (str): La valeur à insérer à la position donnée, soit "X", "O" ou " ".

        Raises:
            QuixoError: Les positions x et y doivent être entre 1 et 5 inclusivement.
            QuixoError: Valeur du cube invalide.
        """
        x, y = position
        if not (1 <= x <= 5 and 1 <= y <= 5):
            raise QuixoError("Les positions x et y doivent être entre 1 et 5 inclusivement.")
        if valeur not in["X", "O", " "]:
            raise QuixoError("Valeur du cube invalide.")

        self.plateau[x-1][y-1] = valeur


    def générer_le_plateau(self, plateau):
        """Génère un plateau de jeu

        Si un plateau est fourni, il est retourné tel quel.
        Sinon, si la valeur est None, un plateau vide de 5x5 est retourné.

        Args:
            plateau (list[list[str]] | None): La représentation du plateau
                tel que retourné par le serveur de jeu ou la valeur None.

        Returns:
            list[list[str]]: La représentation du plateau
                tel que retourné par le serveur de jeu.

        Raises:
            QuixoError: Format du plateau invalide.
            QuixoError: Valeur du cube invalide.
        """
        if plateau is None:
            return [["" for _ in range(5)] for _ in range(5)]
        if len(plateau) != 5:
            raise QuixoError("Format du plateau invalide.")
        for ligne in plateau:
            if len(ligne) != 5:
                raise QuixoError("Format du plateau invalide.")
            for cube in ligne:
                if cube not in ["X", "O", " "]:
                    raise QuixoError("Valeur du cube invalide.")
        return plateau


    def insérer_un_cube(self, cube, origine, direction):
        """Insère un cube dans le plateau

        Cette méthode appelle la méthode d'insertion appropriée selon la direction donnée.

        À noter que la validation des positions sont faites dans
        les méthodes __setitem__ et __getitem__. Vous devez donc en faire usage dans
        les diverses méthodes d'insertion pour vous assurez que les positions sont valides.

        Args:
            cube (str): La valeur du cube à insérer, soit "X" ou "O".
            origine (list[int]): La position [x, y] d'origine du cube à insérer.
            direction (str): La direction de l'insertion, soit "haut", "bas", "gauche" ou "droite".

        Raises:
            QuixoError: La direction doit être "haut", "bas", "gauche" ou "droite".
            QuixoError: Le cube à insérer ne peut pas être vide.
        """
        if direction not in ["haut", "bas", "gauche", "droite"]:
            raise QuixoError("La direction doit être 'haut', 'bas', 'gauche' ou 'droite'.")
        if cube not in ["X", "O"]:
            raise QuixoError("Le cube à insérer ne peut pas être vide.")
        
# modification
# validation de l'insertion du cube

        self.validation(origine, direction)

        if direction == "haut":
            self.insérer_par_le_haut(cube, origine)
        elif direction == "bas":
            self.insérer_par_le_bas(cube, origine)
        elif direction == "gauche":
            self.insérer_par_la_gauche(cube, origine)
        elif direction == "droite":
            self.insérer_par_la_droite(cube, origine)


    def insérer_par_le_bas(self, cube, origine):
        """Insère un cube dans le plateau en direction du bas

        Args:
            cube (str): La valeur du cube à insérer, soit "X" ou "O".
            origine (list[int]): La position [x, y] d'origine du cube à insérer.
        """
# appel de la methode de validation à chaque fonction insérer 
        if not ((y == 1 and x in [1, 2, 3, 4, 5]) or (y in [2, 3, 4] and x in [1, 5])):
           raise QuixoError("Le cube ne peut pas être inséré dans cette direction.")
        self.validation(origine, "bas")
        x, y = origine
        for i in range(4, 0, -1):
            self[(x, i+1)] = self[(x, i)]
        self[(x, 1)] = cube



    def insérer_par_le_haut(self, cube, origine):
        """Insère un cube dans le plateau en direction du haut

        Args:
            cube (str): La valeur du cube à insérer, soit "X" ou "O".
            origine (list[int]): La position [x, y] d'origine du cube à insérer.
        """
# appel de la methode de validation à chaque fonction insérer 
        if not ((y == 5 and x in [1, 2, 3, 4, 5]) or (y in [2, 3, 4] and x in [1, 5])):
            raise QuixoError("Le cube ne peut pas être inséré dans cette direction.")
        self.validation(origine, "haut")
        x, y = origine
        for i in range(1, 5):
            self[(x, i)] = self[(x, i+1)]
        self[(x, 5)] = cube


    def insérer_par_la_gauche(self, cube, origine):
        """Insère un cube dans le plateau en direction de la gauche

        Args:
            cube (str): La valeur du cube à insérer, soit "X" ou "O".
            origine (list[int]): La position [x, y] d'origine du cube à insérer.
        """
# appel de la methode de validation à chaque fonction insérer 
        if not ((x == 5 and y in [1, 2, 3, 4, 5]) or (x in [2, 3, 4] and y in [1, 5])):
            raise QuixoError("Le cube ne peut pas être inséré dans cette direction.")
        self.validation(origine, "gauche")
        x, y = origine
        for i in range(1, 5):
            self[(i, y)] = self[i+1, y]
        self[(5, y)] = cube


    def insérer_par_la_droite(self, cube, origine):
        """Insère un cube dans le plateau en direction de la droite

        Args:
            cube (str): La valeur du cube à insérer, soit "X" ou "O".
            origine (list[int]): La position [x, y] d'origine du cube à insérer.
        """
# appel de la methode de validation à chaque fonction insérer
        if not ((x == 1 and y in [1, 2, 3, 4, 5]) or (x in [2, 3, 4] and y in [1, 5])):
            raise QuixoError("Le cube ne peut pas être inséré dans cette direction.")
        self.validation(origine, "droite")
        x, y = origine
        for i in range(4, 0, -1):
            self[(i+1, y)] = self[(i, y)]
        self[(1, y)] = cube


    def validation(self, origine, direction):
        x, y = origine
        if (
            (direction == "haut" and x == 1) or 
            (direction == "bas" and x == 5) or
            (direction == "gauche" and y == 1) or 
            (direction == "droite" and y == 5)
        ):
            raise QuixoError("Le cube ne peut pas être inséré dans cette direction depuis la position choisie.")


# concernant notre main ! Je travaille a la comprehension du parse !
# Ce soir peut etre je finirai !
# pour le main voici mon idee :

"""
import argparse

et dans le main rajouter les lignes de code tels que :

parser = argprse.ArgumentParser(description='Jeu de Quixo')
parser.add_argument('idul', type=str, help='IDUL du joueur')
action=('store_true', help='Jouer de facon autonome')
args = parser.parse_args()"""

#Je l'ai pas rajouter au main parce qu'il y a encore des choses que je comprends pas.
# Aussi je continue a travailler dessus et tu me dis ce que tu en penses.
