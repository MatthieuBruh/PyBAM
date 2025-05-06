# ⚖️ Projet – Aider les individus à comprendre les conditions d'admission et d'équivalences de l'UNIL

![_J4SKcBjtzpkuJL3-3NJq](https://github.com/user-attachments/assets/25d5ba23-51d8-41c0-b486-2470da3e8552)

## Objectif du projet

Notre projet vise à **automatiser l’évaluation** des **conditions d’admission** aux études de droit de l’Université de Lausanne (**UNIL**) et l’**accès aux professions juridiques** dans le canton de Vaud, notamment :
- **L’examen du barreau vaudois**
- **L'accès à la proffession de notaire**

Ces processus sont longs et fastidieux, et nécessite par conséquence une interprétation manuelle.  
Nous avons conçu une **solution informatique** en Python pour **rationaliser ce processus**, le rendre **plus accessible** pour les candidats.

---

## Impact attendu

- **Pour les candidats** : Gain de temps, meilleure compréhension de leur situation juridique, autonomie accrue.
- **Pour l'administration** : Réduction du travail de filtrage manuel, standardisation des décisions.
- **Pour l'institution (UNIL)** : Meilleure accessibilité aux services, image innovante.

---

## Approche choisie

Nous avons combiné :
- **Méthodologie juridique** : cartographie précise des conditions légales (LPAv, LNo, RLNo, etc.).
- **Méthodologie d'automatisation** : développement d’une **application Python** guidée par des arbres de décision (`barreau_vaudois.json` et `notaire_vaudois.json`).
- **Visualisation interactive** : utilisation de **Pyvis** pour représenter les parcours de décision sous forme de graphes.

-> Cette approche facilite **la navigation utilisateur** et permet une **automatisation partielle de la décision**.

---

## Fonctionnement de la solution

La solution est construite autour de **3 composants principaux** :

1. **Arbres de décision** (format JSON)
   - `barreau_vaudois.json` : Pour l’admission au barreau.
   - `notaire_vaudois.json` : Pour l’obtention de la patente de notaire.

2. **Code Python** (modules)
   - `tree.py` : Gestion de l’arbre de décision (nœuds questions/réponses).
   - `questions.py` : Module de dialogue pour guider l’utilisateur à travers les questions.
   - `category.py` : Organisation thématique (Barreau vs Notariat).
   - `main.py` : Lancement de l’application.

3. **Visualisation**
   - Affichage interactif du chemin parcouru grâce à **Pyvis** (`.html` généré).

---

## Comment utiliser le projet

### Prérequis

- Python 3.9 ou supérieur
- Installation des dépendances :

```bash
pip install -r requirements.txt
```

### Lancer le projet
```bash
python main.py
```

- L’utilisateur est invité à choisir s’il souhaite **évaluer son admissibilité au barreau** ou **obtenir la patente de notaire**.

- Un **parcours dynamique** commence selon ses réponses.

- À la fin, un **graphique interactif** (`result.html`) est généré pour visualiser son **chemin décisionnel**.

## Architecture du projet
```bash
├── main.py                  # Script principal
├── tree.py                  # Gestionnaire d'arbres de décision
├── questions.py             # Interaction utilisateur
├── category.py              # Gestion des catégories d'admission
├── barreau_vaudois.json     # Arbre décisionnel pour le barreau
├── notaire_vaudois.json     # Arbre décisionnel pour les notaires
├── requirements.txt         # Dépendances Python
```
---
## Tests utilisateurs
Nous avons mené plusieurs tests de parcours simulés :
- Des étudiants de la classe ont testé leur propre éligibilité aux deux solutions.
- La navigation intuitive a été validée.
---
## Améliorations futures 
- Développer une interface Web avec un hébergement dédié.
- Ajouter des liens pour guider les utilisateurs vers les démarches administratives.
---
## 🚨 Limites du projet

Malgré son efficacité, notre solution présente quelques limites :
- **Limites d’interprétation** : Certains cas spécifiques nécessitent toujours une appréciation humaine.
- **Évolution légale** : La solution nécessite des mises à jour régulières des arbres décisionnels.
- **Interface minimaliste** : Une interface utilisateur web améliorerait l’accessibilité.
- **Tests restreints** : Nos tests utilisateurs n’ont concerné qu’un échantillon réduit.
- **Multilinguisme non prévu** : La solution est uniquement disponible en français, ce qui limite l'accès aux étudiants internationaux.

---

## Crédits

Projet réalisé dans le cadre du cours d'Enjeux juridiques à l'ère numérique, Université de Lausanne.

**Équipe projet PyBAM:**
- Louni Merk
- Matthieu Brühwiler
- Bayan Alouan

© 2025 – Groupe PyBAM

