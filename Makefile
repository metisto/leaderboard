
lint:
	flake8

test: lint
	python -m unittest discover -s leaderboard -p "*_test.py"
