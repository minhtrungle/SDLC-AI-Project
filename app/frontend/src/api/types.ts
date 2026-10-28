// Friendly aliases over the types generated from app/api-contract/openapi.yaml (npm run gen:api).
import type { components } from "./schema";

type Schemas = components["schemas"];

export type Me = Schemas["Me"];
export type PublicConfig = Schemas["PublicConfig"];
export type DocumentInfo = Schemas["Document"];
export type DocumentStatus = DocumentInfo["status"];
export type UploadResult = Schemas["UploadResult"];
export type Citation = Schemas["Citation"];
export type Turn = Schemas["Turn"];
export type Conversation = Schemas["Conversation"];
export type WeeklyMetric = Schemas["WeeklyMetric"];
export type Problem = Schemas["Problem"];
export type ErrorCode = Problem["code"];

export interface Chunk {
  chunk_id: number;
  document_id: string;
  document_name: string;
  page: number;
  text: string;
}
