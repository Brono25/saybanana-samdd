# SayBanana SAMDD Assessment
This  `python` program reads audio files from the **Say Banana** Firebase storage, applies the `samdd_method` and uploads the results of the assessment as a json file to the Firebase storage.
The program is wrapped in a docker container.

The JSON reports are uploaded to the Firebase storage following a similiar file structure as the audio files, seen below.
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

## Setup & Installation

- **Step 1:** Clone the `samdd-method` and `SBFirebase-Interface` repositories to the `packages` directory.
- **Step 2:** Copy the  `Speech-Attributes` and `phonemizer` directories to `cache/samdd/`.
- **Step 3:** Create an API key on the Firebase website to give the `SBFirebase-Interface` module permission to access the SayBanana Firebase storage. It should give you a JSON file containing something like below.
```json
{
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
```
- **Step 4:** Convert this key into base64 by the command `base64 -i firebase_api_key.json`. Do not store this key in a repository, keep it private.
- **Step 5:** Create a .env file in the root dir and set the base64 key string into the environment variable `FIREBASE_CREDENTIALS_BASE64`. Add the path to the Firebase bucket into the `BUCKET_PATH` environment variable. The `.env` file should look similiar to below.
```txt
BUCKET_PATH="my_app-5a501.appspot.com" 
FIREBASE_CREDENTIALS_BASE64=ewogICJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsCiAgIn....
```

After this setup the project file structure should look like as below.
```txt
.
├── README.md
├── cache/
│   └── samdd/
│       ├── Speech-Attributes/
│       └── phonemizer/
├── docker-compose.yml
├── dockerfile
├── environment.py
├── packages/
│   ├── SBFirebase-Interface/
│   └── samdd-method/
├── requirements.txt
├── samdd-saybanana.py
└── system/
    └── .bashrc
```

Then run the commands to build and run.
- `docker build -t saybanana-samdd`
- `docker run saybanana-samdd`