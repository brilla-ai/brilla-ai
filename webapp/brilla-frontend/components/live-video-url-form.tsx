"use client";

import React from "react";
import { Input } from "./ui/input";
import { Switch } from "./ui/switch";
import { Expandable } from "./ui/expandable";
import { Button } from "./ui/button";

const LiveVideoUrlForm = () => {
  const [checked, setChecked] = React.useState(false);
  return (
    <div className="max-w-[377px] w-full">
      <h4 className="text-lg text-[#0F172A] font-semibold mb-2">
        Add Live Video Url
      </h4>
      <p className="text-[#64748B] text-sm mb-8">
        Add a youtube or stream link to this page. This will give authorized
        users access to the displayed content
      </p>
      <form className="flex flex-col gap-8">
        <div className="grid grid-cols-[82px,calc(100%_-_82px)]  items-center">
          <label htmlFor="link-input">Video link</label>
          <Input id="link-input" />
        </div>
        <div className="grid grid-cols-[82px,calc(100%_-_82px)]  items-center">
          <label htmlFor="tags-input">Tags</label>
          <Input id="tags-input" />
        </div>
        <div className="grid grid-cols-[82px,calc(100%_-_82px)]  items-center">
          <label htmlFor="">Schedule</label>
          <Switch checked={checked} onCheckedChange={setChecked} />
        </div>
        <Expandable open={checked}>
          <div className="flex items-center justify-between">
            <div className="flex flex-col gap-2">
              <label htmlFor="date-picker">Select date</label>
              <Input type="date" innerClassName="!bg-[#F3F4F6]" />
            </div>
            <div className="flex flex-col gap-2">
              <label htmlFor="time-picker">Select time</label>
              <Input type="time" innerClassName="!bg-[#F3F4F6]" />
            </div>
          </div>
        </Expandable>

        <Button className="max-w-[126px] self-end">Save changes</Button>
      </form>
    </div>
  );
};

export default LiveVideoUrlForm;
