"""
Ingest — 自動分類入庫模組

讀取 09_Staging/reviewed/ 中通過審核的檔案，根據審核建議：
1. 自動分類到正確的知識庫目錄
2. 套用對應的模板格式
3. 更新標籤（移除 #Reviewed，加入正式標籤）
4. 更新 08_Bot_Knowledge/ 索引

用法:
    python src/ingest.py                  # 入庫所有 reviewed/ 中的檔案
    python src/ingest.py --file FILE      # 入庫指定檔案
    python src/ingest.py --dry-run        # 預覽不實際執行
"""

import argparse
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.table import Table

# 路徑設定
PROJECT_ROOT = Path(__file__).resolve().parent.parent
KB_ROOT = PROJECT_ROOT.parent.parent
REVIEWED_DIR = KB_ROOT / "09_Staging" / "reviewed"
BOT_KNOWLEDGE_DIR = KB_ROOT / "08_Bot_Knowledge"

# 分類對應表
CATEGORY_MAP = {
    "10_Learning/YouTube": KB_ROOT / "10_Learning" / "YouTube",
    "10_Learning/Articles": KB_ROOT / "10_Learning" / "Articles",
    "10_Learning/Online_Courses": KB_ROOT / "10_Learning" / "Online_Courses",
    "10_Learning/Books": KB_ROOT / "10_Learning" / "Books",
    "02_Concepts": KB_ROOT / "02_Concepts",
    "03_Architecture": KB_ROOT / "03_Architecture",
    "05_Prompts": KB_ROOT / "05_Prompts",
    "12_SOP": KB_ROOT / "12_SOP",
    "13_Insights/Trends": KB_ROOT / "13_Insights" / "Trends",
    "13_Insights/Conferences": KB_ROOT / "13_Insights" / "Conferences",
}

console = Console()


def detect_category(content: str) -> str | None:
    """
    從檔案內容中偵測建議分類

    優先讀取審核記錄中的建議分類，否則根據標籤推斷
    """
    # 嘗試從審核記錄中讀取
    match = re.search(r"\|\s*建議分類\s*\|\s*(.+?)\s*\|", content)
    if match:
        category = match.group(1).strip()
        if category != "N/A" and category in CATEGORY_MAP:
            return category

    # 根據標籤推斷
    if "#YouTube" in content:
        return "10_Learning/YouTube"
    if "#ArticleNote" in content:
        return "10_Learning/Articles"
    if "#BookNote" in content:
        return "10_Learning/Books"
    if "#Architecture" in content:
        return "03_Architecture"
    if "#Trend" in content:
        return "13_Insights/Trends"
    if "#SOP" in content:
        return "12_SOP"

    return None


def generate_ingest_filename(filepath: Path, category: str) -> str:
    """
    根據分類產生正式的入庫檔名

    移除日期前綴和來源類型前綴，保留有意義的標題
    """
    name = filepath.stem  # 不含 .md

    # 移除日期前綴 (YYYY-MM-DD_)
    name = re.sub(r"^\d{4}-\d{2}-\d{2}_", "", name)

    # 移除來源類型前綴 (youtube_, article_)
    name = re.sub(r"^(youtube|article|web)_", "", name)

    return f"{name}.md"


def clean_content_for_ingest(content: str) -> str:
    """
    清理內容以適合正式入庫

    - 移除 #Pending, #Digested, #Reviewed 等流程標籤
    - 保留正式標籤
    - 移除空白的 placeholder 區塊
    """
    # 移除流程標籤
    for tag in ["#Pending", "#Digested", "#Reviewed", "#Rejected"]:
        content = content.replace(f" {tag}", "").replace(tag, "")

    # 清理多餘空白
    content = re.sub(r"\n{3,}", "\n\n", content)

    return content


def update_bot_knowledge_index(ingested_files: list[dict]):
    """
    更新 08_Bot_Knowledge/ 的索引檔

    Args:
        ingested_files: 入庫記錄列表 [{"filename": ..., "category": ..., "date": ...}]
    """
    index_path = BOT_KNOWLEDGE_DIR / "INDEX.md"

    # 如果索引不存在，建立初始版本
    if not index_path.exists():
        BOT_KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
        header = """# Bot Knowledge 索引

> tags: #Meta #Bot

## 說明

此索引由 Knowledge Pipeline 自動維護，記錄所有通過審核入庫的知識文件。
AI Bot 從這裡查詢可用的知識來源。

## 知識清單

| 入庫日期 | 分類 | 檔案 |
|---|---|---|
"""
        index_path.write_text(header, encoding="utf-8")

    # 附加新入庫的記錄
    lines = []
    for record in ingested_files:
        date = record["date"]
        category = record["category"]
        filename = record["filename"]
        rel_path = record.get("rel_path", "")
        lines.append(f"| {date} | {category} | [{filename}](../{rel_path}) |")

    if lines:
        with open(index_path, "a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

        console.print(f"[green]📋 已更新 Bot Knowledge 索引（+{len(lines)} 筆）[/green]")


def ingest_file(filepath: Path, dry_run: bool = False) -> dict | None:
    """
    入庫單一檔案

    Args:
        filepath: reviewed/ 中的檔案
        dry_run: 預覽模式

    Returns:
        入庫記錄 dict 或 None
    """
    content = filepath.read_text(encoding="utf-8")

    # 偵測分類
    category = detect_category(content)
    if not category:
        console.print(f"[yellow]⚠️  無法偵測分類: {filepath.name}，跳過[/yellow]")
        return None

    dest_dir = CATEGORY_MAP.get(category)
    if not dest_dir:
        console.print(f"[yellow]⚠️  未知分類: {category}，跳過[/yellow]")
        return None

    # 產生入庫檔名
    ingest_filename = generate_ingest_filename(filepath, category)
    dest_path = dest_dir / ingest_filename

    console.print(f"[cyan]📦 {filepath.name}[/cyan]")
    console.print(f"   → 分類: {category}")
    console.print(f"   → 目標: {dest_path.relative_to(KB_ROOT)}")

    if dry_run:
        console.print("   [dim](dry-run, 不實際執行)[/dim]")
        return None

    # 清理內容
    cleaned = clean_content_for_ingest(content)

    # 寫入目標
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(cleaned, encoding="utf-8")

    # 移除 reviewed/ 中的來源檔
    filepath.unlink()

    record = {
        "filename": ingest_filename,
        "category": category,
        "date": datetime.now().strftime("%Y/%m/%d"),
        "rel_path": str(dest_path.relative_to(KB_ROOT)),
    }

    console.print("   [green]✅ 入庫完成[/green]")
    return record


def ingest_all(dry_run: bool = False) -> list[dict]:
    """入庫 reviewed/ 中所有檔案"""
    if not REVIEWED_DIR.exists():
        console.print("[yellow]reviewed/ 目錄不存在或為空[/yellow]")
        return []

    files = sorted(f for f in REVIEWED_DIR.glob("*.md") if f.name != ".gitkeep")
    if not files:
        console.print("[yellow]reviewed/ 中沒有待入庫的檔案[/yellow]")
        return []

    console.print(f"\n[bold]📦 找到 {len(files)} 個待入庫檔案[/bold]\n")

    records = []
    for filepath in files:
        record = ingest_file(filepath, dry_run)
        if record:
            records.append(record)

    # 更新 Bot Knowledge 索引
    if records and not dry_run:
        update_bot_knowledge_index(records)

    # 顯示統計
    console.print()
    table = Table(title="📊 入庫統計")
    table.add_column("分類")
    table.add_column("數量", justify="center")

    category_counts = {}
    for r in records:
        cat = r["category"]
        category_counts[cat] = category_counts.get(cat, 0) + 1

    for cat, count in sorted(category_counts.items()):
        table.add_row(cat, str(count))

    table.add_section()
    table.add_row("[bold]總計[/bold]", f"[bold]{len(records)}[/bold]")
    console.print(table)

    return records


def main():
    parser = argparse.ArgumentParser(description="Ingest — Knowledge Pipeline 入庫模組")
    parser.add_argument("--file", type=Path, help="入庫指定檔案")
    parser.add_argument("--dry-run", action="store_true", help="預覽模式")

    args = parser.parse_args()

    if args.file:
        ingest_file(args.file, args.dry_run)
    else:
        ingest_all(args.dry_run)


if __name__ == "__main__":
    main()
