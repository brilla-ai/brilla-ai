import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Select, SelectContent, SelectGroup, SelectItem, SelectLabel, SelectTrigger, SelectValue } from "./ui/select";

 const InviteAdmin = () => {


    return (
        <div className="max-w-[377px] w-full">
        <h4 className="text-xl text-[#0F172A] font-bold mb-2 text-center">
           Invite Admin
        </h4>
        
        <form className="flex flex-col gap-8">
          <div className="flex flex-col align-items-center justify-items-start">
            <label htmlFor="link-input" className="text-md text-[#0c1420] font-medium  pb-2">Full Name*</label>
            <Input id="link-input" placeholder="Full Name" />
          </div>
          <div className="flex flex-col align-items-center justify-items-start">
            <label htmlFor="tags-input" className="text-md text-[#0c1420] font-medium  pb-2">Email Address*</label>
            <Input id="tags-input" placeholder="Email Address" />
          </div>
         
         <div className= " flex flex-col align-items-center justify-items-start">
            <div className="text-md text-[#0c1420] font-medium  pb-2">Role*</div> 
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
            </div>
          <Button
            type="button"
            className="self-end w-full"
          >
            Invite
          </Button>
        </form>
      </div>
    )
}


export default InviteAdmin; 

