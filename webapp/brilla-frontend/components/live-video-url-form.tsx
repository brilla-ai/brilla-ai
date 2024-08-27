"use client";

import React from "react";
import { Input } from "./ui/input";
import { Switch } from "./ui/switch";
import { Expandable } from "./ui/expandable";
import { Button } from "./ui/button";

import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { useVideosStore, Video } from "@/stores";

const schema = z.object({
  link: z.string().min(1, "Link is required").url("Must be a valid URL"),
  tags: z.string().min(1, "Tags are required"),
  schedule_date: z.string().optional(),
  schedule_time: z.string().optional(),
});

type Schema = z.infer<typeof schema>;

type LiveVideoUrlFormProps = {
  isEditing?: boolean;
  video?: Video;
};

const LiveVideoUrlForm = ({
  isEditing = false,
  video,
}: LiveVideoUrlFormProps) => {
  const [checked, setChecked] = React.useState(false);
  const minDate = new Date();
  minDate.setFullYear(minDate.getFullYear());
  // Format the date as YYYY-MM-DD
  const minDateString = minDate.toISOString().split("T")[0];

  const { setVideo, setLiveVideo, editVideo } = useVideosStore();

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
    reset,
  } = useForm<Schema>({
    resolver: zodResolver(schema),
    mode: "onChange",
    defaultValues: {
      link: video?.link,
      tags: video?.tags,
      schedule_date: video?.schedule_date,
      schedule_time: video?.schedule_time,
    },
  });

  const onSubmit = (data: Schema) => {
    console.log("data", data);
    const dataToStore = {
      ...data,
      id: Math.floor(Math.random() * 1000),
      schedule_date: checked ? data.schedule_date! : "",
      schedule_time: checked ? data.schedule_time! : "",
      status: data.schedule_date ? "Scheduled" : "Live",
    };
    if (isEditing) {
      editVideo(dataToStore);
    } else {
      setVideo(dataToStore);
      if (!dataToStore.schedule_date || !dataToStore.schedule_time) {
        setLiveVideo(data.link);
      }
    }
    reset();
  };

  return (
    <div className="max-w-[377px] w-full">
      <h4 className="text-lg text-[#0F172A] font-semibold mb-2">
        {isEditing ? "Edit Live Video Url" : "Add Live Video Url"}
      </h4>
      <p className="text-[#64748B] text-sm mb-8">
        Add a youtube or stream link to this page. This will give authorized
        users access to the displayed content
      </p>
      <form className="flex flex-col gap-8">
        <div className="grid md:grid-cols-[82px,calc(100%_-_82px)] ">
          <label htmlFor="link-input">Video link</label>
          <Input {...register("link")} error={errors.link?.message} />
        </div>
        <div className="grid md:grid-cols-[82px,calc(100%_-_82px)] ">
          <label htmlFor="tags-input">Tags</label>
          <Input {...register("tags")} error={errors.tags?.message} />
        </div>
        <div className="grid md:grid-cols-[82px,calc(100%_-_82px)] ">
          <label htmlFor="">Schedule</label>
          <Switch
            checked={checked}
            onCheckedChange={setChecked}
            data-testid="switch"
          />
        </div>
        <Expandable open={checked}>
          <div className="flex flex-col md:flex-row md:items-center justify-between">
            <div className="flex flex-col gap-2">
              <label htmlFor="date-picker">Select date</label>
              <Input
                type="date"
                innerClassName="!bg-[#F3F4F6]"
                min={minDateString}
                {...register("schedule_date")}
                error={errors.schedule_date?.message}
              />
            </div>
            <div className="flex flex-col gap-2">
              <label htmlFor="time-picker">Select time</label>
              <Input
                type="time"
                innerClassName="!bg-[#F3F4F6]"
                {...register("schedule_time")}
                error={errors.schedule_time?.message}
              />
            </div>
          </div>
        </Expandable>
        <Button
          type="button"
          className="max-w-[126px] self-end"
          onClick={handleSubmit(onSubmit)}
          // disabled={!isValid}
        >
          Save changes
        </Button>
      </form>
    </div>
  );
};

export default LiveVideoUrlForm;
