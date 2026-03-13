"""
Web Crawler — 爬取技術文章與部落格

使用 httpx + BeautifulSoup 爬取網頁內容，輸出 Markdown 到 09_Staging/raw/

用法:
    python src/web_crawler.py --url "https://lilianweng.github.io/posts/..."
    python src/web_crawler.py --config  # 從 config/sources.yaml 讀取
"""

import argparse
import re
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import httpx
import yaml
from bs4 import BeautifulSoup

# 專案根目錄
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "sources.yaml"
KB_ROOT = PROJECT_ROOT.parent.parent  # AI-Knowledge-Base/
OUTPUT_DIR = KB_ROOT / "09_Staging" / "raw"

# 預設 User-Agent
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
}


def load_config() -> dict:
    """載入 sources.yaml 設定檔"""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def fetch_page(url: str, timeout: int = 30) -> str | None:
    """下載網頁 HTML"""
    try:
        with httpx.Client(headers=HEADERS, follow_redirects=True, timeout=timeout) as client:
            resp = client.get(url)
            resp.raise_for_status()
            return resp.text
    except httpx.HTTPError as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return None


def extract_article(html: str, selector: str = "article") -> dict:
    """
    從 HTML 中提取文章內容

    Args:
        html: 原始 HTML
        selector: 文章主體的 CSS selector

    Returns:
        包含 title, content, links, code_blocks 的字典
    """
    soup = BeautifulSoup(html, "html.parser")

    # 提取標題
    title = ""
    title_tag = soup.find("h1")
    if title_tag:
        title = title_tag.get_text(strip=True)
    elif soup.title:
        title = soup.title.get_text(strip=True)

    # 提取 meta description
    meta_desc = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta:
        meta_desc = meta.get("content", "")

    # 提取發布日期
    publish_date = ""
    time_tag = soup.find("time")
    if time_tag:
        publish_date = time_tag.get("datetime", time_tag.get_text(strip=True))

    # 提取主體內容
    article = soup.select_one(selector)
    if not article:
        article = soup.find("main") or soup.find("body")

    # 移除 script, style, nav, footer
    if article:
        for tag in article.find_all(["script", "style", "nav", "footer", "aside"]):
            tag.decompose()

    # 轉換為 Markdown-like 文字
    content = _html_to_markdown(article) if article else ""

    # 提取程式碼區塊
    code_blocks = []
    if article:
        for code in article.find_all("pre"):
            code_text = code.get_text(strip=True)
            if code_text:
                code_blocks.append(code_text)

    return {
        "title": title,
        "description": meta_desc,
        "publish_date": publish_date,
        "content": content,
        "code_blocks": code_blocks,
    }


def _html_to_markdown(element) -> str:
    """簡易 HTML 轉 Markdown"""
    lines = []

    for child in element.children:
        if hasattr(child, "name"):
            tag = child.name

            if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
                level = int(tag[1])
                text = child.get_text(strip=True)
                lines.append(f"\n{'#' * level} {text}\n")

            elif tag == "p":
                text = child.get_text(strip=True)
                if text:
                    lines.append(f"\n{text}\n")

            elif tag in ("ul", "ol"):
                for li in child.find_all("li", recursive=False):
                    text = li.get_text(strip=True)
                    prefix = "-" if tag == "ul" else "1."
                    lines.append(f"{prefix} {text}")
                lines.append("")

            elif tag == "pre":
                code = child.get_text()
                # 嘗試偵測語言
                lang = ""
                code_tag = child.find("code")
                if code_tag and code_tag.get("class"):
                    for cls in code_tag["class"]:
                        if cls.startswith("language-"):
                            lang = cls.replace("language-", "")
                            break
                lines.append(f"\n```{lang}\n{code}\n```\n")

            elif tag == "blockquote":
                text = child.get_text(strip=True)
                lines.append(f"\n> {text}\n")

            elif tag in ("strong", "b"):
                text = child.get_text(strip=True)
                lines.append(f"**{text}**")

            elif tag in ("em", "i"):
                text = child.get_text(strip=True)
                lines.append(f"*{text}*")

            elif tag == "img":
                alt = child.get("alt", "")
                src = child.get("src", "")
                if src:
                    lines.append(f"\n![{alt}]({src})\n")

            elif tag == "table":
                lines.append(_table_to_markdown(child))

            else:
                # 遞迴處理其他標籤
                text = child.get_text(strip=True)
                if text:
                    lines.append(text)
        else:
            # 純文字節點
            text = str(child).strip()
            if text:
                lines.append(text)

    return "\n".join(lines)


def _table_to_markdown(table) -> str:
    """將 HTML table 轉為 Markdown table"""
    rows = []
    for tr in table.find_all("tr"):
        cells = [td.get_text(strip=True) for td in tr.find_all(["th", "td"])]
        rows.append("| " + " | ".join(cells) + " |")
        if tr.find("th") and len(rows) == 1:
            rows.append("| " + " | ".join(["---"] * len(cells)) + " |")
    return "\n" + "\n".join(rows) + "\n"


def generate_markdown(url: str, article: dict, extra_tags: list[str] | None = None) -> str:
    """將文章轉為標準化 Markdown"""
    tags = ["#ArticleNote", "#SelfStudy", "#Pending"]
    if extra_tags:
        tags.extend(extra_tags)

    domain = urlparse(url).netloc

    md = f"""# {article['title']}

> tags: {' '.join(tags)}

## 基本資訊

| 項目 | 內容 |
|---|---|
| 來源 | [{domain}]({url}) |
| 發布日期 | {article['publish_date']} |
| 爬取日期 | {datetime.now().strftime('%Y/%m/%d')} |

## 摘要

{article['description']}

## 內容

{article['content']}

## 筆記

<!-- 消化階段由 LLM 填寫 -->

## 關鍵重點

<!-- 消化階段由 LLM 填寫 -->

## 個人心得

<!-- 咀嚼階段由人工填寫 -->
"""
    return md


def sanitize_filename(name: str) -> str:
    """清理檔名"""
    name = re.sub(r'[<>:"/\\|?*]', "", name)
    name = re.sub(r"\s+", "_", name)
    return name[:100]


def crawl_article(url: str, selector: str = "article",
                  extra_tags: list[str] | None = None) -> Path | None:
    """
    爬取單一文章

    Args:
        url: 文章 URL
        selector: 文章主體 CSS selector
        extra_tags: 額外標籤

    Returns:
        輸出檔案路徑
    """
    print(f"[CRAWL] 爬取文章: {url}")

    html = fetch_page(url)
    if not html:
        return None

    article = extract_article(html, selector)
    if not article["content"]:
        print(f"[WARN] 無法提取文章內容: {url}")
        return None

    md = generate_markdown(url, article, extra_tags)

    # 產生檔名
    date_str = datetime.now().strftime("%Y-%m-%d")
    title = sanitize_filename(article["title"] or urlparse(url).path.split("/")[-1])
    filename = f"{date_str}_article_{title}.md"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / filename
    output_path.write_text(md, encoding="utf-8")

    print(f"[DONE] 已儲存到: {output_path.relative_to(KB_ROOT)}")
    return output_path


def crawl_from_config() -> list[Path]:
    """從 config/sources.yaml 讀取來源並爬取"""
    config = load_config()
    settings = config.get("settings", {})
    delay = settings.get("request_delay", 2)
    output_paths = []

    websites = config.get("websites", {})

    for blog in websites.get("blogs", []):
        path = crawl_article(
            blog["url"],
            selector=blog.get("selector", "article"),
            extra_tags=blog.get("tags", []),
        )
        if path:
            output_paths.append(path)
        time.sleep(delay)

    return output_paths


def main():
    parser = argparse.ArgumentParser(description="Web Crawler — Knowledge Pipeline")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="爬取單一文章 URL")
    group.add_argument("--config", action="store_true", help="從 config/sources.yaml 讀取")
    parser.add_argument("--selector", default="article", help="文章主體 CSS selector")
    parser.add_argument("--tags", nargs="*", help="額外標籤")

    args = parser.parse_args()

    if args.url:
        crawl_article(args.url, args.selector, args.tags)
    elif args.config:
        crawl_from_config()


if __name__ == "__main__":
    main()
