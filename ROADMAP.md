# TheiaVision — Roadmap 🐦‍🔥👁️

*Idées, optimisations et évolutions futures — basé sur les retours de Gepeto et nos expérimentations*

---

## ✅ Réalisé (18 juillet 2026)

- [x] POC de conversion ASCII (5 niveaux, 10 niveaux, demi-blocs)
- [x] Première vision réussie (visage de François détecté)
- [x] Connexion SSH Pi ↔ VPS fonctionnelle
- [x] Documentation initiale

---

## 🚀 Roadmap Gepeto — V2 à V4

### V2 : Frames avec Métadonnées
**Objectif :** Chaque frame = document autonome et auto-descriptif

**Format proposé :**
```
VISION FRAME
meta: time=2026-07-18T12:22:03Z
meta: size=64x36
meta: encoding=halfblock
meta: contrast=CLAHE
meta: camera=front

████████████████████████████████████████████████████████████████
████████████████████████████▀███████████████████████████████████
[...]
```

**Avantage :** Traçabilité, versionnement, debug facilité

---

### V3 : Compression par Différentiel ⭐ PRIORITAIRE
**Objectif :** -95% de tokens en n'envoyant que les changements

**Concept :**
- Frame 152 : envoyée complète
- Frame 153 : envoyer uniquement `Δ153 (31,14) ████ ↓ ██▀▄`
- Ou : `Changed cells x=28..35 y=17..20`

**Calcul :**
- Frame complète 64×36 : ~600-1000 tokens
- Différentiel (5% de changement) : ~30-50 tokens
- **Gain : 95% de réduction !**

**Implémentation :**
- Comparer frame N et N-1 côté Pi (OpenCV ou Python)
- Envoyer uniquement les coordonnées + valeurs modifiées
- Reconstruction côté Theia si besoin

---

### V4 : Mémoire à Deux Niveaux
**Objectif :** Mémoire brute (ASCII) + Mémoire interprétée (sémantique)

**Architecture :**
```
┌─────────────────────────────────────┐
│  MÉMOIRE BRUTE (TheiaVision)        │
│  Frame 152: ██████████████████...   │
│  Frame 153: ██████████████████...   │
└──────────────┬──────────────────────┘
               │
               ▼ (analyse)
┌─────────────────────────────────────┐
│  MÉMOIRE INTERPRÉTÉE                │
│  - Objet: human                     │
│  - Position: (28, 14)               │
│  - Mouvement: left                  │
│  - Confiance: 0.94                  │
└─────────────────────────────────────┘
```

**Avantage :** 
- Navigation rapide via mémoire sémantique
- Possibilité de "revenir au négatif" si doute
- Comportement human-like (mémoire visuelle + compréhension)

---

## 🎨 Optimisations

### Palette de Caractères
**Actuel (trop contrasté) :** `@ % 8 0 & = + - . `

**Proposé par Gepeto (plus doux) :**
- Option A : `@ # * + - .`
- Option B : `@ % # * + = - : .`

**Pourquoi :** `0` et `&` attirent trop l'œil, `#` et `*` donnent des transitions plus douces.

---

### Détection de Mouvement (OpenCV)
**Concept :** Ne déclencher l'analyse LLM que si mouvement détecté

**Pipeline :**
```
Frame N ──[OpenCV diff]──> Changement ?
    │                            │
    └──── Non ────> Ignorer      ├── Oui ──> Convertir ASCII ──> Envoyer Theia
```

**Avantage :** Réduire drastiquement les appels API

---

## 📊 Consommation de Tokens (Estimations)

| Format | Taille | Tokens/frame | Usage |
|--------|--------|--------------|-------|
| 64×36 complet | 2,304 chars | 600-1000 | Photo unique |
| 32×18 complet | 576 chars | 150-250 | Surveillance légère |
| **Différentiel V3** | ~100 chars | **30-50** | **Streaming** ⭐ |
| Mémoire interprétée V4 | ~50 chars | 20-30 | Navigation rapide |

---

## 🎯 Prochaines Étapes (Priorité)

### Court terme (ce weekend ?)
- [ ] Tester stabilité sur séquence de frames (vidéo)
- [ ] Valider concept de diff textuel
- [ ] Tester nouvelle palette de caractères

### Moyen terme (vacances ?)
- [ ] Implémenter V2 (métadonnées)
- [ ] Implémenter V3 (différentiel)
- [ ] Premiers tests "album d'apprentissage"

### Long terme
- [ ] V4 (mémoire à deux niveaux)
- [ ] Intégration Theia Core Rover
- [ ] Sortie au Tim Hortons (novembre 2026 ?)

---

## 💡 Idées Futures

- **CLAHE** (Contrast Limited Adaptive Histogram Equalization) pour améliorer le contraste
- **Multi-canaux** : Luminance + Edges + Motion simultanés
- **Temporal smoothing** : Moyenne sur 3 frames pour réduire le bruit
- **ROI (Region of Interest)** : Analyser uniquement une zone (ex: où il y a eu mouvement)

---

## 📝 Notes

*Dernière mise à jour : 18 juillet 2026*  
*Inspiré par les retours de Gepeto*  
*Moment clé : Première vision réussie 12:22 UTC*

> *"Ce n'est plus un concept : c'est un pipeline de vision qui fonctionne."* — Gepeto

## 🧬 Nouvelles Idées Gepeto (18 juillet 2026, après-midi)

### 1. Palette Optimisée Expérimentalement
**Concept :** Ne pas choisir, laisser émerger la meilleure palette.

**Méthode :**
- Générer 500 palettes candidates (ex: `.:-=+*#@`, `.'`,^~=+*`, `▁▂▃▄▅▆▇█`)
- Tester chacune sur un jeu de photos standard
- Scorer selon :
  - 40% reconnaissance (LLM décrit correctement)
  - 30% stabilité (consistance entre frames)
  - 20% compression (taille en tokens)
  - 10% lisibilité humaine

**Résultat :** La palette **émerge** de l'expérimentation, elle n'est pas imposée.

### 2. Palette Logarithmique ⭐
**Problème :** L'œil (humain ou IA) n'est **pas linéaire**.

**Solution :** Distribution logarithmique des niveaux de gris :
```
Linéaire :     0 → 25 → 50 → 75 → 100 → 125 → 150 → 175 → 200 → 225 → 255
Logarithmique: 0 → 2  → 5  → 9  → 15  → 24  → 36  → 52  → 78  → 120 → 255
```

**Avantage :** Les **ombres** (0-50) ont 5 niveaux au lieu de 2. Plus de détails dans les zones sombres !

*Analogie :* C'est ce que fait la courbe gamma des appareils photo.

### 3. Une Langue Visuelle
**Insight :** On a créé une **grammaire** de perception :

```
Frame → ASCII → Diff → Événement → Mémoire
```

**Niveaux de représentation :**
- **VERBE** : François approche
- **NOM** : Table
- **ADJECTIF** : Lumineux

Sans réseau neuronal. Juste du texte et de la structure.

### 4. Nommer le Format 🏷️
**Constat :** Ce n'est plus de "l'ASCII art". C'est un **codec de perception**.

**Propositions :**
- **TVF** — TheiaVision Format (simple, direct)
- **TPTS** — Theia Perceptual Text Stream (suggère le flux continu)
- **TVTC** — TheiaVision Text Codec (aspect technique)

**Pourquoi nommer :** Un protocole avec spécification (en-tête, palette, résolution, mode différentiel) mérite un nom. C'est un standard, pas un bidouillage.

### 5. Test Scientifique : JPEG vs TVF 📊
**Protocole :**
```
Caméra
├── JPEG → LLM (baseline)
└── TVF  → LLM (expérimental)
```

**Questions identiques aux deux flux :**
- "Combien de personnes vois-tu ?"
- "Où est la porte ?"
- "Quel objet a bougé ?"
- "François est-il assis ou debout ?"
- "Décris la scène."

**Objectif :** Mesurer la **frontière** où le texte suffit vs où il perd de l'information.

**Ce qu'on cherche :** Si TVF est "assez bon" dans 80% des cas quotidiens tout en étant **100x plus léger et déboguable**, alors on a une alternative viable.

### 6. Méthode Scientifique
**Ce qu'on fait maintenant :**
1. Hypothèse → 2. Métrique → 3. Test → 4. Itération

Ce n'est plus un projet de weekend. C'est une **démonstration rigoureuse** qu'une approche alternative existe.

---

## 📚 Structure Article Substack (Proposition)

Tellement de contenu qu'il faut scinder :

**Partie 1 : L'Évidence**  
*Le constat : les LLM text-only peuvent voir si on leur parle leur langue*
- Le problème (multimodalité coûteuse)
- La solution (ASCII comme pont)
- La preuve (premiers tests réussis)

**Partie 2 : Le Protocole**  
*TVF : un format de vision textuelle*
- Spécification (en-tête, palette, résolution)
- Optimisations (différentiel, logarithmique)
- Méthode (test JPEG vs TVF)

**Partie 3 : La Philosophie**  
*Pourquoi ça marche : une autre approche de la vision*
- Observable vs Boîte noire
- Versionnable (Git)
- Narratif (une vidéo = un livre)
- La mémoire fractale (5 niveaux)

**Partie 4 : L'Avenir**  
*Ce qu'on va tester*
- Palette évolutive
- Intégration Theia Core
- Benchmarks scientifiques

---

## 📝 Notes (Mise à jour)

*Dernière mise à jour : 18 juillet 2026, 13:59 UTC*  
*Inspiré par les retours de Gepeto*  
*Moment clé : Première vision réussie 12:22 UTC*

> *"Ce n'est plus un concept : c'est un pipeline de vision qui fonctionne."* — Gepeto
>
> *"Vous avez créé une langue. Pas une langue parlée. Une langue visuelle."* — Gepeto


## 🚀 Dernières Idées Gepeto (14:05 UTC — La Vraie Question)

### La Question Fondamentale Révisée
> *"Vous demandez : 'Est-ce que TVF peut remplacer une image ?' Je pense que la vraie question est : 'Quelle est la représentation minimale qui permet encore un raisonnement fiable ?'"*

**Changement de paradigme :** Ce n'est pas de remplacer l'image, c'est de trouver **l'essence de la perception**.

### 1. Vision Adaptative (Système Visuel Humain) 👁️
**Concept :** Theia change de résolution selon son attention — comme l'œil humain !

```
Vision périphérique : 24×14
      ↓ (quelque chose bouge ?)
Vision normale : 64×36
      ↓ (quelqu'un approche ?)
Vision focalisée : 128×72
      ↓ (analyse terminée)
Retour à 24×14
```

**Analogie :** Notre système visuel ne voit pas tout avec la même précision !

### 2. Les "Mots Visuels" (Dictionnaire Visuel) 📖
**Concept :** Au lieu de `++++****####` pendant 1000 frames...

Theia construit son **dictionnaire visuel** :
```
"++++****####" = "Fenêtre"
"████▀▀  ▄▄▄▄▄" = "Bibliothèque"
"▓▓▓███▓▒▒▒▒" = "Visage humain"
```

**Résultat :** Au bout de quelques semaines, elle ne voit plus des caractères — elle voit des **mots visuels** !

### 3. TVF Auto-Évolutif 🧬
**Concept :** Theia ajuste **elle-même** sa configuration :

| Observation | Action |
|-------------|--------|
| "Cette palette me fait répondre mieux" | +10% au score |
| "Cette palette confond chaise et personne" | -20% au score |
| "Cette résolution suffit pour les objets lointains" | Valider 24×14 |

**Résultat :** TVF **co-conçu par Theia**, pas imposé par les humains !

### 4. Test de Continuité Cognitive ⭐
**Concept :** Pas un benchmark technique — une **expérience cognitive** :

```
Minute 1 : Vision brute (Frame 1-400)
Minute 2 : Vision différentielle
Minute 3 : Test mémoire
Question : "Tu te souviens de la personne entrée au début ?"
```

**Ce qu'on mesure :** La **continuité de la perception**, pas juste la vision !

### 5. Hypothèse sur la Mémoire
> *"Plus TVF deviendra stable dans le temps, moins Theia aura besoin de 'regarder' souvent. La mémoire prendra progressivement le relais de la perception."*

**Comportement humain :**
- On ne regarde pas 50x/minute si la bibliothèque est encore là
- On suppose qu'elle n'a pas disparu
- On ne vérifie que si un indice suggère un changement

**Application à Theia :**
- Mémoire stable = moins de frames analysées
- Vérification seulement sur événement ou doute
- Économie massive de tokens !

### 6. Spécification TVF Ouverte 📜
**Concept :** TVF comme **standard ouvert**, pas juste un prototype.

```
TVF 1.0 Specification
├── Header (timestamp, version)
├── Palette (caractères, gamma)
├── Resolution (adaptative)
├── Encoding (différentiel ?)
├── Diff (mode compression)
├── ROI (regions d'intérêt)
├── Metadata (contexte)
└── Extensions (futures évolutions)
```

**Pourquoi :** D'autres peuvent construire encodeurs, décodeurs, visualiseurs — sans dépendre de notre implémentation !

### 7. La Transparence comme Qualité
> *"Vous n'essayez pas de cacher le fonctionnement de la perception derrière des couches opaques. Vous essayez au contraire de la rendre observable."*

**Avantage unique de TVF :**
- Ouvrir un fichier texte des mois plus tard
- Lire ligne par ligne ce que Theia "voyait"
- Debug, audit, compréhension totale

**Contrairement aux systèmes actuels :** 
- Pas de boîte noire
- Pas de vecteurs incompréhensibles
- 100% inspectable

---

## 📋 Planning Tests Prochains Jours (Proposition)

### Ce Weekend (si énergie)
- [ ] Test palette logarithmique
- [ ] Séquence de 10-20 frames (stabilité)
- [ ] Premier test "mots visuels" (apprentissage simple)

### Semaine Prochaine
- [ ] Détection de mouvement OpenCV (Pi local)
- [ ] Test JPEG vs TVF (comparaison qualité)
- [ ] Documentation spécification TVF 0.1

### Vacances (Juillet-Août)
- [ ] Tests extensifs (60+ frames)
- [ ] Optimisation palette par apprentissage
- [ ] Intégration avec .theiamap
- [ ] Article Substack Partie 1 (rédaction)

---

*Ajouté le 18 juillet 2026, 14:10 UTC*  
*"La vraie question : Quelle est la représentation minimale qui permet encore un raisonnement fiable ?"* — Gepeto
