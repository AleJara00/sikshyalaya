from typing import List
from pydantic import Json
import datetime

users: List[Json] = [
    {
        "full_name": "Mike Hunt",
        "email": "mike.hunt@gmail.com",
        "is_active": True,
        "user_type": 2,
        "address": "Dhulikhel, Kavre",
        "group_id": None,
        "contact_number": "9849721522",
        "teacher_group": [],
        "dob": datetime.datetime(1970, 12, 12),
        "join_year": 1990,
        "password": "test",
    },
    {
        "full_name": "Yugesh Upadhyaya Luitel",
        "email": "yugu.luitel@gmail.com",
        "is_active": True,
        "user_type": 4,
        "roll": 38,
        "address": "Bafal, Kathmandu",
        "group_id": 2,
        "contact_number": "9861589390",
        "teacher_group": [],
        "dob": datetime.datetime(2001, 6, 13),
        "join_year": 2019,
        "password": "test",
    },
    {
        "full_name": "Arpan Koirala",
        "email": "arpan.koirala@gmail.com",
        "is_active": True,
        "user_type": 4,
        "roll": 34,
        "address": "Rampur, Palpa",
        "group_id": 2,
        "contact_number": "9821694321",
        "teacher_group": [],
        "dob": datetime.datetime(2001, 8, 1),
        "join_year": 2019,
        "password": "test",
    },
    {
        "full_name": "Rushab Humagain",
        "email": "rushab.humagain@gmail.com",
        "is_active": True,
        "user_type": 4,
        "address": "Banepa, Kavre",
        "group_id": 2,
        "contact_number": "9854632157",
        "teacher_group": [],
        "dob": datetime.datetime(2002, 11, 30),
        "join_year": 2020,
        "password": "test",
    },
    {
        "full_name": "Abhijeet Poudel",
        "email": "abhijeet.poudel@gmail.com",
        "is_active": True,
        "user_type": 4,
        "address": "Pokhara Airport Side, Pokhara",
        "group_id": 2,
        "contact_number": "9852891559",
        "teacher_group": [],
        "dob": datetime.datetime(2000, 12, 10),
        "join_year": 2018,
        "password": "test",
    },
    {
        "full_name": "Aatish Shrestha",
        "email": "aatish.shrestha@gmail.com",
        "is_active": True,
        "user_type": 4,
        "address": "Koteshowr, Kathmandu",
        "group_id": 2,
        "contact_number": "9845427715",
        "teacher_group": [],
        "dob": datetime.datetime(1998, 4, 12),
        "join_year": 2017,
        "password": "test",
    },
    {
        "full_name": "Suraj Chapagain ",
        "email": "suraj.chapagain@gmail.com",
        "is_active": True,
        "user_type": 3,
        "teacher_department_id": 3,
        "address": "Lake Side, Pokhara",
        "group_id": None,
        "contact_number": "9825852660",
        "teacher_group": [[3, 4], [11, 4]],
        "dob": datetime.datetime(1995, 1, 26),
        "join_year": 2020,
        "password": "test",
    },
    {
        "full_name": "Manoj Pandey",
        "email": "manoj.pandey@gmail.com",
        "is_active": True,
        "user_type": 3,
        "teacher_department_id": 2,
        "address": "Jitgadhi, Butwal",
        "group_id": None,
        "contact_number": "9833584635",
        "teacher_group": [[2, 3], [9, 2], [25, 1], [3, 3]],
        "dob": datetime.datetime(1885, 9, 14),
        "join_year": 2000,
        "password": "test",
    },
    {
        "full_name": "Om Nath Acharya",
        "email": "om.acharya@gmail.com",
        "is_active": False,
        "user_type": 3,
        "teacher_department_id": 4,
        "address": "Dhulikhel, Kavre",
        "group_id": None,
        "contact_number": "9875278464",
        "teacher_group": [[3, 5], [2, 5]],
        "dob": datetime.datetime(1980, 8, 14),
        "join_year": 2005,
        "password": "test",
    },
    {
        "full_name": "Sikshyalaya",
        "email": "sikshyalaya@gmail.com",
        "is_active": True,
        "user_type": 1,
        "address": "Sikshyalaya",
        "group_id": None,
        "contact_number": "9858630918",
        "teacher_group": [],
        "dob": datetime.datetime(2021, 1, 1),
        "join_year": 2021,
        "password": "test",
    },
    {
        "full_name": "Ishan Panta",
        "email": "ishan.panta@gmail.com",
        "is_active": True,
        "user_type": 4,
        "address": "Dhulikhel, Kathmandu",
        "group_id": 2,
        "contact_number": "9845234515",
        "teacher_group": [],
        "dob": datetime.datetime(1999, 2, 22),
        "join_year": 2020,
        "password": "test",
    },
    {
        "full_name": "Mullya Kun Thapa",
        "email": "mullu.kun@gmail.com",
        "is_active": True,
        "user_type": 4,
        "address": "Boys Hostel, Kathmandu University",
        "group_id": 2,
        "contact_number": "9846754715",
        "teacher_group": [],
        "dob": datetime.datetime(1999, 2, 22),
        "join_year": 2020,
        "password": "test",
    },
    {
        "full_name": "Mulyankan T. Sharma",
        "email": "mulyankun.t@gmail.com",
        "is_active": True,
        "user_type": 4,
        "address": "Kathmandu University, Kavre",
        "group_id": 2,
        "contact_number": "9842390715",
        "teacher_group": [],
        "dob": datetime.datetime(1999, 2, 22),
        "join_year": 2020,
        "password": "test",
    },
    {
        "full_name": "Sangharsha Paudel",
        "email": "sangharsha.paudel@gmail.com",
        "is_active": True,
        "user_type": 4,
        "address": "Boys Hostel, Kathmandu University",
        "group_id": 2,
        "contact_number": "9841265895",
        "teacher_group": [],
        "dob": datetime.datetime(1999, 2, 22),
        "join_year": 2020,
        "password": "test",
    },
]
