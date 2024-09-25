import re

# STATUS = [
#     ("draft", "Draft"),
#     ("published", "Published"),
#     ("closed", "Closed"),
# ]
COMPANY_SIZE_CHOICES = [
    (1, "1-10"),
    (2, "11-50"),
    (3, "51-200"),
    (4, "201-500"),
    (5, "501-1000"),
    (6, "1001+"),
]
WORKPLACE_TYPES = [
    ("remote", "Remote"),
    ("hybrid", "Hybrid"),
    ("on-site", "On-Site"),
]
WORK_TYPES = [
    ("full_time", "Full Time"),
    ("part_time", "Part Time"),
    ("internship", "Internship"),
    ("contract", "Contract"),
]
PERIOD_CHOICES = [
    ("Per Hour", "Per Hour"),
    ("Per Day", "Per Day"),
    ("Per Week", "Per Week"),
    ("Per Month", "Per Month"),
    ("Per Year", "Per Year"),
]
MILITARY_STATUS_CHOICES = [
    ("Not Applicable", "Not Applicable"),
    ("Exempted", "Exempted"),
    ("Completed", "Completed"),
    ("Postponed", "Postponed"),
]
GENDER_CHOICES = [("Male", "Male"), ("Female", "Female")]
PHONE_REGEX = re.compile(
    r"""
    ^               # Start of string
    (\+?1[-.\s]?)?  # Optional country code for US (+1, 1-, 1., 1 )
    \(?(\d{3})\)?   # Area code, with or without parentheses
    [-.\s]?         # Optional separator (-, ., or space)
    (\d{3})         # First 3 digits
    [-.\s]?         # Optional separator (-, ., or space)
    (\d{4})         # Last 4 digits
    $               # End of string
""",
    re.VERBOSE,
)

DEGREE_CHOICES = [
    ("Associate", "Associate"),
    ("Bachelor", "Bachelor"),
    ("Master", "Master"),
    ("MBA", "MBA"),
    ("PhD", "PhD"),
    ("Certificate", "Certificate"),
    ("Diploma", "Diploma"),
    ("Other", "Other"),
]
