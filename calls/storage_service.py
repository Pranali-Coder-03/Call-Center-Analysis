import os
import uuid

from supabase import create_client


supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)


BUCKET_NAME = "call-recordings"


def upload_recording(file):

    extension = os.path.splitext(
        file.name
    )[1].lower()

    file_name = f"{uuid.uuid4().hex}{extension}"

    storage_path = f"calls/{file_name}"

    content_type = file.content_type

    if not content_type:
        content_type = "application/octet-stream"

    file_bytes = file.read()

    if len(file_bytes) == 0:
        raise Exception(
            "Uploaded file is empty."
        )

    supabase.storage.from_(
        BUCKET_NAME
    ).upload(
        storage_path,
        file_bytes,
        {
            "content-type": content_type,
            "upsert": "false",
        }
    )

    return storage_path


def get_public_url(file_name):

    return supabase.storage.from_(
        BUCKET_NAME
    ).get_public_url(
        file_name
    )


def delete_recording_file(file_path):

    if not file_path:
        return False

    print("==============================")
    print("DELETE DEBUG")
    print("Bucket:", BUCKET_NAME)
    print("File path:", file_path)
    print("==============================")

    result = supabase.storage.from_(
        BUCKET_NAME
    ).remove([
        file_path
    ])

    print("Supabase delete result:", result)

    return result