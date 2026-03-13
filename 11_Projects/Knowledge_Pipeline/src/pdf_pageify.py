from __future__ import annotations

from pathlib import Path
import re

SOURCE = Path("/Users/williamhuang/Library/Application Support/Code/User/workspaceStorage/9d876f5be2d3c3c30e9b2fd142d51e60/GitHub.copilot-chat/chat-session-resources/82e72875-5a91-4b37-b3ae-02838c4a4ec5/call_XIQ7yTWotW97IN2J4N2GvZiO__vscode-1773394961731/content.txt")
TARGET = Path("/Users/williamhuang/project/LLM筆記/AI-Knowledge-Base/09_Staging/raw/2026-03-09_PNLP課程講義_逐頁原始整理.md")
PDF_REL = "../01_Courses/Python中文NLP與LLM專家課程/assets/PNLP上課筆記_2026-03-09.pdf"


def normalize_page_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("•", "-")
    text = text.replace("●", "-")
    text = text.replace("→", "->")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_pages(text: str) -> list[tuple[int, str]]:
    segments = text.replace("\r\n", "\n").replace("\r", "\n").split("\u000c")
    pages: list[tuple[int, str]] = []
    fallback_page_num = 1

    for segment in segments:
        chunk = normalize_page_text(segment)
        if not chunk:
            continue

        lines = [line.strip() for line in chunk.splitlines()]
        while lines and not lines[0]:
            lines.pop(0)

        page_num = fallback_page_num
        if lines and re.fullmatch(r"\d+", lines[0]):
            page_num = int(lines[0])
            lines = lines[1:]
        elif len(lines) > 1 and re.fullmatch(r"\d+", lines[1]):
            page_num = int(lines[1])
            lines = [lines[0], *lines[2:]]

        body = "\n".join(lines).strip()
        if body:
            body = strip_page_number_noise(body, page_num)
            pages.append((page_num, body))
            fallback_page_num = page_num + 1

    merged: dict[int, list[str]] = {}
    for page_num, body in pages:
        merged.setdefault(page_num, []).append(body)
    return [(page_num, "\n\n".join(chunks).strip()) for page_num, chunks in sorted(merged.items())]


def infer_title(body: str) -> str:
    for line in body.splitlines():
        candidate = line.strip().strip("=").strip()
        if not candidate:
            continue
        if re.fullmatch(r"\d+", candidate):
            continue
        if len(candidate) > 80:
            continue
        return candidate
    return "未命名頁面"


def strip_page_number_noise(body: str, page_num: int) -> str:
    lines = body.splitlines()

    while lines and not lines[-1].strip():
        lines.pop()

    while lines and re.fullmatch(r"\d+", lines[-1].strip()):
        trailing_num = int(lines[-1].strip())
        if trailing_num in {page_num, page_num + 1}:
            lines.pop()
            while lines and not lines[-1].strip():
                lines.pop()
            continue
        break

    return "\n".join(lines).strip()


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    pages = split_pages(normalize_page_text(text))

    out: list[str] = []
    out.append("---")
    out.append('title: "PNLP 課程講義逐頁原始整理"')
    out.append("date: 2026-03-13")
    out.append("source_type: pdf")
    out.append("status: raw")
    out.append('source_pdf: "../01_Courses/Python中文NLP與LLM專家課程/assets/PNLP上課筆記_2026-03-09.pdf"')
    out.append("---\n")
    out.append("# PNLP 課程講義逐頁原始整理\n")
    out.append(f"> 原始檔案：[{Path(PDF_REL).name}]({PDF_REL})")
    out.append("> 說明：此檔為由 PDF 轉寫後切頁的原始整理稿，已保留頁碼，但尚未完成逐頁人工校訂與圖表視覺描述。\n")

    for page_num, body in pages:
        title = infer_title(body)
        out.append(f"## Page {page_num} — {title}\n")
        out.append("### 頁碼")
        out.append(f"- {page_num}\n")
        out.append("### 內容")
        out.append(body)
        out.append("")

    TARGET.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {len(pages)} pages to {TARGET}")


if __name__ == "__main__":
    main()
