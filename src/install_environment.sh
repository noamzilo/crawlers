# install chrome for selenium
sudo snap remove chromium
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" \
> /etc/apt/sources.list.d/google-chrome.list'
sudo apt update
sudo apt install google-chrome-stable

# install python packages. Make sure your src dir is correct
cd my_src && python3 -m venv venv_crawler && source venv_crawler/bin/activate && pip install -r requirements.txt

