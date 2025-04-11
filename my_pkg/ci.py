from pathlib import Path

import modal

ROOT_PATH = Path(__file__).parent.parent

image = (
    modal.Image.debian_slim()
    .pip_install("pytest")
    .pip_install_from_requirements(ROOT_PATH / "requirements.txt")
    .add_local_dir(ROOT_PATH / "my_pkg", remote_path="/root/my_pkg")
    .add_local_dir(ROOT_PATH / "tests", remote_path="/root/tests")
)

app = modal.App("ci-testing", image=image)


@app.function(gpu="any")
def pytest():
    import subprocess

    subprocess.run(["pytest", "-vs"], check=True, cwd="/root")
