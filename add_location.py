from app import LocationList, ProjectList, db

location_list = [
    # Assembly 1
    "A1CB1A", "A1CB1B", "A1CB1C", "A1CB1D", "A1CB1E",  "A1CB1F", "A1CB1G", "A1CB1H",
    "A1CB2A", "A1CB2B", "A1CB2C", "A1CB2D", "A1CB2E",  "A1CB2F",
    "A1CB3A", "A1CB3B", "A1CB3C", "A1CB3D", "A1CB3E",  "A1CB3F", "A1CB3G", "A1CB3H",
    "A1CB4A", "A1CB4B", "A1CB4C", "A1CB4D", "A1CB4E",  "A1CB4F", "A1CB4G", "A1CB4H",
    "A1CB5A", "A1CB5B", "A1CB5C", "A1CB5D", "A1CB5E",  "A1CB5F", "A1CB5G", "A1CB5H",
    "A1CB6A", "A1CB6B", "A1CB6C", "A1CB6D", "A1CB6E",  "A1CB6F", "A1CB6G", "A1CB6H",
    "A1CB7A", "A1CB7B", "A1CB7C", "A1CB7D", "A1CB7E",  "A1CB7F", "A1CB7G", "A1CB7H",
    # Assembly 2
    "A2CB1A", "A2CB1B", "A2CB1C", "A2CB1D", "A2CB1E",  "A2CB1F", "A2CB1G", "A2CB1H",
    "A2CB2A", "A2CB2B", "A2CB2C", "A2CB2D", "A2CB2E",  "A2CB2F", "A2CB2G", "A2CB2H",
    "A2CB3A", "A2CB3B", "A2CB3C", "A2CB3D", "A2CB3E",  "A2CB3F",
    "A2CB4A", "A2CB4B", "A2CB4C", "A2CB4D", "A2CB4E",  "A2CB4F",
    "A2CB5A", "A2CB5B", "A2CB5C", "A2CB5D", "A2CB5E",  "A2CB5F", "A2CB5G", "A2CB5H",
    "A2CB6A", "A2CB6B", "A2CB6C", "A2CB6D", "A2CB6E",  "A2CB6F", "A2CB6G", "A2CB6H",
    "A2CB7A", "A2CB7B", "A2CB7C", "A2CB7D", "A2CB7E",  "A2CB7F", "A2CB7G", "A2CB7H",
    # Assembly 3
    "A3CB1A", "A3CB1B", "A3CB1C", "A3CB1D",
    "A3CB2A", "A3CB2B", "A3CB2C", "A3CB2D",
    "A3CB3A", "A3CB3B", "A3CB3C", "A3CB3D",
    "A3CB4A", "A3CB4B", "A3CB4C", "A3CB4D",
]

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

for project in project_all:
    owner = project[0]
    proj = project[1]

    print(f"Owner : {owner}")
    for a in proj:
        print(a)
    #     obj = ProjectList(Name=a, Owner=owner)
    #     db.session.add(obj)

    # db.session.commit()
    print("\n")