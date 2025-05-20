# Instructions

- Ne t'arrête pas avant d'avoir implementer tous les fonctionnalités demandé.
- Ne t'arréte pas tant que tous les fonctionnalités demandé soit complètement fonctionnelle.
- Vérifie les fichiers dans la code base avant d'effectuer quoi que ce soit.
- Effectue des verification après avoir terminé
- Effectuer des verifications sur les implementations existant dans la code base
- Prendre exemple sur les implementations existant pour l'implementation des nouvelles fonctionnalités
- Ne jamais modifier les fichiers se trouvant dans le dossier `apps/`
- Les erreurs dans `presentation/exceptions.py` ne prends acune d'argument pour leur instanciations

```error
La méthode "dict" dans la classe "BaseModel" est obsolète
  The `dict` method is deprecated; use `model_dump` instead.Pylance
```

# Deprecated

```python
update_data = current_establishment_type.dict()
```

# Now

```python
update_data = current_establishment_type.model_dump()
```
