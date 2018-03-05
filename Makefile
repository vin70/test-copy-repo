VENV_DIR = .env

all:	clean
		if [ ! -d "$(VENV_DIR)" ]; then \
			virtualenv $(VENV_DIR) -p python3; \
			$(VENV_DIR)/bin/pip install -r requirements.txt; \
		fi

clean:
		if [ -d $(VENV_DIR) ]; then \
			rm -r $(VENV_DIR)/*; \
			rmdir $(VENV_DIR); \
		fi


.PHONY: all clean
 