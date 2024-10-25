import argparse
import asyncio
from collections import defaultdict
from contextlib import AsyncExitStack
import glob
import importlib
import os
import sys
from typing import Callable
import prometheus_client
from anyio import AsyncFile, open_file, run


def load_exporter_configs(exporters_dir: str) -> dict[str, list[Callable]]:
    configs = defaultdict(list)
    sys.path.append(exporters_dir)
    for file_path in glob.glob(os.path.join(exporters_dir, "*.py")):
        exporter_module = importlib.import_module(os.path.basename(os.path.splitext(file_path)[0]))
        for log_file, line_parsers in exporter_module.PROMETHEUS_LOG_EXPORTER_CONFIG.items():
            configs[log_file].extend(line_parsers)
    return dict(configs)


async def track_file(log_io: AsyncFile[str], line_parsers: list[Callable], poll_delay: int) -> None:
    while True:
        async for line in log_io:
            for line_parser in line_parsers:
                line_parser(line)
        await asyncio.sleep(poll_delay)


async def export_metrics(configs: dict[str, list[Callable]], poll_delay: int) -> None:
    tasks = []
    async with AsyncExitStack() as stack:
        for log_file, line_parsers in configs.items():
            f = await stack.enter_async_context(await open_file(log_file))
            tasks.append(asyncio.ensure_future(track_file(f, line_parsers, poll_delay)))

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
