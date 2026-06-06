import { addBase, colors, footer, title } from "./deck-utils.mjs";

export async function slide05(presentation, ctx) {
  const slide = presentation.slides.add();
  addBase(slide, ctx, "experiments", 5);
  title(slide, ctx, "Experiments vary behavior and disease pressure.", "Mesa runs four scenarios, six seeded repeats each, with CSV outputs.");
  const rows = [
    ["baseline", "0% distancing", "reference case", colors.red],
    ["moderate", "45% distancing", "behavior change", colors.gold],
    ["high", "80% distancing", "strong behavior change", colors.green],
    ["transmission", "p = 0.34", "harder disease pressure", colors.purple],
  ];
  ctx.addShape(slide, { x: 68, y: 264, w: 818, h: 340, geometry: "roundRect", fill: colors.panel, line: ctx.line(colors.line, 2) });
  ctx.addText(slide, { x: 100, y: 294, w: 180, h: 24, text: "Scenario", fontSize: 17, bold: true, color: colors.muted });
  ctx.addText(slide, { x: 350, y: 294, w: 190, h: 24, text: "Parameter", fontSize: 17, bold: true, color: colors.muted });
  ctx.addText(slide, { x: 588, y: 294, w: 210, h: 24, text: "Question", fontSize: 17, bold: true, color: colors.muted });
  rows.forEach(([name, parameter, question, accent], index) => {
    const y = 338 + index * 62;
    ctx.addShape(slide, { x: 98, y: y + 12, w: 14, h: 14, geometry: "ellipse", fill: accent });
    ctx.addText(slide, { x: 132, y, w: 182, h: 32, text: name, fontSize: 22, bold: true, color: colors.ink });
    ctx.addText(slide, { x: 350, y, w: 190, h: 32, text: parameter, fontSize: 21, color: colors.ink });
    ctx.addText(slide, { x: 588, y, w: 248, h: 32, text: question, fontSize: 20, color: colors.muted });
  });
  ctx.addShape(slide, { x: 936, y: 288, w: 260, h: 274, geometry: "roundRect", fill: "#efe1c8" });
  ctx.addText(slide, { x: 968, y: 326, w: 194, h: 30, text: "Metrics", fontSize: 28, bold: true, color: colors.ink });
  ["state counts", "peak infected", "peak step", "attack rate"].forEach((metric, index) => {
    ctx.addShape(slide, { x: 970, y: 390 + index * 38, w: 9, h: 9, geometry: "ellipse", fill: colors.ink });
    ctx.addText(slide, { x: 992, y: 380 + index * 38, w: 164, h: 28, text: metric, fontSize: 20, color: colors.ink });
  });
  footer(slide, ctx);
  return slide;
}
