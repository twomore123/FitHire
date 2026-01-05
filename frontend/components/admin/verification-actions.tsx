"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { adminAPI } from "@/lib/api-client";

interface VerificationActionsProps {
  coachId: number;
  token: string;
}

export function VerificationActions({ coachId, token }: VerificationActionsProps) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  const handleVerify = async () => {
    setLoading(true);
    try {
      await adminAPI.verifyCoach(coachId, token);
      router.refresh(); // Refresh the page to update the list
    } catch (error: any) {
      console.error("Failed to verify coach:", error);
      alert(`Failed to verify: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleReject = async () => {
    setLoading(true);
    try {
      await adminAPI.rejectCoach(coachId, token);
      router.refresh(); // Refresh the page to update the list
    } catch (error: any) {
      console.error("Failed to reject coach:", error);
      alert(`Failed to reject: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex gap-2">
      <Button
        onClick={handleVerify}
        size="sm"
        disabled={loading}
      >
        {loading ? "Processing..." : "Approve"}
      </Button>
      <Button
        onClick={handleReject}
        size="sm"
        variant="outline"
        disabled={loading}
      >
        {loading ? "Processing..." : "Reject"}
      </Button>
    </div>
  );
}
