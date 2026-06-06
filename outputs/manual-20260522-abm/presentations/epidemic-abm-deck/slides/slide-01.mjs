import { addBase, colors, footer, metric, pill } from "./deck-utils.mjs";

export async function slide01(presentation, ctx) {
  const slide = presentation.slides.add();
  addBase(slide, ctx, "project question", 1);
  ctx.addText(slide, {
    x: 56, y: 102, w: 740, h: 158,
    text: "Epidemic Spread\nwith Distancing Agents",
    fontSize: 58, bold: true, typeface: ctx.fonts.title, color: colors.ink,
  });
  ctx.addText(slide, {
    x: 60, y: 282, w: 620, h: 68,
    text: "A grid-based agent model for contact, recovery, and emergent infection curves.",
    fontSize: 25, color: colors.muted,
  });
  pill(slide, ctx, 60, 382, 164, "Agent behavior", colors.blue);
  pill(slide, ctx, 236, 382, 164, "Experiments", colors.green);
  pill(slide, ctx, 412, 382, 154, "HTML demo", colors.red);
  metric(slide, ctx, 60, 470, "180", "person agents", colors.blue);
  metric(slide, ctx, 286, 470, "4", "scenarios", colors.gold);
  metric(slide, ctx, 512, 470, "6x", "seeded repeats", colors.green);

  ctx.addShape(slide, { x: 854, y: 96, w: 332, h: 548, geometry: "roundRect", fill: colors.panel, line: ctx.line(colors.line, 2) });
  for (let row = 0; row < 9; row += 1) {
    for (let col = 0; col < 5; col += 1) {
      const index = row * 5 + col;
      const fill = index % 11 === 0 ? colors.red : index % 7 === 0 ? colors.green : colors.blue;
      ctx.addShape(slide, {
        x: 910 + col * 48 + (row % 2) * 8,
        y: 154 + row * 46,
        w: 24, h: 24, geometry: "ellipse", fill,
      });
    }
  }
  ctx.addText(slide, {
    x: 894, y: 558, w: 260, h: 46, text: "Local contacts\nbecome a population curve",
    fontSize: 22, bold: true, color: colors.ink, align: "center",
  });
  footer(slide, ctx);
  return slide;
}
