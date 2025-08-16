import { useEffect, useState } from "react";

export default function StoreInsights() {
  const [insights, setInsights] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/insights", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        website_url: "https://memy.co.in",
        persist: true,
        include_competitors: true
      })
    })
      .then(res => res.json())
      .then(data => setInsights(data));
  }, []);

  if (!insights) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6 space-y-8">
      {/* Brand Info */}
      <div className="text-center">
        <h1 className="text-3xl font-bold">{insights.brand?.name}</h1>
        <p className="text-gray-600">{insights.brand?.website}</p>
        <p className="mt-2 max-w-2xl mx-auto text-gray-700 text-sm">
          {insights.brand?.about}
        </p>
      </div>

      {/* Hero Products */}
      <section>
        <h2 className="text-2xl font-semibold mb-4">Hero Products</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {insights.hero_products?.map((p, i) => (
            <div
              key={i}
              className="bg-white rounded-2xl shadow-md overflow-hidden hover:shadow-lg transition"
            >
              <img
                src={p.images?.[0]}
                alt={p.title}
                className="w-full h-56 object-cover"
              />
              <div className="p-4">
                <h3 className="text-lg font-semibold">{p.title}</h3>
                <p className="text-sm text-gray-500">{p.product_type}</p>
                <p className="mt-2 font-medium">
                  ₹{p.price_min}{" "}
                  {p.price_max !== p.price_min && `– ₹${p.price_max}`}
                </p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Full Catalog */}
      <section>
        <h2 className="text-2xl font-semibold mb-4">Catalog</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {insights.catalog?.slice(0, 24).map((p, i) => (
            <a
              key={i}
              href={p.url}
              target="_blank"
              rel="noopener noreferrer"
              className="bg-white rounded-2xl shadow-md overflow-hidden hover:shadow-lg transition block"
            >
              <img
                src={p.images?.[0]}
                alt={p.title}
                className="w-full h-56 object-cover"
              />
              <div className="p-4">
                <h3 className="text-lg font-semibold">{p.title}</h3>
                <p className="text-sm text-gray-500">{p.product_type}</p>
                <p className="mt-2 font-medium">
                  ₹{p.price_min}{" "}
                  {p.price_max !== p.price_min && `– ₹${p.price_max}`}
                </p>
              </div>
            </a>
          ))}
        </div>
      </section>
    </div>
  );
}
