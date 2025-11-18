import os
import pickle
from prefListgen import generate_pref_list

N = 9  # set N here

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    out_path = os.path.join(base_dir, "100prefLists.pkl")

    all_prefs = [generate_pref_list(N) for _ in range(100)]

    with open(out_path, "wb") as f:
        pickle.dump(all_prefs, f)

    print(f"Saved 100 preference lists (N={N}) to {out_path}")