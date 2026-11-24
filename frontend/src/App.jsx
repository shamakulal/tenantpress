import { useEffect, useState } from "react";
import {
  fetchTenant,
  fetchArticles,
  fetchBooks,
} from "./api";

import "./App.css";

function App() {
  const [tenant, setTenant] = useState(null);
  const [articles, setArticles] = useState([]);
  const [books, setBooks] = useState([]);
  const [activeTab, setActiveTab] = useState("articles");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        setError("");

        const [tenantData, articleData, bookData] = await Promise.all([
          fetchTenant(),
          fetchArticles(),
          fetchBooks(),
        ]);

        setTenant(tenantData);
        setArticles(articleData);
        setBooks(bookData);
      } catch (err) {
        setError(err.message || "Unable to load application data.");
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, []);

  if (loading) {
    return <div className="message">Loading TenantPress...</div>;
  }

  if (error) {
    return <div className="message error">Error: {error}</div>;
  }

  if (!tenant) {
    return <div className="message">Tenant not found.</div>;
  }

  const theme = {
    "--primary": tenant.primary_color,
    "--secondary": tenant.secondary_color,
  };

  const items = activeTab === "articles" ? articles : books;

  return (
    <div className="app" style={theme}>
      <header className="header">
        <div className="brand">
          {tenant.logo_url && (
            <img src={tenant.logo_url} alt={`${tenant.name} logo`} />
          )}

          <div>
            <h1>{tenant.name}</h1>
            <p>{tenant.tagline}</p>
          </div>
        </div>

        <nav>
          <button
            className={activeTab === "articles" ? "active" : ""}
            onClick={() => setActiveTab("articles")}
          >
            Articles
          </button>

          <button
            className={activeTab === "books" ? "active" : ""}
            onClick={() => setActiveTab("books")}
          >
            Books
          </button>
        </nav>
      </header>

      <section className="hero">
        <h2>Welcome to {tenant.name}</h2>
        <p>Discover articles and books published by our community.</p>
      </section>

      <main className="content">
        <h2>{activeTab === "articles" ? "Latest Articles" : "Our Books"}</h2>

        {items.length === 0 ? (
          <p className="empty">
            No published {activeTab} are available yet.
          </p>
        ) : (
          <div className="grid">
            {items.map((item) => (
              <article className="content-card" key={item.id}>
                <h3>{item.title}</h3>

                <p>
                  {activeTab === "articles"
                    ? item.content
                    : item.description || "No description available."}
                </p>

                {activeTab === "books" && item.published_year && (
                  <small>Published: {item.published_year}</small>
                )}
              </article>
            ))}
          </div>
        )}
      </main>

      <footer>
        <p>© {new Date().getFullYear()} {tenant.name}. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;