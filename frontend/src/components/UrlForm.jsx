import { useState } from "react";

export default function UrlForm({ onSubmit }) {
  const [url, setUrl] = useState("");
  const [persist, setPersist] = useState(false);
  const [comp, setComp] = useState(false);

  return (
    <form
      className="flex flex-col gap-3"
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit({ url, persist, comp });
      }}
    >
      <input
        type="url"
        required
        placeholder="https://example.myshopify.com"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        className="w-full rounded-2xl bg-zinc-800 px-4 py-3 outline-none"
      />
      <div className="flex items-center gap-4 text-sm text-zinc-300">
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={persist}
            onChange={(e) => setPersist(e.target.checked)}
          />
          Persist to DB
        </label>
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={comp}
            onChange={(e) => setComp(e.target.checked)}
          />
          Include competitors (naive)
        </label>
      </div>
      <button
        type="submit"
        className="rounded-2xl bg-white/10 px-4 py-2 hover:bg-white/20"
      >
        Fetch Insights
      </button>
    </form>
  );
}
