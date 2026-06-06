from __future__ import annotations

import csv
from html import escape
import json
from pathlib import Path
from statistics import mean
from typing import Iterable


STATE_COLORS = {
    "susceptible": "#2878b5",
    "infected": "#d1495b",
    "recovered": "#16825d",
}
SCENARIO_COLORS = {
    "baseline": "#d1495b",
    "moderate_distancing": "#d98c10",
    "high_distancing": "#16825d",
    "high_transmission": "#6b4cc2",
}


def write_csv(path: Path, rows: Iterable[dict[str, object]]) -> None:
    rows = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV to {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def summarize_history(history: list[dict[str, int]]) -> dict[str, int | float]:
    peak_record = max(history, key=lambda record: record["infected"])
    final_record = history[-1]
    population = sum(final_record[state] for state in STATE_COLORS)
    ever_infected = final_record["infected"] + final_record["recovered"]
    return {
        "population": population,
        "duration_steps": final_record["step"],
        "peak_infected": peak_record["infected"],
        "peak_step": peak_record["step"],
        "final_susceptible": final_record["susceptible"],
        "final_recovered": final_record["recovered"],
        "attack_rate_percent": round(ever_infected / population * 100, 1),
    }


def write_demo_html(
    path: Path,
    config: dict[str, int | float],
    snapshots: list[dict[str, object]],
    summary: dict[str, int | float],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps({"config": config, "snapshots": snapshots})
    summary_markup = "".join(
        f"<li><strong>{escape(_label(key))}:</strong> {value}</li>"
        for key, value in summary.items()
    )
    html = f"""<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Epidemic ABM Demo</title>
<style>
* {{ box-sizing: border-box; }}
body {{ margin: 0; font: 16px system-ui, sans-serif; background: #f5f2ea; color: #17202a; }}
main {{ display: grid; grid-template-columns: minmax(320px, 760px) minmax(260px, 360px);
  min-height: 100vh; gap: 24px; padding: clamp(16px, 3vw, 42px); align-items: start; }}
h1, h2 {{ margin: 0 0 12px; letter-spacing: 0; }}
p {{ line-height: 1.45; }}
.board {{ width: min(100%, 760px); aspect-ratio: 1; background: #fffaf0;
  border: 1px solid #c8c0ae; box-shadow: 0 18px 42px #332b1f1f; }}
.panel {{ padding: 20px; border: 1px solid #d3c8b4; background: #fffaf1; border-radius: 8px; }}
.controls {{ display: grid; grid-template-columns: auto 1fr; gap: 12px; align-items: center; margin: 16px 0; }}
button {{ height: 42px; border: 0; border-radius: 6px; padding: 0 16px; color: white;
  background: #17202a; font-weight: 650; cursor: pointer; }}
input {{ width: 100%; accent-color: #d1495b; }}
.counts {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin: 12px 0; }}
.count {{ min-height: 78px; padding: 10px; border: 1px solid #dccfb8; border-radius: 6px; background: white; }}
.count b {{ display: block; font-size: clamp(20px, 2.5vw, 31px); }}
ul {{ margin: 10px 0 0; padding-left: 18px; line-height: 1.55; }}
.legend {{ display: flex; flex-wrap: wrap; gap: 14px; margin-bottom: 14px; }}
.legend span::before {{ content: ""; display: inline-block; width: 12px; height: 12px;
  border-radius: 50%; background: var(--swatch); margin-right: 6px; vertical-align: -1px; }}
@media (max-width: 820px) {{ main {{ grid-template-columns: 1fr; }} }}
</style>
<main>
  <section>
    <h1>Epidemic spread ABM</h1>
    <div class="legend">
      <span style="--swatch:{STATE_COLORS["susceptible"]}">Susceptible</span>
      <span style="--swatch:{STATE_COLORS["infected"]}">Infected</span>
      <span style="--swatch:{STATE_COLORS["recovered"]}">Recovered</span>
    </div>
    <canvas class="board" id="board" width="760" height="760" aria-label="Agent grid"></canvas>
  </section>
  <aside class="panel">
    <h2>Recorded run</h2>
    <p>Each dot is a person agent. Agents move on a wrapped grid, share infection
    risk when they meet, and recover after a fixed infection period.</p>
    <div class="controls">
      <button id="play" type="button">Play</button>
      <input id="step" type="range" min="0" value="0">
    </div>
    <strong id="stepLabel"></strong>
    <div class="counts">
      <div class="count">Susceptible<b id="sCount"></b></div>
      <div class="count">Infected<b id="iCount"></b></div>
      <div class="count">Recovered<b id="rCount"></b></div>
    </div>
    <h2>Run summary</h2>
    <ul>{summary_markup}</ul>
  </aside>
</main>
<script id="payload" type="application/json">{payload}</script>
<script>
const data = JSON.parse(document.querySelector("#payload").textContent);
const canvas = document.querySelector("#board");
const ctx = canvas.getContext("2d");
const slider = document.querySelector("#step");
const play = document.querySelector("#play");
const snapshots = data.snapshots;
const colors = {json.dumps(STATE_COLORS)};
slider.max = snapshots.length - 1;
let timer = null;

function draw(index) {{
  const frame = snapshots[index];
  const cellW = canvas.width / data.config.width;
  const cellH = canvas.height / data.config.height;
  ctx.fillStyle = "#fffaf0";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.strokeStyle = "#eadfca";
  ctx.lineWidth = 1;
  for (let x = 0; x <= data.config.width; x++) {{
    ctx.beginPath(); ctx.moveTo(x * cellW, 0); ctx.lineTo(x * cellW, canvas.height); ctx.stroke();
  }}
  for (let y = 0; y <= data.config.height; y++) {{
    ctx.beginPath(); ctx.moveTo(0, y * cellH); ctx.lineTo(canvas.width, y * cellH); ctx.stroke();
  }}
  frame.agents.forEach((agent) => {{
    const offset = ((agent.id % 5) - 2) * Math.min(cellW, cellH) * 0.09;
    ctx.beginPath();
    ctx.fillStyle = colors[agent.state];
    ctx.arc((agent.x + 0.5) * cellW + offset, (agent.y + 0.5) * cellH - offset,
      Math.max(3.5, Math.min(cellW, cellH) * 0.24), 0, Math.PI * 2);
    ctx.fill();
    if (agent.distancing) {{
      ctx.strokeStyle = "#17202a";
      ctx.lineWidth = 1.2;
      ctx.stroke();
    }}
  }});
  document.querySelector("#stepLabel").textContent = `Step ${{frame.step}} of ${{snapshots.at(-1).step}}`;
  document.querySelector("#sCount").textContent = frame.counts.susceptible;
  document.querySelector("#iCount").textContent = frame.counts.infected;
  document.querySelector("#rCount").textContent = frame.counts.recovered;
}}

function stop() {{
  clearInterval(timer);
  timer = null;
  play.textContent = "Play";
}}
play.addEventListener("click", () => {{
  if (timer) return stop();
  play.textContent = "Pause";
  timer = setInterval(() => {{
    slider.value = Number(slider.value) >= snapshots.length - 1 ? 0 : Number(slider.value) + 1;
    draw(Number(slider.value));
  }}, 170);
}});
slider.addEventListener("input", () => {{ stop(); draw(Number(slider.value)); }});
draw(0);
</script>
</html>
"""
    path.write_text(html, encoding="utf-8")


def write_experiment_report(
    path: Path,
    mean_histories: dict[str, list[dict[str, float]]],
    summaries: list[dict[str, object]],
) -> None:
    chart = _infected_curve_svg(mean_histories)
    summary_rows = "\n".join(
        "<tr>"
        + "".join(f"<td>{escape(str(row[key]))}</td>" for key in row)
        + "</tr>"
        for row in summaries
    )
    header_cells = "".join(f"<th>{escape(_label(key))}</th>" for key in summaries[0])
    html = f"""<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Epidemic ABM Experiment Report</title>
<style>
body {{ margin: 0; background: #f6f3eb; color: #16212a; font: 16px system-ui, sans-serif; }}
main {{ max-width: 1120px; margin: auto; padding: clamp(18px, 4vw, 54px); }}
h1, h2 {{ letter-spacing: 0; }}
.plot, table {{ width: 100%; background: #fffaf1; border: 1px solid #d8ccb7; border-radius: 8px; }}
.plot {{ padding: 12px; overflow-x: auto; }}
table {{ border-collapse: collapse; overflow: hidden; }}
th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #e3d8c4; }}
th {{ background: #17202a; color: white; font-size: 14px; }}
p {{ max-width: 76ch; line-height: 1.5; }}
</style>
<main>
  <h1>Experiment report: distancing and epidemic spread</h1>
  <p>The chart compares mean infected agents across repeated runs. A lower and
  flatter infection curve indicates that the health rule changes the system-level outcome.</p>
  <div class="plot">{chart}</div>
  <h2>Scenario summary</h2>
  <table><thead><tr>{header_cells}</tr></thead><tbody>{summary_rows}</tbody></table>
</main>
</html>
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")


def aggregate_histories(
    rows: list[dict[str, object]],
) -> dict[str, list[dict[str, float]]]:
    scenarios = sorted({str(row["scenario"]) for row in rows})
    result: dict[str, list[dict[str, float]]] = {}
    for scenario in scenarios:
        scenario_rows = [row for row in rows if row["scenario"] == scenario]
        steps = sorted({int(row["step"]) for row in scenario_rows})
        result[scenario] = []
        for step in steps:
            step_rows = [row for row in scenario_rows if int(row["step"]) == step]
            result[scenario].append(
                {
                    "scenario": scenario,
                    "step": step,
                    "susceptible": round(mean(float(row["susceptible"]) for row in step_rows), 2),
                    "infected": round(mean(float(row["infected"]) for row in step_rows), 2),
                    "recovered": round(mean(float(row["recovered"]) for row in step_rows), 2),
                }
            )
    return result


def _infected_curve_svg(mean_histories: dict[str, list[dict[str, float]]]) -> str:
    width, height = 940, 440
    left, right, top, bottom = 62, 24, 32, 58
    max_step = max(float(row["step"]) for rows in mean_histories.values() for row in rows)
    max_infected = max(float(row["infected"]) for rows in mean_histories.values() for row in rows)
    max_infected = max(1, max_infected)

    def x_pos(step: float) -> float:
        return left + step / max_step * (width - left - right) if max_step else left

    def y_pos(infected: float) -> float:
        return height - bottom - infected / max_infected * (height - top - bottom)

    grid = []
    for index in range(5):
        fraction = index / 4
        y = top + fraction * (height - top - bottom)
        count = round(max_infected * (1 - fraction))
        grid.append(
            f'<line x1="{left}" y1="{y:.1f}" x2="{width - right}" y2="{y:.1f}" stroke="#ddd2bf"/>'
            f'<text x="{left - 10}" y="{y + 4:.1f}" text-anchor="end">{count}</text>'
        )
    curves = []
    legend = []
    for index, (scenario, rows) in enumerate(mean_histories.items()):
        points = " ".join(
            f'{x_pos(float(row["step"])):.1f},{y_pos(float(row["infected"])):.1f}'
            for row in rows
        )
        color = SCENARIO_COLORS.get(scenario, "#17202a")
        curves.append(
            f'<polyline fill="none" stroke="{color}" stroke-width="4" points="{points}"/>'
        )
        legend_y = top + index * 24
        legend.append(
            f'<line x1="{width - 258}" y1="{legend_y}" x2="{width - 230}" y2="{legend_y}" '
            f'stroke="{color}" stroke-width="4"/><text x="{width - 220}" y="{legend_y + 5}">'
            f'{escape(scenario.replace("_", " "))}</text>'
        )
    return f"""<svg viewBox="0 0 {width} {height}" role="img" aria-label="Mean infected agents by scenario">
<style>text {{ font: 15px system-ui, sans-serif; fill: #17202a; }}</style>
<rect width="{width}" height="{height}" fill="#fffaf1"/>
{''.join(grid)}
<line x1="{left}" y1="{height - bottom}" x2="{width - right}" y2="{height - bottom}" stroke="#17202a"/>
<line x1="{left}" y1="{top}" x2="{left}" y2="{height - bottom}" stroke="#17202a"/>
<text x="{width / 2}" y="{height - 16}" text-anchor="middle">Simulation step</text>
<text x="18" y="{height / 2}" transform="rotate(-90 18 {height / 2})" text-anchor="middle">Mean infected agents</text>
{''.join(curves)}
{''.join(legend)}
</svg>"""


def _label(key: str) -> str:
    return key.replace("_", " ").title()
