from Crawler_GISAID.pipeline import EpiFlu
EpiFlu(
    "",
    "A",
    "1", #H
    "1", #N
    Host="Human",
    Submission_Date="2023-01-01_2023-12-31",
    Segments="HA",
    not_complete=False,
    Format="protein",
    HeaderPattern="Isolate name | Protein Accession no. | Isolate ID",
    Timeout=5,
    Username="YiLiu", 
    Password="Ftwzofyd",
    Download_dir="./download"
)