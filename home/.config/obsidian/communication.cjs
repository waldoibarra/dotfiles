"use strict";

// Use parsed prose; never rewrite wording to satisfy a numeric limit.
const sentences = new Intl.Segmenter("en", { granularity: "sentence" });

module.exports = {
  names: ["LIFE001", "prose-word-limit"],
  description: "Sentences contain at most 17 words",
  tags: ["communication"],
  parser: "markdownit",
  function: (params, onError) => {
    let inParagraph = false;
    let inTable = false;
    for (const token of params.parsers.markdownit.tokens) {
      if (token.type === "table_open") inTable = true;
      if (token.type === "table_close") inTable = false;
      if (token.type === "paragraph_open") inParagraph = true;
      if (token.type === "paragraph_close") inParagraph = false;
      if (token.type !== "inline" || !inParagraph || inTable) continue;

      const text = (token.children || []).map((child) => {
        if (child.type === "text") return child.content;
        if (child.type === "softbreak" || child.type === "hardbreak") return " ";
        // Inline code counts as one technical term; destinations are not prose.
        if (child.type === "code_inline") return "CODE";
        if (child.type === "image") return child.content;
        return "";
      }).join("");
      for (const { segment } of sentences.segment(text)) {
        const count = segment.trim().split(/\s+/u).filter(Boolean).length;
        if (count > 17) {
          onError({
            lineNumber: token.lineNumber,
            detail: `${count} words; maximum 17 per sentence. Keep safety text; explain exemptions.`
          });
        }
      }
    }
  }
};
