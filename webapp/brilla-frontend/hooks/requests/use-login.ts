import { login } from "@/services/auth";
import { useAuthStore } from "@/stores/auth";
import { useMutation } from "@tanstack/react-query";
import Cookies from "js-cookie";
import { useRouter } from "next/navigation";

export function useLoginMutation() {
  const { setToken } = useAuthStore();
  const router = useRouter();

  return useMutation({
    mutationFn: login,
    onSuccess: (res: any) => {
      console.log(res);
      Cookies.set("access_token", res.access_token);
      setToken(res.access_token);
      router.push("/settings");
    },
  });
}
