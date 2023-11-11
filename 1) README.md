# Projet Cue-Locks - Traitement de Signal

Ce projet vise à développer un système de traitement de signal pour évaluer et comparer des plaques, en se basant sur des critères tels que les dimensions, les défauts, la couleur et l'orientation. Le but est de déterminer si une plaque est conforme à une plaque de référence ou si elle présente des non-conformités.

## Déroulement des tests

Les tests se déroulent en deux étapes principales :

1. **Évaluation de la plaque de référence :** Dans cette étape, une photo de la plaque de référence est utilisée comme base de comparaison. Les critères suivants sont évalués :

   - Dimensions
   - Défauts
   - Couleur
   - Orientation
2. **Évaluation d'une deuxième plaque :** Une deuxième plaque est évaluée en se basant sur les mêmes critères que la plaque de référence. La plaque est considérée valide si et seulement si tous les critères sont validés. Si l'une ou plusieurs de ces critères ne sont pas remplis, la plaque est jugée invalide. Une liste des critères non validés est générée pour indiquer la raison de l'invalidité.

L'objectif ultime de ce projet est de fournir une solution robuste pour l'évaluation des plaques et d'automatiser ce processus de manière efficace. Pour plus d'informations sur l'utilisation de ce système et son intégration dans votre application, veuillez consulter la documentation associée.

N'hésitez pas à contribuer au projet en ouvrant des issues, en proposant des améliorations ou en soumettant des pull requests. Votre participation est grandement appréciée.




## Première entrevue avec les profs:

### Pistes

* inverser la binarisation de l'image afin d'avoir les défauts en blanc + labelisation pour les trous (voir dans le cours théorique)
* dilatation et érosion
* augmenter le contraste pour augmenter la qualité
* songer à peut être boucher les petits trous pour les plaques brunes afin de déterminer si la plaque a des défauts ou pas

### Travail à faire

1) [ ] Plutôt que de faire un filtre gaussien pour avoir une image plus nette on doit pouvoir augmenter le contraste
2) [ ] finaliser la plate_size
3) [ ] finaliser la plate_orientation
4) [ ] finaliser le plate_color
5) [ ] finaliser la plate_holes
6) [ ] finaliser la gui
7) [ ] La gui doit effectuer les différents test et afficher les résultats
