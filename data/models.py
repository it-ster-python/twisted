from playhouse.postgres_ext import PostgresqlExtDatabase

db = PostgresqlExtDatabase(
    "mega_chat",
    user="chat_admin",
    host="localhost",
    port=5432,
    password="Cin>>passwd"
)


