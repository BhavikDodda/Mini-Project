import os
import pickle
from prefListgen import generate_pref_list

N_values = [3, 4, 5, 6]
num_iterations = 1000
# -----------------------------------

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    out_path = os.path.join(base_dir, "100prefLists.pkl")
    all_prefs = []
    for N in N_values:
        for _ in range(num_iterations):
            prefs = generate_pref_list(N)
            all_prefs.append(prefs)

    with open(out_path, "wb") as f:
        pickle.dump(all_prefs, f)

    print(f"Saved {len(all_prefs)} preference lists to {out_path}")
