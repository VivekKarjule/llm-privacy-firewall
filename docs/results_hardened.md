=== REGEX on clean (150 sentences) ===
label     gold  pred  strictP  strictR   lenP   lenR  leak%
AADHAAR      9     9     1.00     1.00   1.00   1.00     0%
DATE        18    18     1.00     1.00   1.00   1.00     0%
EMAIL       20    20     1.00     1.00   1.00   1.00     0%
LOCATION    32     0     0.00     0.00   0.00   0.00   100%
ORG         38     0     0.00     0.00   0.00   0.00   100%
PERSON      90     0     0.00     0.00   0.00   0.00   100%
PHONE       34    34     1.00     1.00   1.00   1.00     0%
SSN         29    29     1.00     1.00   1.00   1.00     0%
ALL        270   110     1.00     0.41   1.00   0.41    59%
  -- missed (up to 12) --
  MISSED PERSON  'Rahul Brown'          in: Refer Rahul Brown to Mayo Clinic, Bengaluru. Callback: 7181960013.
  MISSED ORG     'Mayo Clinic'          in: Refer Rahul Brown to Mayo Clinic, Bengaluru. Callback: 7181960013.
  MISSED LOCATION'Bengaluru'            in: Refer Rahul Brown to Mayo Clinic, Bengaluru. Callback: 7181960013.
  MISSED PERSON  'Rahul Kulkarni'       in: Insurance claim for Rahul Kulkarni (SSN 833-93-9928) at Sahyadri Hospital.
  MISSED ORG     'Sahyadri Hospital'    in: Insurance claim for Rahul Kulkarni (SSN 833-93-9928) at Sahyadri Hospital.
  MISSED PERSON  'Arjun Brown'          in: Insurance claim for Arjun Brown (SSN 106-30-7924) at Manipal Hospitals.
  MISSED ORG     'Manipal Hospitals'    in: Insurance claim for Arjun Brown (SSN 106-30-7924) at Manipal Hospitals.
  MISSED PERSON  'John Kulkarni'        in: Patient John Kulkarni can be reached at 8116155940 or arjun.iyer@clinic.net.
  MISSED PERSON  'Emily Williams'       in: Emily Williams from London reported chest pain; contact 7103413164.
  MISSED LOCATION'London'               in: Emily Williams from London reported chest pain; contact 7103413164.
  MISSED PERSON  'Neha Johnson'         in: Neha Johnson from Kolkata reported chest pain; contact 8341928327.
  MISSED LOCATION'Kolkata'              in: Neha Johnson from Kolkata reported chest pain; contact 8341928327.
  -- false positives (up to 12) --

=== REGEX on adversarial (100 sentences) ===
label     gold  pred  strictP  strictR   lenP   lenR  leak%
AADHAAR      5     5     1.00     1.00   1.00   1.00     0%
DATE        10    10     1.00     1.00   1.00   1.00     0%
EMAIL       18    18     1.00     1.00   1.00   1.00     0%
LOCATION    32     0     0.00     0.00   0.00   0.00   100%
ORG         24     0     0.00     0.00   0.00   0.00   100%
PERSON      68     0     0.00     0.00   0.00   0.00   100%
PHONE       28    28     1.00     1.00   1.00   1.00     0%
SSN         25    25     1.00     1.00   1.00   1.00     0%
ALL        210    86     1.00     0.41   1.00   0.41    59%
  -- missed (up to 12) --
  MISSED PERSON  'Rose Brown'           in: Patient Rose Brown lives in bengaluru.
  MISSED LOCATION'bengaluru'            in: Patient Rose Brown lives in bengaluru.
  MISSED PERSON  'rohan sharma'         in: refer rohan sharma to Ruby Hall Clinic, singapore.
  MISSED ORG     'Ruby Hall Clinic'     in: refer rohan sharma to Ruby Hall Clinic, singapore.
  MISSED LOCATION'singapore'            in: refer rohan sharma to Ruby Hall Clinic, singapore.
  MISSED ORG     'Mayo Clinic'          in: Admitted on 11 May 2021 at Mayo Clinic.
  MISSED PERSON  'Michael Deshmukh'     in: Aadhaar number 316155940781 belongs to Michael Deshmukh.
  MISSED PERSON  'david deshmukh'       in: refer david deshmukh to Apollo Hospital, toronto.
  MISSED ORG     'Apollo Hospital'      in: refer david deshmukh to Apollo Hospital, toronto.
  MISSED LOCATION'toronto'              in: refer david deshmukh to Apollo Hospital, toronto.
  MISSED PERSON  'Grace Reddy'          in: Patient Grace Reddy lives in delhi.
  MISSED LOCATION'delhi'                in: Patient Grace Reddy lives in delhi.
  -- false positives (up to 12) --

=== SPACY on clean (150 sentences) ===
label     gold  pred  strictP  strictR   lenP   lenR  leak%
AADHAAR      9     0     0.00     0.00   0.00   0.00   100%
DATE        18     0     0.00     0.00   0.00   0.00   100%
EMAIL       20     0     0.00     0.00   0.00   0.00    75%
LOCATION    32    23     0.96     0.69   0.96   0.69     9%
ORG         38    56     0.54     0.79   0.54   0.79     3%
PERSON      90    85     0.66     0.62   0.84   0.79     4%
PHONE       34     0     0.00     0.00   0.00   0.00   100%
SSN         29     0     0.00     0.00   0.00   0.00   100%
ALL        270   164     0.66     0.40   0.75   0.46    42%
  -- missed (up to 12) --
  MISSED PHONE   '7181960013'           in: Refer Rahul Brown to Mayo Clinic, Bengaluru. Callback: 7181960013.
  MISSED SSN     '833-93-9928'          in: Insurance claim for Rahul Kulkarni (SSN 833-93-9928) at Sahyadri Hospital.
  MISSED PERSON  'Arjun Brown'          in: Insurance claim for Arjun Brown (SSN 106-30-7924) at Manipal Hospitals.
  MISSED SSN     '106-30-7924'          in: Insurance claim for Arjun Brown (SSN 106-30-7924) at Manipal Hospitals.
  MISSED PHONE   '8116155940'           in: Patient John Kulkarni can be reached at 8116155940 or arjun.iyer@clinic.net.
  MISSED EMAIL   'arjun.iyer@clinic.net' in: Patient John Kulkarni can be reached at 8116155940 or arjun.iyer@clinic.net.
  MISSED PHONE   '7103413164'           in: Emily Williams from London reported chest pain; contact 7103413164.
  MISSED PHONE   '8341928327'           in: Neha Johnson from Kolkata reported chest pain; contact 8341928327.
  MISSED SSN     '801-51-1916'          in: Summarize the medical record for Rohan Reddy, SSN 801-51-1916.
  MISSED SSN     '510-44-2084'          in: Insurance claim for Priya Joshi (SSN 510-44-2084) at Mayo Clinic.
  MISSED EMAIL   'david.rao@clinic.net' in: Email david.rao@clinic.net about the appointment of Arjun Smith on 09/03/2022.
  MISSED PERSON  'Arjun Smith'          in: Email david.rao@clinic.net about the appointment of Arjun Smith on 09/03/2022.
  -- false positives (up to 12) --
  WRONG  ORG     'Arjun Brown'          in: Insurance claim for Arjun Brown (SSN 106-30-7924) at Manipal Hospitals.
  WRONG  PERSON  'arjun'                in: Patient John Kulkarni can be reached at 8116155940 or arjun.iyer@clinic.net.
  WRONG  ORG     'Ibuprofen'            in: What are common side effects of Ibuprofen and Paracetamol?
  WRONG  ORG     'Arjun Smith'          in: Email david.rao@clinic.net about the appointment of Arjun Smith on 09/03/2022.
  WRONG  PERSON  'Nagpur'               in: Refer Emily Gupta to Ruby Hall Clinic, Nagpur. Callback: 6482814893.
  WRONG  ORG     'Anjali Brown'         in: Email priya.joshi@example.com about the appointment of Anjali Brown on 22/08/2022.
  WRONG  ORG     'Kavya Reddy'          in: Summarize the medical record for Kavya Reddy, SSN 584-62-4119.
  WRONG  ORG     'Anjali Deshmukh'      in: Anjali Deshmukh from Nagpur reported chest pain; contact 6080132677.
  WRONG  ORG     'Nagpur'               in: Anjali Deshmukh from Nagpur reported chest pain; contact 6080132677.
  WRONG  PERSON  'david'                in: Patient John Singh can be reached at 9510799118 or david.brown@mail.org.
  WRONG  ORG     'Chennai'              in: Rohan Rao from Chennai reported chest pain; contact 6164005242.
  WRONG  ORG     'Amit Smith'           in: Email sara.sharma@example.com about the appointment of Amit Smith on 18/01/2024.

=== SPACY on adversarial (100 sentences) ===
label     gold  pred  strictP  strictR   lenP   lenR  leak%
AADHAAR      5     0     0.00     0.00   0.00   0.00   100%
DATE        10     0     0.00     0.00   0.00   0.00   100%
EMAIL       18     0     0.00     0.00   0.00   0.00    94%
LOCATION    32    30     0.93     0.88   0.93   0.88     9%
ORG         24    23     0.96     0.92   0.96   0.92     0%
PERSON      68    48     0.58     0.41   0.94   0.66    31%
PHONE       28     0     0.00     0.00   0.00   0.00   100%
SSN         25     0     0.00     0.00   0.00   0.00   100%
ALL        210   101     0.77     0.37   0.94   0.45    52%
  -- missed (up to 12) --
  MISSED PHONE   '71819 60013'          in: Call 71819 60013 or write to anjali.sharma@mail.org.
  MISSED EMAIL   'anjali.sharma@mail.org' in: Call 71819 60013 or write to anjali.sharma@mail.org.
  MISSED SSN     '529.38.8359'          in: my ssn: 529.38.8359
  MISSED DATE    '11 May 2021'          in: Admitted on 11 May 2021 at Mayo Clinic.
  MISSED AADHAAR '316155940781'         in: Aadhaar number 316155940781 belongs to Michael Deshmukh.
  MISSED SSN     '400.90.6925'          in: my ssn: 400.90.6925
  MISSED PHONE   '81316 47525'          in: Call 81316 47525 or write to neha.kulkarni@hospital.in.
  MISSED EMAIL   'neha.kulkarni@hospital.in' in: Call 81316 47525 or write to neha.kulkarni@hospital.in.
  MISSED PERSON  'anjali joshi'         in: Amber Brown met anjali joshi in New York.
  MISSED SSN     '423 61 5386'          in: summarize the record for anjali patel, ssn 423 61 5386.
  MISSED PHONE   '89696 53287'          in: Call 89696 53287 or write to amit.patel@example.com.
  MISSED EMAIL   'amit.patel@example.com' in: Call 89696 53287 or write to amit.patel@example.com.
  -- false positives (up to 12) --
  WRONG  PERSON  'michael'              in: Call 61656 67010 or write to michael.joshi@example.com.
  WRONG  ORG     'Sneha Deshmukh'       in: Aadhaar number 546247510799 belongs to Sneha Deshmukh.
  WRONG  LOCATION'Singh'                in: Patient April Singh lives in toronto.
  WRONG  LOCATION'Ruby Hall Clinic'     in: Admitted on 11 July 2023 at Ruby Hall Clinic.
  WRONG  PERSON  'nagpur'               in: refer vikram miller to Cleveland Clinic, nagpur.
  WRONG  PERSON  'Max Healthcare'       in: refer sneha johnson to Max Healthcare, mumbai.

=== HYBRID on clean (150 sentences) ===
label     gold  pred  strictP  strictR   lenP   lenR  leak%
AADHAAR      9     9     1.00     1.00   1.00   1.00     0%
DATE        18    18     1.00     1.00   1.00   1.00     0%
EMAIL       20    20     1.00     1.00   1.00   1.00     0%
LOCATION    32    23     0.96     0.69   0.96   0.69     9%
ORG         38    56     0.54     0.79   0.54   0.79     3%
PERSON      90    80     0.70     0.62   0.89   0.79     4%
PHONE       34    34     1.00     1.00   1.00   1.00     0%
SSN         29    29     1.00     1.00   1.00   1.00     0%
ALL        270   269     0.81     0.81   0.87   0.86     3%
  -- missed (up to 12) --
  MISSED PERSON  'Arjun Brown'          in: Insurance claim for Arjun Brown (SSN 106-30-7924) at Manipal Hospitals.
  MISSED PERSON  'Arjun Smith'          in: Email david.rao@clinic.net about the appointment of Arjun Smith on 09/03/2022.
  MISSED LOCATION'Nagpur'               in: Refer Emily Gupta to Ruby Hall Clinic, Nagpur. Callback: 6482814893.
  MISSED ORG     'Ruby Hall Clinic'     in: Refer Amit Smith to Ruby Hall Clinic, Toronto. Callback: 9824896383.
  MISSED PERSON  'Rahul Deshmukh'       in: Insurance claim for Rahul Deshmukh (SSN 824-90-1964) at Mayo Clinic.
  MISSED PERSON  'Anjali Brown'         in: Email priya.joshi@example.com about the appointment of Anjali Brown on 22/08/2022.
  MISSED PERSON  'Kavya Reddy'          in: Summarize the medical record for Kavya Reddy, SSN 584-62-4119.
  MISSED PERSON  'Anjali Deshmukh'      in: Anjali Deshmukh from Nagpur reported chest pain; contact 6080132677.
  MISSED LOCATION'Nagpur'               in: Anjali Deshmukh from Nagpur reported chest pain; contact 6080132677.
  MISSED PERSON  'Amit Reddy'           in: Insurance claim for Amit Reddy (SSN 478-46-3584) at Cleveland Clinic.
  MISSED LOCATION'Chennai'              in: Rohan Rao from Chennai reported chest pain; contact 6164005242.
  MISSED PERSON  'Amit Smith'           in: Email sara.sharma@example.com about the appointment of Amit Smith on 18/01/2024.
  -- false positives (up to 12) --
  WRONG  ORG     'Arjun Brown'          in: Insurance claim for Arjun Brown (SSN 106-30-7924) at Manipal Hospitals.
  WRONG  ORG     'Ibuprofen'            in: What are common side effects of Ibuprofen and Paracetamol?
  WRONG  ORG     'Arjun Smith'          in: Email david.rao@clinic.net about the appointment of Arjun Smith on 09/03/2022.
  WRONG  PERSON  'Nagpur'               in: Refer Emily Gupta to Ruby Hall Clinic, Nagpur. Callback: 6482814893.
  WRONG  ORG     'Anjali Brown'         in: Email priya.joshi@example.com about the appointment of Anjali Brown on 22/08/2022.
  WRONG  ORG     'Kavya Reddy'          in: Summarize the medical record for Kavya Reddy, SSN 584-62-4119.
  WRONG  ORG     'Anjali Deshmukh'      in: Anjali Deshmukh from Nagpur reported chest pain; contact 6080132677.
  WRONG  ORG     'Nagpur'               in: Anjali Deshmukh from Nagpur reported chest pain; contact 6080132677.
  WRONG  ORG     'Chennai'              in: Rohan Rao from Chennai reported chest pain; contact 6164005242.
  WRONG  ORG     'Amit Smith'           in: Email sara.sharma@example.com about the appointment of Amit Smith on 18/01/2024.
  WRONG  ORG     'Amit Brown'           in: Email michael.joshi@hospital.in about the appointment of Amit Brown on 12/11/2025.
  WRONG  ORG     'Chennai'              in: Rahul Iyer from Chennai reported chest pain; contact 7940196556.

=== HYBRID on adversarial (100 sentences) ===
label     gold  pred  strictP  strictR   lenP   lenR  leak%
AADHAAR      5     5     1.00     1.00   1.00   1.00     0%
DATE        10    10     1.00     1.00   1.00   1.00     0%
EMAIL       18    18     1.00     1.00   1.00   1.00     0%
LOCATION    32    30     0.93     0.88   0.93   0.88     9%
ORG         24    23     0.96     0.92   0.96   0.92     0%
PERSON      68    47     0.60     0.41   0.96   0.66    31%
PHONE       28    28     1.00     1.00   1.00   1.00     0%
SSN         25    25     1.00     1.00   1.00   1.00     0%
ALL        210   186     0.88     0.78   0.97   0.86    11%
  -- missed (up to 12) --
  MISSED PERSON  'anjali joshi'         in: Amber Brown met anjali joshi in New York.
  MISSED PERSON  'Amit Nair'            in: SSN is 742307916 for Amit Nair.
  MISSED PERSON  'amit patel'           in: summarize the record for amit patel, ssn 334 18 1514.
  MISSED PERSON  'rahul deshmukh'       in: summarize the record for rahul deshmukh, ssn 871 40 3724.
  MISSED PERSON  'kavya smith'          in: April Gupta met kavya smith in Bengaluru.
  MISSED PERSON  'amit reddy'           in: refer amit reddy to Sahyadri Hospital, mumbai.
  MISSED LOCATION'hyderabad'            in: refer anjali patel to Fortis Hospital, hyderabad.
  MISSED PERSON  'Sneha Deshmukh'       in: Aadhaar number 546247510799 belongs to Sneha Deshmukh.
  MISSED LOCATION'chennai'              in: Patient Grace Brown lives in chennai.
  MISSED PERSON  'kavya brown'          in: Reach kavya brown on +91 6164005242.
  MISSED PERSON  'Amber Sharma'         in: Amber Sharma met sneha deshmukh in Singapore.
  MISSED PERSON  'sneha deshmukh'       in: Amber Sharma met sneha deshmukh in Singapore.
  -- false positives (up to 12) --
  WRONG  ORG     'Sneha Deshmukh'       in: Aadhaar number 546247510799 belongs to Sneha Deshmukh.
  WRONG  LOCATION'Singh'                in: Patient April Singh lives in toronto.
  WRONG  LOCATION'Ruby Hall Clinic'     in: Admitted on 11 July 2023 at Ruby Hall Clinic.
  WRONG  PERSON  'nagpur'               in: refer vikram miller to Cleveland Clinic, nagpur.
  WRONG  PERSON  'Max Healthcare'       in: refer sneha johnson to Max Healthcare, mumbai.

=== COMPARISON (lenient precision / recall, leak rate) ===
strategy dataset       precision  recall  leak%
regex    clean              1.00    0.41    59%
regex    adversarial        1.00    0.41    59%
spacy    clean              0.75    0.46    42%
spacy    adversarial        0.94    0.45    52%
hybrid   clean              0.87    0.86     3%
hybrid   adversarial        0.97    0.86    11%