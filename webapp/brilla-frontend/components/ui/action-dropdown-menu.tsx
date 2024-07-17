"use client";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

type DropdownProps = Readonly<{
  children: React.ReactNode;
  actions: { action: string; onClickFn: () => void }[];
}>;

export function ActionDropdown({ children, actions }: DropdownProps) {
  return (
    <>
      <DropdownMenu>
        <DropdownMenuTrigger>{children}</DropdownMenuTrigger>
        <DropdownMenuContent>
          {actions.map(({ action, onClickFn }) => (
            <DropdownMenuItem
              key={action}
              className="py-2 px-3 text-xs rounded-[4px] min-w-[116px] hover:outline-none hover:cursor-pointer hover:bg-blue-50 outline-none"
              onSelect={onClickFn}
              data-testid="dropdown-menu-item"
            >
              {action}
            </DropdownMenuItem>
          ))}
        </DropdownMenuContent>
      </DropdownMenu>
    </>
  );
}
