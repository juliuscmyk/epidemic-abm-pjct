import { addBase, bullet, colors, footer, title } from "./deck-utils.mjs";

export async function slide02(presentation, ctx) {
  const slide = presentation.slides.add();
  addBase(slide, ctx, "rationale", 2);
  title(slide, ctx, "Why use ABM for this problem?", "Spread depends on who meets whom, not only on an average rate.");
  bullet(slide, ctx, 62, 270, "Each person makes a movement decision.", colors.ink, colors.blue, 420);
  bullet(slide, ctx, 62, 338, "Contact happens locally inside grid cells.", colors.ink, colors.red, 420);
  bullet(slide, ctx, 62, 406, "Population curves emerge after many encounters.", colors.ink, colors.green, 440);

  const x = [610, 800, 990];
  const labels = [
    ["Agents", "move\nisolate\ndistance", colors.blue],
    ["Contacts", "share cell\nrisk update", colors.red],
    ["Results", "peak\nattack rate\ncurve", colors.green],
  ];
  labels.forEach(([heading, body, accent], index) => {
    ctx.addShape(slide, { x: x[index], y: 280, w: 160, h: 226, geometry: "roundRect", fill: colors.panel, line: ctx.line(colors.line, 2) });
    ctx.addShape(slide, { x: x[index], y: 280, w: 160, h: 10, fill: accent });
    ctx.addText(slide, { x: x[index] + 20, y: 318, w: 120, h: 32, text: heading, fontSize: 25, bold: true, color: colors.ink, align: "center" });
    ctx.addText(slide, { x: x[index] + 20, y: 382, w: 120, h: 98, text: body, fontSize: 22, color: colors.muted, align: "center" });
  });
  ctx.addText(slide, { x: 777, y: 366, w: 18, h: 24, text: ">", fontSize: 24, bold: true, color: colors.muted });
  ctx.addText(slide, { x: 967, y: 366, w: 18, h: 24, text: ">", fontSize: 24, bold: true, color: colors.muted });
  footer(slide, ctx);
  return slide;
}
