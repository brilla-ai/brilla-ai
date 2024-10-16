import { cn } from "@/lib/utils";
import React from "react";

type Props = Readonly<{
  [other: string]: any;
  error?: string | boolean;
  className?: string;
  type?: React.InputHTMLAttributes<HTMLInputElement>["type"];
  name?: string;
  id?: string;
  prefix?: React.ReactNode;
  innerClassName?: string;
  inputClassName?: string;
}> &
  React.HTMLAttributes<HTMLInputElement> &
  React.HTMLAttributes<HTMLTextAreaElement>;

const Input = React.forwardRef(
  (props: Props, ref: React.Ref<HTMLInputElement & HTMLTextAreaElement>) => {
    const {
      label,
      type = "text",
      error = "",
      className,
      innerClassName,
      inputClassName,
      prefix,
      suffix,
      id,
      ...otherProps
    } = props;
    const computedInputClassName = cn(
      "w-full border-none min-w-[0px] !outline-0 !bg-[transparent] self-stretch outline-none disabled:text-base-400",
      "placeholder:text-base-400 disabled:cursor-not-allowed",
      inputClassName
    );
    return (
      <div>
        <div
          className={cn(
            innerClassName,
            "flex items-center bg-base-100 p-2 px-4 rounded-lg border border-[#CBD5E1]",
            "focus-within:ring-1 focus-within:ring-[#CBD5E1]",
            { "ring-1 ring-error": !!error }
          )}
        >
          {prefix}

          <input
            type={type}
            ref={ref}
            className={computedInputClassName}
            id={id ?? otherProps.name}
            {...otherProps}
          />

          {suffix}
        </div>
        {/*ERROR MESSAGE */}
        <p>{error}</p>
      </div>
    );
  }
);

Input.displayName = "Input";

export { Input };
