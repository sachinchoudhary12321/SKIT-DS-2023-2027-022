"""Data access layer.

Every repository is an abstract interface; services depend only on the
interface. TEMPORARY in-memory implementations make the API fully functional
and testable without PostgreSQL.

TODO(Database Integration task): add SQLAlchemy-backed implementations of
`PredictionRepository` / `DiseaseRepository` and swap them in `create_app()`.
No route or service changes will be needed.
"""
