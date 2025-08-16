export async function fetchInsights(baseUrl, website_url, opts = {}) {
    const res = await fetch(`${baseUrl}/api/insights`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        website_url,
        persist: Boolean(opts.persist),
        include_competitors: Boolean(opts.include_competitors),
      }),
    });
    const json = await res.json();
    if (!res.ok || !json.ok) {
      const msg = json?.error || res.statusText || "Error";
      throw new Error(`${res.status}: ${msg}`);
    }
    return json.data;
  }
  