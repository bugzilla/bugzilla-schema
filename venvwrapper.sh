#!/bin/bash
set -e
if [ -z "$1" ]; then
  echo "This is designed to be used as a shebang interpreter at the top of"
  echo "Python CGI files to allow them to make use of the virtualenv setup."
  echo "Don't use it directly."
  exit -1
fi
if [ ! -e "venv" ]; then
  echo "VirtualEnv does not exist. Creating..."
  virtualenv -p python3 venv > /dev/null
  source venv/bin/activate
  pip install -r requirements.txt > /dev/null
  deactivate
fi
source venv/bin/activate
python3 "$@"
