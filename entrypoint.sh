
echo "User = $(whoami)"
echo "LOGFILE = $LOGFILE"
echo "BUCKET_PATH = $BUCKET_PATH"
cd /usr/src/app/src
echo "Running main...."
python "main.py"