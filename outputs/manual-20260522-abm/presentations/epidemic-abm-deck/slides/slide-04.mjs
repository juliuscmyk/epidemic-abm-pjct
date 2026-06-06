import { addBase, colors, footer, title } from "./deck-utils.mjs";

export async function slide04(presentation, ctx) {
  const slide = presentation.slides.add();
  addBase(slide, ctx, "decision loop", 4);
  title(slide, ctx, "A simulation step turns choices into exposure.", "Movement, contact, infection, and recovery repeat for every time step.");
  const steps = [
    ["1", "Move", "neighbor cell\nor stay", colors.blue],
    ["2", "Isolate", "infected agents\nmay skip move", colors.gold],
    ["3", "Meet", "share one\ncell", colors.red],
    ["4", "Update", "risk and\nrecovery", colors.green],
  ];
  steps.forEach(([number, heading, body, accent], index) => {
    const x = 64 + index * 282;
    ctx.addShape(slide, { x, y: 282, w: 226, h: 206, geometry: "roundRect", fill: colors.panel, line: ctx.line(colors.line, 2) });
    ctx.addShape(slide, { x: x + 18, y: 304, w: 42, h: 42, geometry: "ellipse", fill: accent });
    ctx.addText(slide, { x: x + 30, y: 313, w: 20, h: 22, text: number, fontSize: 20, bold: true, color: colors.panel, align: "center" });
    ctx.addText(slide, { x: x + 22, y: 370, w: 178, h: 32, text: heading, fontSize: 27, bold: true, color: colors.ink });
    ctx.addText(slide, { x: x + 22, y: 424, w: 178, h: 48, text: body, fontSize: 21, color: colors.muted });
    if (index < steps.length - 1) ctx.addText(slide, { x: x + 242, y: 370, w: 24, h: 28, text: ">", fontSize: 28, bold: true, color: colors.muted });
  });
  ctx.addShape(slide, { x: 190, y: 544, w: 900, h: 76, geometry: "roundRect", fill: "#efe1c8" });
  ctx.addText(slide, {
    x: 228, y: 562, w: 830, h: 38,
    text: "Infection risk = 1 - (1 - p) ^ infected contacts",
    fontSize: 28, bold: true, typeface: ctx.fonts.mono, color: colors.ink, align: "center",
  });
  footer(slide, ctx);
  return slide;
}
