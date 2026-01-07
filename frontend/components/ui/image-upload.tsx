"use client";

import { useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { useAuth } from "@clerk/nextjs";
import Image from "next/image";

interface ImageUploadProps {
  value?: string;
  onChange: (url: string) => void;
  folder: "profile-pictures" | "brand-logos" | "brand-banners";
  label: string;
  aspectRatio?: "square" | "wide" | "portrait";
  maxSizeMB?: number;
}

export function ImageUpload({
  value,
  onChange,
  folder,
  label,
  aspectRatio = "square",
  maxSizeMB = 5,
}: ImageUploadProps) {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { getToken } = useAuth();

  const aspectRatioClasses = {
    square: "aspect-square",
    wide: "aspect-video",
    portrait: "aspect-[3/4]",
  };

  const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith("image/")) {
      setError("Please select an image file");
      return;
    }

    // Validate file size
    const sizeMB = file.size / (1024 * 1024);
    if (sizeMB > maxSizeMB) {
      setError(`File size must be less than ${maxSizeMB}MB`);
      return;
    }

    setError(null);
    setUploading(true);

    try {
      const token = await getToken();
      if (!token) {
        throw new Error("Not authenticated");
      }

      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/upload/image?folder=${folder}`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Upload failed");
      }

      const data = await response.json();
      onChange(data.url);
    } catch (err: any) {
      console.error("Upload error:", err);
      setError(err.message || "Failed to upload image");
    } finally {
      setUploading(false);
    }
  };

  const handleRemove = () => {
    onChange("");
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div className="space-y-4">
      <label className="block text-sm font-medium">{label}</label>

      {value ? (
        <div className="space-y-2">
          <div className={`relative w-full max-w-sm ${aspectRatioClasses[aspectRatio]} overflow-hidden rounded-lg border`}>
            <Image
              src={value}
              alt={label}
              fill
              className="object-cover"
            />
          </div>
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={handleRemove}
          >
            Remove Image
          </Button>
        </div>
      ) : (
        <div className="space-y-2">
          <div
            className={`relative w-full max-w-sm ${aspectRatioClasses[aspectRatio]} border-2 border-dashed rounded-lg flex items-center justify-center bg-zinc-50 hover:bg-zinc-100 transition-colors cursor-pointer`}
            onClick={() => fileInputRef.current?.click()}
          >
            <div className="text-center p-4">
              <svg
                className="mx-auto h-12 w-12 text-zinc-400"
                stroke="currentColor"
                fill="none"
                viewBox="0 0 48 48"
              >
                <path
                  d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                  strokeWidth={2}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
              <p className="mt-2 text-sm text-muted-foreground">
                Click to upload
              </p>
              <p className="text-xs text-muted-foreground mt-1">
                PNG, JPG, WebP up to {maxSizeMB}MB
              </p>
            </div>
          </div>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/png,image/jpeg,image/jpg,image/webp"
            className="hidden"
            onChange={handleFileSelect}
            disabled={uploading}
          />
        </div>
      )}

      {uploading && (
        <p className="text-sm text-muted-foreground">Uploading...</p>
      )}

      {error && (
        <p className="text-sm text-red-600">{error}</p>
      )}
    </div>
  );
}
