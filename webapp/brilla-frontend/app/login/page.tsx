"use client";

import QuizFooter from "@/components/quiz-footer";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useLoginMutation } from "@/hooks/requests/use-login";
import { zodResolver } from "@hookform/resolvers/zod";
import { EyeOpenIcon } from "@radix-ui/react-icons";
import { useForm } from "react-hook-form";
import { z } from "zod";

const schema = z.object({
  username: z.string().email(),
  password: z.string().min(8),
});

type LoginForm = z.infer<typeof schema>;

const Login = () => {
  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
  } = useForm<LoginForm>({
    resolver: zodResolver(schema),
  });

  const { mutate, isPending } = useLoginMutation();

  const onSubmit = (data: LoginForm) => {
    const formData = new URLSearchParams();
    formData.append("username", data.username);
    formData.append("password", data.password);
    mutate(formData);
  };

  return (
    <div className="bg-white h-screen">
      <div className="flex flex-col items-center justify-center p-5 md:py-[127px] md:px-[173px]">
        <div className="mb-20 md:mb-[200px] self-start">
          <h1 className="text-[30px] text-[#64748B]">BRILLA AI</h1>
        </div>
        <div className="bg-white border border-[#F3EBEF] max-w-[430px] p-10 rounded-md">
          <div className="text-center">
            <h2 className="text-xl text-[#1F2937] mb-2">Admin Login</h2>
            <p className="text-sm text-[#4F5559]">
              Enter your email address and password to login into your account
            </p>
          </div>

          <form
            className="mt-6 flex flex-col gap-6"
            onSubmit={handleSubmit(onSubmit)}
          >
            <div className="items-center">
              <label htmlFor="email">Email Address*</label>
              <Input
                id="email"
                {...register("username")}
                error={errors.username?.message}
              />
            </div>
            <div className="items-center">
              <label htmlFor="password">Password</label>
              <Input
                id="password"
                type="password"
                {...register("password")}
                error={errors.password?.message}
              />
            </div>

            <Button disabled={isPending || !isValid}>Login</Button>
          </form>
        </div>
      </div>
      <QuizFooter />
    </div>
  );
};

export default Login;
