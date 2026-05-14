import os
import shutil
import pytest

PROJECT_DIR = "/home/user/app"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_page_tsx_exists():
    page_path = os.path.join(PROJECT_DIR, "src/app/page.tsx")
    assert os.path.isfile(page_path), f"Page file {page_path} does not exist."

def test_form_exists_but_no_action():
    page_path = os.path.join(PROJECT_DIR, "src/app/page.tsx")
    with open(page_path, "r") as f:
        content = f.read()
    assert "<form>" in content, "Expected <form> to be present in page.tsx."
    assert "action={" not in content, "Expected <form> to not have an action handler initially."
