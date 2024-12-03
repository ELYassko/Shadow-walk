import pygame
import random
import sys
import time

# Dimensions de la fenêtre de jeu
LARGEUR = 800
HAUTEUR = 600

# Couleurs
COULEUR_BOUTON = (0, 0, 128)
COULEUR_TEXTE = (255, 255, 255)
COULEUR_PERSONNAGE = (0, 255, 0)
COULEUR_ETOILE = (255, 255, 0)
COULEUR_CASE_VIDE = (50, 50, 50)
COULEUR_BOUCLIER = (50, 50, 50)
COULEUR_BOUGIE = (255, 165, 0)
COULEUR_BOMBE = (50, 50, 50)
COULEUR_PERSONNAGE_BOUGIE = (128, 207, 0)  # Mélange de COULEUR_PERSONNAGE et COULEUR_BOUGIE
COULEUR_PERSONNAGE_BOUCLIER = (0, 128, 128)  # Mélange de COULEUR_PERSONNAGE et COULEUR_BOUCLIER
COULEUR_PERSONNAGE_BOUGIE_BOUCLIER = (64, 164, 64)  # Mélange de COULEUR_PERSONNAGE, COULEUR_BOUGIE et COULEUR_BOUCLIER

# Chemins des fichiers
FICHIER_IMAGE = "chateau_hante.jpg"
FICHIER_POLICE = "Vampir.otf"
CHEMIN_MUSIQUE = "D:/L2/DEV APP/Programme/songaccueil.wav"



# Classe pour l'interface du jeu
class Interface:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  # Initialisation du module mixer de Pygame

        # Charger et jouer la musique de l'accueil
        pygame.mixer.music.load(CHEMIN_MUSIQUE)
        pygame.mixer.music.play(-1)  # Joue la musique en boucle
        pygame.mixer.music.set_volume(0.3)  # Règle le volume

        self.fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
        pygame.display.set_caption("Shadow Walk")
        self.clock = pygame.time.Clock()
        self.arriere_plan = pygame.image.load(FICHIER_IMAGE)
        self.arriere_plan = pygame.transform.scale(self.arriere_plan, (LARGEUR, HAUTEUR))
        self.police_titre = pygame.font.Font(FICHIER_POLICE, 82)
        self.police_bouton = pygame.font.Font(None, 36)

    def afficher_bouton(self, texte, position, taille):
        bouton_rect = pygame.Rect(position, taille)
        pygame.draw.rect(self.fenetre, COULEUR_BOUTON, bouton_rect)
        texte_surface = self.police_bouton.render(texte, True, COULEUR_TEXTE)
        texte_rect = texte_surface.get_rect(center=bouton_rect.center)
        self.fenetre.blit(texte_surface, texte_rect)
        return bouton_rect

    def afficher_interface(self):
        plein_ecran = False  # Ajout d'une variable de contrôle pour le plein écran
        while True:
            self.fenetre.blit(self.arriere_plan, (0, 0))
            titre = self.police_titre.render("Shadow Walk", True, COULEUR_TEXTE)
            titre_rect = titre.get_rect(center=(LARGEUR // 2, HAUTEUR // 4))
            self.fenetre.blit(titre, titre_rect)

            bouton_jouer = self.afficher_bouton("Jouer", (LARGEUR // 2 - 100, HAUTEUR // 2 - 50), (200, 50))
            bouton_quitter = self.afficher_bouton("Quitter", (LARGEUR // 2 - 100, HAUTEUR // 2 + 50), (200, 50))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()  # Arrêter la musique quand on quitte
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if bouton_jouer.collidepoint(event.pos):
                        pygame.mixer.music.stop()  # Arrêter la musique quand on joue
                        return True  # Lancer le jeu
                    elif bouton_quitter.collidepoint(event.pos):
                        pygame.mixer.music.stop()  # Arrêter la musique quand on quitte
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Basculer en plein écran
                        plein_ecran = not plein_ecran
                        if plein_ecran:
                            self.fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR), pygame.FULLSCREEN)
                        else:
                            self.fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
                    elif event.key == pygame.K_ESCAPE:  # Quitter
                        pygame.mixer.music.stop()  # Arrêter la musique quand on quitte
                        pygame.quit()
                        sys.exit()

            self.clock.tick(30)


class ShadowWalk:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.deplacements_bougie = 0  # Compteur des déplacements avec la bougie
        self.bouclier_actif = False  # Indique si le bouclier est actif
        self.bouclier_detruit = False  # Indique si le bouclier a été détruit
        self.message_actuel = ""  # Message contextuel actuel
        self.generation_map()
        self.victoires = 0
        self.defaites = 0
        self.victoires_successives = 0
        self.defaites_successives = 0

    def generer_bombes(self):
        bombes = []
        nb_bombes = self.n * self.n // 4
        while len(bombes) < nb_bombes:
            x, y = random.randint(0, self.n - 1), random.randint(0, self.n - 1)
            if (x, y) != self.etoile and (x, y) != self.personnage and (x, y) != self.bougie and (x, y) != self.bouclier and (x, y) not in bombes:
                bombes.append((x, y))
        return bombes

    def generation_map(self):
        self.n = random.randint(5, 18)  # Taille de la carte générée aléatoirement
        self.taille_case = 40
        self.map = [[0] * self.n for _ in range(self.n)]  # Carte de jeu
        self.etoile = (random.randint(0, self.n - 1), random.randint(0, self.n - 1))  # Position de l'étoile
        self.personnage = (random.randint(0, self.n - 1), random.randint(0, self.n - 1))  # Position du personnage
        self.bougie = (random.randint(0, self.n - 1), random.randint(0, self.n - 1))  # Position de la bougie
        self.bouclier = (random.randint(0, self.n - 1), random.randint(0, self.n - 1))  # Position du bouclier
        self.bouclier_initial = self.bouclier  # Stocke la position initiale du bouclier
        self.bombes = self.generer_bombes()  # Liste des bombes

        self.map[self.etoile[1]][self.etoile[0]] = 2  # Etoile
        self.map[self.bougie[1]][self.bougie[0]] = 3  # Bougie
        self.map[self.bouclier[1]][self.bouclier[0]] = 4  # Bouclier
        for bombe in self.bombes:
            self.map[bombe[1]][bombe[0]] = 1  # Bombe

        self.temps_debut = time.time()
        self.message_actuel = ""  # Réinitialiser le message contextuel

    def deplacer_personnage(self, direction):
        x, y = self.personnage
        if direction == "haut" and y > 0:
            y -= 1
        elif direction == "bas" and y < self.n - 1:
            y += 1
        elif direction == "gauche" and x > 0:
            x -= 1
        elif direction == "droite" and x < self.n - 1:
            x += 1

        # Mise à jour de la position du personnage
        if (x, y) == self.etoile:
            self.victoires += 1
            self.victoires_successives += 1
            self.defaites_successives = 0
            self.message_actuel = "Victoire"
            self.generation_map()  # Générer une nouvelle map
            return True
        elif (x, y) == self.bougie:
            self.deplacements_bougie = len(self.bombes) // 2
            self.map[self.bougie[1]][self.bougie[0]] = 0  # La case de la bougie devient vide
            self.bougie = None  # La bougie est prise
            self.message_actuel = "Une lumière a été trouvée"
        elif (x, y) == self.bouclier:
            self.bouclier_actif = True
            self.map[self.bouclier[1]][self.bouclier[0]] = 0  # La case du bouclier devient vide
            self.bouclier = None  # Le bouclier est pris
            self.message_actuel = "Protection trouvée"
        elif (x, y) in self.bombes:
            if self.bouclier_actif:
                self.bouclier_actif = False  # Le bouclier est utilisé
                self.bouclier_detruit = True  # Le bouclier est détruit
                self.bombes.remove((x, y))  # La bombe disparaît
                self.map[y][x] = 0  # La case de la bombe devient vide
                self.message_actuel = "Protection détruite"
            else:
                self.defaites += 1
                self.defaites_successives += 1
                self.victoires_successives = 0
                self.message_actuel = "Défaite"
                self.personnage = (random.randint(0, self.n - 1), random.randint(0, self.n - 1))  # Nouveau spawn
                self.bouclier = self.bouclier_initial  # Réinitialiser le bouclier à sa position initiale
                self.map[self.bouclier[1]][self.bouclier[0]] = 4  # Réinitialiser le bouclier sur la carte
                return False

        self.personnage = (x, y)
        if self.deplacements_bougie > 0:
            self.deplacements_bougie -= 1
            if self.deplacements_bougie == 0:
                self.message_actuel = "Le vent souffle fort"
        return True

    def afficher(self, fenetre):
        fenetre.fill((0,0,0))
        # Affiche la map
        for y in range(self.n):
            for x in range(self.n):
                case = self.map[y][x]
                if case == 0:
                    pygame.draw.rect(fenetre, COULEUR_CASE_VIDE, pygame.Rect(x * self.taille_case, y * self.taille_case, self.taille_case, self.taille_case))
                elif case == 1:
                    if self.deplacements_bougie > 0 and self.est_voisine((x, y)):
                        pygame.draw.rect(fenetre, (255, 0, 0), pygame.Rect(x * self.taille_case, y * self.taille_case, self.taille_case, self.taille_case))  # Bombe visible
                    else:
                        pygame.draw.rect(fenetre, COULEUR_BOMBE, pygame.Rect(x * self.taille_case, y * self.taille_case, self.taille_case, self.taille_case))  # Bombe cachée
                elif case == 2:
                    pygame.draw.rect(fenetre, COULEUR_ETOILE, pygame.Rect(x * self.taille_case, y * self.taille_case, self.taille_case, self.taille_case))  # Etoile
                elif case == 3:
                    pygame.draw.rect(fenetre, COULEUR_BOUGIE, pygame.Rect(x * self.taille_case, y * self.taille_case, self.taille_case, self.taille_case))  # Bougie
                elif case == 4:
                    if self.deplacements_bougie > 0:
                        pygame.draw.rect(fenetre, (0, 0, 255), pygame.Rect(x * self.taille_case, y * self.taille_case, self.taille_case, self.taille_case))  # Bouclier visible
                    else:
                        pygame.draw.rect(fenetre, COULEUR_BOUCLIER, pygame.Rect(x * self.taille_case, y * self.taille_case, self.taille_case, self.taille_case))  # Bouclier caché

        # Déterminer la couleur du personnage en fonction des items
        if self.bouclier_actif and self.deplacements_bougie > 0:
            couleur_personnage = COULEUR_PERSONNAGE_BOUGIE_BOUCLIER
        elif self.bouclier_actif:
            couleur_personnage = COULEUR_PERSONNAGE_BOUCLIER
        elif self.deplacements_bougie > 0:
            couleur_personnage = COULEUR_PERSONNAGE_BOUGIE
        else:
            couleur_personnage = COULEUR_PERSONNAGE

        pygame.draw.rect(fenetre, couleur_personnage, pygame.Rect(self.personnage[0] * self.taille_case, self.personnage[1] * self.taille_case, self.taille_case, self.taille_case))  # Personnage

    def est_voisine(self, position):
        px, py = self.personnage
        x, y = position
        return abs(px - x) <= 1 and abs(py - y) <= 1

    def afficher_scores(self, fenetre):
        police = pygame.font.Font(None, 36)
        temps_ecoule = time.time() - self.temps_debut
        scores = [
            f"Victoires: {self.victoires}",
            f"Défaites: {self.defaites}",
            f"Victoires successives: {self.victoires_successives}",
            f"Défaites successives: {self.defaites_successives}",
            f"Temps écoulé: {temps_ecoule:.2f}s",
            f"Nombre de bombes: {len(self.bombes)}",
            f"Bouclier: {'à trouver' if not self.bouclier_actif and not self.bouclier_detruit else 'équipé' if self.bouclier_actif else 'détruit'}",
            f"Bougie: {'allumée' if self.deplacements_bougie == 0 else 'éteinte'}"
        ]
        y_offset = 50
        for score in scores:
            texte_surface = police.render(score, True, COULEUR_TEXTE)
            fenetre.blit(texte_surface, (LARGEUR - 75, y_offset))
            y_offset += 40

        # Afficher le message contextuel
        if self.message_actuel:
            message_surface = police.render(self.message_actuel, True, COULEUR_TEXTE)
            fenetre.blit(message_surface, (LARGEUR - 75, y_offset))

if __name__ == "__main__":
    pygame.init()
    interface = Interface()
    if interface.afficher_interface():
        jeu = ShadowWalk()
        fenetre = pygame.display.set_mode((jeu.n * jeu.taille_case, jeu.n * jeu.taille_case))
        fullScreen = False
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if not jeu.deplacer_personnage("haut"):
                            print("Perdu !")
                    elif event.key == pygame.K_DOWN:
                        if not jeu.deplacer_personnage("bas"):
                            print("Perdu !")
                    elif event.key == pygame.K_LEFT:
                        if not jeu.deplacer_personnage("gauche"):
                            print("Perdu !")
                    elif event.key == pygame.K_RIGHT:
                        if not jeu.deplacer_personnage("droite"):
                            print("Perdu !")
                    elif event.key == pygame.K_RETURN:  # Basculer en plein écran
                        fenetre = pygame.display.set_mode((LARGEUR + 200, HAUTEUR), pygame.FULLSCREEN) if fullScreen else pygame.display.set_mode((jeu.n * jeu.taille_case, jeu.n * jeu.taille_case))
                        fullScreen = not fullScreen
                    elif event.key == pygame.K_ESCAPE:  # Quitter
                        pygame.quit()
                        sys.exit()

            jeu.afficher(fenetre)
            if pygame.display.is_fullscreen():
                jeu.afficher_scores(fenetre)
            pygame.display.flip()
            jeu.clock.tick(30)
