#!/usr/bin/env python3
import os
import json
import pandas as pd

def process_log(log_dir):
    summary_path = os.path.join(log_dir, 'summary.json')
    if not os.path.exists(summary_path):
        return None
    with open(summary_path, 'r') as f:
        data = json.load(f)
        
    duration = data.get('navigation_time_s', 0.0)
    dose = data.get('total_exposure_mSv', 0.0)
    
    # Optional rules based on article context
    # Usually: filter wait times, trim stop time if velocity < 0.03
    
    return {'Duration (s)': duration, 'Dose (mSv)': dose}

def main():
    print("Log Processing Script")
    print("Run this to parse logs/ folder and generate comparison tables.")
    print("Integration uses trapezoidal rule on the initial source field.")
    print("Movement boundaries are typically computed using a threshold of |v| > 0.03 m/s.")
    
    # Iterate through logs/series_00 and logs/series_01
    results = []
    for series in ['logs/series_00', 'logs/series_01']:
        if not os.path.exists(series): continue
        for d in sorted(os.listdir(series)):
            dpath = os.path.join(series, d)
            if os.path.isdir(dpath):
                r = process_log(dpath)
                if r:
                    r['Run'] = d
                    r['Series'] = series
                    results.append(r)
    
    if results:
        df = pd.DataFrame(results)
        print(df.to_string(index=False))

if __name__ == '__main__':
    main()
