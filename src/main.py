import tempfile
from SBFirebase.interface import SBFirebaseInterface
from environment import BUCKET_PATH, CREDENTIALS, WORKSPACE_VOLUME
from utils import cleanup
from SBFirebase.utilities import init_logging, logging
import os
from samdd.method import SAMDDMethod
import shutil


init_logging()
samdd = SAMDDMethod()
sbfirebase = SBFirebaseInterface(BUCKET_PATH, CREDENTIALS)


def download_and_extract_audio_batch_zip(audio_batch_zip, local_volume):
    kwargs = {"audio_batch": audio_batch_zip, "target": local_volume}
    extracted_audio_files = sbfirebase.download_and_extract_audio_batch_to_target(
        **kwargs
    )
    audio_full_path_list = (
        []
    )  # exclude system files which may have snuck in to the zip file.
    for file in extracted_audio_files:
        if file.startswith("_") or file.startswith(".") or not file.endswith(".wav"):
            continue
        audio_full_path_list.append(os.path.join(local_volume, file))
    return audio_full_path_list


def process_audio_save_reports(audio_files):

    for audio_file in audio_files:
        path, filename = os.path.split(audio_file)
        filename_nosuffix = filename.removesuffix(".wav")
        audio_dir, prompt = os.path.split(path)
        report_dir = audio_dir + "_REPORT"  # tmp name to avoid clash
        prompt_subdir = os.path.join(report_dir, prompt)
        os.makedirs(prompt_subdir, exist_ok=True)

        report = samdd(prompt=prompt, audio_input=audio_file)
        output_path = os.path.join(prompt_subdir, filename_nosuffix + ".json")
        report.write_to_json_file(os.path.join(prompt_subdir, output_path))
    return report_dir, audio_dir


def prepare_output_dir_before_zipping(report_dir, audio_dir):
    # Make the output dir the same name as the original audio dir
    os.rename(audio_dir, audio_dir + "DISCARD")
    os.rename(report_dir, audio_dir)
    report_dir = audio_dir
    return report_dir

def create_firebae_upload_path(uid, report_dir):
    final_report_name = os.path.basename(report_dir + ".zip")
    firebase_upload_path = os.path.join(uid, "Daily_Audio_Assessment", final_report_name)
    return firebase_upload_path


def process_audio_batch_pipeline(uid, audio_batch_zip):
    kwargs = {"dir": WORKSPACE_VOLUME, "prefix": "SAMDD_"}
    with tempfile.TemporaryDirectory(**kwargs) as local_volume:

        kwargs = {"audio_batch_zip": audio_batch_zip, "local_volume": local_volume}
        audio_files = download_and_extract_audio_batch_zip(**kwargs)
        report_dir, audio_dir = process_audio_save_reports(audio_files)
        final_report_dir = prepare_output_dir_before_zipping(report_dir, audio_dir)
        zipped_file = shutil.make_archive(final_report_dir, "zip", final_report_dir)

        firebase_upload_path = create_firebae_upload_path(uid, final_report_dir)
    
        sbfirebase.upload_zip_to_SBFirebase(zipped_file, firebase_upload_path)


        logging.info(f"UPLOAD: {firebase_upload_path}")


def main():
    try:
        print(sbfirebase.database)
        cleanup()
        unprocessed_audio_batch_zips = (
            sbfirebase.database.find_unprocessed_audio_batches()
        )
        for uid, audio_batch_zips in unprocessed_audio_batch_zips.items():
            for audio_batch_zip in audio_batch_zips:

                process_audio_batch_pipeline(uid, audio_batch_zip)
    finally:
        cleanup()
        sbfirebase.refresh_database()
        print(sbfirebase.database)


def delete():
    sbfirebase._delete_all_audio_assessments_from_firebase()
    sbfirebase.refresh_database()


if __name__ == "__main__":
    main()
    #delete()
