import { FormEvent, useEffect, useState } from "react";
import { api, Book, Claim, Project, Source } from "./api";

const stageLabels: Record<string, string> = {
  brief_pending: "Brief pending", brief_approved: "Brief approved", research: "Research",
  evidence_review: "Evidence review", thesis_review: "Thesis review", script_review: "Script review",
  production: "Production", qa: "Quality assurance", complete: "Complete",
};

function App() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selected, setSelected] = useState<Project | null>(null);
  const [books, setBooks] = useState<Book[]>([]);
  const [sources, setSources] = useState<Source[]>([]);
  const [claims, setClaims] = useState<Claim[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);

  const loadProjects = async () => {
    setLoading(true);
    try { setProjects(await api.projects()); setError(""); }
    catch (err) { setError(err instanceof Error ? err.message : "Unable to load projects."); }
    finally { setLoading(false); }
  };

  const loadResearch = async (project: Project) => {
    if (project.status === "brief_pending") return;
    try {
      const [bookList, sourceList, claimList] = await Promise.all([api.books(project.id), api.sources(project.id), api.claims(project.id)]);
      setBooks(bookList); setSources(sourceList); setClaims(claimList);
    } catch (err) { setError(err instanceof Error ? err.message : "Unable to load research workspace."); }
  };

  useEffect(() => { void loadProjects(); }, []);
  useEffect(() => { if (selected) void loadResearch(selected); }, [selected]);

  const createProject = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault(); const form = new FormData(event.currentTarget);
    try {
      const project = await api.createProject({ title: String(form.get("title")), topic: String(form.get("topic")), description: String(form.get("description")) });
      setProjects((current) => [project, ...current]); setSelected(project); setShowForm(false); setError("");
    } catch (err) { setError(err instanceof Error ? err.message : "Unable to create project."); }
  };

  const approveBrief = async () => {
    if (!selected) return;
    try {
      await api.approveBrief(selected.id, "Brief approved from the project dashboard.");
      const project = { ...selected, status: "brief_approved" as const };
      setSelected(project); setProjects((all) => all.map((item) => item.id === project.id ? project : item));
    } catch (err) { setError(err instanceof Error ? err.message : "Unable to record approval."); }
  };

  const updateProjectStatus = (status: Project["status"]) => {
    if (!selected) return;
    const project = { ...selected, status };
    setSelected(project); setProjects((all) => all.map((item) => item.id === project.id ? project : item));
  };

  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand"><span className="brand-mark">V</span><span>VIDBOOK</span></div>
      <p className="eyebrow">DOCUMENTARY STUDIO</p>
      <nav aria-label="Main navigation"><button className="nav-item active">Projects <span>{projects.length}</span></button><button className="nav-item" disabled>Research library <span>—</span></button><button className="nav-item" disabled>Exports <span>—</span></button></nav>
      <div className="sidebar-footer"><span className="status-dot" /> Local workspace<br /><small>Evidence-led production</small></div>
    </aside>
    <main className="main-content">
      <header className="topbar"><div><p className="eyebrow">WORKSPACE / PROJECTS</p><h1>Documentary projects</h1></div><button className="primary-button" onClick={() => setShowForm(true)}>＋ New project</button></header>
      {error && <div className="alert" role="alert">{error}</div>}
      {showForm && <ProjectForm onCancel={() => setShowForm(false)} onSubmit={createProject} />}
      {loading ? <div className="empty-state card">Loading workspace…</div> : projects.length === 0 && !showForm ? <section className="welcome card"><div className="welcome-art">✦</div><p className="eyebrow">YOUR FIRST PRODUCTION</p><h2>Start with a question worth following.</h2><p>Create a project to shape a researched, cited documentary package with explicit approval gates at every major stage.</p><button className="primary-button" onClick={() => setShowForm(true)}>Create your first project</button></section> : <div className="workspace-grid"><section><div className="section-heading"><div><p className="eyebrow">ACTIVE WORK</p><h2>Projects</h2></div><span className="count-pill">{projects.length} total</span></div><div className="project-list">{projects.map((project) => <button key={project.id} className={`project-card ${selected?.id === project.id ? "selected" : ""}`} onClick={() => setSelected(project)}><div className="project-card-top"><span className="project-symbol">◈</span><span className={`status status-${project.status}`}>{stageLabels[project.status]}</span></div><h3>{project.title}</h3><p>{project.topic}</p><div className="project-meta"><span>Updated {new Date(project.updated_at).toLocaleDateString()}</span><span>→</span></div></button>)}</div></section><section className="detail-panel card">{selected ? <ProjectDetail project={selected} books={books} sources={sources} claims={claims} onApproveBrief={approveBrief} onBooksChange={setBooks} onSourcesChange={setSources} onClaimsChange={setClaims} onStatusChange={updateProjectStatus} /> : <div className="detail-placeholder"><span>◈</span><p>Select a project</p><small>Its brief, approval gates, and production status will appear here.</small></div>}</section></div>}
    </main>
  </div>;
}

function ProjectForm({ onCancel, onSubmit }: { onCancel: () => void; onSubmit: (event: FormEvent<HTMLFormElement>) => void }) {
  return <form className="project-form card" onSubmit={onSubmit}><div className="form-header"><div><p className="eyebrow">START A NEW PACKAGE</p><h2>Project brief</h2></div><button type="button" className="icon-button" aria-label="Close" onClick={onCancel}>×</button></div><label>Working title<input name="title" required maxLength={160} placeholder="e.g. The making of a modern border" /></label><label>Topic or central question<input name="topic" required maxLength={500} placeholder="What should this documentary investigate?" /></label><label>Initial direction <span className="optional">optional</span><textarea name="description" rows={3} maxLength={4000} placeholder="Audience, scope, constraints, or ideas to preserve..." /></label><div className="form-actions"><button type="button" className="secondary-button" onClick={onCancel}>Cancel</button><button className="primary-button" type="submit">Create project</button></div></form>;
}

function ProjectDetail({ project, books, sources, claims, onApproveBrief, onBooksChange, onSourcesChange, onClaimsChange, onStatusChange }: { project: Project; books: Book[]; sources: Source[]; claims: Claim[]; onApproveBrief: () => void; onBooksChange: (books: Book[]) => void; onSourcesChange: (sources: Source[]) => void; onClaimsChange: (claims: Claim[]) => void; onStatusChange: (status: Project["status"]) => void }) {
  const progress = project.status === "brief_pending" ? 12.5 : project.status === "brief_approved" ? 25 : 37.5;
  return <><div className="detail-kicker"><span className="project-symbol">◈</span><span className={`status status-${project.status}`}>{stageLabels[project.status]}</span></div><h2>{project.title}</h2><p className="detail-topic">{project.topic}</p>{project.description && <p className="detail-description">{project.description}</p>}<div className="progress-block"><div className="progress-label"><span>Workflow progress</span><strong>{project.status === "brief_pending" ? "1 of 8" : project.status === "brief_approved" ? "2 of 8" : "3 of 8"}</strong></div><div className="progress-track"><span style={{ width: `${progress}%` }} /></div></div>{project.status === "brief_pending" ? <div className="next-step"><p className="eyebrow">NEXT APPROVAL GATE</p><h3>Review the project brief</h3><p>Confirm the scope and direction before research begins.</p><button className="primary-button" onClick={onApproveBrief}>Approve brief</button></div> : <ResearchWorkspace project={project} books={books} sources={sources} claims={claims} onBooksChange={onBooksChange} onSourcesChange={onSourcesChange} onClaimsChange={onClaimsChange} onStatusChange={onStatusChange} />}</>;
}

function ResearchWorkspace({ project, books, sources, claims, onBooksChange, onSourcesChange, onClaimsChange, onStatusChange }: { project: Project; books: Book[]; sources: Source[]; claims: Claim[]; onBooksChange: (books: Book[]) => void; onSourcesChange: (sources: Source[]) => void; onClaimsChange: (claims: Claim[]) => void; onStatusChange: (status: Project["status"]) => void }) {
  const [showBookForm, setShowBookForm] = useState(false); const [selectedBookIds, setSelectedBookIds] = useState<string[]>([]); const [showSourceForm, setShowSourceForm] = useState(false); const [showClaimForm, setShowClaimForm] = useState(false); const [localError, setLocalError] = useState("");
  const addBook = async (event: FormEvent<HTMLFormElement>) => { event.preventDefault(); const form = new FormData(event.currentTarget); try { const book = await api.createBook(project.id, { title: String(form.get("title")), author: String(form.get("author")), publication_year: form.get("year") ? Number(form.get("year")) : null, publisher: String(form.get("publisher")), relevance_score: Number(form.get("relevance") || 0), credibility_score: Number(form.get("credibility") || 0), accessibility: String(form.get("accessibility")), rationale: String(form.get("rationale")), rank: books.length + 1 }); onBooksChange([...books, book]); setShowBookForm(false); } catch (err) { setLocalError(err instanceof Error ? err.message : "Unable to add book."); } };
  const approveBooks = async () => { try { const approved = await api.approveBooks(project.id, selectedBookIds); onBooksChange(books.map((book) => ({ ...book, approval_status: approved.some((item) => item.id === book.id) ? "approved" : "rejected" }))); setSelectedBookIds([]); onStatusChange("research"); } catch (err) { setLocalError(err instanceof Error ? err.message : "Select exactly five books first."); } };
  const addSource = async (event: FormEvent<HTMLFormElement>) => { event.preventDefault(); const form = new FormData(event.currentTarget); try { const source = await api.createSource(project.id, { kind: String(form.get("kind")), title: String(form.get("title")), author: String(form.get("author")), url: String(form.get("url")), local_path: "", access_status: String(form.get("access_status")), notes: String(form.get("notes")) }); onSourcesChange([source, ...sources]); setShowSourceForm(false); } catch (err) { setLocalError(err instanceof Error ? err.message : "Unable to add source."); } };
  const addClaim = async (event: FormEvent<HTMLFormElement>) => { event.preventDefault(); const form = new FormData(event.currentTarget); try { const claim = await api.createClaim(project.id, { claim_text: String(form.get("claim_text")), claim_type: String(form.get("claim_type")), evidence_strength: String(form.get("evidence_strength")), verification_status: String(form.get("verification_status")), source_id: null, locator: String(form.get("locator")), supporting_passage: String(form.get("supporting_passage")), conflict_note: "" }); onClaimsChange([claim, ...claims]); setShowClaimForm(false); } catch (err) { setLocalError(err instanceof Error ? err.message : "Unable to add claim."); } };
  return <div className="research-workspace"><div className="research-heading"><div><p className="eyebrow">PHASE 2 / RESEARCH & EVIDENCE</p><h3>Research workspace</h3></div><span className="research-count">{books.filter((book) => book.approval_status === "approved").length}/5 books approved</span></div>{localError && <div className="inline-error">{localError}</div>}<div className="research-section"><div className="research-section-header"><div><p className="eyebrow">BOOK SHORTLIST</p><p className="section-note">Ranked candidates and scholarly credibility notes.</p></div><button className="secondary-button small-button" onClick={() => setShowBookForm(!showBookForm)}>＋ Add book</button></div>{showBookForm && <form className="mini-form" onSubmit={addBook}><input name="title" required placeholder="Book title" /><input name="author" required placeholder="Author" /><input name="year" type="number" placeholder="Year" /><input name="publisher" placeholder="Publisher" /><input name="credibility" type="number" min="0" max="100" placeholder="Credibility / 100" /><input name="relevance" type="number" min="0" max="100" placeholder="Relevance / 100" /><select name="accessibility" defaultValue="unknown"><option value="unknown">Access unknown</option><option value="accessible">Legally accessible</option><option value="limited">Limited access</option><option value="unavailable">Unavailable</option></select><input name="rationale" placeholder="Why this book belongs" /><button className="primary-button small-button">Save candidate</button></form>}{books.length === 0 ? <p className="empty-note">No candidates yet. Add books manually until a provider-backed ranking workflow is connected.</p> : <>{books.map((book) => <label className="book-row" key={book.id}><input type="checkbox" checked={selectedBookIds.includes(book.id)} disabled={book.approval_status === "approved"} onChange={(event) => setSelectedBookIds(event.target.checked ? [...selectedBookIds, book.id] : selectedBookIds.filter((id) => id !== book.id))} /><span className="book-rank">{book.rank || "—"}</span><span className="book-info"><strong>{book.title}</strong><small>{book.author}{book.publication_year ? ` · ${book.publication_year}` : ""}</small></span><span className={`book-status ${book.approval_status}`}>{book.approval_status}</span></label>)}<button className="primary-button small-button approve-books" disabled={selectedBookIds.length !== 5} onClick={() => void approveBooks()}>Approve selected five</button></>}</div><div className="research-section compact-section"><div className="research-section-header"><div><p className="eyebrow">SOURCE REGISTER</p><p className="section-note">Primary and supplementary sources with access disclosure.</p></div><button className="secondary-button small-button" onClick={() => setShowSourceForm(!showSourceForm)}>＋ Add source</button></div>{showSourceForm && <form className="mini-form" onSubmit={addSource}><input name="kind" required placeholder="Kind: archive, paper, web..." /><input name="title" required placeholder="Source title" /><input name="author" placeholder="Author / institution" /><input name="url" type="url" placeholder="URL, if applicable" /><select name="access_status" defaultValue="unverified"><option value="unverified">Unverified access</option><option value="accessible">Accessible</option><option value="limited">Limited</option><option value="unavailable">Unavailable</option></select><input name="notes" placeholder="Provenance or access note" /><button className="primary-button small-button">Save source</button></form>}{sources.length === 0 ? <p className="empty-note">No sources registered yet.</p> : sources.map((source) => <div className="source-row" key={source.id}><span className="source-kind">{source.kind}</span><span><strong>{source.title}</strong><small>{source.author || "Author not recorded"}</small></span><span className={`book-status ${source.access_status}`}>{source.access_status}</span></div>)}</div><div className="research-section compact-section"><div className="research-section-header"><div><p className="eyebrow">EVIDENCE LEDGER</p><p className="section-note">Claim-level traceability begins here.</p></div><button className="secondary-button small-button" onClick={() => setShowClaimForm(!showClaimForm)}>＋ Add claim</button></div>{showClaimForm && <form className="mini-form claim-form" onSubmit={addClaim}><textarea name="claim_text" required placeholder="Claim text" /><input name="claim_type" required placeholder="Fact, interpretation, allegation..." /><select name="evidence_strength" defaultValue="unassessed"><option value="unassessed">Evidence unassessed</option><option value="strong">Strong</option><option value="moderate">Moderate</option><option value="weak">Weak</option><option value="contested">Contested</option></select><select name="verification_status" defaultValue="unverified"><option value="unverified">Not directly verified</option><option value="verified">Directly verified</option><option value="uncertain">Uncertain</option></select><input name="locator" placeholder="Page, section, timestamp" /><textarea name="supporting_passage" placeholder="Supporting passage and context" /><button className="primary-button small-button">Save claim</button></form>}{claims.length === 0 ? <p className="empty-note">No claims recorded yet.</p> : claims.map((claim) => <div className="claim-row" key={claim.id}><strong>{claim.claim_text}</strong><span>{claim.evidence_strength} · {claim.verification_status}{claim.locator ? ` · ${claim.locator}` : ""}</span></div>)}</div></div>;
}

export default App;
