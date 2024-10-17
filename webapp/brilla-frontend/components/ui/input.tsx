"use client";
import { cn } from "@/lib/utils";
import { EyeClosedIcon, EyeOpenIcon } from "@radix-ui/react-icons";
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

    const wrapperRef = React.useRef<HTMLDivElement | null>(null);

    const isPassword = type === "password";

    const [show, setShow] = React.useState(false);

    const computedInputClassName = cn(
      "w-full border-none min-w-[0px] !outline-0 !bg-[transparent] self-stretch outline-none disabled:text-base-400",
      "placeholder:text-base-400 disabled:cursor-not-allowed",
      inputClassName
    );

    const computedType = React.useMemo(() => {
      switch (type) {
        case "password":
          return show ? "text" : "password";
        case "date":
          return "date";
        default:
          return type;
      }
    }, [type, show]);

    function focusOnInput() {
      const input = wrapperRef.current?.querySelector("input");
      if (!input) return;
      input.focus();
    }

    function handleToggleShow() {
      setShow((prev) => !prev);
      focusOnInput();
    }

    return (
      <div>
        <div
          className={cn(
            innerClassName,
            "flex items-center bg-base-100 p-2 px-4 rounded-lg border border-[#CBD5E1]",
            "focus-within:ring-1 focus-within:ring-[#CBD5E1]",
            { "ring-1 ring-destructive": !!error }
          )}
        >
          {prefix}

          <input
            type={computedType}
            ref={ref}
            className={computedInputClassName}
            id={id ?? otherProps.name}
            {...otherProps}
          />

          {suffix}

          {isPassword ? (
            <button
              type="button"
              className="grid place-content-center h-6 w-6 text-base text-base-500"
              onClick={handleToggleShow}
            >
              {!show ? <EyeOpenIcon /> : null}
              {show ? <EyeClosedIcon /> : null}
            </button>
          ) : null}
        </div>
        {/*ERROR MESSAGE */}
        <p className="text-sm text-destructive">{error}</p>
      </div>
    );
  }
);

Input.displayName = "Input";

export { Input };
