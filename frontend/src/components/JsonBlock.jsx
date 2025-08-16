export default function JsonBlock({ data }) {
    return (
      <pre className="overflow-auto rounded-xl bg-black/40 p-4 text-xs leading-relaxed">
        {JSON.stringify(data, null, 2)}
      </pre>
    );
  }
  