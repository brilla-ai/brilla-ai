

"use client"

import * as React from "react"

import {
  ColumnDef,
  ColumnFiltersState,
  SortingState,
  VisibilityState,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
} from "@tanstack/react-table"
import { ArrowUpDown, ChevronDown, MoreHorizontal, Plus, Search, SearchIcon } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Input } from "@/components/ui/input"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Modal } from "./ui/modal";
import InviteAdmin from "./invite-admin";
import { DialogClose } from "@radix-ui/react-dialog";
import EditAdminStatus from "./edit-status";

const data: Payment[] = [
  {
    id: "m5gr84i9",
    amount: 316,
    status: "revoked",
    name: "Carmella",
    email_address: "ken99@yahoo.com",
    role: "admin",
    date_created: new Date().toDateString()
  },
  {
    id: "3u1reuv4",
    amount: 242,
    status: "active",
    email_address: "Abe45@gmail.com",
    name: "Monserrat",
    role: "admin",
    date_created: new Date().toDateString()
  },
  {
    id: "derv1ws0",
    amount: 837,
    status: "pending",
    email_address: "Monserrat44@gmail.com",
    name: "Monserrat",
    role: "admin",
    date_created: new Date().toDateString(),
  },
  {
    id: "5kma53ae",
    amount: 874,
    status: "pending",
    email_address: "Silas22@gmail.com",
    name: "Silas",
    role: "admin",
    date_created: new Date().toDateString(),
  },
  {
    id: "bhqecj4p",
    amount: 721,
    status: "revoked",
    email_address: "carmella@hotmail.com",
    name: "Carmella",
    role: "admin",
    date_created: new Date().toDateString()
  },
]

export type Payment = {
  id: string
  amount: number
  status: "pending" | "revoked" | "active"
  email_address: string
  name: string
  role: string 
  date_created: string
}



export function AdminUser() {
  const [sorting, setSorting] = React.useState<SortingState>([])
  const [ isEditModalOpen, setIsEditModalOpen] = React.useState(false)  
  const [isDeleteModalOpen, setIsDeleteModalOpen] = React.useState(false)
  const [ isInviteModalOpen, setInviteModal] = React.useState(false)
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>(
    []
  )
  const columns: ColumnDef<Payment>[] = [
    {
      id: "select",
      header: ({ table }) => (
        <Checkbox
          checked={
            table.getIsAllPageRowsSelected() ||
            (table.getIsSomePageRowsSelected() && "indeterminate")
          }
          onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
          aria-label="Select all"
        />
      ),
      cell: ({ row }) => (
        <Checkbox
          checked={row.getIsSelected()}
          onCheckedChange={(value) => row.toggleSelected(!!value)}
          aria-label="Select row"
        />
      ),
      enableSorting: false,
      enableHiding: false,
    },
  
    {
      accessorKey: "name",
      header: "Name",
      cell: ({ row }) => (
        <div className="capitalize">{row.getValue("name")}</div>
      ),
    },
    {
      accessorKey: "email_address",
      header: ({ column }) => {
        return (
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          >
            Email Address
            <ArrowUpDown className="ml-2 h-4 w-4" />
          </Button>
        )
      },
      cell: ({ row }) => <div className="lowercase">{row.getValue("email_address")}</div>,
    },
  
    {
      accessorKey: "role",
      header: "Role",
      cell: ({ row }) => (
        <div className="capitalize">{row.getValue("role")}</div>
      ),
    },
    {
      accessorKey: "date_created",
      header: "Date Created",
      cell: ({ row }) => (
        <div className="capitalize">{row.getValue("date_created")}</div>
      ),
    },
    {
      accessorKey: "status",
      header: "Status",
      cell: ({ row }) => (
        <div className={`capitalize ${row.getValue("status") === "active" ? "text-[#149B3E] border-2 bg-[#F1FEF5] border-[#fff] rounded p-1  px-2 w-fit" : row.getValue("status") === "pending" ? "text-yellow-500 border-2 bg-yellow-50 border-[#fff] rounded p-1 px-2 w-fit" : "text-red-500 bg-red-50 border-2 border-[#fff] rounded p-1  px-2 w-fit "}`}>
            {row.getValue("status")}
        </div>
  
      ),
    },
    {
      id: "actions",
      enableHiding: false,
      cell: ({ row }) => {
        const payment = row.original
  
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="h-8 w-8 p-0">
                <span className="sr-only">Open menu</span>
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>Actions</DropdownMenuLabel>
              <DropdownMenuItem
                onClick={() => setIsEditModalOpen(true)}
              >
                Edit
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => setIsDeleteModalOpen(true)}>Delete</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        )
      },
    },
  ]
  const [columnVisibility, setColumnVisibility] =
    React.useState<VisibilityState>({})
  const [rowSelection, setRowSelection] = React.useState({})

  const table = useReactTable({
    data,
    columns,
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onColumnVisibilityChange: setColumnVisibility,
    onRowSelectionChange: setRowSelection,
    state: {
      sorting,
      columnFilters,
      columnVisibility,
      rowSelection,
    },
  })

  return (
    <div className="w-full">
      <div className="flex items-center py-4">
       
      <div className="relative max-w-sm">
        <Input
          placeholder="Search by name..." 
          value={(table.getColumn("email_address")?.getFilterValue() as string) ?? ""}
          onChange={(event) =>
            table.getColumn("email_address")?.setFilterValue(event.target.value)
          }
          className="ml-32" // Ensure enough padding for the placeholder text
        />
      </div>
        {/* <Input
          placeholder="Search by name..."
          value={(table.getColumn("email_address")?.getFilterValue() as string) ?? ""}
          onChange={(event) =>
            table.getColumn("email_address")?.setFilterValue(event.target.value)
          }
          className="max-w-sm"
        /> */}

          <Button className="ml-auto" onClick={ () => setInviteModal(true)} > 
          <Plus className="mr-2 h-4 w-4 "  />
          Invite admin
           </Button>

           <Modal isOpen={isInviteModalOpen} setIsOpen={setInviteModal}>
            <div className="bg-white p-4 flex gap-4 items-center justify-center rounded-b-lg">
            <InviteAdmin />
            </div>
            </Modal>


            <Modal isOpen={isEditModalOpen} setIsOpen={setIsEditModalOpen}>
            <div className="bg-white p-4 flex gap-4 items-center justify-center rounded-b-lg">
            <EditAdminStatus />
            </div>
            </Modal>


            <Modal isOpen={isDeleteModalOpen} setIsOpen={setIsDeleteModalOpen}
            title ="Delete Admin User"
            description= "Are you sure you want to delete the admin user?">
            <div className="bg-[#FAFAFA] p-4 flex gap-4 items-center justify-center rounded-b-lg">
          <DialogClose asChild>
            <Button className="max-w-[126px] self-end" variant={"outline"}>
              Cancel
            </Button>
          </DialogClose>
          <Button className="max-w-[126px] self-end">Proceed</Button>
            </div>
            </Modal>
    
      </div>
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => {
                  return (
                    <TableHead key={header.id}>
                      {header.isPlaceholder
                        ? null
                        : flexRender(
                            header.column.columnDef.header,
                            header.getContext()
                          )}
                    </TableHead>
                  )
                })}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow
                  key={row.id}
                  data-state={row.getIsSelected() && "selected"}
                >
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext()
                      )}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center"
                >
                  No results.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
      <div className="flex items-center justify-end space-x-2 py-4">
        <div className="flex-1 text-sm text-muted-foreground">
          {table.getFilteredSelectedRowModel().rows.length} of{" "}
          {table.getFilteredRowModel().rows.length} row(s) selected.
        </div>
        <div className="space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => table.previousPage()}
            disabled={!table.getCanPreviousPage()}
          >
            Previous
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => table.nextPage()}
            disabled={!table.getCanNextPage()}
          >
            Next
          </Button>
        </div>
      </div>
    </div>
  )
}
export default AdminUser;
