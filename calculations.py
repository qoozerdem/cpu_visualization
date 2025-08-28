import csv
from datetime import datetime
import math





# When data is taken from the sheet negatives are binned to 1.3 volts
def get_value(x):
    if x< 0:
        return 1.3
    else:
        return x
    


#OCTA CORE CALCULATIONS
# APC1 CX Dynamic Power (2C)
def dyn_apc1cx_2c(APC1_CX_VMIN, Freq_NCC1):
    return 0.1745 * math.exp(0.0025 * 1000 * APC1_CX_VMIN) * Freq_NCC1



# APC1 CX Static Power
def stt_apc1cx(APC1_CX_VMIN, Tj, IDDQ_APC1CX):
    term1 = 0.1916 * math.exp(2.2009 * APC1_CX_VMIN)
    term2 = 0.3578 * math.exp(0.0345 * Tj)
    term3 = -0.7739 * APC1_CX_VMIN**2 + 1.2883 * APC1_CX_VMIN + 0.4716
    return (term1 * term2 * term3) * IDDQ_APC1CX * APC1_CX_VMIN

def total_apc1_cx(APC1_CX_VMIN, Freq_NCC1, Tj, IDDQ_APC1CX):
    return dyn_apc1cx_2c(APC1_CX_VMIN, Freq_NCC1) + stt_apc1cx(APC1_CX_VMIN, Tj, IDDQ_APC1CX)

# APC1 MX Dynamic Power (2C)
def dyn_apc1mx_2c(APC1_MX_VMIN, Freq_NCC1):
    return 0.0169 * math.exp(0.0025 * 1000 * APC1_MX_VMIN) * Freq_NCC1

# APC1 MX Static Power
def stt_apc1mx(APC1_MX_VMIN, Tj, IDDQ_APC1MX):
    term1 = 0.0024 * math.exp(7.7139 * APC1_MX_VMIN)
    term2 = 0.3664 * math.exp(0.0336 * Tj)
    term3 = 2.1226 * APC1_MX_VMIN**2 - 6.1697 * APC1_MX_VMIN + 4.4854
    return (term1 * term2 * term3) * IDDQ_APC1MX * APC1_MX_VMIN

def total_apc1_mx(APC1_MX_VMIN, Freq_NCC1, Tj, IDDQ_APC1MX):
    return dyn_apc1mx_2c(APC1_MX_VMIN, Freq_NCC1) + stt_apc1mx(APC1_MX_VMIN, Tj, IDDQ_APC1MX)

def total_apc1_power(APC1_CX_VMIN, APC1_MX_VMIN, Freq_NCC1, Tj, IDDQ_APC1CX, IDDQ_APC1MX):
    return total_apc1_cx(APC1_CX_VMIN, Freq_NCC1, Tj, IDDQ_APC1CX) + total_apc1_mx(APC1_MX_VMIN, Freq_NCC1, Tj, IDDQ_APC1MX)

# APC0 CX Dynamic Power (6C)
def dyn_apc0cx_6c(APC0_CX_VMIN, Freq_NCC0):
    return 0.1993 * math.exp(0.0024 * 1000 * APC0_CX_VMIN) * Freq_NCC0

# APC0 CX Static Power
def stt_apc0cx(APC0_CX_VMIN, Tj, IDDQ_APC0CX):
    term1 = 0.1848 * math.exp(2.2468 * APC0_CX_VMIN)
    term2 = 0.3543 * math.exp(0.0349 * Tj)
    term3 = -1.0477 * APC0_CX_VMIN**2 + 1.683 * APC0_CX_VMIN + 0.3295
    return (term1 * term2 * term3) * IDDQ_APC0CX * APC0_CX_VMIN

def total_apc0_cx(APC0_CX_VMIN, Freq_NCC0, Tj, IDDQ_APC0CX):
    return dyn_apc0cx_6c(APC0_CX_VMIN, Freq_NCC0) + stt_apc0cx(APC0_CX_VMIN, Tj, IDDQ_APC0CX)

# APC0 MX Dynamic Power (6C)
def dyn_apc0mx_6c(APC0_MX_VMIN, Freq_NCC0):
    return 0.0307 * math.exp(0.0024 * 1000 * APC0_MX_VMIN) * Freq_NCC0

# APC0 MX Static Power
def stt_apc0mx(APC0_MX_VMIN, Tj, IDDQ_APC0MX):
    term1 = 0.0039 * math.exp(7.0622 * APC0_MX_VMIN)
    term2 = 0.3746 * math.exp(0.0329 * Tj)
    term3 = 0.8083 * APC0_MX_VMIN**2 - 3.6729 * APC0_MX_VMIN + 3.3496
    return (term1 * term2 * term3) * IDDQ_APC0MX * APC0_MX_VMIN

def total_apc0_mx(APC0_MX_VMIN, Freq_NCC0, Tj, IDDQ_APC0MX):
    return dyn_apc0mx_6c(APC0_MX_VMIN, Freq_NCC0) + stt_apc0mx(APC0_MX_VMIN, Tj, IDDQ_APC0MX)

def total_apc0_power(APC0_CX_VMIN, APC0_MX_VMIN, Freq_NCC0, Tj, IDDQ_APC0CX, IDDQ_APC0MX):
    return total_apc0_cx(APC0_CX_VMIN, Freq_NCC0, Tj, IDDQ_APC0CX) + total_apc0_mx(APC0_MX_VMIN, Freq_NCC0, Tj, IDDQ_APC0MX)

def total_octacore_power(APC0_CX_VMIN, APC0_MX_VMIN, Freq_NCC0, Tj, IDDQ_APC0CX, IDDQ_APC0MX,
                         APC1_CX_VMIN, APC1_MX_VMIN, Freq_NCC1, IDDQ_APC1CX, IDDQ_APC1MX):
    return total_apc0_power(APC0_CX_VMIN, APC0_MX_VMIN, Freq_NCC0, Tj, IDDQ_APC0CX, IDDQ_APC0MX) + \
           total_apc1_power(APC1_CX_VMIN, APC1_MX_VMIN, Freq_NCC1, Tj, IDDQ_APC1CX, IDDQ_APC1MX)

# Single Core Calculations
def dyn_apc1cx_1c(APC1_CX_VMIN, Freq):
    return 0.0914 * math.exp(0.0025 * 1000 * APC1_CX_VMIN) * Freq

def stt_apc1cx_sc(APC1_CX_VMIN, Tj, IDDQ_APC1CX):
    term1 = 0.1916 * math.exp(2.2009 * APC1_CX_VMIN)
    term2 = 0.3578 * math.exp(0.0345 * Tj)
    term3 = -0.7739 * APC1_CX_VMIN**2 + 1.2883 * APC1_CX_VMIN + 0.4716
    return (term1 * term2 * term3) * IDDQ_APC1CX * APC1_CX_VMIN

def total_apc1_cx_sc(APC1_CX_VMIN, Freq, Tj, IDDQ_APC1CX):
    return dyn_apc1cx_1c(APC1_CX_VMIN, Freq) + stt_apc1cx_sc(APC1_CX_VMIN, Tj, IDDQ_APC1CX)

def dyn_apc1mx_1c(APC1_MX_VMIN, Freq):
    return 0.0087 * math.exp(0.0025 * 1000 * APC1_MX_VMIN) * Freq

def stt_apc1mx_sc(APC1_MX_VMIN, Tj, IDDQ_APC1MX):
    term1 = 0.0024 * math.exp(7.7139 * APC1_MX_VMIN)
    term2 = 0.3664 * math.exp(0.0336 * Tj)
    term3 = 2.1226 * APC1_MX_VMIN**2 - 6.1697 * APC1_MX_VMIN + 4.4854
    return (term1 * term2 * term3) * IDDQ_APC1MX * APC1_MX_VMIN

def total_apc1_mx_sc(APC1_MX_VMIN, Freq, Tj, IDDQ_APC1MX):
    return dyn_apc1mx_1c(APC1_MX_VMIN, Freq) + stt_apc1mx_sc(APC1_MX_VMIN, Tj, IDDQ_APC1MX)

def total_apc1_power_sc(APC1_CX_VMIN, APC1_MX_VMIN, Freq, Tj, IDDQ_APC1CX, IDDQ_APC1MX):
    return total_apc1_cx_sc(APC1_CX_VMIN, Freq, Tj, IDDQ_APC1CX) + total_apc1_mx_sc(APC1_MX_VMIN, Freq, Tj, IDDQ_APC1MX)



# Main path to the data
input_path = r'\\encore\pteit_mlds_datasync\SmlApp_PTE\users\nandeepd\ecid_iddq_apss.csv'
#the csv file for powerbi to read
output_path = 'output_dhrystone.csv'







#because we check the keywords it is a good practice to check the keywords looked in the data were found exatly once
# safety list is appended with a different value every time and checked if it has any duplicate elements
safety=[]
with open(input_path, 'r') as f, open(output_path, 'w', newline='') as g:
    reader = csv.reader(f)
    writer = csv.writer(g)
    headers = next(reader)
    names = {}
    for idx, col in enumerate(headers):
        if 'IDDQ' in col and 'APC1_CX' in col and 'fprom' in col:
            names['iddq_apc1_cx'] = idx
            safety.append(1)

        if 'IDDQ' in col and 'APC1_MX' in col and 'fprom' in col:
            names['iddq_apc1_mx'] = idx
            safety.append(2)

        if 'IDDQ' in col and 'APC0_CX' in col and 'fprom' in col:
            names['iddq_apc0_cx'] = idx
            safety.append(3)
        if 'IDDQ' in col and 'APC0_MX' in col and 'fprom' in col:
            names['iddq_apc0_mx'] = idx
            safety.append(4)
        if 'fablot' in col:
            names['fab'] = idx
            safety.append(5)
        if 'starttime_utc_FT1' in col:
            names['time'] = idx
            safety.append(6)
        if 'FUSE' in col and "BOOSTP2]" in col and 'Vmin' in col and (not "HTHP" in col):
            names["boostp2_cx_vmin"] = idx
            safety.append(7)

        if 'APC1_MX' in col and 'BOOST' in col and "PREMEM" in col:
            names["mx_vmin_apc1_boost1"] = idx
            safety.append(8)
            print(col)
        if 'APC0_MX' in col and 'BOOST' in col and "PREMEM" in col:
            names["mx_vmin_apc0_boost1"] = idx
            safety.append(9)
            print(col)

        if 'APC1_MX' in col and 'TURL3' in col and "PREMEM" in col:
            names["mx_vmin_apc1_tur3"] = idx
            safety.append(10)

        if 'APC0_MX' in col and 'TURL3' in col and "PREMEM" in col:
            names["mx_vmin_apc0_tur3"] = idx
            safety.append(11)

        if 'FUSE' in col and "TURL3" in col and 'Vmin' in col and "NCC0" in col and "D001" in col and (not "HTHP" in col):
            names["octa_tur3_ncc0_cx_vmin_d001"] = idx
            safety.append(12)
        if 'FUSE' in col and "TURL3" in col and 'Vmin' in col and "NCC0" in col and "D000" in col and (not "HTHP" in col):
            names["octa_tur3_ncc0_cx_vmin_d000"] = idx
            safety.append(13)

        if 'FUSE' in col and "TURL3" in col and 'Vmin' in col and "NCC1" in col and "D001" in col and (not "HTHP" in col):
            names["octa_tur3_ncc1_cx_vmin_d001"] = idx
            safety.append(14)
        if 'FUSE' in col and "TURL3" in col and 'Vmin' in col and "NCC1" in col and "D000" in col and (not "HTHP" in col):
            names["octa_tur3_ncc1_cx_vmin_d000"] = idx
            safety.append(15)


        if 'FUSE' in col and "BOOST]" in col and 'Vmin' in col and "NCC0" in col and "D001" in col and (not "HTHP" in col):
            names["octa_boost1_ncc0_cx_vmin_d001"] = idx
            safety.append(16)
        if 'FUSE' in col and "BOOST]" in col and 'Vmin' in col and "NCC0" in col and "D000" in col and (not "HTHP" in col):
            names["octa_boost1_ncc0_cx_vmin_d000"] = idx
            safety.append(17)

        if 'FUSE' in col and "BOOST]" in col and 'Vmin' in col and "NCC1" in col and "D001" in col and (not "HTHP" in col):
            names["octa_boost1_ncc1_cx_vmin_d001"] = idx
            safety.append(18)

        if 'FUSE' in col and "BOOST]" in col and 'Vmin' in col and "NCC1" in col and "D000" in col and (not "HTHP" in col):
            names["octa_boost1_ncc1_cx_vmin_d000"] = idx
            safety.append(19)


        if 'FUSE' in col and "TURL5]" in col and 'Vmin' in col and "NCC0" in col and "D001" in col and (not "HTHP" in col):
            names["octa_boost_ncc0_cx_vmin_d001"] = idx
            safety.append(20)

        if 'FUSE' in col and "TURL5]" in col and 'Vmin' in col and "NCC0" in col and "D000" in col and (not "HTHP" in col):
            names["octa_boost_ncc0_cx_vmin_d000"] = idx
            safety.append(21)
            

        if 'FUSE' in col and "TURL5]" in col and 'Vmin' in col and "NCC1" in col and "D001" in col and (not "HTHP" in col):
            names["octa_boost_ncc1_cx_vmin_d001"] = idx
            safety.append(22)

        if 'FUSE' in col and "TURL5]" in col and 'Vmin' in col and "NCC1" in col and "D000" in col and (not "HTHP" in col):
            names["octa_boost_ncc1_cx_vmin_d000"] = idx
            safety.append(23)



        if 'FUSE' in col and "BOOSTP]" in col and "D000" in col and 'Vmin' in col and (not "HTHP" in col):
            names["boostp_cx_vmin_d000"] = idx
            safety.append(24)

        if 'FUSE' in col and "BOOSTP]" in col and "D001" in col and 'Vmin' in col and (not "HTHP" in col):
            names["boostp_cx_vmin_d001"] = idx
            safety.append(25)

        if 'APC1_MX' in col and 'TURL5' in col and "PREMEM" in col:
            names["mx_vmin_apc1_boost"] = idx
            safety.append(26)

        if 'APC0_MX' in col and 'TURL5' in col and "PREMEM" in col:
            names["mx_vmin_apc0_boost"] = idx
            safety.append(27)

    #if 0 is printed it means the key words looked for each test were found in exactly one test 
    print(len(safety)-len(list(set(safety))))
  


    #we check all weeks to find the minimum week which will be used to start the weeks from 0 
    weeks = set()
    rows = []
    for row in reader:
        try:
            dt = datetime.strptime(row[names['time']], "%Y-%m-%d %H:%M:%S")
            week_number = dt.isocalendar()[1]
            weeks.add(week_number)
            rows.append((week_number, row))
        except Exception:
            continue

    min_week = min(weeks)


    # for dhrystone we create a csv file that has the week, fablot. apc1_cx iddq and power info the power is for boost, boost1 and turl3 for octa core and boostp and boostp2 for single core
    writer.writerow([
    'week', 

    'fablot', 


    'iddq_apc1_cx', 





    # --- Octa-core TURL3 metrics ---
 'total_octacore_power_tur3',


    # --- Octa-core BOOST metrics ---
 'total_octacore_power_boost',
    # --- Octa-core BOOST metrics ---
 'total_octacore_power_boost1',

    # --- Single core BOOSTP metrics ---

    'total_apc1_power_boostp2',
    'total_apc1_power_boostp'

])  
    


    #this parameter is fixed
    Tj=85




    for week_number, row in rows:


        try:

           
            #iddq datas needed
            iddq_apc1_cx = float(row[names['iddq_apc1_cx']])
            iddq_apc0_cx = float(row[names['iddq_apc0_cx']])
            iddq_apc0_mx = float(row[names['iddq_apc0_mx']])
            iddq_apc1_mx = float(row[names['iddq_apc1_mx']])
           
      


            #octa core turl3

            vmin_cx_tur3_ncc0_d000=row[names["octa_tur3_ncc0_cx_vmin_d000"]]
            vmin_cx_tur3_ncc0_d001=row[names["octa_tur3_ncc0_cx_vmin_d001"]]
            vmin_cx_tur3_ncc1_d000=row[names["octa_tur3_ncc1_cx_vmin_d000"]]
            vmin_cx_tur3_ncc1_d001=row[names["octa_tur3_ncc1_cx_vmin_d001"]]
           
      

            # We check d000 and d001 to see which is available 
            if vmin_cx_tur3_ncc0_d000!="":
                 vmin_cx_tur3_ncc0 = max(get_value(float(row[names["octa_tur3_ncc0_cx_vmin_d000"]])) + 0.04, 0.768)
            elif vmin_cx_tur3_ncc0_d001!="":
                vmin_cx_tur3_ncc0 = max(get_value(float(row[names["octa_tur3_ncc0_cx_vmin_d001"]])) + 0.04, 0.768)
            else:
                 vmin_cx_tur3_ncc0=""
        


            # We check d000 and d001 to see which is available
                
            if vmin_cx_tur3_ncc1_d000!="":
                 vmin_cx_tur3_ncc1 = max(get_value(float(row[names["octa_tur3_ncc1_cx_vmin_d000"]])) + 0.04, 0.768)
            elif vmin_cx_tur3_ncc1_d001!="":
                vmin_cx_tur3_ncc1 = max(get_value(float(row[names["octa_tur3_ncc1_cx_vmin_d001"]])) + 0.04, 0.768)
            else:
                 vmin_cx_tur3_ncc1=""

                 
            #octa core boost

            vmin_cx_boost_ncc0_d000=row[names["octa_boost_ncc0_cx_vmin_d000"]]
            vmin_cx_boost_ncc0_d001=row[names["octa_boost_ncc0_cx_vmin_d001"]]
            vmin_cx_boost_ncc1_d000=row[names["octa_boost_ncc1_cx_vmin_d000"]]
            vmin_cx_boost_ncc1_d001=row[names["octa_boost_ncc1_cx_vmin_d001"]]

            


            # We check d000 and d001 to see which is available
            if vmin_cx_boost_ncc0_d000!="":
                 vmin_cx_boost_ncc0 = max(get_value(float(row[names["octa_boost_ncc0_cx_vmin_d000"]])) + 0.04, 0.768)
            elif vmin_cx_boost_ncc0_d001!="":
                vmin_cx_boost_ncc0 = max(get_value(float(row[names["octa_boost_ncc0_cx_vmin_d001"]])) + 0.04, 0.768)
            else:
                 vmin_cx_boost_ncc0=""
        


            # We check d000 and d001 to see which is available
                
            if vmin_cx_boost_ncc1_d000!="":
                 vmin_cx_boost_ncc1 = max(get_value(float(row[names["octa_boost_ncc1_cx_vmin_d000"]])) + 0.04, 0.768)
            elif vmin_cx_boost_ncc1_d001!="":
                vmin_cx_boost_ncc1 = max(get_value(float(row[names["octa_boost_ncc1_cx_vmin_d001"]])) + 0.04, 0.768)
            else:
                 vmin_cx_boost_ncc1=""

            #octa core boost1

     


            vmin_cx_boost1_ncc0_d000=row[names["octa_boost1_ncc0_cx_vmin_d000"]]
            vmin_cx_boost1_ncc0_d001=row[names["octa_boost1_ncc0_cx_vmin_d001"]]
            vmin_cx_boost1_ncc1_d000=row[names["octa_boost1_ncc1_cx_vmin_d000"]]
            vmin_cx_boost1_ncc1_d001=row[names["octa_boost1_ncc1_cx_vmin_d001"]]

            # We check d000 and d001 to see which is available
            if vmin_cx_boost1_ncc0_d000!="":
                 vmin_cx_boost1_ncc0 = max(get_value(float(row[names["octa_boost1_ncc0_cx_vmin_d000"]])) + 0.04, 0.768)
            elif vmin_cx_boost1_ncc0_d001!="":
                vmin_cx_boost1_ncc0 = max(get_value(float(row[names["octa_boost1_ncc0_cx_vmin_d001"]])) + 0.04, 0.768)
            else:
                 vmin_cx_boost1_ncc0=""
        


            
                # We check d000 and d001 to see which is available
            if vmin_cx_boost1_ncc1_d000!="":
                 vmin_cx_boost1_ncc1 = max(get_value(float(row[names["octa_boost1_ncc1_cx_vmin_d000"]])) + 0.04, 0.768)
            elif vmin_cx_boost1_ncc1_d001!="":
                vmin_cx_boost1_ncc1 = max(get_value(float(row[names["octa_boost1_ncc1_cx_vmin_d001"]])) + 0.04, 0.768)
            else:
                 vmin_cx_boost1_ncc1=""


        
            #single core boostp2 
            # this frequency mode does not have a d000 version
            vmin_cx_boostp2=row[names["boostp2_cx_vmin"]]
            if vmin_cx_boostp2!="":
                vmin_cx_boostp2 = max(get_value(float(row[names["boostp2_cx_vmin"]])) + 0.04, 0.8)


 
            #single core boostp
    
            vmin_cx_boostp_d000=row[names["boostp_cx_vmin_d000"]]
            vmin_cx_boostp_d001=row[names["boostp_cx_vmin_d001"]]
   
         
            if vmin_cx_boostp_d000!="":
                 vmin_cx_boostp= max(get_value(float(row[names["boostp_cx_vmin_d000"]])) + 0.04, 0.8)
            elif vmin_cx_boostp_d001!="":
                vmin_cx_boostp = max(get_value(float(row[names["boostp_cx_vmin_d001"]])) + 0.04, 0.8)
            else:
                 vmin_cx_boostp=""

   
            #mx vmin
            # for boostp and boostp2 the boost vmin for memory is used
            vmin_mx_tur3_apc0 = max(float(row[names["mx_vmin_apc0_tur3"]]) + 0.075, 0.8)
            vmin_mx_tur3_apc1 = max(float(row[names["mx_vmin_apc1_tur3"]]) + 0.075, 0.8)
        
            vmin_mx_boost_apc0 = max(float(row[names["mx_vmin_apc0_boost"]]) + 0.075, 0.8)
            vmin_mx_boost_apc1 = max(float(row[names["mx_vmin_apc1_boost"]]) + 0.075, 0.8)
            
            vmin_mx_boost1_apc0 = max(float(row[names["mx_vmin_apc0_boost1"]]) + 0.075, 0.8)
            vmin_mx_boost1_apc1 = max(float(row[names["mx_vmin_apc1_boost1"]]) + 0.075, 0.8)

            #power calculations
            if vmin_cx_boostp2!="":
               boostp2_power=total_apc1_power_sc(vmin_cx_boostp2, vmin_mx_boost_apc1, 4742.4, Tj, iddq_apc1_cx, iddq_apc1_mx)
            else:
                 boostp2_power=""


            if vmin_cx_boostp!="":
               boostp_power=total_apc1_power_sc(vmin_cx_boostp, vmin_mx_boost_apc1, 4608, Tj, iddq_apc1_cx, iddq_apc1_mx)
            else:
                 boostp_power=""


            if vmin_cx_tur3_ncc0!="":
               turl3_power=total_octacore_power(vmin_cx_tur3_ncc0, vmin_mx_tur3_apc0, 3187.2, Tj, iddq_apc0_cx, iddq_apc0_mx,vmin_cx_tur3_ncc1, vmin_mx_tur3_apc1, 3648, iddq_apc1_cx, iddq_apc1_mx)

            else:
                 turl3_power=""

            if vmin_cx_boost_ncc0!="":
               boost_power=    total_octacore_power(vmin_cx_boost_ncc0, vmin_mx_boost_apc0, 3744, Tj, iddq_apc0_cx, iddq_apc0_mx,vmin_cx_boost_ncc1, vmin_mx_boost_apc1, 4185.6, iddq_apc1_cx, iddq_apc1_mx)
            else:
                 boost_power="" 


     
            if vmin_cx_boost1_ncc0!="":
               boost1_power=   total_octacore_power(vmin_cx_boost1_ncc0, vmin_mx_boost1_apc0, 3955.2, Tj, iddq_apc0_cx, iddq_apc0_mx,vmin_cx_boost1_ncc1, vmin_mx_boost1_apc1, 4396.8, iddq_apc1_cx, iddq_apc1_mx)
            else:
                 boost1_power="" 
     


            writer.writerow([
    "week {}".format(week_number-min_week),

    row[names['fab']],


    iddq_apc1_cx,




    # --- Octa-core TURL3 metrics ---
    turl3_power,
    # --- Octa-core BOOST metrics ---
    boost_power,
    # --- Octa-core BOOST metrics ---
    boost1_power,
    # --- Single core BOOSTP metrics ---
    boostp2_power,
    boostp_power

    
])
        except Exception:
            continue



