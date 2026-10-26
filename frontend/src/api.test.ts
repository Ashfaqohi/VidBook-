import { afterEach, describe, expect, it, vi } from "vitest";
import { api } from "./api";

describe("project API client", () => {
  afterEach(() => vi.restoreAllMocks());

  it("creates a project with the expected request shape", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify({ id: "p1", title: "Test", status: "brief_pending" }), { status: 201 }),
    );

    await api.createProject({ title: "Test", topic: "A topic", description: "" });

    expect(fetchMock).toHaveBeenCalledWith(
      "http://localhost:8000/api/v1/projects",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ title: "Test", topic: "A topic", description: "" }),
      }),
    );
  });
});
