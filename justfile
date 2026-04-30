dev:
  python src/main.py

train:
  python src/training.py

lnf:
  python src/input_lostandfound.py

clean:
  rm -rf parent_objects
  rm -rf tagged_objects
  rm abandoned_objects

fmt:
  black --line-length 80 .

req:
  pip freeze > requirements.txt
