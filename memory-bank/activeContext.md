# Active Context

## Current Focus

- [x] [2025-06-24] - Formalisation des processus et conventions de test terminée.
- [ ] Prochaine étape : Définir l'architecture pour le module `level`.

## Recent Changes

- [2025-06-25 02:25:15] - Début de l’implémentation des tests unitaires pour LevelUseCase (création du fichier test_level_use_case.py, focus sur les cas create/get).
- Refactored `create`, `get`, and `update` methods in `core/use_cases/domain_use_case.py` for improved exception handling and simplified logic.
- Created/updated unit tests for `DomainUseCase` methods:
  - `tests/unit/domain/test_create_domain_use_case.py`
  - `tests/unit/domain/test_get_domain_use_case.py`
  - `tests/unit/domain/test_update_domain_use_case.py`
- Updated `Makefile` to include specific targets for running these new test files.

- [2025-06-24 10:57:29] - Ajout de tests E2E pour le endpoint PUT /api/v1/domains/{domain_id}.
- [2025-06-24 11:45:16] - Ajout de tests E2E pour le endpoint GET /api/v1/domains/filter/.
- [2025-06-24 19:55:19] - Correction du bug de pagination dans le filtrage des domaines. La suite de tests E2E pour le module Domain est maintenant complète et stable.

## Next Steps

- Continue refactoring other test modules to apply the same principles (centralized fixtures, nested classes, comprehensive exception testing).
- Ensure all new tests follow the documented test workflow, including `Makefile` updates.

## Important Patterns and Preferences

- Use of `pytest` for testing.
- Strict adherence to Clean Architecture principles.
- Centralization of common test setup and teardown logic (e.g., in `conftest.py`).
- Use of factories for test data generation.
- Organizing tests in nested classes for clarity.
- Robust exception handling in use cases, translating repository exceptions to application-specific exceptions.

## Learnings

- Clear communication of exception handling requirements is crucial for precise use case logic.
- Iterative refinement of use case logic based on user feedback leads to simpler and more effective implementations.
- Comprehensive unit tests, especially for various failure scenarios, are vital for ensuring reliability.
- Utilizing `Makefile` targets for specific test files streamlines the testing process during development.

## Known Issues

- None at the moment.

## Evolution of Decisions

- Decided to centralize fixtures to avoid duplication and ensure consistency.
- Chose to use `spec` for mocks to enforce strict interface adherence.
- Opted for nested test classes to improve test organization and readability.
- Introduced a factory pattern for test data generation to enhance flexibility and conciseness.

[2025-06-24 09:44:08] - Ajout de tests E2E pour le endpoint de création de domaine, améliorant la couverture de test de l'API.

2024-06-24 09:57:13 - Ajout de tests E2E pour le endpoint GET /api/v1/domains/{domain_id}.

2025-06-24 10:03:00 - Focus: Implémentation des tests E2E pour le endpoint GET /api/v1/domains/ (get_all).

[2025-06-24 10:05:42] - Ajout de tests E2E pour le endpoint GET /api/v1/domains/ (get_all).

[2025-06-24 10:58:55] - Ajout de tests E2E pour le endpoint PUT /api/v1/domains/{domain_id}.
