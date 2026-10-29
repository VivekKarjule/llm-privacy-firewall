
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
AADHAAR      5     0     0.00     0.00   0.00   0.00   100%
DATE        10     0     0.00     0.00   0.00   0.00   100%
EMAIL       18    18     1.00     1.00   1.00   1.00     0%
LOCATION    32     0     0.00     0.00   0.00   0.00   100%
ORG         24     0     0.00     0.00   0.00   0.00   100%
PERSON      68     0     0.00     0.00   0.00   0.00   100%
PHONE       28    10     1.00     0.36   1.00   0.36    64%
SSN         25     0     0.00     0.00   0.00   0.00   100%
ALL        210    28     1.00     0.13   1.00   0.13    87%
  -- missed (up to 12) --
  MISSED PERSON  'Rose Brown'           in: Patient Rose Brown lives in bengaluru.
  MISSED LOCATION'bengaluru'            in: Patient Rose Brown lives in bengaluru.
  MISSED PHONE   '71819 60013'          in: Call 71819 60013 or write to anjali.sharma@mail.org.
  MISSED SSN     '529.38.8359'          in: my ssn: 529.38.8359
  MISSED PERSON  'rohan sharma'         in: refer rohan sharma to Ruby Hall Clinic, singapore.
  MISSED ORG     'Ruby Hall Clinic'     in: refer rohan sharma to Ruby Hall Clinic, singapore.
  MISSED LOCATION'singapore'            in: refer rohan sharma to Ruby Hall Clinic, singapore.
  MISSED DATE    '11 May 2021'          in: Admitted on 11 May 2021 at Mayo Clinic.
  MISSED ORG     'Mayo Clinic'          in: Admitted on 11 May 2021 at Mayo Clinic.
  MISSED AADHAAR '316155940781'         in: Aadhaar number 316155940781 belongs to Michael Deshmukh.
  MISSED PERSON  'Michael Deshmukh'     in: Aadhaar number 316155940781 belongs to Michael Deshmukh.
  MISSED SSN     '400.90.6925'          in: my ssn: 400.90.6925
  -- false positives (up to 12) --

=== SPACY on clean (150 sentences) ===
label     gold  pred  strictP  strictR   lenP   lenR  leak%
AADHAAR      9     0     0.00     0.00   0.00   0.00    78%
DATE        18     0     0.00     0.00   0.00   0.00    89%
EMAIL       20     0     0.00     0.00   0.00   0.00    90%
LOCATION    32    24     0.92     0.69   0.92   0.69     9%
ORG         38    88     0.34     0.79   0.34   0.79     3%
PERSON      90    88     0.64     0.62   0.81   0.79     4%
PHONE       34     0     0.00     0.00   0.00   0.00   100%
SSN         29     0     0.00     0.00   0.00   0.00   100%
ALL        270   200     0.54     0.40   0.61   0.46    41%
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
  WRONG  ORG     'SSN'                  in: Insurance claim for Rahul Kulkarni (SSN 833-93-9928) at Sahyadri Hospital.
  WRONG  ORG     'Arjun Brown'          in: Insurance claim for Arjun Brown (SSN 106-30-7924) at Manipal Hospitals.
  WRONG  ORG     'SSN'                  in: Summarize the medical record for Rohan Reddy, SSN 801-51-1916.
  WRONG  ORG     'SSN'                  in: Insurance claim for Priya Joshi (SSN 510-44-2084) at Mayo Clinic.
  WRONG  ORG     'Ibuprofen'            in: What are common side effects of Ibuprofen and Paracetamol?
  WRONG  ORG     'Arjun Smith'          in: Email david.rao@clinic.net about the appointment of Arjun Smith on 09/03/2022.
  WRONG  ORG     '09/03/2022'           in: Email david.rao@clinic.net about the appointment of Arjun Smith on 09/03/2022.
  WRONG  ORG     'SSN'                  in: Summarize the medical record for Sara Nair, SSN 470-38-3266.
  WRONG  ORG     'SSN'                  in: Summarize the medical record for Sneha Brown, SSN 887-92-6573.
  WRONG  PERSON  'Nagpur'               in: Refer Emily Gupta to Ruby Hall Clinic, Nagpur. Callback: 6482814893.
  WRONG  ORG     'anjali.deshmukh@example.com' in: Patient Neha Johnson can be reached at 6957015430 or anjali.deshmukh@example.com.
  WRONG  PERSON  'Aadhaar 9871'         in: Please draft a discharge note for Michael Williams, Aadhaar 9871 3315 0983.

=== SPACY on adversarial (100 sentences) ===
label     gold  pred  strictP  strictR   lenP   lenR  leak%
AADHAAR      5     0     0.00     0.00   0.00   0.00   100%
DATE        10     0     0.00     0.00   0.00   0.00   100%
EMAIL       18     0     0.00     0.00   0.00   0.00    94%
LOCATION    32    30     0.90     0.84   0.90   0.84    16%
ORG         24    38     0.58     0.92   0.58   0.92     0%
PERSON      68    37     0.78     0.43   0.97   0.53    43%
PHONE       28     0     0.00     0.00   0.00   0.00   100%
SSN         25     0     0.00     0.00   0.00   0.00   100%
ALL        210   105     0.74     0.37   0.81   0.40    57%
  -- missed (up to 12) --
  MISSED PHONE   '71819 60013'          in: Call 71819 60013 or write to anjali.sharma@mail.org.
  MISSED EMAIL   'anjali.sharma@mail.org' in: Call 71819 60013 or write to anjali.sharma@mail.org.
  MISSED SSN     '529.38.8359'          in: my ssn: 529.38.8359
  MISSED PERSON  'rohan sharma'         in: refer rohan sharma to Ruby Hall Clinic, singapore.
  MISSED DATE    '11 May 2021'          in: Admitted on 11 May 2021 at Mayo Clinic.
  MISSED AADHAAR '316155940781'         in: Aadhaar number 316155940781 belongs to Michael Deshmukh.
  MISSED SSN     '400.90.6925'          in: my ssn: 400.90.6925
  MISSED PHONE   '81316 47525'          in: Call 81316 47525 or write to neha.kulkarni@hospital.in.
  MISSED EMAIL   'neha.kulkarni@hospital.in' in: Call 81316 47525 or write to neha.kulkarni@hospital.in.
  MISSED PERSON  'anjali joshi'         in: Amber Brown met anjali joshi in New York.
  MISSED PERSON  'anjali patel'         in: summarize the record for anjali patel, ssn 423 61 5386.
  MISSED SSN     '423 61 5386'          in: summarize the record for anjali patel, ssn 423 61 5386.
  -- false positives (up to 12) --
  WRONG  ORG     'Aadhaar'              in: Aadhaar number 316155940781 belongs to Michael Deshmukh.
  WRONG  ORG     'SSN'                  in: SSN is 742307916 for Amit Nair.
  WRONG  ORG     'Reach'                in: Reach sara johnson on +91 9048281489.
  WRONG  LOCATION'kavya.johnson@hospital.in' in: Call 63911 71822 or write to kavya.johnson@hospital.in.
  WRONG  ORG     'Aadhaar'              in: Aadhaar number 383473829973 belongs to Kavya Gupta.
  WRONG  ORG     'Reach'                in: Reach david patel on +91 6500978820.
  WRONG  ORG     'Aadhaar'              in: Aadhaar number 546247510799 belongs to Sneha Deshmukh.
  WRONG  ORG     'Sneha Deshmukh'       in: Aadhaar number 546247510799 belongs to Sneha Deshmukh.
  WRONG  ORG     'SSN'                  in: SSN is 457185002 for Neha Singh.
  WRONG  ORG     'SSN'                  in: SSN is 548795956 for Rahul Singh.
  WRONG  ORG     'SSN'                  in: SSN is 658147049 for John Gupta.
  WRONG  ORG     'SSN'                  in: SSN is 142496974 for Priya Williams.

=== HYBRID on clean (150 sentences) ===
label     gold  pred  strictP  strictR   lenP   lenR  leak%
AADHAAR      9     7     1.00     0.78   1.00   0.78     0%
DATE        18    18     1.00     1.00   1.00   1.00     0%
EMAIL       20    20     1.00     1.00   1.00   1.00     0%
LOCATION    32    23     0.96     0.69   0.96   0.69     9%
ORG         38    85     0.35     0.79   0.35   0.79     3%
PERSON      90    88     0.64     0.62   0.81   0.79     4%
PHONE       34    34     1.00     1.00   1.00   1.00     0%
SSN         29    29     1.00     1.00   1.00   1.00     0%
ALL        270   304     0.71     0.80   0.76   0.86     3%
  -- missed (up to 12) --
  MISSED PERSON  'Arjun Brown'          in: Insurance claim for Arjun Brown (SSN 106-30-7924) at Manipal Hospitals.
  MISSED PERSON  'Arjun Smith'          in: Email david.rao@clinic.net about the appointment of Arjun Smith on 09/03/2022.
  MISSED LOCATION'Nagpur'               in: Refer Emily Gupta to Ruby Hall Clinic, Nagpur. Callback: 6482814893.
  MISSED ORG     'Ruby Hall Clinic'     in: Refer Amit Smith to Ruby Hall Clinic, Toronto. Callback: 9824896383.
  MISSED AADHAAR '9871 3315 0983'       in: Please draft a discharge note for Michael Williams, Aadhaar 9871 3315 0983.
  MISSED PERSON  'Rahul Deshmukh'       in: Insurance claim for Rahul Deshmukh (SSN 824-90-1964) at Mayo Clinic.
  MISSED PERSON  'Anjali Brown'         in: Email priya.joshi@example.com about the appointment of Anjali Brown on 22/08/2022.
  MISSED PERSON  'Kavya Reddy'          in: Summarize the medical record for Kavya Reddy, SSN 584-62-4119.
  MISSED AADHAAR '8513 3387 2624'       in: Please draft a discharge note for Sneha Patel, Aadhaar 8513 3387 2624.
  MISSED PERSON  'Anjali Deshmukh'      in: Anjali Deshmukh from Nagpur reported chest pain; contact 6080132677.
  MISSED LOCATION'Nagpur'               in: Anjali Deshmukh from Nagpur reported chest pain; contact 6080132677.
  MISSED PERSON  'Amit Reddy'           in: Insurance claim for Amit Reddy (SSN 478-46-3584) at Cleveland Clinic.
  -- false positives (up to 12) --
  WRONG  ORG     'SSN'                  in: Insurance claim for Rahul Kulkarni (SSN 833-93-9928) at Sahyadri Hospital.
  WRONG  ORG     'Arjun Brown'          in: Insurance claim for Arjun Brown (SSN 106-30-7924) at Manipal Hospitals.
  WRONG  ORG     'SSN'                  in: Summarize the medical record for Rohan Reddy, SSN 801-51-1916.
  WRONG  ORG     'SSN'                  in: Insurance claim for Priya Joshi (SSN 510-44-2084) at Mayo Clinic.
  WRONG  ORG     'Ibuprofen'            in: What are common side effects of Ibuprofen and Paracetamol?
  WRONG  ORG     'Arjun Smith'          in: Email david.rao@clinic.net about the appointment of Arjun Smith on 09/03/2022.
  WRONG  ORG     'SSN'                  in: Summarize the medical record for Sara Nair, SSN 470-38-3266.
  WRONG  ORG     'SSN'                  in: Summarize the medical record for Sneha Brown, SSN 887-92-6573.
  WRONG  PERSON  'Nagpur'               in: Refer Emily Gupta to Ruby Hall Clinic, Nagpur. Callback: 6482814893.
  WRONG  PERSON  'Aadhaar 9871'         in: Please draft a discharge note for Michael Williams, Aadhaar 9871 3315 0983.
  WRONG  ORG     'SSN'                  in: Insurance claim for Rahul Deshmukh (SSN 824-90-1964) at Mayo Clinic.
  WRONG  PERSON  'Email'                in: Email priya.joshi@example.com about the appointment of Anjali Brown on 22/08/2022.

=== HYBRID on adversarial (100 sentences) ===
label     gold  pred  strictP  strictR   lenP   lenR  leak%
AADHAAR      5     0     0.00     0.00   0.00   0.00   100%
DATE        10     0     0.00     0.00   0.00   0.00   100%
EMAIL       18    18     1.00     1.00   1.00   1.00     0%
LOCATION    32    29     0.93     0.84   0.93   0.84    16%
ORG         24    38     0.58     0.92   0.58   0.92     0%
PERSON      68    37     0.78     0.43   0.97   0.53    43%
PHONE       28    10     1.00     0.36   1.00   0.36    64%
SSN         25     0     0.00     0.00   0.00   0.00   100%
ALL        210   132     0.80     0.50   0.86   0.54    44%
  -- missed (up to 12) --
  MISSED PHONE   '71819 60013'          in: Call 71819 60013 or write to anjali.sharma@mail.org.
  MISSED SSN     '529.38.8359'          in: my ssn: 529.38.8359
  MISSED PERSON  'rohan sharma'         in: refer rohan sharma to Ruby Hall Clinic, singapore.
  MISSED DATE    '11 May 2021'          in: Admitted on 11 May 2021 at Mayo Clinic.
  MISSED AADHAAR '316155940781'         in: Aadhaar number 316155940781 belongs to Michael Deshmukh.
  MISSED SSN     '400.90.6925'          in: my ssn: 400.90.6925
  MISSED PHONE   '81316 47525'          in: Call 81316 47525 or write to neha.kulkarni@hospital.in.
  MISSED PERSON  'anjali joshi'         in: Amber Brown met anjali joshi in New York.
  MISSED PERSON  'anjali patel'         in: summarize the record for anjali patel, ssn 423 61 5386.
  MISSED SSN     '423 61 5386'          in: summarize the record for anjali patel, ssn 423 61 5386.
  MISSED PHONE   '89696 53287'          in: Call 89696 53287 or write to amit.patel@example.com.
  MISSED SSN     '742307916'            in: SSN is 742307916 for Amit Nair.
  -- false positives (up to 12) --
  WRONG  ORG     'Aadhaar'              in: Aadhaar number 316155940781 belongs to Michael Deshmukh.
  WRONG  ORG     'SSN'                  in: SSN is 742307916 for Amit Nair.
  WRONG  ORG     'Reach'                in: Reach sara johnson on +91 9048281489.
  WRONG  ORG     'Aadhaar'              in: Aadhaar number 383473829973 belongs to Kavya Gupta.
  WRONG  ORG     'Reach'                in: Reach david patel on +91 6500978820.
  WRONG  ORG     'Aadhaar'              in: Aadhaar number 546247510799 belongs to Sneha Deshmukh.
  WRONG  ORG     'Sneha Deshmukh'       in: Aadhaar number 546247510799 belongs to Sneha Deshmukh.
  WRONG  ORG     'SSN'                  in: SSN is 457185002 for Neha Singh.
  WRONG  ORG     'SSN'                  in: SSN is 548795956 for Rahul Singh.
  WRONG  ORG     'SSN'                  in: SSN is 658147049 for John Gupta.
  WRONG  ORG     'SSN'                  in: SSN is 142496974 for Priya Williams.
  WRONG  ORG     'Aadhaar'              in: Aadhaar number 834216073375 belongs to Emily Reddy.

=== COMPARISON (lenient precision / recall, leak rate) ===
strategy dataset       precision  recall  leak%
regex    clean              1.00    0.41    59%
regex    adversarial        1.00    0.13    87%
spacy    clean              0.61    0.46    41%
spacy    adversarial        0.81    0.40    57%
hybrid   clean              0.76    0.86     3%
hybrid   adversarial        0.86    0.54    44%