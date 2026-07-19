# import os
# from dotenv import load_dotenv
# from langgraph.checkpoint.postgres import PostgresSaver

# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")

# print(f"DEBUG: DATABASE_URL is: {DATABASE_URL}")

# if DATABASE_URL is None:
#     raise ValueError("DATABASE_URL is not set. Check your .env file or environment variables.")

# with PostgresSaver.from_conn_string(DATABASE_URL) as checkpointer:
#     checkpointer.setup()
#     print("Checkpoint tables created")


import os

import requests
