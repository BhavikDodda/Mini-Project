# log_utils.py
import csv, os, time

def log_stats(method_name, prefList, num_pareto, start_time, end_time, start_time2, end_time2):
    """Record stats for an algorithm run."""
    csv_filename = "results_summary.csv"
    file_exists = os.path.isfile(csv_filename)

    record = {
        "method": method_name,
        "prefList": str(prefList),
        "num_pareto_solutions": num_pareto,
        "time_taken_sec": round(end_time - start_time, 4),
        "time_taken_sec_2": round(end_time2 - start_time2, 4),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(csv_filename, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=record.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(record)

    print(f"✅ Stats logged for {method_name} in {csv_filename}")
