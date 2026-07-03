from database.database import Base, engine
import database.models

def main():
    Base.metadata.create_all(bind=engine)
    print("Base de données créée avec succès !")

if __name__ == "__main__":
    main()