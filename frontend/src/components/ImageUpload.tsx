"use client";

import { useState } from "react";

export default function ImageUpload() {
  const [uploading, setUploading] = useState(false);
  const [uploadedUrl, setUploadedUrl] = useState<string | null>(null);

  async function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;

    try {
      setUploading(true);

      // 1. Ask FastAPI for the temporary pre-signed URL
      const res = await fetch("http://localhost:8000/api/media/presigned-url", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ file_type: file.type }),
      });

      if (!res.ok) throw new Error("Could not retrieve presigned URL");
      const { upload_url, public_url } = await res.json();

      // 2. Upload file directly to S3 via HTTP PUT
      const s3Res = await fetch(upload_url, {
        method: "PUT",
        headers: { "Content-Type": file.type },
        body: file,
      });

      if (!s3Res.ok) throw new Error("Direct S3 upload failed");

      setUploadedUrl(public_url);
    } catch (err) {
      console.error("Upload error:", err);
      alert("Failed to upload image.");
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="flex flex-col items-center gap-4 p-8 border-2 border-dashed border-gray-300 rounded-xl bg-white shadow-sm max-w-md mx-auto mt-6">
      <h3 className="font-semibold text-lg text-gray-800">Add Clothing Item</h3>
      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        disabled={uploading}
        className="block text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer"
      />
      {uploading && <p className="text-blue-600 animate-pulse text-sm">Uploading directly to S3...</p>}
      {uploadedUrl && (
        <div className="mt-4 flex flex-col items-center">
          <p className="text-emerald-600 font-medium text-sm mb-2">Upload successful!</p>
          <img
            src={uploadedUrl}
            alt="Uploaded item"
            className="w-48 h-48 object-cover rounded-lg border shadow-sm"
          />
        </div>
      )}
    </div>
  );
}