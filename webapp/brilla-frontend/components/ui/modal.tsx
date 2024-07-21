import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { cn } from "@/lib/utils";
import { PropsWithChildren } from "react";

type ModalProps = PropsWithChildren<{
  className?: string;
  title?: string;
  description?: string;
  isOpen: boolean;
  setIsOpen: (o: boolean) => void;
}>;

export function Modal({
  className,
  children,
  title,
  description,
  isOpen,
  setIsOpen,
}: ModalProps) {
  return (
    <>
      {isOpen ? (
        <Dialog open={isOpen} onOpenChange={setIsOpen}>
          <DialogContent
            className={cn("sm:max-w-[425px] bg-white p-0", className)}
          >
            <DialogHeader className="p-6">
              <DialogTitle className="text-lg font-semibold text-[#0F172A] text-center">
                {title}
              </DialogTitle>
              <DialogDescription className="text-sm text-[#64748B] text-center">
                {description}
              </DialogDescription>
            </DialogHeader>
            <div>{children}</div>
          </DialogContent>
        </Dialog>
      ) : null}
    </>
  );
}
