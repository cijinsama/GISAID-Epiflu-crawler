import argparse
import textwrap
import sys
import os
from .shared import IPipeline
from .util import Registry, parse_daterange, merge_fasta
from datetime import timedelta
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
            "--Lineage",
            type=str,
            default="",
            help="Family tree"
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
            "--Required_Segments",
            type=str,
            nargs="+",
            default=["HA"],
            help="Required Segments to filter sequence."
        )
        pipeline_parser.add_argument(
            "--Download_Segments",
            type=str,
            nargs="+",
            default=["HA"],
            help="Which segments to include in FASTA file"
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
            "--Download_dir",
            type=str,
            default="downloads",
            help="Download dir"
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
        Lineage,
        Host,
        Submission_Date,
        Required_Segments,
        Download_Segments,
        not_complete,
        Format,
        HeaderPattern,
        Timeout,
        Username, 
        Password,
        Download_dir,
        **kwargs
    ):
        from .chrome import setup_driver, login, goto_SearchPage, search, select_all, goto_download_frame, download_meta, download_protein, filters, TooMuchSeqError, wait_for_downloads
        start_date, end_date = parse_daterange(Submission_Date)
        original_start_date, original_end_date = start_date, end_date
        date_stack = [(start_date, end_date)]
        downloaded_stack = []
        while len(date_stack) > 0:
            start_date, end_date = date_stack.pop()
            try:
                driver = setup_driver(Download_dir)
                login(driver, Username, Password, Timeout)
                goto_SearchPage(driver, Timeout)
                filters(driver, SearchPatterns, Type, H, N, Lineage, Host, start_date, end_date, Required_Segments, not_complete, Timeout)
                try:
                    search(driver, Timeout)
                except TooMuchSeqError:
                    if start_date is not None and end_date is not None:
                        mid_date = start_date + (end_date - start_date) / 2
                        date_stack.append((start_date, mid_date))
                        date_stack.append((mid_date + timedelta(days=1), end_date))
                        print("Split date and retrying...")
                    else:
                        raise NotImplementedError("Currently don't support None date split. Please split date by yourself.")
                    continue
                select_all(driver, Timeout)
                goto_download_frame(driver, Timeout)
                if Format == "meta":
                    download_meta(driver, Timeout)
                    print("Waiting for the download to complete...", flush=True)
                    wait_for_downloads(os.path.join(Download_dir, "gisaid_epiflu_sequence.csv"))
                elif Format == "protein":
                    target = os.path.join(Download_dir, "gisaid_epiflu_sequence.fasta")
                    download_protein(driver, Timeout, HeaderPattern, Download_Segments)
                    print("Waiting for the download to complete...", flush=True)
                    wait_for_downloads(target)
                    os.rename(target, os.path.join(Download_dir, f"{start_date.strftime('%Y-%m-%d') if start_date is not None else ''}_{end_date.strftime('%Y-%m-%d') if end_date is not None else ''}.fasta"))
                    downloaded_stack.append(os.path.join(Download_dir, f"{start_date.strftime('%Y-%m-%d') if start_date is not None else ''}_{end_date.strftime('%Y-%m-%d') if end_date is not None else ''}.fasta"))
                else:
                    raise ValueError(f"Unknown format {Format}")
            finally:
                print("Quit driver.", flush=True)
                driver.quit()
        if Format == "protein":
            merge_fasta(downloaded_stack, os.path.join(Download_dir, f"{original_start_date.strftime('%Y-%m-%d')}_{original_end_date.strftime('%Y-%m-%d')}.fasta"))
        return 0