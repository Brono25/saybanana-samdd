import tempfile
from SBFirebase.interface import SBFirebaseInterface
from samdd.method import SAMDDMethod
from environment import BUCKET_PATH, CREDENTIALS, WORKSPACE_VOLUME


samdd = SAMDDMethod()
sbfirebase = SBFirebaseInterface(BUCKET_PATH, CREDENTIALS)


def construct_firebase_target(uid, filename):
    target = f"{uid}/Daily_Audio_Assessment/{filename.split('.')[0]}.json"
    return target


def process_audio_batch(uid, audio_batch):
    try:
        with tempfile.TemporaryDirectory(dir=WORKSPACE_VOLUME) as target:
            audio_files = sbfirebase.download_and_extract_audio_batch_to_target(
                audio_batch=audio_batch, target=target
            )

            for audio_file in audio_files:
                prompt = audio_file.split("/")[1]  # The prompt is the parent dir name
                full_path = f"{target}/{audio_file}"
                SBFirebase_target = construct_firebase_target(uid, audio_file)
                # result = samdd(prompt=prompt, audio_input=full_path)
                # sbfirebase.upload_report_to_SBFirebase_as_json(
                #    content=result, firebase_target=SBFirebase_target
                # )
    except IndexError:
        print("Index error: ", audio_batch)


def main():
    try:
        unprocessed_audio_batches = sbfirebase.database.find_unprocessed_audio_batches()
        print(sbfirebase)
        for uid, audio_batches in unprocessed_audio_batches.items():
            for audio_batch in audio_batches:
                print(audio_batch)
                process_audio_batch(uid, audio_batch)
    finally:
        sbfirebase.refresh_database()


def inspect():
    print("\n" * 5)
    print(sbfirebase.database)
    print("\n" * 5)
    [print(x.split("/")) for x in sbfirebase.get_SBFirebase_contents_list()]


def delete():
    sbfirebase._delete_all_audio_assessments_from_firebase()
    sbfirebase.refresh_database()


def analyse():
    unprocessed_audio_batches = sbfirebase.database.find_unprocessed_audio_batches()
    [print(k, "\n\t", v[0]) for k, v in unprocessed_audio_batches.items()]


if __name__ == "__main__":
    # main()
    # sb_test_main()

    inspect()
    # delete()
    # analyse()
