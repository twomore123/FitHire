"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@clerk/nextjs";
import { jobAPI } from "@/lib/api-client";

export function DeleteJobButton({ jobId, jobTitle }: { jobId: number; jobTitle: string }) {
  const [isDeleting, setIsDeleting] = useState(false);
  const router = useRouter();
  const { getToken } = useAuth();

  async function handleDelete() {
    const confirmed = window.confirm(
      `Are you sure you want to delete "${jobTitle}"? This action cannot be undone.`
    );
    if (!confirmed) return;

    setIsDeleting(true);
    try {
      const token = await getToken();
      if (!token) throw new Error("Not authenticated");
      await jobAPI.delete(jobId, token);
      router.refresh();
    } catch (error) {
      console.error("Error deleting job:", error);
      alert("Failed to delete job. Please try again.");
    } finally {
      setIsDeleting(false);
    }
  }

  return (
    <button
      onClick={handleDelete}
      disabled={isDeleting}
      className="p-1 rounded-full text-muted-foreground/50 hover:text-destructive hover:bg-destructive/10 transition-colors disabled:opacity-50"
      aria-label={`Delete ${jobTitle}`}
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <line x1="18" y1="6" x2="6" y2="18" />
        <line x1="6" y1="6" x2="18" y2="18" />
      </svg>
    </button>
  );
}
