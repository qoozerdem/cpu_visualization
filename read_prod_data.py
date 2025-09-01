import csv
from datetime import datetime

# Frequency and core definitions
freqs = ['M0_', 'M1_', 'M2_', 'M3_', 'M4_', 'M5_', 'M6_', 'M7_', 'M8_', 'M9_', 'M10_']
cores = ['core6', 'core7']

# Dictionary to store column indices
wlc_cx = {}

# Frequency mapping
freq_dict = {
    'M0_': 4435.2, 'M1_': 4531.2, 'M2_': 4646.4, 'M3_': 4742.4, 'M4_': 4838.4,
    'M5_': 4934.4, 'M6_': 4761.6, 'M7_': 4800, 'M8_': 4857.6, 'M9_': 5107.2, 'M10_': 5203.2
}
freq_dict_avg = {
    'M0_': [0,0], 'M1_': [0,0], 'M2_': [0,0], 'M3_': [0,0], 'M4_': [0,0],
    'M5_': [0,0], 'M6_': [0,0], 'M7_': [0,0], 'M8_': [0,0], 'M9_': [0,0], 'M10_': [0,0]
}

# Parse header to get column indices
with open(r'\\encore\pteit_mlds_datasync\SmlApp_PTE\users\nandeepd\ecid_iddq_apss.csv', 'r') as f:
    reader = csv.reader(f)
    headers = next(reader)  # Reads the first line (header row)
    count = 0
    #because we check the keywords it is a good practice to check the keywords looked in the data were found exatly once
    # safety list is appended with a different value every time and checked if it has any duplicate elements
    safety=[]

    for i in headers:
        if "fprom" in i and 'IDDQ' in i and 'APC1_CX' in i:
            wlc_cx.update({'iddq': count})
            safety.append(0)
        if 'fablot' in i:
            wlc_cx.update({'fab': count})
            safety.append(1)
        if 'starttime_utc_FT1' in i:
            wlc_cx.update({"time": count})
            safety.append(2)

        if 'core' in i and 'cl1' in i and 'cx' in i and 'apc1' in i:
            for j in freqs:
                if j in i:
                    for k in cores:
                        if k in i:
                            wlc_cx.update({j + k: count})
                            safety.append((freqs.index(j)+1)*len(freqs)+cores.index(k))
        

        count += 1

    # 0 printed means key wrods looked in the data were found in nore more than 1 test
    print(len(safety)-len(list(set(safety))))



# Collect all week numbers
weeks = []
with open(r'\\encore\pteit_mlds_datasync\SmlApp_PTE\users\nandeepd\ecid_iddq_apss.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header

    for row in reader:
        dt = datetime.strptime(row[wlc_cx['time']], "%Y-%m-%d %H:%M:%S")
        week_number = dt.isocalendar()[1]
        if week_number not in weeks:
            weeks.append(week_number)

min_week = min(weeks)

# Helper function to select slot value this is needed because we take the max of 2 cores 
def slot(x, y):
    try:
        a1 = float(x)
        a2 = float(y)
        if a1 < 0:
            a1 = 1.3
        if a2 < 0:
            a2 = 1.3
        m = max(a1, a2)
        return m
    except Exception:
        try:
            a1 = float(x)
            if a1 < 0:
                a1 = 1.3
            return a1
        except Exception:
            try:
                a2 = float(y)
                if a2 < 0:
                    a2 = 1.3
                return a2
            except Exception:
                return -1






total_positive_tests=0
# Process CSV and write output
with open(r'\\encore\pteit_mlds_datasync\SmlApp_PTE\users\nandeepd\ecid_iddq_apss.csv', 'r') as f:
    with open('output.csv', 'w', newline='') as g:
        writer = csv.writer(g)
        reader = csv.reader(f)
        writer.writerow(['week', 'freq', 'vmin', 'iddq', 'fablot'])
        next(reader)  # Skip header

        for row in reader:
            dt = datetime.strptime(row[wlc_cx['time']], "%Y-%m-%d %H:%M:%S")
            week_number = dt.isocalendar()[1] - min_week

            for i in range(11):
                x1 = row[wlc_cx[freqs[i] + 'core6']]
                x2 = row[wlc_cx[freqs[i] + 'core7']]
                bin_val = slot(x1, x2)
                if bin_val > -1:
                     writer.writerow([
                         f"week {week_number}",
                         freq_dict[freqs[i]],
                         bin_val,
                         float(row[wlc_cx["iddq"]]) / 127.15,
                         row[wlc_cx['fab']]
                     ])
                     #while filling up the output.csv file with prod data we also  keep a record of voltage values and how many data points exist for each frequency so we can take average
                     if bin_val!=1.3:
                       freq_dict_avg[freqs[i]][0]+=1
                       freq_dict_avg[freqs[i]][1]+=bin_val
                       total_positive_tests+=1

#after we are done with the output.csv file we quickly write the average voltage values to freq_dict_avg.csv for MHz per Mv table 
with open('freq_dict_avg.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['freq', 'avg'])
    for key in freq_dict_avg:
        #Because of outliers in higher frequencies only the frequencies that has at least 1/1000 of valid vmin 
        if freq_dict_avg[key][1]>0.001*total_positive_tests:
           writer.writerow([freq_dict[key], freq_dict_avg[key][1]/freq_dict_avg[key][0]])




















