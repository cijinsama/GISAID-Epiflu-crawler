import argparse
import textwrap
import sys
import os
from .shared import IPipeline
from .util import Registry, parse_daterange
import abc
from typing import Union
import time

PipelineRegistry = Registry("Pipeline")


@PipelineRegistry.register("EpiFlu")
class EpiFlu(IPipeline):
    @classmethod
    def setup_parser(
        cls,
        parser: Union[argparse.ArgumentParser, None] = None,
    ) -> argparse.ArgumentParser:
        parser = super().setup_parser(parser)
        pipeline_parser = parser.add_argument_group("pipeline")
        pipeline_parser.add_argument(
            "--Username",
            type=str,
            required=True,
            help="Username for GISAID"
        )
        pipeline_parser.add_argument(
            "--Password",
            type=str,
            required=True,
            help="Password for GISAID"
        )
        pipeline_parser.add_argument(
            "--SearchPatterns",
            type=str,
            default="",
            help="pattern used to filter viruses"
        )
        pipeline_parser.add_argument(
            "--Type",
            type=str,
            default="A",
            help="Virus type"
        )
        pipeline_parser.add_argument(
            "--H",
            type=str,
            default="3",
            help="Virus type"
        )
        pipeline_parser.add_argument(
            "--N",
            type=str,
            default="2",
            help="Virus type"
        )
        pipeline_parser.add_argument(
            "--Host",
            type=str,
            default="Human",
            help="Virus Host"
        )
        pipeline_parser.add_argument(
            "--Submission_Date",
            type=str,
            default="2020-12-11_2022-02-23", #string like 2020-12-11_2023-02-23
                                             #it can also be _2023-02-23
                                             #it can also be 2023-02-23_
            help="Sequence submission date. Input string like 2020-12-11_2023-02-23. It can also be _2023-02-23 for no start date or 2023-02-23_ for no end date"
        )
        pipeline_parser.add_argument(
            "--Segments",
            type=str,
            default="HA",
        )
        pipeline_parser.add_argument(
            "--HeaderPattern",
            type=str,
            default="Isolate name | Isolate ID",
            help="Header pattern used when you download protein."
        )
        pipeline_parser.add_argument(
            "--not_complete",
            action='store_false',
            help="Whether download incomplete ones"
        )
        pipeline_parser.add_argument(
            "--Format",
            choices=["protein", "meta"],
            type=str,
            default="protein",
            help="Which file you want to download. protein for fasta and meta for csv"
        )
        pipeline_parser.add_argument(
            "--Timeout",
            type=int,
            default=5,
            help="Time to prevent stucking"
        )
        return parser

    def __new__(
        cls,
        SearchPatterns,
        Type,
        H,
        N,
        Host,
        Submission_Date,
        Segments,
        not_complete,
        Format,
        HeaderPattern,
        Timeout,
        Username, 
        Password,
        **kwargs
    ):
        from .chrome import setup_driver, login, goto_SearchPage, search, select_all, goto_download_frame, download_meta, download_protein, filters
        start_date, end_date = parse_daterange(Submission_Date)
        driver = setup_driver()
        try:
            login(driver, Username, Password, Timeout)
            goto_SearchPage(driver, Timeout)
            filters(driver, SearchPatterns, Type, H, N, Host, start_date, end_date, Segments, not_complete, Timeout)
            search(driver, Timeout)
            select_all(driver, Timeout)
            goto_download_frame(driver, Timeout)
            if Format == "meta":
                download_meta(driver, Timeout)
            elif Format == "protein":
                download_protein(driver, Timeout, HeaderPattern)
            else:
                raise ValueError(f"Unknown format {Format}")
            print("Waiting for the download to complete...", flush=True)
            input("After Downloading, press any key to exit.")
        finally:
            print("Quit driver.", flush=True)
            driver.quit()
        return 0