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

        if "qblizzard_core7" in i and "BOOSTP2" in i and 'Vmin' in i and (not 'HTHP' in i):
            wlc_cx.update({"local_boostp2_core7": count})
            safety.append(0)
        if "qblizzard_core6" in i and "BOOSTP2" in i and 'Vmin' in i and (not 'HTHP' in i):
            wlc_cx.update({"local_boostp2_core6": count}) 
            safety.append(1)       

        if "fprom" in i and 'IDDQ' in i and 'APC1_CX' in i:
            wlc_cx.update({'iddq': count})
            safety.append(2)
        if 'fablot' in i:
            wlc_cx.update({'fab': count})
            safety.append(3)
        if 'starttime_utc_FT1' in i:
            wlc_cx.update({"time": count})
            safety.append(4)
        if 'core' in i and 'cl1' in i and 'cx' in i and 'apc1' in i:
            for j in freqs:
                if j in i:
                    for k in cores:
                        if k in i:
                            wlc_cx.update({j + k: count})
                            safety.append(5+(freqs.index(j)+1)*len(freqs)+cores.index(k))

        count += 1
    # 0 printed means key wrods looked in the data were found in nore more than 1 test
    print(len(safety)-len(list(set(safety))))
 
# Collect all week numbers
min_week=60

with open(r'\\encore\pteit_mlds_datasync\SmlApp_PTE\users\nandeepd\ecid_iddq_apss.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        dt = datetime.strptime(row[wlc_cx['time']], "%Y-%m-%d %H:%M:%S")
        week_number = dt.isocalendar()[1]
        # Determine min week so we start weeks from 0
        min_week=min(min_week,week_number)




with open(r'\\encore\pteit_mlds_datasync\SmlApp_PTE\users\nandeepd\ecid_iddq_apss.csv', 'r') as f:
    with open('local.csv', 'w', newline='') as g:
        writer = csv.writer(g)
        reader = csv.reader(f)
        # write the header
        writer.writerow(['week', 'fablot', 'M3 Core6', 'M3 Core7', 'BOOSTP2 Core6','BOOSTP2 Core7'])
        next(reader)  # Skip header

        for row in reader:
            dt = datetime.strptime(row[wlc_cx['time']], "%Y-%m-%d %H:%M:%S")
            week_number = dt.isocalendar()[1] - min_week


            try:
              

              m3_core6=float(row[wlc_cx['M3_core6']])

              m3_core7=float(row[wlc_cx['M3_core7']])
   
              boostp2_core6=float(row[wlc_cx['local_boostp2_core6']])

              boostp2_core7=float(row[wlc_cx['local_boostp2_core7']])



              if m3_core6<0:
                  m3_core6=1.3
              if m3_core7<0:
                  m3_core7=1.3
              if boostp2_core6<0:
                  boostp2_core6=1.3
              if boostp2_core7<0:
                  boostp2_core7=1.3

              # fill up the file
              writer.writerow([
                         f"week {week_number}",
                         row[wlc_cx['fab']],
                         m3_core6,
                         m3_core7,
                         boostp2_core6,
                         boostp2_core7
                     ])

            except:
                pass

              













