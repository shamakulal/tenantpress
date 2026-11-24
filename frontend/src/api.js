const API_BASE = import.meta.env.VITE_API_BASE_URL;

export function getTenantSlug() {
  const hostname = window.location.hostname;

  // Local testing: localhost:5173/?tenant=tenant-b
  if (hostname === "localhost" || hostname === "127.0.0.1") {
    return (
      new URLSearchParams(window.location.search).get("tenant") ||
      "tenant-a"
    );
  }

  // Production: tenant-a.yourdomain.com
  return hostname.split(".")[0];
}

async function apiRequest(endpoint) {
  const tenantSlug = getTenantSlug();

  const response = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      "X-Tenant-Slug": tenantSlug,
    },
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json();
}

export function fetchTenant() {
  return apiRequest("/tenants/current");
}

export function fetchArticles() {
  return apiRequest("/articles/");
}

export function fetchBooks() {
  return apiRequest("/books/");
}