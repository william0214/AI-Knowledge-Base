"""
Review Gate — LLM 自動評分 + 人工審核閘門

讀取 09_Staging/digested/ 的消化後內容，分兩步把關：
1. LLM 自動評分（相關性、正確性、可操作性、時效性、獨特性）
2. 人工互動式審核（CLI 介面，approve / reject / edit）

通過的檔案移到 09_Staging/reviewed/
不通過的檔案移到 09_Staging/rejected/（保留紀錄）

用法:
    python src/review_gate.py               # 互動式審核所有 digested/ 檔案
    python src/review_gate.py --auto-only   # 僅 LLM 自動審核，不進人工
    python src/review_gate.py --file FILE   # 審核指定檔案
"""

import argparse
import json
import os
import shutil
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

load_dotenv()

# 路徑設定
PROJECT_ROOT = Path(__file__).resolve().parent.parent
KB_ROOT = PROJECT_ROOT.parent.parent
DIGESTED_DIR = KB_ROOT / "09_Staging" / "digested"
REVIEWED_DIR = KB_ROOT / "09_Staging" / "reviewed"
REJECTED_DIR = KB_ROOT / "09_Staging" / "rejected"
REVIEW_PROMPT_PATH = PROJECT_ROOT / "config" / "review_prompt.txt"

console = Console()


def get_llm_client() -> OpenAI:
    """取得 OpenAI client"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("請設定 OPENAI_API_KEY 環境變數")

    kwargs = {"api_key": api_key}
    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        kwargs["base_url"] = base_url

    return OpenAI(**kwargs)


def load_review_prompt() -> str:
    """載入審核 Prompt 模板"""
    return REVIEW_PROMPT_PATH.read_text(encoding="utf-8")


def llm_review(client: OpenAI, content: str) -> dict:
    """
    呼叫 LLM 進行自動審核評分

    Returns:
        LLM 回傳的審核結果 dict
    """
    prompt_template = load_review_prompt()
    prompt = prompt_template.replace("{content}", content)

    model = os.getenv("OPENAI_MODEL", "gpt-4o")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=1024,
        response_format={"type": "json_object"},
    )

    try:
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        console.print("[red]LLM 回傳格式錯誤，無法解析 JSON[/red]")
        return {"verdict": "needs-review", "total": 0, "reason": "JSON parse error"}


def display_review_result(filename: str, review: dict):
    """在終端顯示審核結果"""
    scores = review.get("scores", {})

    # 建立評分表格
    table = Table(title=f"🔍 審核結果: {filename}")
    table.add_column("維度", style="cyan")
    table.add_column("分數", justify="center")

    score_labels = {
        "relevance": "相關性",
        "accuracy": "正確性",
        "actionability": "可操作性",
        "timeliness": "時效性",
        "uniqueness": "獨特性",
    }

    for key, label in score_labels.items():
        score = scores.get(key, 0)
        style = "green" if score >= 4 else "yellow" if score >= 3 else "red"
        table.add_row(label, f"[{style}]{score}/5[/{style}]")

    total = review.get("total", sum(scores.values()))
    verdict = review.get("verdict", "needs-review")
    verdict_style = {
        "approve": "bold green",
        "auto-approve": "bold green",
        "needs-review": "bold yellow",
        "reject": "bold red",
    }.get(verdict, "white")

    table.add_section()
    table.add_row("總分", f"[bold]{total}/25[/bold]")
    table.add_row("判定", f"[{verdict_style}]{verdict.upper()}[/{verdict_style}]")

    console.print(table)

    # 顯示其他資訊
    if review.get("category"):
        console.print(f"  📂 建議分類: [cyan]{review['category']}[/cyan]")
    if review.get("suggested_tags"):
        console.print(f"  🏷️  建議標籤: {', '.join(review['suggested_tags'])}")
    if review.get("summary"):
        console.print(f"  📝 摘要: {review['summary']}")
    if review.get("reason"):
        console.print(f"  💬 原因: {review['reason']}")
    console.print()


def human_review(filepath: Path, review: dict) -> str:
    """
    人工互動式審核

    Returns:
        "approve" | "reject" | "skip" | "view"
    """
    while True:
        choice = Prompt.ask(
            "你的決定",
            choices=["approve", "reject", "skip", "view"],
            default="approve" if review.get("verdict") in ("approve", "auto-approve") else "skip",
        )

        if choice == "view":
            # 顯示完整內容
            content = filepath.read_text(encoding="utf-8")
            console.print(Panel(Markdown(content[:3000]), title=filepath.name))
            continue

        return choice


def move_file(filepath: Path, dest_dir: Path, review: dict | None = None):
    """
    移動檔案到目標目錄，並附加審核 metadata

    Args:
        filepath: 來源檔案
        dest_dir: 目標目錄
        review: 審核結果
    """
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / filepath.name

    content = filepath.read_text(encoding="utf-8")

    # 替換標籤
    content = content.replace("#Digested", "#Reviewed" if dest_dir == REVIEWED_DIR else "#Rejected")

    # 附加審核記錄
    if review:
        content += f"""

---

## 審核記錄

| 項目 | 內容 |
|---|---|
| 審核時間 | {datetime.now().strftime('%Y/%m/%d %H:%M')} |
| LLM 評分 | {review.get('total', 'N/A')}/25 |
| LLM 判定 | {review.get('verdict', 'N/A')} |
| 建議分類 | {review.get('category', 'N/A')} |
| 建議標籤 | {', '.join(review.get('suggested_tags', []))} |
"""

    dest_path.write_text(content, encoding="utf-8")

    # 刪除來源檔案
    filepath.unlink()
    console.print(f"  ✅ 已移至: {dest_path.relative_to(KB_ROOT)}")


def review_all(client: OpenAI, auto_only: bool = False) -> dict:
    """
    審核 digested/ 中所有檔案

    Returns:
        統計結果 {"approved": n, "rejected": n, "skipped": n}
    """
    if not DIGESTED_DIR.exists():
        console.print("[yellow]digested/ 目錄不存在或為空[/yellow]")
        return {"approved": 0, "rejected": 0, "skipped": 0}

    files = sorted(f for f in DIGESTED_DIR.glob("*.md") if f.name != ".gitkeep")
    if not files:
        console.print("[yellow]digested/ 中沒有待審核的檔案[/yellow]")
        return {"approved": 0, "rejected": 0, "skipped": 0}

    console.print(f"\n[bold]📋 找到 {len(files)} 個待審核檔案[/bold]\n")

    stats = {"approved": 0, "rejected": 0, "skipped": 0}

    for i, filepath in enumerate(files, 1):
        console.rule(f"[{i}/{len(files)}] {filepath.name}")

        content = filepath.read_text(encoding="utf-8")

        # Step 1: LLM 自動評分
        console.print("[dim]🤖 LLM 評分中...[/dim]")
        review = llm_review(client, content)
        display_review_result(filepath.name, review)

        verdict = review.get("verdict", "needs-review")

        if auto_only:
            # 自動模式：直接按 LLM 判定
            if verdict in ("approve", "auto-approve"):
                move_file(filepath, REVIEWED_DIR, review)
                stats["approved"] += 1
            elif verdict == "reject":
                move_file(filepath, REJECTED_DIR, review)
                stats["rejected"] += 1
            else:
                console.print("  ⏭️  需人工審核，跳過")
                stats["skipped"] += 1
        else:
            # 互動模式：人工最終決定
            decision = human_review(filepath, review)

            if decision == "approve":
                move_file(filepath, REVIEWED_DIR, review)
                stats["approved"] += 1
            elif decision == "reject":
                move_file(filepath, REJECTED_DIR, review)
                stats["rejected"] += 1
            else:
                stats["skipped"] += 1

    # 顯示統計
    console.print()
    summary = Table(title="📊 審核統計")
    summary.add_column("狀態")
    summary.add_column("數量", justify="center")
    summary.add_row("✅ 通過", str(stats["approved"]), style="green")
    summary.add_row("❌ 拒絕", str(stats["rejected"]), style="red")
    summary.add_row("⏭️  跳過", str(stats["skipped"]), style="yellow")
    console.print(summary)

    return stats


def main():
    parser = argparse.ArgumentParser(description="Review Gate — Knowledge Pipeline 審核閘門")
    parser.add_argument("--auto-only", action="store_true", help="僅 LLM 自動審核，不進人工")
    parser.add_argument("--file", type=Path, help="審核指定檔案")

    args = parser.parse_args()

    client = get_llm_client()

    if args.file:
        content = args.file.read_text(encoding="utf-8")
        review = llm_review(client, content)
        display_review_result(args.file.name, review)
        if not args.auto_only:
            decision = human_review(args.file, review)
            if decision == "approve":
                move_file(args.file, REVIEWED_DIR, review)
            elif decision == "reject":
                move_file(args.file, REJECTED_DIR, review)
    else:
        review_all(client, args.auto_only)


if __name__ == "__main__":
    main()
