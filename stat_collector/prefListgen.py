import random
import pickle
import os

def generate_pref_list(N: int):
    prefList = []
    for i in range(1, N+1):
        prefs = list(range(1, N+1))
        random.shuffle(prefs)
        prefList.append((i, prefs))
    return prefList

if __name__ == "__main__":
    N = 9   # change this to whatever size you want
    prefList = generate_pref_list(N)

    with open(os.path.join(os.path.dirname(__file__), "prefList.pkl"), "wb") as f:
        pickle.dump(prefList, f)

    print(f"Preference list for N={N} saved to prefList.pkl")
