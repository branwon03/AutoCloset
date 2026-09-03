import ImageUpload from "@/src/components/ImageUpload";

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-xl mx-auto">
        <h1 className="text-3xl font-bold text-center text-gray-900 mb-8">
          Digital Wardrobe
        </h1>
        <ImageUpload />
      </div>
    </main>
  );
}