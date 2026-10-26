import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import App from "./App";

const project = {
  id: "project-1",
  title: "The Silk Roads",
  topic: "How trade connected Eurasia",
  description: "A focused pilot.",
  status: "brief_pending",
  created_at: "2026-01-01T00:00:00+00:00",
  updated_at: "2026-01-01T00:00:00+00:00",
  folders: ["brief", "research", "sources", "evidence", "script", "production", "exports"],
};

afterEach(() => vi.unstubAllGlobals());

describe("project dashboard", () => {
  it("shows the empty workspace and opens the project form", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify([]), { status: 200 })));

    render(<App />);

    expect(await screen.findByText("Start with a question worth following.")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: /create your first project/i }));

    expect(screen.getByRole("heading", { name: "Project brief" })).toBeInTheDocument();
    expect(screen.getByLabelText("Working title")).toBeRequired();
  });

  it("creates a project and presents its first approval gate", async () => {
    const fetchMock = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      if ((init?.method ?? "GET") === "POST") return Promise.resolve(new Response(JSON.stringify(project), { status: 201 }));
      return Promise.resolve(new Response(JSON.stringify([]), { status: 200 }));
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<App />);
    fireEvent.click(await screen.findByRole("button", { name: /create your first project/i }));
    fireEvent.change(screen.getByLabelText("Working title"), { target: { value: project.title } });
    fireEvent.change(screen.getByLabelText("Topic or central question"), { target: { value: project.topic } });
    fireEvent.submit(screen.getByRole("button", { name: /create project/i }).closest("form")!);

    expect(await screen.findByRole("heading", { name: project.title, level: 2 })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /approve brief/i })).toBeInTheDocument();
    await waitFor(() => expect(fetchMock).toHaveBeenCalledWith("http://localhost:8000/api/v1/projects", expect.objectContaining({ method: "POST" })));
  });
});
