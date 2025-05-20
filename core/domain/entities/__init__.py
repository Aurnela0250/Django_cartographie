from .establishment_entity import EstablishmentEntity
from .formation_entity import FormationEntity

# On reconstruit les modèles ici, une fois que tout est importé
FormationEntity.model_rebuild()
EstablishmentEntity.model_rebuild()
