"""Jeu Quixo

Ce programme permet de joueur au jeu Quixo.
"""
from api import initialiser_partie, jouer_un_coup, récupérer_une_partie
from quixo import Quixo, interpréter_la_commande
from quixo_ia import QuixoIA

# Mettre ici votre secret récupérer depuis le site de PAX
SECRET = "52f01beb-dd36-4a81-8485-cbb30659c2c5"


if __name__ == "__main__":
    args = interpréter_la_commande()
    id_partie, joueurs, plateau = initialiser_partie(args.idul, SECRET)
    ia = QuixoIA()

    while True:
        # Créer une instance de Quixo
        quixo = Quixo(joueurs, plateau)
        # Afficher la partie
        print(quixo)
        # Pour l'IA
        if args.autonome:
            origine, direction = ia.déterminer_coup(plateau)
        # Demander au joueur de choisir son prochain coup
        else:
            origine, direction = quixo.choisir_un_coup()
        # Envoyez le coup au serveur
        id_partie, joueurs, plateau = jouer_un_coup(
            id_partie,
            origine,
            direction,
            args.idul,
            SECRET,
        )

        # pour afficher l'état du jeu après chaque coup :
        print(quixo)

        partie = récupérer_une_partie(id_partie)
        if partie.get('gagnant'):
            print(f"Le vainqueur est: {partie['gagnant']}")
            break
