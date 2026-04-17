dev:
  python src/main.py

fmt:
  black .

req:
  pip freeze > requirements.txt
