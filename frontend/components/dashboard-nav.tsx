"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { UserButton } from "@clerk/nextjs";
import { Button } from "@/components/ui/button";

export function DashboardNav() {
  const [role, setRole] = useState<string | null>(null);

  useEffect(() => {
    setRole(localStorage.getItem("fithire_role"));
  }, []);

  return (
    <nav className="bg-white border-b">
      <div className="container mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <Link href="/dashboard">
            <h1 className="text-2xl font-bold">FitHire</h1>
          </Link>

          <div className="flex items-center gap-6">
            {role !== "manager" && (
              <>
                <Link href="/dashboard/coach">
                  <Button variant="ghost">My Profile</Button>
                </Link>
                <Link href="/dashboard/coach/matches">
                  <Button variant="ghost">My Matches</Button>
                </Link>
              </>
            )}
            {role !== "coach" && (
              <Link href="/dashboard/manager">
                <Button variant="ghost">Jobs</Button>
              </Link>
            )}
            <UserButton />
          </div>
        </div>
      </div>
    </nav>
  );
}
