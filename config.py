from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
TEST_SAMPLES_DIR = BASE_DIR / "test_samples"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"

for path in [DATA_DIR, MODELS_DIR, TEST_SAMPLES_DIR, NOTEBOOKS_DIR]:
    path.mkdir(parents=True, exist_ok=True)
