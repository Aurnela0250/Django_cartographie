# Journal des décisions

---

### [2025-06-24] - Adoption des conventions de test standardisées

**Décision** : Adopter un ensemble de conventions de test pour l'ensemble du projet.

**Justification** : Garantir la cohérence, la lisibilité et la maintenabilité des tests. La standardisation facilite l'intégration des nouveaux développeurs et simplifie l'exécution des tests.

**Implications** :

- Tous les nouveaux tests doivent suivre la structure **Arrange/Act/Assert**.
- Les cas de test doivent être regroupés dans des classes imbriquées `TestSuccess` et `TestFailures`.
- Les fixtures Pytest doivent être définies dans des fichiers `conftest.py` locaux pour maintenir l'encapsulation.
- L'exécution des tests est centralisée via des commandes `Makefile` (`make test`, `make test-unit`, etc.).
