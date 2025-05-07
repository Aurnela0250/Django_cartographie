# Instruction

## Model base instructions

- Base toi sur #file:models.py
- Crée un model `XXX-name` qui aura comme proprieté :
  - `name` : str
  - `address` : str
  - `code_postal` : int
  - `ville` : str
  - `contacts` : list[str]
  - `site_url` : str
  - `description` : Optional[str]
  - `coordonnee_gps` : ??

## Model relations

- `Establishment` one to one #file:models.py (`EstablishmentType`)
