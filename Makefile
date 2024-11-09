setup-pip:
	pip install -r setup/pip_torch.txt
	pip install -r setup/pip_requirements.txt

run: setup-pip
	flask run
