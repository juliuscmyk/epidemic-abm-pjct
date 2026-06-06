import { addBase, colors, footer, pill, title } from "./deck-utils.mjs";

export async function slide03(presentation, ctx) {
  const slide = presentation.slides.add();
  addBase(slide, ctx, "system design", 3);
  title(slide, ctx, "Mesa agents. Three health states.", "A Mesa MultiGrid creates contact opportunities.");
  ctx.addShape(slide, { x: 62, y: 260, w: 380, h: 326, geometry: "roundRect", fill: colors.panel, line: ctx.line(colors.line, 2) });
  ctx.addText(slide, { x: 88, y: 292, w: 250, h: 32, text: "Mesa PersonAgent", fontSize: 25, bold: true, color: colors.ink });
  pill(slide, ctx, 88, 354, 138, "position", colors.blue);
  pill(slide, ctx, 238, 354, 146, "health state", colors.red);
  pill(slide, ctx, 88, 402, 178, "infection timer", colors.green);
  pill(slide, ctx, 88, 450, 196, "distancing flag", colors.gold, colors.ink);
  ctx.addText(slide, {
    x: 88, y: 516, w: 290, h: 38,
    text: "Autonomous rules are simple and inspectable.",
    fontSize: 19, color: colors.muted,
  });

  const stateX = [560, 742, 924];
  const stateLabels = [
    ["S", "susceptible", colors.blue],
    ["I", "infected", colors.red],
    ["R", "recovered", colors.green],
  ];
  stateLabels.forEach(([code, label, fill], index) => {
    ctx.addShape(slide, { x: stateX[index], y: 270, w: 118, h: 118, geometry: "ellipse", fill });
    ctx.addText(slide, { x: stateX[index] + 34, y: 296, w: 50, h: 58, text: code, fontSize: 54, bold: true, color: colors.panel, align: "center" });
    ctx.addText(slide, { x: stateX[index] - 10, y: 408, w: 138, h: 26, text: label, fontSize: 19, bold: true, color: colors.ink, align: "center" });
  });
  ctx.addText(slide, { x: 692, y: 314, w: 34, h: 28, text: ">", fontSize: 28, bold: true, color: colors.muted });
  ctx.addText(slide, { x: 874, y: 314, w: 34, h: 28, text: ">", fontSize: 28, bold: true, color: colors.muted });
  ctx.addShape(slide, { x: 568, y: 480, w: 506, h: 106, geometry: "roundRect", fill: "#efe1c8" });
  ctx.addText(slide, {
    x: 596, y: 508, w: 450, h: 52,
    text: "Mesa MultiGrid: agents can meet in the same cell without artificial borders.",
    fontSize: 23, bold: true, color: colors.ink,
  });
  footer(slide, ctx);
  return slide;
}
