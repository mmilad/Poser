export default function HomePage() {
  return (
    <main style={{ padding: 24, fontFamily: "sans-serif" }}>
      <h1>Poser Pose API</h1>
      <p>Deterministic pose resolution service is running.</p>
      <p>POST to <code>/api/v1/pose/resolve</code>.</p>
    </main>
  );
}
