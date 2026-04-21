dev:
  python src/main.py

train:
  python src/training.py

fmt:
  black .

req:
  pip freeze > requirements.txt
