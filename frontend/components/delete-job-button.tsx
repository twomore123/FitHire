"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@clerk/nextjs";
import { Button } from "@/components/ui/button";
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
    <Button
      size="sm"
      variant="destructive"
      onClick={handleDelete}
      disabled={isDeleting}
    >
      {isDeleting ? "Deleting..." : "Delete"}
    </Button>
  );
}
