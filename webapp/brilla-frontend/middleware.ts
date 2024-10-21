import { NextResponse, NextRequest } from "next/server";
// Remove this line:
// import { useAuthStore } from "./stores";

export const config = {
  matcher: ["/",],
};

export function middleware(req: NextRequest) {

  // You can't use hooks or client-side code in middleware
  // const token = useAuthStore.getState().token;

  // Instead, you should get the token from a cookie or header
  const token = req.cookies.get("access_token")?.value;

  // This condition was inverted, causing the middleware to only run for the home page
  if (req.nextUrl.pathname !== "/login" && req.nextUrl.pathname !== "/") {
    if (!token) {
      return NextResponse.redirect(new URL("/login", req.url));
    }
  }

  // If we reach here, allow the request to continue
  return NextResponse.next();
}
