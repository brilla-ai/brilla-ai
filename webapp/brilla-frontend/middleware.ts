import { NextResponse, NextRequest } from "next/server";
// Remove this line:
// import { useAuthStore } from "./stores";

export const config = {
  matcher: ["/", "/((?!api|_next/static|_next/image|favicon.ico).*)"],
};

export function middleware(req: NextRequest) {
  console.log("Middleware is running");

  // You can't use hooks or client-side code in middleware
  // const token = useAuthStore.getState().token;

  // Instead, you should get the token from a cookie or header
  const token = req.cookies.get("access_token")?.value;

  console.log("token", token);

  // This condition was inverted, causing the middleware to only run for the home page
  if (req.nextUrl.pathname !== "/login") {
    if (!token) {
      return NextResponse.redirect(new URL("/login", req.url));
    }
  }

  // If we reach here, allow the request to continue
  return NextResponse.next();
}
