from app import LocationList, ProjectList, db

location_list = [
    # Assembly 1
    "CB1A", "CB1B", "CB1C", "CB1D", "CB1E",  "CB1F", "CB1G", "CB1H",
    "CB2A", "CB2B", "CB2C", "CB2D", "CB2E",  "CB2F",
    "CB3A", "CB3B", "CB3C", "CB3D", "CB3E",  "CB3F", "CB3G", "CB3H",
    "CB4A", "CB4B", "CB4C", "CB4D", "CB4E",  "CB4F", "CB4G", "CB4H",
    "CB5A", "CB5B", "CB5C", "CB5D", "CB5E",  "CB5F", "CB5G", "CB5H",
    "CB6A", "CB6B", "CB6C", "CB6D", "CB6E",  "CB6F", "CB6G", "CB6H",
    "CB7A", "CB7B", "CB7C", "CB7D", "CB7E",  "CB7F", "CB7G", "CB7H",
    # Assembly 2
    "CB8A", "CB8B", "CB8C", "CB8D", "CB8E",  "CB8F", "CB8G", "CB8H",
    "CB9A", "CB9B", "CB9C", "CB9D", "CB9E",  "CB9F", "CB9G", "CB9H",
    "CB10A", "CB10B", "CB10C", "CB10D", "CB10E",  "CB10F",
    "CB11A", "CB11B", "CB11C", "CB11D", "CB11E",  "CB11F",
    "CB12A", "CB12B", "CB12C", "CB12D", "CB12E",  "CB12F", "CB12G", "CB12H",
    "CB13A", "CB13B", "CB13C", "CB13D", "CB13E",  "CB13F", "CB13G", "CB13H",
    "CB14A", "CB14B", "CB14C", "CB14D", "CB14E",  "CB14F", "CB14G", "CB14H",
    # Assembly 3
    "CB15A", "CB15B", "CB15C", "CB15D",
    "CB16A", "CB16B", "CB16C", "CB16D",
    "CB17A", "CB17B", "CB17C", "CB17D",
    "CB18A", "CB18B", "CB18C", "CB18D",
]

# for i in range(len(location_list)):
#     print(f"{i+1}:{location_list[i]}")

#     obj = LocationList.query.filter_by(ID=i+1).first()
#     obj.Location = location_list[i]
#     db.session.commit()


# for locate in location_list:
#     obj = LocationList(Location=locate)
#     db.session.add(obj)

# # db.session.commit()

# for i in LocationList.query.all():
#     print(i.Location)

project_all = [
    [
        "Anupong",
        [
            "Robot Line 2 Frame Honing Machine",
            "Robot Line 2 Frame Drilling Machine.",
        ]
    ],
    [
        "Anuwat",
        [
            "Electric Testing & Running Machine at Process S259 F4-1",
        ]
    ],
    [
        "Arsan",
        [
            "Kanban Frame&Head to RFID",
            "LGV Platform Development",
            "Robot Crank Shaft C138,C148,C158,C198",
        ]
    ],
    [
        "Attapol",
        [
            "Robot Line 1 Head Honing MC F.4",
            "Robot Line 1 Head Drilling MC F.4",
        ]
    ],
    [
        "Chaiwut",
        [
            "Electric Testing Machine at Process AS16 Scroll F3",
            "New Life Test Z043 (R290)",
        ]
    ],
    [
        "Kanisorn",
        [
            "G027 Automation Line Shell Assy F4",
            "G037 Automation Line Shell Assy F4",
            "H027,H037 Automation Line Shell Assy F4",
            "H057 Automation Line Shell Assy F4",
            "Modify Robot line A167 ,A133",
            "Robot for Repress Stator ANB",
            "Robot Line 3 Frame Head Drilling&Spinning MC",
            "Robot Line 3 Frame Head Honing&Buffing MC",
        ]
    ],
    [
        "Kitti",
        [
            "Improve model change (Line 4)",
            "Robot A059c2 (U cylinder L1)",
            "Robot A059c6 (L cylinder L3)",
            "Robot MP039",
            "Robot MP049",
            "Setting Internal part",
        ]
    ],
    [
        "Norrarit",
        [
            "Calorie meter gas type phase 3 (Adding injection system)",
            "Running testing machine F.2 (N2 gas)",
        ]
    ],
    [
        "Prinpapar",
        [
            "Line Rework Nameplate",
            "Matching Stator & Shell Number(Assy4-2)",
            "Weight Checking Phase2 Improvement",
        ]
    ],
    [
        "Rungkaeo",
        [
            "Conveyor for stock part scroll washing machine F.3",
        ]
    ],
    [
        "Siwaroj",
        [
            "Improvement testing function WIT machine",
            "New Life Test Z044 (R290)",
        ]
    ],
    [
        "Soonthorn",
        [
            "Agv for delivery Casting F.1",
            "Agv for delivery Rotor&Rolling F.2",
            "Liftless for Assembly F.1",
            "Remove Dummy Jig AS18",
        ]
    ],
    [
        "Thanwa",
        [
            "Robot at CF062-063",
        ]
    ],
    [
        "Tuangyos",
        [
            "Auto Induction Brazing",
            "Auto Rework SubFrame",
            "Smart Loading",
        ]
    ],
    [
        "Wachiraphong",
        [
            "Cylinder Marking by Laser Mark",
            "Data Recording New Running Test Machine Final Line 3-1",
            "Matching Cylinder and Shell Number Assembly 4-2",
            "Matching Stator and Shell Number Assembly 4-1",
            "Reduce Manpower Line Base Factory 4",
            "Robot Fixed Scroll FS013",
            "SF Measuring Selector and Data Recording",
            "Smart Assembly AS09",
        ]
    ],
    [
        "Wanlop",
        [
            "M.Plate Data to RFID Tag Assy 4-1",
            "New Matching internal part 4-1",
            "New Matching internal part 4-2",
            "Robot for P019",
            "Vision Accessories part packing checking",
            "Vision comp outline checking",
        ]
    ],
]

# for project in project_all:
#     owner = project[0]
#     proj = project[1]

#     print(f"Owner : {owner}")
#     for a in proj:
#         print(a)
#     #     obj = ProjectList(Name=a, Owner=owner)
#     #     db.session.add(obj)

#     # db.session.commit()
#     print("\n")