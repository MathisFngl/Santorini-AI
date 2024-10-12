from Game.Player import Joueur
from Game.Pion import Pion
from Game.Board import tableau_de_jeu, PlayerList

Joueur_1 = Joueur("Antoine", "Rebelle")
Joueur_2 = Joueur("Alexis", "Raiponse")
PlayerList.append(Joueur_1)
PlayerList.append(Joueur_2)

Joueur_1.pion1.build(0, 1)

Joueur_2.movementHandler()

print()
for li in tableau_de_jeu:
    print(li)
