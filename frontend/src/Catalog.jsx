export default function Catalog({ products }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
      {products.map((p) => (
        <div
          key={p.handle}
          className="bg-white rounded-2xl shadow-md overflow-hidden relative"
        >
          <div className="relative">
            <img
              src={p.images[0]}
              alt={p.title}
              className="w-full h-96 object-cover"
            />
            {/* Gradient Overlay */}
            <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 via-black/40 to-transparent p-4">
              <h2 className="text-lg font-semibold text-white">{p.title}</h2>
              <p className="text-sm text-gray-200">{p.product_type}</p>
              <p className="text-sm text-gray-300">By {p.vendor}</p>

              <div className="mt-2 text-base font-bold text-white">
                ₹{p.price_min}
                {p.price_max !== p.price_min && ` - ₹${p.price_max}`}
              </div>
            </div>
          </div>

          <div className="p-4">
            <div className="flex flex-wrap gap-1">
              {p.variants.map((v) => (
                <span
                  key={v.id}
                  className={`px-2 py-1 rounded text-xs ${
                    v.available
                      ? "bg-gray-200 text-gray-800"
                      : "bg-gray-100 text-gray-400 line-through"
                  }`}
                >
                  {v.title}
                </span>
              ))}
            </div>

            <button
              className="mt-4 w-full bg-black text-white py-2 rounded-lg hover:bg-gray-800"
              onClick={() => window.open(p.url, "_blank")}
            >
              View Product
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
