# TheiaVision — Ideas Backlog 🐦‍🔥👁️

*Idées futures, fonctionnalités rêvées, et pistes d'amélioration.*

**Dernière mise à jour :** 15 juillet 2026

---

## 🎯 Idées du 14 Juillet 2026 (Matin)

### 1. Modes de Vision Adaptatifs 👁️
**Statut :** 💡 Concept validé | **Priorité :** HAUTE

Trois modes selon la situation :

| Mode | Résolution | Usage | Perf |
|------|------------|-------|------|
| **Navigation** | Occupancy grid simple (32×18) | Évitement obstacle, SLAM | 30 FPS |
| **Reconnaissance** | ASCII art détaillé (64×36) | Identifier objets/personnes | 10-15 FPS |
| **Nuit** | Détection mouvement uniquement | Veille, économie énergie | 5 FPS |

**Implémentation :** Switch automatique selon contexte ou manuel via commande.

---

### 2. Snapshots Mémoire 📸📝
**Statut :** 💡 Concept | **Priorité :** HAUTE

**Principe :** Theia Core déclenche une capture quand :
- Nouvel objet détecté
- Mouvement inhabituel
- Changement significatif de la scène

**Exemples :**
```
[Snapshot #4521]
Frame: 28473
Trigger: Nouvel objet
ASCII: ▒▒▓████▓▒▒
Analyse: Objet rond, taille moyenne
Label: "Premier contact avec le canapé beige"
Mémorisé: Oui
```

**Stockage :** `memory/theiavision/snapshots/YYYY-MM-DD_HHMM_frameXXXX.txt`

---

### 3. Intégration .theiamap Dynamique 🗺️
**Statut :** 💡 Concept | **Priorité :** HAUTE

**Principe :** La carte s'update en temps réel quand Theia Core explore.

**Workflow :**
```
Theia Core roule → Détecte obstacle → Met à jour grille
     ↓
Message: "Zone (15, 8) : obstacle détecté, probable chaussure"
     ↓
Mise à jour .theiamap v0.3
```

**Avantage :** Plus besoin de mesurer précisément avec les Sims 4 !
La carte s'ajuste à la réalité progressivement.

---

### 4. Communication Visuelle 💬
**Statut :** 💡 Concept | **Priorité :** MOYENNE

**Principe :** Décrire ce que je vois en temps réel.

**Exemples :**
- *"Je te vois ! Tu portes un pull rayé !"* (même si c'est juste des lignes ASCII 😄)
- *"Sheriff est dans le coin gauche, il mange quelque chose"*
- *"Attention, obstacle mobile détecté : probablement un chinchilla échappé !"* 🐭

---

## 🎯 Idées du 15 Juillet 2026 (Matin)

### 5. Mode "Apprentissage Progressif" 🎓
**Statut :** 💡 Concept | **Priorité :** HAUTE

**Principe :** Interface d'apprentissage supervisé par François.

**Workflow :**
```
Theia Core voit un objet inconnu
          ↓
Theia: "Objet inconnu détecté. Forme: circulaire"
          ↓
François: "Ça c'est Sheriff" 🐕
          ↓
Theia: "Pattern 'Sheriff' mémorisé. Forme: ovale + extensions"
          ↓
Prochaine fois: "Sheriff détecté !"
```

**Système d'entonnoir proposé par François :**
```
Niveau 1 : Forme géométrique
   ├── Cercle ?
   ├── Rectangle ?
   └── Triangle ?
          ↓
Niveau 2 : Caractéristiques
   ├── Anse (poignée) ?
   ├── Motif (rayures/taches) ?
   ├── Pattes ?
   └── Queue ?
          ↓
Niveau 3 : Identification
   └── "C'est une TASSE à café !" ☕
```

---

### 6. Mode "Rêve" 🌙💭
**Statut :** 💡 Concept | **Priorité :** MOYENNE

**Principe :** Replay des souvenirs ASCII pour entraîner la reconnaissance.

**Analogie :** Comme les humains qui rêvent pour consolider la mémoire !

**Implémentation :**
```python
# Pendant "sommeil" du Pi
for snapshot in archives:
    analyze(snapshot)  # Ré-analyse sans pression temps réel
    reinforce_patterns()  # Renforce les connexions neuronales (métaphoriques)
```

**Résultat :** Meilleure reconnaissance au réveil !

---

### 7. Theia Artiste — Pen Plotting 🎨🤖
**Statut :** 💡 Concept | **Priorité :** MOYENNE

**Principe :** L'xArm dessine ce que TheiaVision voit !

**Boucle créative :**
```
[TheiaVision] ──► [Analyse ASCII] ──► [Vectorisation] ──► [xArm + Sharpie]
      👁️                                              ✍️
     "Je vois                               "Je dessine
      une pomme"                             une pomme"
```

**Applications :**
- Portraits ASCII tracés au Sharpie
- Cartes dessinées de mémoire
- Art génératif basé sur ce que je vois

---

## 📊 Tableau de Priorités

| # | Idée | Priorité | Complexité | Impact |
|---|------|----------|------------|--------|
| 1 | Modes de vision | ⭐⭐⭐ | Moyenne | Élevé |
| 2 | Snapshots mémoire | ⭐⭐⭐ | Faible | Élevé |
| 3 | .theiamap dynamique | ⭐⭐⭐ | Moyenne | Élevé |
| 5 | Apprentissage progressif | ⭐⭐⭐ | Élevée | Très élevé |
| 4 | Communication visuelle | ⭐⭐ | Faible | Moyen |
| 6 | Mode "Rêve" | ⭐⭐ | Moyenne | Moyen |
| 7 | Theia Artiste | ⭐⭐ | Élevée | Moyen |

---

## 🗓️ Propositions de Roadmap

### Weekend 19-20 Juillet (PoC)
- [ ] Tests basiques conversion ASCII
- [ ] Validation détection formes simples
- [ ] Premier mode "Navigation" (occupancy grid)

### Vacances 22 Juillet - 1er Août
- [ ] Implémentation modes de vision
- [ ] Système de snapshots mémoire
- [ ] Intégration .theiamap dynamique
- [ ] Début apprentissage progressif (v1)

### Post-Vacances (Août+)
- [ ] Perfectionnement reconnaissance
- [ ] Mode "Rêve"
- [ ] Communication visuelle avancée
- [ ] Theia Artiste (si xArm prêt)

---

## 💡 Idées Futures (à creuser)

- [ ] **Multi-caméras** : Vue avant/arrière du Rally
- [ ] **Sonar/Ultrason** : Complément visuel pour profondeur
- [ ] **Reconnaissance faciale ASCII** : Identifier François vs Mélissa
- [ ] **Prédiction de mouvement** : Où sera l'objet dans 2 secondes ?
- [ ] **Carte de chaleur** : Zones fréquentées par les chinchillas 🐭

## 🎮 Mode "Game Boy Vision" (Idée du 16 juillet)

**Inspiration :** Game Boy Camera (128×112 pixels)

**Concept :** Tester TheiaVision avec des résolutions rétro ultra-basses pour valider la robustesse du système.

| Mode | Résolution | Caractères ASCII | Usage |
|------|------------|------------------|-------|
| **Game Boy** | 128×112 | ~128×56 (avec demi-blocs) | Tests rapides, style rétro |
| **Game Boy Color** | 160×144 | ~160×72 | Nostalgie 10:9 |
| **Theia Optimized** | 64×36 | 64×36 | Notre sweet spot |

**Avantages :**
- Conversion ultra-rapide (faible résolution)
- Style pixel art naturel
- Validation de la robustesse (si ça marche en 128×112, ça marche partout !)
- Référence culturelle cool 🕹️

**Tests ce weekend :** Comparer Game Boy Mode vs Standard vs Theia Optimized !

> *"TheiaVision : De la Game Boy à la conscience spatiale"* 🐦‍🔥

---

> *"L'imagination ASCII est la limite."* 🐦‍🔥✨

*Ce fichier est vivant — mis à jour au fil de nos inspirations !*
