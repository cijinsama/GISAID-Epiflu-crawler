from Crawler_GISAID.pipeline import EpiFlu
"""
This is for H1N1 for 2024
"""
# EpiFlu(
#     "",
#     "A",
#     "1", #H
#     "1", #N
#     "",
#     Host="Human",
#     Submission_Date="2024-01-01_2024-12-31",
#     Segments=["HA"],
#     not_complete=False,
#     Format="protein",
#     HeaderPattern="Isolate name | Protein Accession no. | Isolate ID",
#     Timeout=5,
#     Username="YiLiu", 
#     Password="Ftwzofyd",
#     Download_dir="./download"
# )

"""
This is for H3N2 for 2023
"""
# EpiFlu(
#     "\"A/Hong Kong/4801/2014\"",
#     "A",
#     "3", #H
#     "2", #N
#     "",
#     Host="Human",
#     Submission_Date="2000-01-01_2050-12-31",
#     Segments=["NA"],
#     not_complete=False,
#     Format="protein",
#     HeaderPattern="Isolate name | Protein Accession no. | Isolate ID",
#     Timeout=5,
#     Username="YiLiu", 
#     Password="Ftwzofyd",
#     Download_dir="./download"
# )

"""
This is for B for 2023
"""
EpiFlu(
    "",
    "B",
    "", #H
    "", #N
    "Victoria",
    Host="Human",
    Submission_Date="2023-01-01_2023-12-31",
    Segments=["HA"],
    not_complete=False,
    Format="protein",
    HeaderPattern="Isolate name | Protein Accession no. | Isolate ID",
    Timeout=5,
    Username="YiLiu", 
    Password="Ftwzofyd",
    Download_dir="./download"
)