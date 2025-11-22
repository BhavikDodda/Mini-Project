# log_utils.py
import csv, os, time

def log_stats(method_name, prefList, num_pareto1, num_pareto2, start_time, end_time, start_time2, end_time2):
    """Record stats for an algorithm run."""
    csv_filename = "results_summary.csv"
    file_exists = os.path.isfile(csv_filename)

    record = {
        "method": method_name,
        "prefList": str(prefList),
        "pareto_solutions1": num_pareto1,
        "size1": len(num_pareto1),
        "pareto_solutions2": num_pareto2,
        "size2": len(num_pareto2),
        "time_taken_sec_1": round(end_time - start_time, 4),
        "time_taken_sec_2": round(end_time2 - start_time2, 4),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(csv_filename, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=record.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(record)

    print(f"✅ Stats logged for {method_name} in {csv_filename}")
