import os

CODE_DIR = os.path.dirname(__file__)
MAIN_DIR = os.path.dirname(CODE_DIR)
IMAGES_DIR = os.path.join(MAIN_DIR, "static", "images")

RES_DIR = os.path.join(MAIN_DIR, "resources")
EXCEL_DIR = os.path.join(RES_DIR, "excel_uploads")
BASE_RES_DIR = os.path.join(RES_DIR, "main_files")

TEST_DIR = os.path.join(os.path.dirname(MAIN_DIR), "test")
MONITORING_DIR = os.path.join(TEST_DIR, "monitoring_data")
