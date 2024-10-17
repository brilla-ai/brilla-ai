import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Select, SelectContent, SelectGroup, SelectItem, SelectLabel, SelectTrigger, SelectValue } from "./ui/select";

 const EditAdminStatus = () => {


    return (
        <div className="max-w-[377px] w-full">
        <h4 className="text-xl text-[#0F172A] font-bold mb-2 text-center">
           Edit Admin
        </h4>
        
        <form className="flex flex-col gap-8">         
         <div className= " flex flex-col align-items-center justify-items-start">
            <div className="text-md text-[#0c1420] font-medium  pb-2">Role</div> 
          <Select>
                <SelectTrigger className="w-full">
                    <SelectValue placeholder="Admin" />
                </SelectTrigger>
                <SelectContent>
                    <SelectGroup>
                    <SelectLabel>Role</SelectLabel>
                    <SelectItem value="admin">Admin</SelectItem>
                    <SelectItem value="user">User</SelectItem>
                   
                    </SelectGroup>
                </SelectContent>
            </Select>

            <div className="text-md text-[#0c1420] font-medium  pb-2 mt-6">Status</div> 
            <Select>
                <SelectTrigger className="w-full">
                    <SelectValue placeholder="Active" />
                </SelectTrigger>
                <SelectContent>
                    <SelectGroup>
                    <SelectLabel>Status</SelectLabel>
                    <SelectItem value="active">Active</SelectItem>
                    <SelectItem value="revoked">Revoked</SelectItem>
                    <SelectItem value="pending">Pending</SelectItem>
                   
                    </SelectGroup>
                </SelectContent>
            </Select>
            </div>


          <Button
            type="button"
            className="self-end w-full"
          >
            Update
          </Button>
        </form>
      </div>
    )
}

export default EditAdminStatus; 

