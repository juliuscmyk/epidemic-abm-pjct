import { addBase, colors, footer, metric, title } from "./deck-utils.mjs";

export async function slide06(presentation, ctx) {
  const slide = presentation.slides.add();
  addBase(slide, ctx, "results", 6);
  title(slide, ctx, "Distancing flattens the simulated outbreak.", "Verified mean results from six seeded runs per scenario.");
  metric(slide, ctx, 64, 262, "75.8", "baseline peak infected", colors.red);
  metric(slide, ctx, 292, 262, "27.2", "high-distancing peak", colors.green);
  metric(slide, ctx, 520, 262, "89.6%", "baseline attack rate", colors.red);
  metric(slide, ctx, 748, 262, "45.6%", "high-distancing attack", colors.green);
  ctx.addShape(slide, { x: 80, y: 446, w: 1040, h: 18, geometry: "roundRect", fill: "#e0d3be" });
  ctx.addShape(slide, { x: 80, y: 446, w: 873, h: 18, geometry: "roundRect", fill: colors.red });
  ctx.addText(slide, { x: 80, y: 474, w: 420, h: 24, text: "Baseline attack rate", fontSize: 18, bold: true, color: colors.red });
  ctx.addText(slide, { x: 980, y: 474, w: 140, h: 24, text: "89.6%", fontSize: 18, bold: true, color: colors.ink, align: "right" });
  ctx.addShape(slide, { x: 80, y: 536, w: 1040, h: 18, geometry: "roundRect", fill: "#e0d3be" });
  ctx.addShape(slide, { x: 80, y: 536, w: 445, h: 18, geometry: "roundRect", fill: colors.green });
  ctx.addText(slide, { x: 80, y: 564, w: 420, h: 24, text: "High-distancing attack rate", fontSize: 18, bold: true, color: colors.green });
  ctx.addText(slide, { x: 980, y: 564, w: 140, h: 24, text: "45.6%", fontSize: 18, bold: true, color: colors.ink, align: "right" });
  ctx.addText(slide, {
    x: 978, y: 292, w: 208, h: 60,
    text: "Experiment report adds the infection curves.",
    fontSize: 20, bold: true, color: colors.ink,
  });
  footer(slide, ctx, "Source: outputs/experiments/scenario_summary.csv");
  return slide;
}
