# """Use this script to migrate your Agno tables from v1 to v2

# - Automatically reads configuration from app.agent
# - Creates backups before migration
# - Run the script: uv run python scripts/agnoMigration.py
# """

# import sys
# from pathlib import Path
# from dotenv import load_dotenv
# # load_dotenv('D:\story-flow\test-2\story-flow\backend\.env')
# load_dotenv('D:\\story-flow\\test-2\\story-flow\\backend\\.env')

# # Add backend directory to path to import app modules
# backend_dir = Path(__file__).parent.parent
# sys.path.insert(0, str(backend_dir))

# from agno.db.migrations.v1_to_v2 import migrate
# from agno.db.postgres.postgres import PostgresDb
# from agno.utils.log import log_info


# # --- Configuration from agent.py ---

# # Get database URL from settings
# # db_url = "postgresql://postgres.dvqlgbbvxxredfbtlvpv:qULL0ySEHrpY6IuQ@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
# # db_url = "postgresql://postgres.hihuhuxpgcsecmruczco:iV9YOlfdzsFaF6s7@aws-0-ap-south-1.pooler.supabase.com:6543/postgres?"
# db_url = "postgresql://postgres.hihuhuxpgcsecmruczco:iV9YOlfdzsFaF6s7@aws-0-ap-south-1.pooler.supabase.com:6543/postgres?"
# print(db_url)
# # Convertyes// if needed for Agno v2


# # V1 table names from agent.py
# v1_tables_schema = "public"  # Schema from agent.py
# v1_agent_sessions_table_name = "agent_sessions"  
# v1_team_sessions_table_name = ""  # Not used in this project
# v1_workflow_sessions_table_name = ""  # Not used in this project
# v1_memories_table_name = ""  


# v2_sessions_table_name = "agent_sessions_v2"  
# v2_memories_table_name = ""  

# # Migration batch size (adjust based on available memory and table size)
# migration_batch_size = 1000

# # --- Set your database connection ---

# log_info(f"Connecting to database: {db_url.split('@')[1] if '@' in db_url else 'hidden'}")
# log_info(f"V1 Tables - Schema: {v1_tables_schema}, Agent Sessions: {v1_agent_sessions_table_name}, Memories: {v1_memories_table_name}")
# log_info(f"V2 Tables - Sessions: {v2_sessions_table_name}, Memories: {v2_memories_table_name}")

# db = PostgresDb(  # type: ignore
#     db_url=db_url,
#     session_table=v2_sessions_table_name, 
#     memory_table=v2_memories_table_name ,
# )

# # For MySQL:
# #
# # from agno.db.mysql.mysql import MySQLDb
# # db = MySQLDb(
# #     db_url=db_url,
# #     session_table=v2_sessions_table_name,
# #     memory_table=v2_memories_table_name,
# # )


# # For SQLite:
# #
# # from agno.db.sqlite.sqlite import SqliteDb
# # db = SqliteDb(
# #     db_file=sqlite_db_file,
# #     session_table=v2_sessions_table_name,
# #     memory_table=v2_memories_table_name,
# # )


# # For MongoDB:
# #
# # from agno.db.mongo.mongo import MongoDb
# # db = MongoDb(db_url=db_url)
# # or
# # db = MongoDb(
# #     host=mongo_host,
# #     port=mongo_port,
# #     db_name=mongo_db_name,
# #     session_collection=v2_sessions_table_name,
# #     memory_collection=v2_memories_table_name,
# # )


# #  --- Exit if no tables are provided ---

# if (
#     not v1_agent_sessions_table_name
#     and not v1_team_sessions_table_name
#     and not v1_workflow_sessions_table_name
#     and not v1_memories_table_name
# ):
#     log_info(
#         "No tables provided, nothing can be migrated. Update the variables in the migration script to point to the tables you want to migrate."
#     )
#     exit()

# # --- Pre-migration warnings ---

# log_info("=" * 60)
# log_info("⚠️  IMPORTANT: Make sure you have created backup tables!")
# log_info("   Run these SQL commands before migration:")
# log_info(f"   CREATE TABLE agent_sessions_backup AS SELECT * FROM {v1_agent_sessions_table_name};")
# log_info(f"   CREATE TABLE agno_memories_backup AS SELECT * FROM {v1_memories_table_name};")
# log_info("=" * 60)

# # Ask for confirmation (optional - comment out for automated runs)
# response = input("\nHave you created backup tables? (yes/no): ")
# if response.lower() != "yes":
#     log_info("Migration cancelled. Please create backup tables first.")
#     exit()

# # --- Run the migration ---

# log_info("Starting migration...")
# try:
#     migrate(
#         db=db,
#         v1_db_schema=v1_tables_schema,
#         agent_sessions_table_name=v1_agent_sessions_table_name,
#         team_sessions_table_name=v1_team_sessions_table_name,
#         workflow_sessions_table_name=v1_workflow_sessions_table_name,
#         memories_table_name=v1_memories_table_name,
#         batch_size=migration_batch_size,
#     )
#     log_info("✅ Migration completed successfully!")
# except Exception as e:
#     log_info(f"❌ Migration failed: {e}")
#     log_info("You can restore from backup tables if needed.")
#     raise