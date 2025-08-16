export default function Section({ title, children, right }) {
    return (
      <section className="rounded-2xl bg-[var(--card)] p-5 shadow border border-white/5">
        <div className="mb-3 flex items-center justify-between">
          <h2 className="text-lg font-semibold">{title}</h2>
          {right}
        </div>
        <div className="text-sm text-zinc-300">{children}</div>
      </section>
    );
  }
  