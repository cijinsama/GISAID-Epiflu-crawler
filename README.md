### GISAID Epiflu crawler
#### Install
```shell
pip install git+https://gitlab.lji.org/einav/GISAID-Epiflu-crawler.git
```
#### Usage
```shell
crawler EpiFlu --Username YOUR_USER_NAME_IN_GISAID --Password YOUR_PASSWORD_IN_GISAID
```

For more detail arguments:
```
usage: crawler [-h] --Username USERNAME --Password PASSWORD [--SearchPatterns SEARCHPATTERNS] [--Type TYPE] [--H H]
               [--N N] [--Lineage LINEAGE] [--Host HOST] [--Submission_Date SUBMISSION_DATE]
               [--Required_Segments REQUIRED_SEGMENTS [REQUIRED_SEGMENTS ...]]
               [--Download_Segments DOWNLOAD_SEGMENTS [DOWNLOAD_SEGMENTS ...]] [--HeaderPattern HEADERPATTERN]
               [--not_complete] [--Format {protein,meta}] [--Download_dir DOWNLOAD_DIR] [--Timeout TIMEOUT]
               {EpiFlu}

positional arguments:
  {EpiFlu}

optional arguments:
  -h, --help            show this help message and exit

pipeline:
  --Username USERNAME   Username for GISAID
  --Password PASSWORD   Password for GISAID
  --SearchPatterns SEARCHPATTERNS
                        pattern used to filter viruses
  --Type TYPE           Virus type
  --H H                 Virus type
  --N N                 Virus type
  --Lineage LINEAGE     Family tree
  --Host HOST           Virus Host
  --Submission_Date SUBMISSION_DATE
                        Sequence submission date. Input string like 2020-12-11_2023-02-23. It can also be _2023-02-23 for no start date or 2023-02-23_ for no end date
  --Required_Segments REQUIRED_SEGMENTS [REQUIRED_SEGMENTS ...]
                        Required Segments to filter sequence.
  --Download_Segments DOWNLOAD_SEGMENTS [DOWNLOAD_SEGMENTS ...]
                        Which segments to include in FASTA file
  --HeaderPattern HEADERPATTERN
                        Header pattern used when you download protein.
  --not_complete        Whether download incomplete ones
  --Format {protein,meta}
                        Which file you want to download. protein for fasta and meta for csv
  --Download_dir DOWNLOAD_DIR
                        Download dir
  --Timeout TIMEOUT     Time to prevent stucking
```

You can also use it with python. Examples are list in `test` folder.
