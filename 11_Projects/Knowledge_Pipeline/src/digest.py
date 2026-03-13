"""
Digest — LLM 自動消化模組

讀取 09_Staging/raw/ 的原始內容，呼叫 LLM 進行：
1. 自動摘要
2. 關鍵重點提取
3. 分類建議
4. 標籤建議
5. 結構化整理

輸出到 09_Staging/digested/

用法:
    python src/digest.py                  # 處理所有 raw/ 中的檔案
    python src/digest.py --file FILE      # 處理指定檔案
    python src/digest.py --dry-run        # 預覽不實際執行
"""

import argparse
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# 路徑設定
PROJECT_ROOT = Path(__file__).resolve().parent.parent
KB_ROOT = PROJECT_ROOT.parent.parent
RAW_DIR = KB_ROOT / "09_Staging" / "raw"
DIGESTED_DIR = KB_ROOT / "09_Staging" / "digested"

# LLM 設定
DIGEST_SYSTEM_PROMPT = """你是一位 AI 知識工程師，負責消化原始知識素材並產出結構化筆記。

你的任務：
1. 閱讀原始內容（YouTube 字幕、技術文章等）
2. 產出以下結構化內容：

## 摘要
用 3-5 句話總結核心內容。

## 關鍵重點
列出 5-10 個關鍵技術重點，用 bullet points。

## 核心概念
列出內容涉及的核心技術概念，每個概念用 1-2 句話解釋。

## 程式碼 / 實作要點
如果有相關程式碼或實作步驟，整理出來。沒有的話寫「無」。

## 延伸學習
建議的延伸探索方向或相關資源。

## 分類建議
建議這份知識應該入庫到哪個目錄，以及應該加上什麼標籤。

注意事項：
- 使用繁體中文
- 保留專有名詞的英文原文（如 Transformer, Attention, RAG）
- 重點標記用 **粗體**
- 如果是 YouTube 字幕，字幕可能有辨識錯誤，請根據上下文修正
"""


def get_llm_client() -> OpenAI:
    """取得 OpenAI / Azure OpenAI client"""
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")  # 可選，用於 Azure OpenAI

    if not api_key:
        raise ValueError(
            "請設定 OPENAI_API_KEY 環境變數。\n"
            "可在專案根目錄建立 .env 檔案：\n"
            "OPENAI_API_KEY=sk-...\n"
            "OPENAI_MODEL=gpt-4o  # 選用"
        )

    kwargs = {"api_key": api_key}
    if base_url:
        kwargs["base_url"] = base_url

    return OpenAI(**kwargs)


def digest_content(client: OpenAI, raw_content: str, model: str | None = None) -> str:
    """
    呼叫 LLM 消化原始內容

    Args:
        client: OpenAI client
        raw_content: 原始 Markdown 內容
        model: LLM 模型名稱

    Returns:
        LLM 產出的結構化內容
    """
    if model is None:
        model = os.getenv("OPENAI_MODEL", "gpt-4o")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": DIGEST_SYSTEM_PROMPT},
            {"role": "user", "content": f"請消化以下原始知識素材：\n\n---\n{raw_content}\n---"},
        ],
        temperature=0.3,
        max_tokens=4096,
    )

    return response.choices[0].message.content


def process_file(filepath: Path, client: OpenAI, dry_run: bool = False) -> Path | None:
    """
    消化單一檔案

    Args:
        filepath: raw/ 中的檔案路徑
        client: OpenAI client
        dry_run: 預覽模式

    Returns:
        digested/ 中的輸出路徑
    """
    print(f"[DIGEST] 消化中: {filepath.name}")

    raw_content = filepath.read_text(encoding="utf-8")

    if dry_run:
        print(f"  [DRY-RUN] 會處理 {len(raw_content)} 字元的內容")
        return None

    # 呼叫 LLM
    digested_content = digest_content(client, raw_content)

    # 在原始內容中插入 LLM 消化結果
    # 找到 "## 筆記" 和 "## 關鍵重點" 的位置並填入
    output_content = raw_content

    # 替換 Pending 標籤為 Digested
    output_content = output_content.replace("#Pending", "#Digested")

    # 在檔案末尾附加 LLM 消化結果
    output_content += f"""

---

## LLM 消化結果

> 消化時間: {datetime.now().strftime('%Y/%m/%d %H:%M')}
> 模型: {os.getenv('OPENAI_MODEL', 'gpt-4o')}

{digested_content}
"""

    # 輸出到 digested/
    DIGESTED_DIR.mkdir(parents=True, exist_ok=True)
    output_path = DIGESTED_DIR / filepath.name
    output_path.write_text(output_content, encoding="utf-8")

    print(f"[DONE] 已輸出到: {output_path.relative_to(KB_ROOT)}")
    return output_path


def process_all(client: OpenAI, dry_run: bool = False) -> list[Path]:
    """處理 raw/ 中所有檔案"""
    if not RAW_DIR.exists():
        print("[INFO] raw/ 目錄不存在或為空")
        return []

    files = [f for f in RAW_DIR.glob("*.md") if f.name != ".gitkeep"]
    if not files:
        print("[INFO] raw/ 中沒有待消化的檔案")
        return []

    print(f"[INFO] 找到 {len(files)} 個待消化檔案")

    results = []
    for f in sorted(files):
        result = process_file(f, client, dry_run)
        if result:
            results.append(result)

    print(f"\n[SUMMARY] 共消化 {len(results)}/{len(files)} 個檔案")
    return results


def main():
    parser = argparse.ArgumentParser(description="Digest — Knowledge Pipeline LLM 消化模組")
    parser.add_argument("--file", type=Path, help="指定要消化的檔案")
    parser.add_argument("--dry-run", action="store_true", help="預覽模式，不實際呼叫 LLM")
    parser.add_argument("--model", help="指定 LLM 模型（預設讀取 OPENAI_MODEL 環境變數）")

    args = parser.parse_args()

    if not args.dry_run:
        client = get_llm_client()
    else:
        client = None

    if args.file:
        process_file(args.file, client, args.dry_run)
    else:
        process_all(client, args.dry_run)


if __name__ == "__main__":
    main()
