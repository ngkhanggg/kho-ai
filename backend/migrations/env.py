from alembic import context

from app import models
from app.db import make_engine

metadata = models.Base.metadata

if context.is_offline_mode():
    import os

    context.configure(
        url=os.environ["DATABASE_URL"], target_metadata=metadata, literal_binds=True
    )
    with context.begin_transaction():
        context.run_migrations()
else:
    engine = make_engine()
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=metadata)
        with context.begin_transaction():
            context.run_migrations()
    engine.dispose()
