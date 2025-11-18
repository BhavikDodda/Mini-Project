import os
import pickle
import subprocess
import sys

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    batch_path = os.path.join(base_dir, "100prefLists.pkl")
    target_pref_path = os.path.join(base_dir, "prefList.pkl")
    script_path = os.path.join(base_dir, "stablesets_allinone.py")

    with open(batch_path, "rb") as f:
        batch = pickle.load(f)

    total = len(batch)
    for idx, pref in enumerate(batch, 1):
        with open(target_pref_path, "wb") as pf:
            pickle.dump(pref, pf)
        print(f"Running {idx}/{total} ...")
        subprocess.run([sys.executable, script_path], cwd=base_dir, check=True)