from peewee import PostgresqlDatabase, Model
from env import DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class PostgresSQLPeeweeConnection(metaclass=Singleton):
    def __init__(self):
        self.db = self.getConnection()

    def getConnection(self):
        print ('creating connection to database...')
        return PostgresqlDatabase(
            DATABASE_NAME,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            host=DATABASE_HOST,
            port=DATABASE_PORT
        )

    def closeConnection(self):
        self.db.close()

    def createTables(self, models):
        self.db.connect()
        self.db.create_tables(models)
        self.db.close()


class BaseModel(Model):
    class Meta:
        postgresSQL = PostgresSQLPeeweeConnection()
        database = postgresSQL.db
