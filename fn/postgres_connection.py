from sqlalchemy import create_engine
import config

def postgres_connect(
    user: str = config.DB_USER,
    password: str = config.DB_PASSWORD,
    host: str = config.DB_HOST, 
    port: int = config.DB_PORT,
    database: str = config.DB_NAME
) -> tuple:

    engine = create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    )
    connection = engine.connect()
    
    print("\nConnected to Postgres.\n")
    return engine, connection


def postgres_disconnect(engine, connection) -> None:
    
    connection.close()
    engine.dispose()
    
    print("\nDisconnected to Postgres.\n")