import contextlib
import os
import sys
import time
from collections.abc import Mapping
from collections.abc import Sequence
from typing import Any
from typing import Dict
from typing import NamedTuple
from typing import Optional
from typing import Tuple

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

OrigamiRequest = dict[str, Any]
s3 = boto3.client("s3")
ORIGAMI_URL = "https://fashion-analytics.search.zalan.do/search/article/ad{ad}"
console = rich.console.Console()
new_names = {"trace.origami.timestamp": "last_updated", "sku": "config_sku"}


class SalesChannelInfo(NamedTuple):
    ad: int
    lang: str


scs = {
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
cc_to_sc = {info.lang[-2:]: sc for sc, info in scs.items()}
sc_to_cc = {sc: cc for cc, sc in cc_to_sc.items()}


def num(x: int, color: str = "green") -> str:
    return f"[{color}]{x:,}[/{color}]"


def get_headers():
    return {"Authorization": f"Bearer {token}", "Accept-Encoding": "gzip"}


def get_token() -> str:
    if os.getenv("ZTOKEN"):
        return os.getenv("ZTOKEN")
    if "auth" in globals() and type(auth).__name__ == "module":
        return auth.get_valid_token()
    return get_token_implicit_flow().get("access_token")


def origami_request_to_df(
        origami_request: OrigamiRequest, sc: str, lang: str | None = None
) -> tuple[pd.DataFrame, int]:
    sc_headers = {"Accept-Language": lang or scs[sc].lang, "X-Sales-Channel": sc}
    url = ORIGAMI_URL.format(ad=scs[sc].ad)
    r = http_client.post(url, json=origami_request, headers=sc_headers)
    origami_response = r.json()
    try:
        res = pd.json_normalize(origami_response["results"])
    except KeyError:
        console.log(r.text)
        console.log(origami_response)
        raise
    if len(res) > 0:
        res["sales_channel_id"] = sc
    return res, origami_response["total_count"]


def base_origami_request() -> OrigamiRequest:
    return {
        "offset": 0,
        "limit": 36_000,
        "select": {
            "include": [
                "trace.origami.timestamp",
                "sku",
            ]
        },
        "filters": [{"field": "is_out_of_stock", "terms": ["false"]}],
        "explain": False,
        "promote": False,
    }


token = get_token()
http_client = httpx.Client(headers=get_headers(), timeout=10.0)

avail_sc = {
    "00f2a393-6889-4fc0-8cd9-86e454e6dfa3",
    "01924c48-49bb-40c2-9c32-ab582e6db6f4",
    "043ec789-a3c7-4556-92df-bf1845c741ab",
    "091dcbdd-7839-4f39-aa05-324eb4599df0",
    "371e627a-2c44-4dbd-8e63-3344327a25c1",
    "4b8c533b-26b8-4c41-9a60-72a0df43d26f",
    "53075bd4-0205-4b5d-8145-e7a7745ab137",
    "733af55a-4133-4d7c-b5f3-d64d42c135fe",
    "7ce94f55-7a4d-4416-95c1-bf34193a47e8",
    "7fb9880f-de8d-4e56-bac1-5527da550a74",
    "8be9fe4a-397a-4bfb-9d1b-cfe7d01caf91",
    "a13a1960-5d57-4c51-a3ea-7e8d28e2c0b7",
    "aadd3adf-500f-4372-8137-dc0e4b2f0582",
    "b773b421-c719-4dfd-afc8-e97da508a88d",
    "b8949dea-af4e-42e7-8271-2e7b1bb123c5",
    "c2bd90da-0090-4751-8f16-35dea7002071",
    "ca9d5f22-2a1b-4799-b3b7-83f47c191489",
    "ebf57ebf-e26d-4ebd-8009-6ad519073d2a",
}

dfs = []
for cc, sc in list(cc_to_sc.items()):
    if sc not in avail_sc:
        console.print(f"skipping {sc!r}: {cc}")
        continue
    with Status(f"Getting SKUs from Origami in {sc_to_cc[sc]}…"):
        q = base_origami_request()
        q["negative_filters"] = [
            {"field": "boost.buckets.visible_inditex", "terms": ["0", "1"]}
        ]
        q["select"]["include"].extend(
            ["name", "boost.scores.web_learn_to_rank", "first_activated"]
        )
        tmp, tc = origami_request_to_df(q, sc)
        console.print(f"{tc:,} missing in {cc}")
        tmp = tmp.rename(columns=new_names)
        time.sleep(0.6)
        dfs.append(tmp)
df = pd.concat(dfs, ignore_index=True)
df["last_updated"] = pd.to_datetime(df["last_updated"], unit="ms")
df["first_activated"] = pd.to_datetime(df["first_activated"], unit="ms")
df.head()
