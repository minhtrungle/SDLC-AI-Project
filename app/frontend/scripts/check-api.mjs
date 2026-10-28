// Fails when src/api/schema.d.ts is out of date with ../api-contract/openapi.yaml (contract drift guard).
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

import openapiTS, { astToString } from "openapi-typescript";

const contract = new URL("../../api-contract/openapi.yaml", import.meta.url);
const generatedPath = fileURLToPath(new URL("../src/api/schema.d.ts", import.meta.url));

const fresh = astToString(await openapiTS(contract));
const normalize = (s) => s.replace(/\r\n/g, "\n").replace(/^\/\*\*[\s\S]*?\*\/\n/, "").trim();
const current = readFileSync(generatedPath, "utf8");

if (normalize(fresh) !== normalize(current)) {
  console.error("src/api/schema.d.ts is out of date. Run `npm run gen:api` and commit the result.");
  process.exit(1);
}
console.log("API types match api-contract/openapi.yaml");
