import { addBase, bullet, colors, footer, title } from "./deck-utils.mjs";

export async function slide07(presentation, ctx) {
  const slide = presentation.slides.add();
  addBase(slide, ctx, "defense and demo", 7);
  title(slide, ctx, "The model is explainable because its limits are explicit.", "Close with the live HTML demo and the experiment report.");
  ctx.addText(slide, { x: 68, y: 260, w: 270, h: 32, text: "Limitations", fontSize: 27, bold: true, color: colors.ink });
  bullet(slide, ctx, 72, 320, "Grid co-location abstracts real distance.", colors.ink, colors.red, 420);
  bullet(slide, ctx, 72, 382, "Recovery time is fixed per agent.", colors.ink, colors.gold, 420);
  bullet(slide, ctx, 72, 444, "Parameters are illustrative.", colors.ink, colors.purple, 420);
  ctx.addShape(slide, { x: 620, y: 266, w: 520, h: 316, geometry: "roundRect", fill: colors.panel, line: ctx.line(colors.line, 2) });
  ctx.addText(slide, { x: 658, y: 306, w: 392, h: 34, text: "Demo handoff", fontSize: 29, bold: true, color: colors.ink });
  [
    "1. Play simulation_demo.html",
    "2. Show state counts change",
    "3. Open experiment_report.html",
    "4. Defend assumptions",
  ].forEach((line, index) => {
    ctx.addText(slide, { x: 662, y: 378 + index * 42, w: 382, h: 28, text: line, fontSize: 22, color: colors.ink });
  });
  ctx.addText(slide, {
    x: 72, y: 570, w: 980, h: 40,
    text: "Conclusion: simple agent rules produce measurable collective outcomes.",
    fontSize: 28, bold: true, color: colors.green,
  });
  footer(slide, ctx);
  return slide;
}
