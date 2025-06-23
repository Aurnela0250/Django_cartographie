# Patch Tortoise ORM AVANT toute importation
import sys
from unittest.mock import MagicMock

# Ce patch doit s'exécuter AVANT l'import des use cases
if "tortoise.transactions" not in sys.modules:
    mock_transactions = MagicMock()
    mock_transactions.atomic = (
        lambda *args, **kwargs: lambda func: func
    )  # No-op decorator
    sys.modules["tortoise.transactions"] = mock_transactions
