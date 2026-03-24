try:
    from app.database.db_session import engine  # type: ignore
    from app.database.models import Base  # type: ignore

    def create_all():
        Base.metadata.create_all(bind=engine)
        print("Created tables")

except Exception as e:
    engine = None
    Base = None
    def create_all():
        print("SQLAlchemy not available or failed to import; skipping table creation.")


if __name__ == '__main__':
    create_all()
