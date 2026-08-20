export default async function Home() {
  // Fetch data from the FastAPI backend
  const res = await fetch('http://localhost:8000', { cache: 'no-store' });
  const data = await res.json();

  return (
    <main className="flex min-h-screen items-center justify-center bg-gray-100">
      <div className="p-8 bg-white rounded shadow-md">
        <h1 className="text-2xl font-bold mb-4">Wardrobe App Setup</h1>
        <p className="text-green-600 font-semibold">Backend says: {data.message}</p>
      </div>
    </main>
  );
}