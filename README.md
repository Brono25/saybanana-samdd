# SayBanana SAMDD Assessment
This  `python` program reads audio files from the **Say Banana** Firebase storage, applies the `samdd_method` and uploads the results of the assessment as a json file to the Firebase storage.
The program is wrapped in a docker container.

The `json` reports are uploaded to the Firebase storage following a similiar file structure as the audio files, seen below.
```txt
└── user_example@email.com/ 
        ├── Daily_Audio/
                ├── 04-10-2021-Audio-1633338100611.zip
                       ├── Flea/
                            ├── 1633337174099.wav
                            ├── 1633337490066.wav
                       ├── Frog/
                            ├── 1633337204901.wav
                            ├── 1633337330507.wav
        ├── Daily_Audio_Assessment/
                ├── 04-10-2021-Audio-1633338100611/
                       ├── Flea/
                            ├── 1633337174099.json
                            ├── 1633337490066.json
                       ├── Frog/
                            ├── 1633337204901.json
                            ├── 1633337330507.json
```

## Setup and Installation







The `SBFirebaseInterface` class is designed to read and write data related to audio processing.




Create an API key for a service account in Firebase, you should get a JSON file with contents like below. Keep this key private, do not store in a repo.
Find the path to the firebase storage bucket.
```python
credentials = {
  "type": "service_account",
  "project_id": "example-5a501",
  "private_key_id": "abc1234567890def1234567890abcdef12345678",
  "private_key": "-----BEGIN PRIVATE KEY-----\n[REDACTED]\n-----END PRIVATE KEY-----\n",
  "client_email": "email@example-5a501.iam.gserviceaccount.com",
  "client_id": "123456789012345678901",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/example-5a501.iam.gserviceaccount.com"
}
bucket_path = "example-5a501.appspot.com"
```



Initialise `SBFirebaseInterface` with the bucket path and the credentials. The firebase storage will now be able to be accessed.

```python
from SBFirebase.interface import SBFirebaseInterface

sbfinterface = SBFirebaseInterface(bucket_path, credentials)
```




Assumptions:
user IDs are the form (any non '_' characters)_local@domain

