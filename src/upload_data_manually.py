import os
from utils.create_vectordb import CreateVectordb
from utils.Config import LoadConfig

config = LoadConfig()


def upload_data_manually() ->None:

    vectordb_instance = CreateVectordb(
    data_folder = config.data_directory,
    persist_folder = config.persist_directory,
    embedding_engine = config.embedding_model,
    chunk_size = config.chunk_size,
    chunk_overlap = config.chunk_overlap
    )

    if not len(os.listdir(config.persist_directory)) != 0:
        vectordb_instance.prepare_and_save_vectordb()
    else:
        print(f"VectorDB already exists in {config.persist_directory}")
    
    return None

if __name__ == "__main__":
    upload_data_manually()

    