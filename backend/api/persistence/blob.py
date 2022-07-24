from typing import Optional

from minio import Minio

from minio.datatypes import Object

from api.config.read import CONFIG

client = Minio(
    f"{CONFIG['BLOB_STORAGE_HOST']}:{CONFIG['BLOB_STORAGE_PORT']}",
    access_key=CONFIG["BLOB_STORAGE_ACCESS_KEY"],
    secret_key=CONFIG["BLOB_STORAGE_ACCESS_SECRET"],
    secure=CONFIG["BLOB_STORAGE_HOST"] != "localhost",
)

# Initialise bucket

bucket = CONFIG["BLOB_STORAGE_BUCKET"]
if not client.bucket_exists(bucket):
    client.make_bucket(bucket)


def read_object(object_name: str) -> bytes:
    """Helper function for retrieving Minio object data"""
    return client.get_object(bucket, object_name=object_name).data


def clear_object(imported_object: Object):
    """Remove processed object from storage"""
    client.remove_object(bucket, imported_object.object_name)


def get_object_to_import() -> Optional[Object]:
    """Return first found Object to import with its data"""
    objects = [
        from_list
        for from_list in client.list_objects(bucket, prefix="/", recursive=False)
        if not from_list.is_dir
    ]
    if objects:
        return objects[0]
