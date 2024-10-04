import re

APPLICATION_STATUS_CHOICES = [
    ("pending", "Pending"),
    ("reviewed", "Reviewed"),
    ("selected", "selected"),
    ("rejected", "Rejected"),
]
JOB_STATUS_CHOICES = [("opened", "Opened"), ("closed", "Closed")]
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
    \+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|
2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|
4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$
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
