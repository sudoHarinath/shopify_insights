// import { useState } from "react";
// import UrlForm from "./components/UrlForm.jsx";
// import Section from "./components/Section.jsx";
// import JsonBlock from "./components/JsonBlock.jsx";
// import { fetchInsights } from "./lib/api.js";

// const API_BASE =
//   import.meta.env.VITE_API_BASE || "http://localhost:8000";

// export default function App() {
//   const [loading, setLoading] = useState(false);
//   const [err, setErr] = useState("");
//   const [data, setData] = useState(null);

//   async function run({ url, persist, comp }) {
//     setErr("");
//     setData(null);
//     setLoading(true);
//     try {
//       const payload = await fetchInsights(API_BASE, url, {
//         persist,
//         include_competitors: comp,
//       });
//       setData(payload);
//     } catch (e) {
//       setErr(String(e.message || e));
//     } finally {
//       setLoading(false);
//     }
//   }

//   return (
//     <div className="mx-auto max-w-5xl p-6 space-y-6">
//       <h1 className="text-2xl font-bold">Shopify Store Insights</h1>
//       <UrlForm onSubmit={run} />
//       {loading && <div className="text-sm">Loading…</div>}
//       {err && (
//         <Section title="Error">
//           <div className="text-red-400">{err}</div>
//         </Section>
//       )}
//       {data && (
//         <>
//           <Section title="Brand">
//             <div className="grid gap-2">
//               <div>
//                 <span className="text-zinc-400">Website: </span>
//                 <a
//                   href={data.website}
//                   target="_blank"
//                   rel="noreferrer"
//                   className="underline"
//                 >
//                   {data.website}
//                 </a>
//               </div>
//               {data.brand_name && (
//                 <div>
//                   <span className="text-zinc-400">Name: </span>
//                   {data.brand_name}
//                 </div>
//               )}
//               {data.about_text && (
//                 <div className="whitespace-pre-wrap">{data.about_text}</div>
//               )}
//             </div>
//           </Section>

//           <Section
//             title={`Hero Products (${data.hero_products?.length || 0})`}
//             right={
//               <a
//                 className="text-xs text-zinc-400 underline"
//                 href={data.website}
//                 target="_blank"
//                 rel="noreferrer"
//               >
//                 Home
//               </a>
//             }
//           >
//             <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
//               {(data.hero_products || []).map((p) => (
//                 <a
//                   key={p.handle}
//                   className="rounded-xl border border-white/10 p-3 hover:bg-white/5"
//                   href={p.url}
//                   target="_blank"
//                   rel="noreferrer"
//                 >
//                   <div className="font-medium">{p.title}</div>
//                   {p.product_type && (
//                     <div className="text-xs text-zinc-400">
//                       {p.product_type}
//                     </div>
//                   )}
//                   {p.price_min != null && (
//                     <div className="text-sm">
//                       {p.price_min === p.price_max
//                         ? `₹${p.price_min}`
//                         : `₹${p.price_min} – ₹${p.price_max}`}
//                     </div>
//                   )}
//                 </a>
//               ))}
//             </div>
//           </Section>

//           <Section title={`Catalog (${data.catalog?.length || 0})`}>
//             <JsonBlock data={(data.catalog || []).slice(0, 50)} />
//           </Section>

//           <Section title="Policies">
//             <ul className="list-disc pl-5 space-y-1">
//               {(data.policies || []).map((p, i) => (
//                 <li key={i}>
//                   <span className="font-medium capitalize">{p.kind}</span>{" "}
//                   {p.url && (
//                     <a className="underline" href={p.url} target="_blank" rel="noreferrer">
//                       link
//                     </a>
//                   )}
//                 </li>
//               ))}
//             </ul>
//           </Section>

//           <Section title={`FAQs (${data.faqs?.length || 0})`}>
//             <ul className="space-y-3">
//               {(data.faqs || []).slice(0, 20).map((f, i) => (
//                 <li key={i} className="rounded-xl border border-white/10 p-3">
//                   <div className="font-medium">{f.question}</div>
//                   <div className="text-sm text-zinc-300">{f.answer}</div>
//                 </li>
//               ))}
//             </ul>
//           </Section>

//           <Section title="Socials">
//             <ul className="list-disc pl-5">
//               {(data.socials || []).map((s, i) => (
//                 <li key={i}>
//                   <span className="capitalize">{s.platform}</span>:{" "}
//                   <a className="underline" href={s.url} target="_blank" rel="noreferrer">
//                     {s.url}
//                   </a>
//                 </li>
//               ))}
//             </ul>
//           </Section>

//           <Section title="Contacts">
//             <div className="grid md:grid-cols-3 gap-4">
//               <div>
//                 <div className="text-sm text-zinc-400 mb-1">Emails</div>
//                 <ul className="space-y-1">
//                   {(data.contacts?.emails || []).map((e, i) => (
//                     <li key={i} className="text-sm">{e}</li>
//                   ))}
//                 </ul>
//               </div>
//               <div>
//                 <div className="text-sm text-zinc-400 mb-1">Phones</div>
//                 <ul className="space-y-1">
//                   {(data.contacts?.phones || []).map((p, i) => (
//                     <li key={i} className="text-sm">{p}</li>
//                   ))}
//                 </ul>
//               </div>
//               <div>
//                 <div className="text-sm text-zinc-400 mb-1">Addresses</div>
//                 <ul className="space-y-1">
//                   {(data.contacts?.addresses || []).map((a, i) => (
//                     <li key={i} className="text-sm">{a}</li>
//                   ))}
//                 </ul>
//               </div>
//             </div>
//           </Section>

//           <Section title="Important Links">
//             <JsonBlock data={data.important_links || {}} />
//           </Section>

//           <Section title="Meta">
//             <JsonBlock data={data.meta || {}} />
//           </Section>
//         </>
//       )}
//     </div>
//   );
// }


import { useState } from "react";
import UrlForm from "./components/UrlForm.jsx";
import Section from "./components/Section.jsx";
import JsonBlock from "./components/JsonBlock.jsx";
import { fetchInsights } from "./lib/api.js";
import Catalog from "./Catalog.jsx"

const API_BASE =
  import.meta.env.VITE_API_BASE || "http://localhost:8000";

export default function App() {
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");
  const [data, setData] = useState(null);

  async function run({ url, persist, comp }) {
    setErr("");
    setData(null);
    setLoading(true);
    try {
      const payload = await fetchInsights(API_BASE, url, {
        persist,
        include_competitors: comp,
      });
      setData(payload);
    } catch (e) {
      setErr(String(e.message || e));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-5xl p-6 space-y-6">
      <h1 className="text-2xl font-bold">Shopify Store Insights</h1>
      <UrlForm onSubmit={run} />
      {loading && <div className="text-sm">Loading…</div>}
      {err && (
        <Section title="Error">
          <div className="text-red-400">{err}</div>
        </Section>
      )}
      {data && (
        <>
          <Section title="Brand">
            <div className="grid gap-2">
              <div>
                <span className="text-zinc-400">Website: </span>
                <a
                  href={data.website}
                  target="_blank"
                  rel="noreferrer"
                  className="underline"
                >
                  {data.website}
                </a>
              </div>
              {data.brand_name && (
                <div>
                  <span className="text-zinc-400">Name: </span>
                  {data.brand_name}
                </div>
              )}
              {data.about_text && (
                <div className="whitespace-pre-wrap">{data.about_text}</div>
              )}
            </div>
          </Section>

          <Section
            title={`Hero Products (${data.hero_products?.length || 0})`}
            right={
              <a
                className="text-xs text-zinc-400 underline"
                href={data.website}
                target="_blank"
                rel="noreferrer"
              >
                Home
              </a>
            }
          >
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {(data.hero_products || []).map((p) => (
                <a
                  key={p.handle}
                  className="rounded-xl border border-white/10 p-3 hover:bg-white/5 flex gap-3"
                  href={p.url}
                  target="_blank"
                  rel="noreferrer"
                >
                  {p.images?.length > 0 && (
                    <img
                      src={p.images[0]}
                      alt={p.title}
                      className="w-20 h-20 object-cover rounded-md border border-white/10"
                    />
                  )}
                  <div className="flex flex-col">
                    <div className="font-medium">{p.title}</div>
                    {p.product_type && (
                      <div className="text-xs text-zinc-400">
                        {p.product_type}
                      </div>
                    )}
                    {p.price_min != null && (
                      <div className="text-sm">
                        {p.price_min === p.price_max
                          ? `₹${p.price_min}`
                          : `₹${p.price_min} – ₹${p.price_max}`}
                      </div>
                    )}
                  </div>
                </a>
              ))}
            </div>
          </Section>

          <div className="p-8">
            <h1 className="text-2xl font-bold mb-6">Catalog</h1>
            <Catalog products={(data.catalog || []).slice(0, 50)} />
          </div>
          {/* <Section title={`Catalog (${data.catalog?.length || 0})`}>
            <JsonBlock data={(data.catalog || []).slice(0, 50)} />
          </Section> */}

          <Section title="Policies">
            <ul className="list-disc pl-5 space-y-1">
              {(data.policies || []).map((p, i) => (
                <li key={i}>
                  <span className="font-medium capitalize">{p.kind}</span>{" "}
                  {p.url && (
                    <a className="underline" href={p.url} target="_blank" rel="noreferrer">
                      link
                    </a>
                  )}
                </li>
              ))}
            </ul>
          </Section>

          <Section title={`FAQs (${data.faqs?.length || 0})`}>
            <ul className="space-y-3">
              {(data.faqs || []).slice(0, 20).map((f, i) => (
                <li key={i} className="rounded-xl border border-white/10 p-3">
                  <div className="font-medium">{f.question}</div>
                  <div className="text-sm text-zinc-300">{f.answer}</div>
                </li>
              ))}
            </ul>
          </Section>

          <Section title="Socials">
            <ul className="list-disc pl-5">
              {(data.socials || []).map((s, i) => (
                <li key={i}>
                  <span className="capitalize">{s.platform}</span>:{" "}
                  <a className="underline" href={s.url} target="_blank" rel="noreferrer">
                    {s.url}
                  </a>
                </li>
              ))}
            </ul>
          </Section>

          <Section title="Contacts">
            <div className="grid md:grid-cols-3 gap-4">
              <div>
                <div className="text-sm text-zinc-400 mb-1">Emails</div>
                <ul className="space-y-1">
                  {(data.contacts?.emails || []).map((e, i) => (
                    <li key={i} className="text-sm">{e}</li>
                  ))}
                </ul>
              </div>
              <div>
                <div className="text-sm text-zinc-400 mb-1">Phone</div>
                <ul className="space-y-1">
                  {data.contacts[1]?.phones?.[1] && (
                    <li className="text-sm">{data.contacts[0].phones[0]}</li>
                  )}
                </ul>
              </div>

              <div>
                <div className="text-sm text-zinc-400 mb-1">Addresses</div>
                <ul className="space-y-1">
                  {(data.contacts?.addresses || []).map((a, i) => (
                    <li key={i} className="text-sm">{a}</li>
                  ))}
                </ul>
              </div>
            </div>
          </Section>

          {/* Important Links */}
          <div className="mt-6">
            <h2 className="text-xl font-semibold">Important Links</h2>
            <ul className="list-disc pl-5 space-y-1">
              {Object.entries(data.important_links)
                .filter(([_, v]) => v) // remove null or empty
                .map(([key, value]) => (
                  <li key={key}>
                    <a
                      href={value}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline"
                    >
                      {key.replace("_", " ")}
                    </a>
                  </li>
                ))}
            </ul>
          </div>

          {/* Meta */}
          <div className="mt-6">
            <h2 className="text-xl font-semibold">Meta</h2>
            <p>Total Products: {data.meta.catalog_count}</p>
          </div>

        </>
      )}
    </div>
  );
}
