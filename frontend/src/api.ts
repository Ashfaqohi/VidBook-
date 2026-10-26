export type ProjectStatus =
  | "brief_pending" | "brief_approved" | "research" | "evidence_review"
  | "thesis_review" | "script_review" | "production" | "qa" | "complete";

export type Project = {
  id: string;
  title: string;
  topic: string;
  description: string;
  status: ProjectStatus;
  created_at: string;
  updated_at: string;
  folders: string[];
};

type Approval = { id: number; project_id: string; stage: string; decision: string; note: string; created_at: string };
export type Book = { id: string; project_id: string; title: string; author: string; publication_year: number | null; publisher: string; relevance_score: number; credibility_score: number; accessibility: string; rationale: string; rank: number; approval_status: string; created_at: string };
export type Source = { id: string; project_id: string; kind: string; title: string; author: string; url: string; local_path: string; access_status: string; notes: string; created_at: string };
export type Claim = { id: string; project_id: string; claim_text: string; claim_type: string; evidence_strength: string; verification_status: string; source_id: string | null; locator: string; supporting_passage: string; conflict_note: string; created_at: string; updated_at: string };

const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", ...(options?.headers ?? {}) },
  });
  if (!response.ok) throw new Error((await response.json().catch(() => null))?.detail ?? "Request failed");
  return response.status === 204 ? (undefined as T) : response.json();
}

export const api = {
  projects: () => request<Project[]>("/api/v1/projects"),
  createProject: (payload: { title: string; topic: string; description: string }) =>
    request<Project>("/api/v1/projects", { method: "POST", body: JSON.stringify(payload) }),
  approveBrief: (id: string, note: string) =>
    request<Approval>(`/api/v1/projects/${id}/approvals/brief`, { method: "POST", body: JSON.stringify({ decision: "approve", note }) }),
  books: (id: string) => request<Book[]>(`/api/v1/projects/${id}/books`),
  createBook: (id: string, payload: Omit<Book, "id" | "project_id" | "approval_status" | "created_at">) =>
    request<Book>(`/api/v1/projects/${id}/books`, { method: "POST", body: JSON.stringify(payload) }),
  approveBooks: (id: string, bookIds: string[]) =>
    request<Book[]>(`/api/v1/projects/${id}/books/approve`, { method: "POST", body: JSON.stringify({ book_ids: bookIds }) }),
  sources: (id: string) => request<Source[]>(`/api/v1/projects/${id}/sources`),
  createSource: (id: string, payload: Omit<Source, "id" | "project_id" | "created_at">) =>
    request<Source>(`/api/v1/projects/${id}/sources`, { method: "POST", body: JSON.stringify(payload) }),
  claims: (id: string) => request<Claim[]>(`/api/v1/projects/${id}/claims`),
  createClaim: (id: string, payload: Omit<Claim, "id" | "project_id" | "created_at" | "updated_at">) =>
    request<Claim>(`/api/v1/projects/${id}/claims`, { method: "POST", body: JSON.stringify(payload) }),
};
