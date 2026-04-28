dev:
  python src/main.py

train:
  python src/training.py

fmt:
  black --line-length 80 .

req:
  pip freeze > requirements.txt
