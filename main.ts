// The World Today — Friday 20 November 2026 in one image.
//
// Entry for make.fun's "Sum up 20 November's world news in one image"
// bounty (news-image-20261120). The picture itself is entry.png, drawn at
// build time by generate_image.py from the day's reported headlines (see
// SOURCES.md). This program's whole job is to deliver those exact bytes
// to the grader: it copies entry.png to <output>/entry.png.
//
// Deterministic by construction: no clock, no randomness, no network,
// no input besides the file beside this one. Run it any number of times
// and the output is byte-for-byte identical.
//
// The grader sets MAKEFUN_OUTPUT_DIR to its writable output directory
// (its /output); locally it defaults to /output as the bounty specifies.

import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { join } from "node:path";

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const source = new URL("./entry.png", import.meta.url);
const destination = join(outputDir, "entry.png");

// The grader hands us a writable output directory; creating it when it
// is absent keeps a bare local run (MAKEFUN_OUTPUT_DIR=new/dir) working
// the same way, and recursive mkdir is a no-op when it already exists.
mkdirSync(outputDir, { recursive: true });
copyFileSync(source, destination);

// Fail loudly rather than hand the judge a truncated picture: the copy
// must be exactly as many bytes as the image this repository ships.
const shipped = statSync(source).size;
const written = statSync(destination).size;
if (written !== shipped) {
  throw new Error(`entry.png copy is ${written} bytes, expected ${shipped}`);
}
