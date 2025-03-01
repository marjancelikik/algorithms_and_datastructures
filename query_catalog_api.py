import contextlib
import os
import sys
from typing import Any
from typing import NamedTuple
import re

try:
    import boto3
    import httpx
    import numpy as np
    import pandas as pd
    import rich
    from rich.status import Status
    from zign.api import get_token_implicit_flow
except ImportError:
    deps = ("httpx", "stups-zign", "pandas", "numpy", "rich", "boto3")
    msg = f"Install missing dependencies with\npython3 -m pip install {' '.join(deps)}"
    sys.exit(msg)
with contextlib.suppress(ImportError):
    import auth

Request = dict[str, Any]
s3 = boto3.client("s3")
CATALOG_API_URL = "https://catalog-api.search.zalan.do/api/entities?query={query}"
console = rich.console.Console()


class SalesChannelInfo(NamedTuple):
    ad: int
    lang: str


SALES_CHANNELS = {
    "01924c48-49bb-40c2-9c32-ab582e6db6f4": SalesChannelInfo(1, "de-DE"),
    "00f2a393-6889-4fc0-8cd9-86e454e6dfa3": SalesChannelInfo(5, "nl-NL"),
    "733af55a-4133-4d7c-b5f3-d64d42c135fe": SalesChannelInfo(11, "fr-FR"),
    "ebf57ebf-e26d-4ebd-8009-6ad519073d2a": SalesChannelInfo(15, "it-IT"),
    "83c4e87f-6819-41bb-af61-46cddb8453f5": SalesChannelInfo(16, "en-GB"),
    "53075bd4-0205-4b5d-8145-e7a7745ab137": SalesChannelInfo(19, "de-AT"),
    "c2bd90da-0090-4751-8f16-35dea7002071": SalesChannelInfo(20, "de-CH"),
    "ca9d5f22-2a1b-4799-b3b7-83f47c191489": SalesChannelInfo(24, "pl-PL"),
    "043ec789-a3c7-4556-92df-bf1845c741ab": SalesChannelInfo(25, "nl-BE"),
    "091dcbdd-7839-4f39-aa05-324eb4599df0": SalesChannelInfo(27, "sv-SE"),
    "aadd3adf-500f-4372-8137-dc0e4b2f0582": SalesChannelInfo(28, "fi-FI"),
    "7ce94f55-7a4d-4416-95c1-bf34193a47e8": SalesChannelInfo(29, "da-DK"),
    "1e161d6e-0427-4cfc-a357-e2b501188a15": SalesChannelInfo(30, "es-ES"),
    "ef064ea7-1d91-442c-bcbb-9d20749af19b": SalesChannelInfo(32, "no-NO"),
    "b773b421-c719-4dfd-afc8-e97da508a88d": SalesChannelInfo(47, "cs-CZ"),
    "a13a1960-5d57-4c51-a3ea-7e8d28e2c0b7": SalesChannelInfo(48, "en-IE"),
    "371e627a-2c44-4dbd-8e63-3344327a25c1": SalesChannelInfo(52, "sk-SK"),
    "b8949dea-af4e-42e7-8271-2e7b1bb123c5": SalesChannelInfo(53, "sl-SI"),
    "8a46930c-01ec-4027-98fd-23d304f247d6": SalesChannelInfo(54, "lt-LT"),
    "98478cb5-85f1-4775-a130-0b2413b1c4b8": SalesChannelInfo(55, "lv-LV"),
    "3d334e1f-112a-427f-96ae-e31948ed5163": SalesChannelInfo(56, "et-EE"),
    "8be9fe4a-397a-4bfb-9d1b-cfe7d01caf91": SalesChannelInfo(57, "hr-HR"),
    "4b8c533b-26b8-4c41-9a60-72a0df43d26f": SalesChannelInfo(58, "hu-HU"),
    "7fb9880f-de8d-4e56-bac1-5527da550a74": SalesChannelInfo(59, "ro-RO"),
}

CC_TO_SC = {info.lang: sc for sc, info in SALES_CHANNELS.items()}


def get_token() -> str:
    if os.getenv("ZTOKEN"):
        return os.getenv("ZTOKEN")
    if "auth" in globals() and type(auth).__name__ == "module":
        return auth.get_valid_token()
    return get_token_implicit_flow().get("access_token")


def get_default_headers() -> dict:
    return {"Authorization": f"Bearer {token}", "Accept-Encoding": "gzip", "Content-Type": "application/json"}


token = get_token()
http_client = httpx.Client(timeout=5.0)


def create_catalog_request(query: str, lang: str, sales_channel: str, additional_headers: dict):
    headers = {
        **get_default_headers(),
        **{"Accept-Language": lang or SALES_CHANNELS[sales_channel].lang,
           "X-Sales-Channel": sales_channel,
           "X-Zalando-Client-Id": "db4df249-63ab-46d3-b5f9-2f9ca782eccc"},
        **additional_headers
    }
    url = CATALOG_API_URL.format(query=query)
    return url, headers


def make_catalog_request(url: str, headers: dict):
    response = http_client.post(url, headers=headers).json()
    print(response)
    return response["entities"]


def is_query_contained_in_name(s1: str, s2: str):
    s1_tokens = [s.lower() for s in re.split('([^a-zA-Z0-9])', s1)]
    s2_tokens = set([s.lower() for s in re.split('([^a-zA-Z0-9])', s2)])
    all_terms_contained = all([s1_token in s2_tokens for s1_token in s1_tokens])
    return all_terms_contained


def compute_exact_match_rate(topk: int, queries: list, variant_headers=dict()):
    rate_sum = 0
    for query, lang in queries:
        url, headers = create_catalog_request(
            query,
            lang,
            CC_TO_SC[lang],
            variant_headers
        )
        articles = make_catalog_request(url, headers)[:topk]
        names = [" ".join([a["name"], a["brand_name"]]) for a in articles]
        print("\n".join(names))
        is_exact_match_list = [is_query_contained_in_name(query, name) for name in names]
        rate = len([_ for _ in is_exact_match_list if _]) / len(is_exact_match_list)
        rate_sum += rate

    return rate_sum / len(queries)


if __name__ == '__main__':
    topk = 10
    exact_match_rate = compute_exact_match_rate(
        topk=topk,
        queries=[("nike shoes", "de-DE")],
        variant_headers={"x-zalando-experiments": "sort-variant=force-base-layer-ranking-layer"}
    )
    print("Exact match rate @ {topk} = {exact_match_rate}".format(topk=topk, exact_match_rate=exact_match_rate))
    exact_match_rate = compute_exact_match_rate(
        topk=topk,
        queries=[("nike shoes", "de-DE")],
        # variant_headers={"x-zalando-experiments": "sort-variant=force-base-layer-ranking-layer"}
    )
    print("Exact match rate @ {topk} = {exact_match_rate}".format(topk=topk, exact_match_rate=exact_match_rate))
