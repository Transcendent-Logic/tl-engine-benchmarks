"""Report building blocks: ranking metrics, percentiles, markdown tables and charts.

Charts are emitted as Mermaid xychart blocks, which GitHub renders inline in job summaries, and
optionally as PNG files via matplotlib."""

import itertools
import json
import math
import os
from pathlib import Path


def ranking_metrics(scores: list[float], relevant: list[int]) -> tuple[float, float]:
    """nDCG@10 and reciprocal rank of the first relevant document."""
    ranked = sorted(range(len(scores)), key=lambda i: -scores[i])
    rel = set(relevant)
    dcg = sum(1 / math.log2(r + 2) for r, i in enumerate(ranked[:10]) if i in rel)
    idcg = sum(1 / math.log2(r + 2) for r in range(min(len(rel), 10)))
    rr = next((1 / (r + 1) for r, i in enumerate(ranked) if i in rel), 0.0)
    return dcg / idcg if idcg else 0.0, rr


def reference_metrics(out_dir: Path, prepared_dir: Path) -> dict:
    """nDCG@10 / MRR per set for every <set>.jsonl of reference scores in out_dir, against the
    labels in prepared_dir, and write them to out_dir/metrics.json. Robust to partial runs."""
    summary = {}
    for path in sorted(out_dir.glob("*.jsonl")):
        labels = {r["id"]: r["relevant"] for r in map(json.loads, open(prepared_dir / path.name))}
        m = [ranking_metrics(r["scores"], labels[r["id"]]) for r in map(json.loads, open(path)) if r["id"] in labels]
        if m:
            summary[path.stem] = {"requests": len(m), "ndcg@10": sum(x for x, _ in m) / len(m),
                                  "mrr": sum(x for _, x in m) / len(m)}
    (out_dir / "metrics.json").write_text(json.dumps(summary, indent=2))
    return summary


def pct(values, p: float) -> float:
    if not values:
        return math.nan
    s = sorted(values)
    k = (len(s) - 1) * p / 100
    f = math.floor(k)
    c = min(f + 1, len(s) - 1)
    return s[f] + (s[c] - s[f]) * (k - f)


def fmt(v) -> str:
    if isinstance(v, bool) or v is None:
        return {True: "✅", False: "❌", None: "–"}[v]
    if isinstance(v, int):
        return f"{v:,}"
    if isinstance(v, float):
        if math.isnan(v):
            return "–"
        return f"{v:,.0f}" if abs(v) >= 100 else f"{v:.1f}" if abs(v) >= 10 else f"{v:.3f}"
    return str(v)


HIGHLIGHT = "API"  # series drawn in HIGHLIGHT_COLOR in every chart (the endpoint under test)
HIGHLIGHT_COLOR = "#2ca02c"
PALETTE = ["#1f77b4", "#ff7f0e", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf", "#d62728",
           "#aec7e8", "#ffbb78", "#c5b0d5", "#c49c94", "#f7b6d2", "#c7c7c7", "#dbdb8d", "#9edae5", "#ff9896", "#98df8a"]


class Report:
    """Accumulates markdown; `write` saves it and appends it to the GitHub job summary if present."""

    def __init__(self, title: str):
        self.parts = [f"## {title}\n"]
        self.charts = []

    def h(self, text: str):
        self.parts.append(f"\n### {text}\n")

    def p(self, text: str):
        self.parts.append(text + "\n")

    def table(self, headers: list[str], rows: list[list]):
        lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
        lines += ["| " + " | ".join(fmt(v) for v in row) + " |" for row in rows]
        self.parts.append("\n".join(lines) + "\n")

    def chart(self, title: str, x: list, series: list[tuple[str, list[float]]], y_label: str,
              kind: str = "line", x_label: str = ""):
        """series: (name, values) pairs; kind 'line' or 'bar' (a 'bar' chart draws extra series as lines).
        Missing values (None/NaN) are gaps in the PNG; Mermaid cannot draw gaps, so a series with any
        missing value is left out of the Mermaid chart and listed as incomplete under it."""
        series = [(n, [math.nan if v is None else float(v) for v in vals]) for n, vals in series]
        series.sort(key=lambda sv: sv[0] != HIGHLIGHT)  # highlighted series first: it gets the first palette colour
        complete = [(n, vals) for n, vals in series if not any(math.isnan(v) for v in vals)]
        partial = [n for n, vals in series if any(math.isnan(v) for v in vals)]
        ymax = max((v for _, vals in complete for v in vals), default=1.0) or 1.0
        palette = ([HIGHLIGHT_COLOR] if complete and complete[0][0] == HIGHLIGHT else []) + PALETTE
        lines = ["```mermaid", '%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "' + ", ".join(palette) + '"}}}}%%',
                 "xychart-beta", f'    title "{title}"',
                 "    x-axis " + (f'"{x_label}" ' if x_label else "") + "[" + ", ".join(f'"{v}"' for v in x) + "]",
                 f'    y-axis "{y_label}" 0 --> {ymax * 1.1:.4g}']
        if kind == "stacked":  # Mermaid cannot stack: show the totals; the PNG has the segments
            totals = [sum(vals[i] for _, vals in series if not math.isnan(vals[i])) for i in range(len(x))]
            complete, partial = [("total", totals)], []
            ymax = max(totals, default=1.0) or 1.0
            lines[-1] = f'    y-axis "{y_label}" 0 --> {ymax * 1.1:.4g}'
        for i, (_, vals) in enumerate(complete):
            shape = "bar" if kind in ("bar", "stacked") and i == 0 else "line"
            lines.append(f"    {shape} [" + ", ".join(f"{v:.4g}" for v in vals) + "]")
        lines.append("```")
        legend = ", ".join(n for n, _ in complete)
        note = f" (incomplete, see table: {', '.join(partial)})" if partial else ""
        self.parts.append("\n".join(lines) + f"\n\n*{title}: {legend}{note}*\n")
        self.charts.append((title, x, series, y_label, kind, x_label))

    def write(self, path: Path, data=None):
        md = "\n".join(self.parts)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(md)
        if data is not None:
            path.with_suffix(".json").write_text(json.dumps(data, indent=1))
        if self.charts:
            self.png(path.with_suffix(".png"))
        if os.environ.get("GITHUB_STEP_SUMMARY"):
            with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
                f.write(md + "\n")
        print(md)

    def png(self, path: Path):
        """All charts stacked in <mode>.png, plus one <mode>-<k>.png per chart."""
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except ImportError:
            return

        def draw(ax, chart):
            title, x, series, y_label, kind, x_label = chart
            if kind == "bar":  # one bar per x label: drop labels without data, no legend, value on each bar
                keep = [i for i, v in enumerate(series[0][1]) if not math.isnan(v)]
                x = [x[i] for i in keep]
                series = [(n, [vals[i] for i in keep]) for n, vals in series]
            xs = range(len(x))
            if kind == "stacked":  # one bar per x label, one shaded segment per series (bucket)
                from matplotlib import colormaps
                from matplotlib.patches import Patch
                n = len(series)
                bottom = [0.0] * len(x)
                for i, (name, vals) in enumerate(series):
                    shade = 0.3 + 0.65 * i / max(1, n - 1)
                    vals = [0.0 if math.isnan(v) else v for v in vals]
                    ax.bar(xs, vals, bottom=bottom, width=0.7,
                           color=[colormaps["Greens"](shade) if str(lbl) == HIGHLIGHT else colormaps["Blues"](shade) for lbl in x],
                           edgecolor="white", linewidth=0.4)
                    bottom = [b + v for b, v in zip(bottom, vals)]
                for xi, total in zip(xs, bottom):
                    ax.text(xi, total, f"{total:.3g}", ha="center", va="bottom", fontsize=8)
                ax.legend(handles=[Patch(color=colormaps["Blues"](0.3 + 0.65 * i / max(1, n - 1)), label=name)
                                   for i, (name, _) in enumerate(series)], fontsize=7, title=x_label or None,
                          loc="upper left", bbox_to_anchor=(1.01, 1.0), borderaxespad=0)
                ax.set_xticks(list(xs), [str(v) for v in x], rotation=45 if len(x) > 8 else 0, ha="right" if len(x) > 8 else "center")
                ax.set_title(title)
                ax.set_ylabel(y_label)
                ax.grid(alpha=0.3, axis="y")
                ax.margins(y=0.15)
                return
            colors = itertools.cycle(PALETTE)
            for i, (name, vals) in enumerate(series):
                if kind == "bar" and i == 0:
                    bars = ax.bar(xs, vals, label=name, alpha=0.8,  # green if the bars are the highlighted series
                                  color=[HIGHLIGHT_COLOR if HIGHLIGHT in (name, str(lbl)) else PALETTE[0] for lbl in x])
                    ax.bar_label(bars, fmt="%.3g", fontsize=8, padding=2)
                elif name == HIGHLIGHT:
                    ax.plot(xs, vals, marker="o", label=name, color=HIGHLIGHT_COLOR, linewidth=2.5, zorder=5)
                else:
                    ax.plot(xs, vals, marker="o", label=name, color=next(colors))
            ax.set_xticks(list(xs), [str(v) for v in x], rotation=45 if len(x) > 8 else 0, ha="right" if len(x) > 8 else "center")
            ax.set_title(title)
            ax.set_ylabel(y_label)
            ax.set_xlabel(x_label)
            ax.grid(alpha=0.3)
            if not (kind == "bar" and len(series) == 1):
                if len(series) > 6:  # many series: legend beside the plot, never over the data
                    ax.legend(fontsize=7, loc="upper left", bbox_to_anchor=(1.01, 1.0), borderaxespad=0, ncol=1 + (len(series) > 12))
                else:
                    ax.legend(fontsize=8)
            if kind == "bar":
                ax.margins(y=0.15)

        n = len(self.charts)
        fig, axes = plt.subplots(n, 1, figsize=(9, 3.2 * n), squeeze=False)
        for ax, chart in zip(axes[:, 0], self.charts):
            draw(ax, chart)
        fig.tight_layout()
        fig.savefig(path, dpi=110)
        plt.close(fig)
        index = []
        for k, chart in enumerate(self.charts, 1):
            fig, ax = plt.subplots(figsize=(8, 3.2))
            draw(ax, chart)
            fig.tight_layout()
            file = path.with_name(f"{path.stem}-{k}.png")
            fig.savefig(file, dpi=110)
            plt.close(fig)
            index.append({"title": chart[0], "file": file.name})
        # title -> file index, so charts can be found by title rather than by number
        path.with_name(f"{path.stem}.charts.json").write_text(json.dumps(index, indent=1, ensure_ascii=False))
