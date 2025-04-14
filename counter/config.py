import os
from pathlib import Path

# Try to load .env file if it exists
try:
    from dotenv import load_dotenv
    env_path = Path('.') / '.env'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        print("Loaded environment variables from .env file")
except ImportError:
    pass

from counter.adapters.count_repo import CountMongoDBRepo, CountInMemoryRepo, CountMongoDBAtlasRepo
from counter.adapters.object_detector import TFSObjectDetector, FakeObjectDetector
from counter.domain.actions import CountDetectedObjects


def dev_count_action() -> CountDetectedObjects:
    return CountDetectedObjects(FakeObjectDetector(), CountInMemoryRepo())


def prod_count_action() -> CountDetectedObjects:
    tfs_host = os.environ.get('TFS_HOST', 'localhost')
    tfs_port = os.environ.get('TFS_PORT', 8501)
    mongo_host = os.environ.get('MONGO_HOST', 'localhost')
    mongo_port = os.environ.get('MONGO_PORT', 27017)
    mongo_db = os.environ.get('MONGO_DB', 'prod_counter')
    return CountDetectedObjects(TFSObjectDetector(tfs_host, tfs_port, 'rfcn'),
                                CountMongoDBRepo(host=mongo_host, port=mongo_port, database=mongo_db))


def atlas_count_action() -> CountDetectedObjects:
    tfs_host = os.environ.get('TFS_HOST', 'localhost')
    tfs_port = os.environ.get('TFS_PORT', 8501)
    mongo_connection_string = os.environ.get('MONGO_CONNECTION_STRING')
    mongo_db = os.environ.get('MONGO_DB', 'object_counter')

    if not mongo_connection_string:
        raise ValueError("MONGO_CONNECTION_STRING environment variable must be set for Atlas connection")

    return CountDetectedObjects(TFSObjectDetector(tfs_host, tfs_port, 'rfcn'),
                                CountMongoDBAtlasRepo(connection_string=mongo_connection_string, database=mongo_db))


def get_count_action() -> CountDetectedObjects:
    env = os.environ.get('ENV', 'dev')
    count_action_fn = f"{env}_count_action"
    return globals()[count_action_fn]()
