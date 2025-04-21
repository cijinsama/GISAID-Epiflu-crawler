from Crawler_GISAID.pipeline import EpiFlu
EpiFlu(
    "",
    "A",
    "3",
    "2",
    Host="Human",
    Submission_Date="2022-01-01_2022-12-31",
    Segments="HA",
    not_complete=False,
    Format="protein",
    HeaderPattern="Isolate name | Protein Accession no. | Isolate ID",
    Timeout=5,
    Username="YiLiu", 
    Password="Ftwzofyd",
    Download_dir="./download"
)