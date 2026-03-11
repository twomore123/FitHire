"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { UserButton } from "@clerk/nextjs";
import { BrandLogo } from "@/components/brand-logo";

export function DashboardNav() {
  const [role, setRole] = useState<string | null>(null);
  const pathname = usePathname();

  useEffect(() => {
    setRole(localStorage.getItem("fithire_role"));
  }, []);

  function navLinkClass(href: string) {
    const isActive = pathname.startsWith(href);
    return `text-sm font-medium px-3 py-2 rounded-lg transition-colors ${
      isActive
        ? "bg-primary/10 text-primary"
        : "text-muted-foreground hover:text-foreground hover:bg-secondary"
    }`;
  }

  return (
    <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-border/50">
      <div className="container mx-auto px-6">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center gap-8">
            <Link href="/dashboard">
              <BrandLogo size="sm" />
            </Link>

            <div className="hidden md:flex items-center gap-1">
              {role !== "manager" && (
                <>
                  <Link href="/dashboard/coach" className={navLinkClass("/dashboard/coach")}>
                    My Profile
                  </Link>
                  <Link href="/dashboard/coach/matches" className={navLinkClass("/dashboard/coach/matches")}>
                    My Matches
                  </Link>
                </>
              )}
              {role !== "coach" && (
                <Link href="/dashboard/manager" className={navLinkClass("/dashboard/manager")}>
                  Jobs
                </Link>
              )}
            </div>
          </div>

          <UserButton
            appearance={{
              elements: {
                avatarBox: "w-9 h-9",
              },
            }}
          />
        </div>
      </div>
    </nav>
  );
}
