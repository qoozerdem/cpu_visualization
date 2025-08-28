import csv

# Function to bin negative values to 1.3 volts
def get_value(x):
    if x < 0:
        return 1.3
    else:
        return x

# Input and output file paths
input_path = r'\\encore\pteit_mlds_datasync\SmlApp_PTE\users\nandeepd\ecid_iddq_apss.csv'
output_path_ncc0 = 'freqmode_voltage_averages_ncc0.csv'
output_path_ncc1 = 'freqmode_voltage_averages_ncc1.csv'

# D values to consider in column matching
d_values = ["D000", "D001"]

# Voltage values for each frequency mode for NCC0 and NCC1
voltage_ncc0 = {
    "LSVSD3": "",  # No value provided
    "LSVS": 1132.8,
    "NOML1": 2438.4,
    "SVSL1": 1920,
    "TUR": 2611.2,
    "BOOST": 3955.2,
    "LSVSD1": 883.2,
    "LSVSD2": 691.2,
    "NOM": 2227.2,
    "SVS": 1555.2,
    "TURL1": 2745.6,
    "TURL3": 3187.2,
    "TURL5": 3744,
    "BOOST1": "",    # No value provided
    "BOOSTP2": "",   # No value provided
    "BOOSTP": ""     # No value provided
}

voltage_ncc1 = {
    "LSVSD3": "",  # No value provided
    "LSVS": 883.2,
    "NOML1": 2592,
    "SVSL1": 1843.2,
    "TUR": 2880,
    "BOOST": 4185.6,
    "LSVSD1": 633.6,
    "LSVSD2": "",  # No value provided
    "NOM": 2227.2,
    "SVS": 1382.4,
    "TURL1": 3225.6,
    "TURL3": 3648,
    "TURL5": 3936,
    "BOOST1":4396.8,
    "BOOSTP2":4742.4,
    "BOOSTP":4608
}

# ss and tt values for each frequency mode for NCC0 and NCC1
ss_tt_ncc0 = {
    "LSVSD3": ("0.525", "0.435"),
    "LSVS": ("0.58", "0.515"),
    "NOML1": ("0.73", "0.69"),
    "SVSL1": ("0.675", "0.615"),
    "TUR": ("0.765", "0.72"),
    "BOOST": ("1", "0.95"),
    "LSVSD1": ("0.58", "0.49"),
    "LSVSD2": ("0.555", "0.465"),
    "NOM": ("0.7", "0.655"),
    "SVS": ("0.665", "0.565"),
    "TURL1": ("0.815", "0.77"),
    "TURL3": ("0.95", "0.89"),
    "TURL5": ("1", "0.95")
}

ss_tt_ncc1 = {
    "LSVSD3": ("", ""),
    "LSVS": ("0.632", "0.532"),
    "NOML1": ("0.756", "0.712"),
    "SVSL1": ("0.695", "0.635"),
    "TUR": ("0.792", "0.744"),
    "BOOST": ("1.032", "0.98"),
    "LSVSD1": ("0.6", "0.508"),
    "LSVSD2": ("", ""),
    "NOM": ("0.724", "0.676"),
    "SVS": ("0.688", "0.584"),
    "TURL1": ("0.84", "0.796"),
    "TURL3": ("0.98", "0.92"),
    "TURL5": ("1.032", "0.98"),
    "BOOST1":("1.032", "0.98"),
    "BOOSTP2":("1.032", "0.98"),
    "BOOSTP":("1.032", "0.98")
}

# Get available frequency modes from voltage dictionaries
freq_modes_ncc0 = [k for k in voltage_ncc0.keys()]
freq_modes_ncc1 = [k for k in voltage_ncc1.keys()]

# Prepare dictionary to collect values for each frequency mode and NCC
freqmode_values = {
    "NCC0": {opt: [] for opt in freq_modes_ncc0},
    "NCC1": {opt: [] for opt in freq_modes_ncc1}
}

# Read the input CSV and collect relevant column indices for each frequency mode and NCC
with open(input_path, 'r') as f:
    reader = csv.reader(f)
    headers = next(reader)
    # Map columns for each NCC and frequency mode
    mode_columns = {
        "NCC0": {opt: [] for opt in freq_modes_ncc0},
        "NCC1": {opt: [] for opt in freq_modes_ncc1}
    }
    # Find matching columns for each NCC, frequency mode, and D value
    for idx, col in enumerate(headers):
        for ncc, freq_modes in zip(["NCC0", "NCC1"], [freq_modes_ncc0, freq_modes_ncc1]):
            for opt in freq_modes:
                for d_val in d_values:
                    if (
                        'FUSEBIN' in col and
                        opt+']' in col and
                        d_val in col and
                        #this part can be changed to Vmin if desired
                        "CPR_Guardband" in col and
                        #belowe line makes sure HT values are taken 
                        ("HTHP" not in col)
                    ):
                        if ncc in col:
                          
                            mode_columns[ncc][opt].append(idx)

    # For each row, collect values for each NCC and frequency mode
    for row in reader:
        for ncc, freq_modes in zip(["NCC0", "NCC1"], [freq_modes_ncc0, freq_modes_ncc1]):
            for opt in freq_modes:
                for idx in mode_columns[ncc][opt]:
                    value = row[idx]
                    if value != "":
                        try:
                            val = get_value(float(value))
                            freqmode_values[ncc][opt].append(val)
                        except Exception:
                            continue  # Skip values that can't be converted

# Write the averages and metadata to output CSVs for NCC0 and NCC1
for ncc, output_path, voltage_dict, ss_tt_dict, freq_modes in zip(
    ["NCC0", "NCC1"],
    [output_path_ncc0, output_path_ncc1],
    [voltage_ncc0, voltage_ncc1],
    [ss_tt_ncc0, ss_tt_ncc1],
    [freq_modes_ncc0, freq_modes_ncc1]
):
    with open(output_path, 'w', newline='') as g:
        writer = csv.writer(g)
        # Write header row
        writer.writerow(['Voltage', 'Average Value', 'ss', 'tt', 'delta_ss', 'delta_tt'])
        # For each frequency mode, write the average and metadata if voltage and ss/tt are present
        for opt in freq_modes:
            voltage = voltage_dict[opt]
            if voltage == "" or voltage is None:
                continue  # Skip modes with no voltage value
            values = freqmode_values[ncc][opt]
            ss, tt = ss_tt_dict.get(opt, ("", ""))
            if values and ss != "" and tt != "":
                avg = sum(values) / len(values)
                writer.writerow([voltage, avg, ss, tt, float(ss)-float(avg), float(tt)-float(avg)])