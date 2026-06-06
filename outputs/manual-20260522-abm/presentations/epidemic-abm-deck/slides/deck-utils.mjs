export const colors = {
  ink: "#10212b",
  paper: "#f7f0e3",
  panel: "#fff9ee",
  line: "#d5c6aa",
  blue: "#2878b5",
  red: "#d1495b",
  green: "#16825d",
  gold: "#d98c10",
  purple: "#6b4cc2",
  muted: "#5a6870",
};

export function addBase(slide, ctx, eyebrow, page) {
  ctx.addShape(slide, { x: 0, y: 0, w: ctx.W, h: ctx.H, fill: colors.paper });
  ctx.addShape(slide, { x: 0, y: 0, w: ctx.W, h: 14, fill: colors.ink });
  ctx.addText(slide, {
    x: 54, y: 34, w: 600, h: 24, text: eyebrow.toUpperCase(),
    fontSize: 16, bold: true, color: colors.red,
  });
  ctx.addText(slide, {
    x: 1180, y: 34, w: 52, h: 28, text: String(page).padStart(2, "0"),
    fontSize: 18, bold: true, color: colors.muted, align: "right",
  });
}

export function title(slide, ctx, text, subtext) {
  ctx.addText(slide, {
    x: 54, y: 72, w: 1030, h: 102, text, fontSize: 46, bold: true,
    typeface: ctx.fonts.title, color: colors.ink,
  });
  if (subtext) {
    ctx.addText(slide, {
      x: 58, y: 180, w: 900, h: 54, text: subtext, fontSize: 22,
      color: colors.muted,
    });
  }
}

export function footer(slide, ctx, text = "Applied AI | ABM epidemic simulation") {
  ctx.addShape(slide, { x: 54, y: 673, w: 1172, h: 1, fill: colors.line });
  ctx.addText(slide, { x: 54, y: 684, w: 500, h: 18, text, fontSize: 13, color: colors.muted });
}

export function pill(slide, ctx, x, y, w, text, fill, textColor = colors.panel) {
  ctx.addShape(slide, { x, y, w, h: 34, geometry: "roundRect", fill });
  ctx.addText(slide, {
    x: x + 12, y: y + 7, w: w - 24, h: 20, text, fontSize: 15,
    bold: true, color: textColor,
  });
}

export function metric(slide, ctx, x, y, value, label, accent) {
  ctx.addShape(slide, { x, y, w: 212, h: 120, geometry: "roundRect", fill: colors.panel, line: ctx.line(colors.line, 2) });
  ctx.addShape(slide, { x, y, w: 212, h: 9, fill: accent });
  ctx.addText(slide, { x: x + 16, y: y + 24, w: 178, h: 42, text: value, fontSize: 34, bold: true, color: colors.ink });
  ctx.addText(slide, { x: x + 16, y: y + 75, w: 180, h: 30, text: label, fontSize: 16, color: colors.muted });
}

export function bullet(slide, ctx, x, y, text, color = colors.ink, accent = colors.red, width = 470) {
  ctx.addShape(slide, { x, y: y + 10, w: 10, h: 10, geometry: "ellipse", fill: accent });
  ctx.addText(slide, { x: x + 22, y, w: width, h: 46, text, fontSize: 20, color });
}
