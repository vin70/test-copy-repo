VENV_DIR = ".venv"

all:	clean update
		if [ ! -d "$(VENV_DIR)" ]; then \
			virtualenv $(VENV_DIR) -p python3; \
			source $(VENV_DIR)/bin/activate; \
			pip install -r requirements.txt; \
		fi

clean:
	if [ -d $(VENV_DIR) ]; then \
		rm -r $(VENV_DIR)/*; \
		rmdir $(VENV_DIR); \
	fi

update:
		git pull

.PHONY: create_venv init_venv update init
 