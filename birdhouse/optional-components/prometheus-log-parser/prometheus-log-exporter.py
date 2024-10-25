import argparse
import asyncio
from collections import defaultdict
from enum import Enum
import glob
import importlib
import os
import sys
from typing import Callable
import prometheus_client
from anyio import AsyncFile, open_file, run


class FileStates(Enum):
    NOCHANGE = 0
    TRUNCATED = 1
    DELETED = 2
    DIFFERENT = 3


def load_exporter_configs(exporters_dir: str) -> dict[str, list[Callable]]:
    configs = defaultdict(list)
    sys.path.append(exporters_dir)
    for file_path in glob.glob(os.path.join(exporters_dir, "*.py")):
        exporter_module = importlib.import_module(os.path.basename(os.path.splitext(file_path)[0]))
        for log_file, line_parsers in exporter_module.PROMETHEUS_LOG_EXPORTER_CONFIG.items():
            configs[log_file].extend(line_parsers)
    return dict(configs)


async def check_file_state(log_io: AsyncFile[str]):
    try:
        same_name_file_stat = os.stat(log_io.name)
    except FileNotFoundError:
        return FileStates.DELETED
    file_stat = os.stat(log_io.fileno())
    if same_name_file_stat == file_stat:
        if await log_io.tell() > file_stat.st_size:
            return FileStates.TRUNCATED
        else:
            return FileStates.NOCHANGE
    return FileStates.DIFFERENT


async def track_file(log_file: str, line_parsers: list[Callable], poll_delay: int) -> None:
    try:
        log_io = await open_file(log_file)
        while True:
            file_state = await check_file_state(log_io)
            if file_state == FileStates.NOCHANGE:
                async for line in log_io:
                    for line_parser in line_parsers:
                        line_parser(line)
            elif file_state == FileStates.TRUNCATED:
                await log_io.seek(0)
            elif file_state == FileStates.DIFFERENT:
                await log_io.aclose()
                log_io = await open_file(log_file)
            # if file is deleted, do nothing and wait to see if it is recreated later on
            await asyncio.sleep(poll_delay)
    finally:
        await log_io.aclose()


async def export_metrics(configs: dict[str, list[Callable]], poll_delay: int) -> None:
    tasks = []
    for log_file, line_parsers in configs.items():
        tasks.append(asyncio.ensure_future(track_file(log_file, line_parsers, poll_delay)))

    await asyncio.gather(*tasks)


def main(port: int, exporters_dir: str, poll_delay: int) -> None:
    prometheus_client.start_http_server(port)
    run(export_metrics, load_exporter_configs(exporters_dir), poll_delay)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--port", type=int, default=int(os.getenv("PROMETHEUS_LOG_PARSER_CLIENT_PORT", 8000))
    )
    parser.add_argument(
        "--exporters-dir",
        default=os.getenv(
            "PROMETHEUS_LOG_PARSER_EXPORTERS_DIR", os.path.join(os.getcwd(), "exporters.d")
        ),
    )
    parser.add_argument(
        "--poll-delay", type=int, default=int(os.getenv("PROMETHEUS_LOG_PARSER_POLL_DELAY", 1))
    )
    return parser.parse_args()


if __name__ == "__main__":
    main(**vars(parse_args()))
