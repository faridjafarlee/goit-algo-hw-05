import re
import timeit
from dataclasses import dataclass
from typing import Callable, List, Tuple, Dict, Optional

def bm_search(text: str, pattern: str) -> int:
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    if m > n:
        return -1

    skip = {}
    for i in range(m - 1):
        skip[pattern[i]] = m - 1 - i

    i = m - 1
    while i < n:
        k = 0
        while k < m and pattern[m - 1 - k] == text[i - k]:
            k += 1
        if k == m:
            return i - (m - 1)

        i += skip.get(text[i], m)

    return -1


def _build_lps(pattern: str) -> List[int]:
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps

def kmp_search(text: str, pattern: str) -> int:
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    if m > n:
        return -1

    lps = _build_lps(pattern)
    i = j = 0
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                return i - j
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1
    return -1


def rk_search(text: str, pattern: str) -> int:
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    if m > n:
        return -1

    base = 256
    mod = 1_000_000_007

    p_hash = 0
    t_hash = 0
    h = 1

    for _ in range(m - 1):
        h = (h * base) % mod

    for i in range(m):
        p_hash = (p_hash * base + ord(pattern[i])) % mod
        t_hash = (t_hash * base + ord(text[i])) % mod

    for i in range(n - m + 1):
        if p_hash == t_hash:
            if text[i:i+m] == pattern:
                return i

        if i < n - m:
            left = ord(text[i])
            right = ord(text[i + m])
            t_hash = (t_hash - (left * h) % mod + mod) % mod
            t_hash = (t_hash * base + right) % mod

    return -1


def best_time(fn: Callable[[], None], repeats: int = 10, number: int = 1) -> float:
    return min(timeit.repeat(fn, repeat=repeats, number=number))


def pick_existing_substring(text: str, length: int = 32) -> str:
    clean = re.sub(r"\s+", " ", text).strip()
    if len(clean) <= length:
        return clean
    start = len(clean) // 3
    return clean[start:start + length]


@dataclass
class AlgoResult:
    algo: str
    exist_s: float
    fake_s: float

@dataclass
class TextReport:
    label: str
    exist_sub: str
    fake_sub: str
    results: List[AlgoResult]
    fastest_algo: str


def run_for_text(label: str, text: str) -> TextReport:
    exist = pick_existing_substring(text, 32)
    fake = "qwertyuiopas"

    algos: List[Tuple[str, Callable[[str, str], int]]] = [
        ("Boyer–Moore", bm_search),
        ("KMP", kmp_search),
        ("Rabin–Karp", rk_search),
    ]

    results: List[AlgoResult] = []
    for name, fn in algos:
        t_exist = best_time(lambda: fn(text, exist), repeats=15, number=1)
        t_fake = best_time(lambda: fn(text, fake), repeats=15, number=1)
        results.append(AlgoResult(name, t_exist, t_fake))

    fastest = min(results, key=lambda r: r.exist_s + r.fake_s).algo
    return TextReport(label, exist, fake, results, fastest)


def write_conclusions(reports: List[TextReport], path: str = "conclusions.md") -> None:
    lines: List[str] = []
    lines.append("# Висновки щодо швидкості алгоритмів пошуку підрядка\n")

    for r in reports:
        lines.append(f"## {r.label}\n")
        lines.append(f"**Підрядок (існує):** `{r.exist_sub.replace('`', "'")}`\n")
        lines.append(f"**Підрядок (вигаданий):** `{r.fake_sub}`\n")
        lines.append("| Алгоритм | Час (існує), ms | Час (вигаданий), ms | Сума, ms |")
        lines.append("|---|---:|---:|---:|")
        for row in r.results:
            exist_ms = row.exist_s * 1000
            fake_ms = row.fake_s * 1000
            total_ms = exist_ms + fake_ms
            lines.append(f"| {row.algo} | {exist_ms:.4f} | {fake_ms:.4f} | {total_ms:.4f} |")
        lines.append(f"\n**Найшвидший для {r.label}:** **{r.fastest_algo}**\n")

    totals: Dict[str, List[float]] = {}
    for r in reports:
        for row in r.results:
            totals.setdefault(row.algo, []).append(row.exist_s + row.fake_s)

    overall_algo = min(totals.items(), key=lambda kv: sum(kv[1]) / len(kv[1]))[0]
    overall_avg_ms = (sum(totals[overall_algo]) / len(totals[overall_algo])) * 1000

    lines.append("## Загальний висновок\n")
    lines.append(f"У середньому по двох текстах (існує+вигаданий) найшвидший: **{overall_algo}** (avg total: {overall_avg_ms:.4f} ms)\n")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    with open("article_1.txt", "r", encoding="utf-8") as f:
        t1 = f.read()
    with open("article_2.txt", "r", encoding="utf-8") as f:
        t2 = f.read()

    r1 = run_for_text("Article 1", t1)
    r2 = run_for_text("Article 2", t2)

    write_conclusions([r1, r2], "conclusions.md")
    print("Готово: згенеровано conclusions.md")


if __name__ == "__main__":
    main()