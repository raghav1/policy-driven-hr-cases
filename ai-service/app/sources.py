"""Read-only access to policy articles and cases.

ServiceNow is the source of truth. A local corpus directory stands in for it during development.
Create one source per process with make_source() and close it on shutdown.
"""

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import httpx

from app.config import Settings


@dataclass
class Article:
    sys_id: str
    number: str
    version: int
    title: str
    html: str
    published: bool
    category: str | None
    country: str | None


class Source(Protocol):
    def get_article(self, sys_id: str) -> Article | None: ...

    def list_articles(self) -> list[Article]: ...

    def get_case(self, number: str) -> dict | None: ...

    def close(self) -> None: ...


def parse_meta(meta: str) -> tuple[str | None, str | None]:
    """Article metadata lives in the KB meta field as 'area:leave country:DE'."""
    area = re.search(r"\barea:(\w+)", meta or "")
    country = re.search(r"\bcountry:(\w+)", meta or "")
    return (area.group(1).lower() if area else None, country.group(1).upper() if country else None)


def _sanitize(value: str) -> str:
    # '^' separates conditions in a ServiceNow encoded query; never let input add conditions.
    return value.replace("^", " ").strip()


_ARTICLE_FIELDS = "sys_id,number,short_description,text,meta,workflow_state,sys_mod_count"


class ServiceNowClient:
    """ServiceNow Table API as the read-only integration user. One connection pool per process."""

    def __init__(self, settings: Settings):
        self._table = settings.sn_case_table
        self._kb = settings.sn_hr_kb_sys_id
        self._http = httpx.Client(
            base_url=settings.sn_instance_url.rstrip("/"),
            auth=(settings.sn_user, settings.sn_password),
            headers={"Accept": "application/json"},
            timeout=20,
        )

    def close(self) -> None:
        self._http.close()

    def _get(self, path: str, params: dict) -> list[dict]:
        r = self._http.get(path, params=params)
        r.raise_for_status()
        return r.json()["result"]

    @staticmethod
    def _article(row: dict) -> Article:
        category, country = parse_meta(row.get("meta", ""))
        return Article(
            sys_id=row["sys_id"],
            number=row["number"],
            version=int(row.get("sys_mod_count") or 0),
            title=row["short_description"],
            html=row.get("text") or "",
            published=row.get("workflow_state") == "published",
            category=category,
            country=country,
        )

    def get_article(self, sys_id: str) -> Article | None:
        rows = self._get(
            "/api/now/table/kb_knowledge",
            {
                "sysparm_query": f"sys_id={_sanitize(sys_id)}^kb_knowledge_base={self._kb}",
                "sysparm_fields": _ARTICLE_FIELDS,
                "sysparm_limit": 1,
            },
        )
        return self._article(rows[0]) if rows else None

    def list_articles(self) -> list[Article]:
        rows = self._get(
            "/api/now/table/kb_knowledge",
            {
                "sysparm_query": f"kb_knowledge_base={self._kb}",
                "sysparm_fields": _ARTICLE_FIELDS,
                "sysparm_limit": 1000,
            },
        )
        return [self._article(r) for r in rows]

    def get_case(self, number: str) -> dict | None:
        rows = self._get(
            f"/api/now/table/{self._table}",
            {
                "sysparm_query": f"number={_sanitize(number)}",
                "sysparm_fields": "number,short_description,description,state,category,priority,"
                "assignment_group,comments,work_notes",
                "sysparm_display_value": "true",
                "sysparm_exclude_reference_link": "true",
                "sysparm_limit": 1,
            },
        )
        return rows[0] if rows else None


class LocalSource:
    """Reads the generated corpus (one JSON file per article) instead of ServiceNow."""

    def __init__(self, settings: Settings):
        self._dir = Path(settings.corpus_dir)

    def close(self) -> None:
        pass

    def _load(self, path: Path) -> Article:
        row = json.loads(path.read_text())
        category, country = parse_meta(row.get("meta", ""))
        return Article(
            sys_id=row["sys_id"],
            number=row["number"],
            version=int(row.get("version", 0)),
            title=row["title"],
            html=row["html"],
            published=row.get("workflow_state", "published") == "published",
            category=category,
            country=country,
        )

    def get_article(self, sys_id: str) -> Article | None:
        for path in self._dir.glob("*.json"):
            article = self._load(path)
            if article.sys_id == sys_id:
                return article
        return None

    def list_articles(self) -> list[Article]:
        return [self._load(p) for p in sorted(self._dir.glob("*.json"))]

    def get_case(self, number: str) -> dict | None:
        return None


def make_source(settings: Settings) -> Source:
    return (
        ServiceNowClient(settings) if settings.kb_source == "servicenow" else LocalSource(settings)
    )
