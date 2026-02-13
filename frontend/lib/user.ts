/**
 * Server-side utility to fetch the current user's role from the backend.
 * Used in server components to determine role-based navigation and access.
 */

import { auth } from "@clerk/nextjs/server";
import { userAPI } from "@/lib/api-client";

export type UserRole = "coach" | "location_manager" | "regional_director" | "brand_admin";

export interface UserProfile {
  id: number;
  clerk_user_id: string;
  email: string;
  first_name: string | null;
  last_name: string | null;
  role: UserRole;
  brand_id: number | null;
}

/**
 * Fetches the current user's profile from the backend.
 * Returns null if the user hasn't created a profile yet (no backend User record).
 */
export async function getCurrentUserProfile(): Promise<UserProfile | null> {
  try {
    const { getToken } = await auth();
    const token = await getToken();

    if (!token) {
      return null;
    }

    const user = await userAPI.getMe(token);
    return user as UserProfile;
  } catch {
    // User hasn't created a profile yet (404) or other error
    return null;
  }
}
