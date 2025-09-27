sudo apt update
sudo apt upgrade -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt install -y python3.12-venv python3.12

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.12 get-pip.py

mkdir logs

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3.12 -m venv venv
else
    echo "Virtual environment already exists. Skipping creation."
fi

source venv/bin/activate

echo "Installing required Python packages..."

pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "Copying example.env to .env..."
    cp example.env .env
else
    echo ".env file already exists. Skipping copy."
fi
#wait for env setup
#python3.12 main.py