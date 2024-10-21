import { axiosClient } from "@/config/axios-client";

type LoginResponse = {
  access_token: string;
  token_type: string;
};

export async function login(credentials: URLSearchParams) {
  const response = await axiosClient.post("/users/token", credentials, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });
  return response;
}
