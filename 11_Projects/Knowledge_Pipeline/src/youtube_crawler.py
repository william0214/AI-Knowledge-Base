"""
YouTube Crawler — 爬取 YouTube 影片字幕與 metadata

使用 yt-dlp 抓取影片資訊，輸出結構化 Markdown 到 09_Staging/raw/

用法:
    python src/youtube_crawler.py --url "https://youtube.com/watch?v=..."
    python src/youtube_crawler.py --channel "3Blue1Brown" --limit 5
    python src/youtube_crawler.py --config  # 從 config/sources.yaml 讀取
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import yaml

# 專案根目錄
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "sources.yaml"
KB_ROOT = PROJECT_ROOT.parent.parent  # AI-Knowledge-Base/
OUTPUT_DIR = KB_ROOT / "09_Staging" / "raw"


def load_config() -> dict:
    """載入 sources.yaml 設定檔"""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def extract_video_info(url: str, subtitle_langs: list[str] | None = None) -> dict | None:
    """
    使用 yt-dlp 提取影片資訊與字幕

    Args:
        url: YouTube 影片 URL
        subtitle_langs: 字幕語言偏好列表

    Returns:
        包含 title, channel, duration, description, subtitles 等的字典
    """
    if subtitle_langs is None:
        subtitle_langs = ["zh-Hant", "zh-Hans", "en"]

    cmd = [
        "yt-dlp",
        "--skip-download",
        "--print-json",
        "--write-sub",
        "--write-auto-sub",
        "--sub-langs", ",".join(subtitle_langs),
        "--sub-format", "vtt",
        "--no-warnings",
        url,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            print(f"[ERROR] yt-dlp failed for {url}: {result.stderr[:200]}")
            return None

        info = json.loads(result.stdout)
        return {
            "title": info.get("title", "Untitled"),
            "channel": info.get("channel", "Unknown"),
            "channel_url": info.get("channel_url", ""),
            "url": info.get("webpage_url", url),
            "duration": info.get("duration", 0),
            "upload_date": info.get("upload_date", ""),
            "description": (info.get("description", "") or "")[:500],
            "tags": info.get("tags", []),
            "view_count": info.get("view_count", 0),
            "subtitles": _extract_subtitles(info, subtitle_langs),
        }
    except subprocess.TimeoutExpired:
        print(f"[ERROR] yt-dlp timeout for {url}")
        return None
    except (json.JSONDecodeError, KeyError) as e:
        print(f"[ERROR] Failed to parse yt-dlp output: {e}")
        return None


def _extract_subtitles(info: dict, langs: list[str]) -> str:
    """從 yt-dlp 輸出中提取字幕文字"""
    # 嘗試手動字幕 → 自動字幕
    for sub_source in ["subtitles", "automatic_captions"]:
        subs = info.get(sub_source, {})
        for lang in langs:
            if lang in subs:
                # 取得 VTT 格式字幕的 URL，下載並清理
                for fmt in subs[lang]:
                    if fmt.get("ext") == "vtt":
                        return _download_and_clean_vtt(fmt["url"])
    return ""


def _download_and_clean_vtt(vtt_url: str) -> str:
    """下載 VTT 字幕並清理為純文字"""
    try:
        import httpx
        resp = httpx.get(vtt_url, timeout=30)
        resp.raise_for_status()
        vtt_text = resp.text

        # 移除 VTT header 和時間戳
        lines = []
        for line in vtt_text.split("\n"):
            # 跳過空行、時間戳行、VTT header
            if not line.strip():
                continue
            if re.match(r"^\d{2}:\d{2}", line):
                continue
            if line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
                continue
            # 移除 HTML tags
            clean = re.sub(r"<[^>]+>", "", line).strip()
            if clean and clean not in lines[-1:]:  # 去重連續重複行
                lines.append(clean)

        return "\n".join(lines)
    except Exception as e:
        print(f"[WARN] Failed to download subtitles: {e}")
        return ""


def format_duration(seconds: int) -> str:
    """將秒數轉為 HH:MM:SS 格式"""
    h, remainder = divmod(seconds, 3600)
    m, s = divmod(remainder, 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def generate_markdown(info: dict, extra_tags: list[str] | None = None) -> str:
    """
    將影片資訊轉為標準化 Markdown 格式

    Args:
        info: extract_video_info 回傳的字典
        extra_tags: 額外標籤

    Returns:
        Markdown 字串
    """
    tags = ["#YouTube", "#SelfStudy", "#Pending"]
    if extra_tags:
        tags.extend(extra_tags)

    upload_date = info.get("upload_date", "")
    if upload_date:
        upload_date = f"{upload_date[:4]}/{upload_date[4:6]}/{upload_date[6:]}"

    md = f"""# {info['title']}

> tags: {' '.join(tags)}

## 基本資訊

| 項目 | 內容 |
|---|---|
| 頻道 | [{info['channel']}]({info['channel_url']}) |
| 影片連結 | [YouTube]({info['url']}) |
| 時長 | {format_duration(info['duration'])} |
| 上傳日期 | {upload_date} |
| 觀看次數 | {info['view_count']:,} |
| 爬取日期 | {datetime.now().strftime('%Y/%m/%d')} |

## 影片描述

{info['description']}

## 字幕內容

{info['subtitles'] if info['subtitles'] else '<!-- 無可用字幕 -->'}

## 筆記

<!-- 消化階段由 LLM 填寫 -->

## 關鍵重點

<!-- 消化階段由 LLM 填寫 -->

## 個人心得

<!-- 咀嚼階段由人工填寫 -->
"""
    return md


def sanitize_filename(name: str) -> str:
    """清理檔名，移除不合法字元"""
    # 移除或替換不合法字元
    name = re.sub(r'[<>:"/\\|?*]', "", name)
    name = re.sub(r"\s+", "_", name)
    return name[:100]  # 限制長度


def crawl_video(url: str, extra_tags: list[str] | None = None) -> Path | None:
    """
    爬取單一 YouTube 影片，輸出 Markdown 到 09_Staging/raw/

    Args:
        url: YouTube 影片 URL
        extra_tags: 額外標籤

    Returns:
        輸出檔案路徑，失敗時回傳 None
    """
    print(f"[CRAWL] 爬取影片: {url}")
    info = extract_video_info(url)
    if not info:
        return None

    md = generate_markdown(info, extra_tags)

    # 產生檔名
    date_str = datetime.now().strftime("%Y-%m-%d")
    channel = sanitize_filename(info["channel"])
    title = sanitize_filename(info["title"])
    filename = f"{date_str}_youtube_{channel}_{title}.md"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / filename
    output_path.write_text(md, encoding="utf-8")

    print(f"[DONE] 已儲存到: {output_path.relative_to(KB_ROOT)}")
    return output_path


def crawl_channel(channel_url: str, limit: int = 5, extra_tags: list[str] | None = None) -> list[Path]:
    """
    爬取頻道最新影片

    Args:
        channel_url: YouTube 頻道 URL
        limit: 最多爬取幾部影片
        extra_tags: 額外標籤

    Returns:
        輸出檔案路徑列表
    """
    print(f"[CRAWL] 爬取頻道: {channel_url} (最新 {limit} 部)")

    # 取得頻道影片清單
    cmd = [
        "yt-dlp",
        "--flat-playlist",
        "--print", "url",
        "--playlist-items", f"1:{limit}",
        f"{channel_url}/videos",
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        urls = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
    except Exception as e:
        print(f"[ERROR] Failed to list channel videos: {e}")
        return []

    output_paths = []
    for url in urls:
        path = crawl_video(url, extra_tags)
        if path:
            output_paths.append(path)

    print(f"[DONE] 共爬取 {len(output_paths)}/{len(urls)} 部影片")
    return output_paths


def crawl_from_config() -> list[Path]:
    """從 config/sources.yaml 讀取來源清單並爬取"""
    config = load_config()
    output_paths = []

    # YouTube 頻道
    yt_config = config.get("youtube", {})
    settings = config.get("settings", {})
    limit = settings.get("max_items_per_source", 5)

    for channel in yt_config.get("channels", []):
        paths = crawl_channel(
            channel["url"],
            limit=limit,
            extra_tags=channel.get("tags", []),
        )
        output_paths.extend(paths)

    # YouTube 單一影片
    for video_url in yt_config.get("videos", []):
        path = crawl_video(video_url)
        if path:
            output_paths.append(path)

    return output_paths


def main():
    parser = argparse.ArgumentParser(description="YouTube Crawler — Knowledge Pipeline")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="爬取單一影片 URL")
    group.add_argument("--channel", help="爬取頻道 URL")
    group.add_argument("--config", action="store_true", help="從 config/sources.yaml 讀取來源")
    parser.add_argument("--limit", type=int, default=5, help="頻道模式下最多爬取幾部（預設 5）")
    parser.add_argument("--tags", nargs="*", help="額外標籤")

    args = parser.parse_args()

    if args.url:
        crawl_video(args.url, args.tags)
    elif args.channel:
        crawl_channel(args.channel, args.limit, args.tags)
    elif args.config:
        crawl_from_config()


if __name__ == "__main__":
    main()
