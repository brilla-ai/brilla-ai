"use client";

import React from "react";
import { Input } from "./ui/input";
import { Switch } from "./ui/switch";
import { Expandable } from "./ui/expandable";
import { Button } from "./ui/button";

import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { useVideosStore } from "@/stores";
import useWebSocket from "react-use-websocket";
import { useVideoLinkMutation } from "@/hooks/requests/use-video-links";
import { Video } from "@/types";

const schema = z.object({
  video_link: z.string().min(1, "Link is required").url("Must be a valid URL"),
  tag: z.string().min(1, "Tags are required"),
  start_time: z.string().optional(),
  end_time: z.string().optional(),
});

type Schema = z.infer<typeof schema>;

type LiveVideoUrlFormProps = {
  isEditing?: boolean;
  video?: Video;
  closeModal?: () => void;
};

const LiveVideoUrlForm = ({
  isEditing = false,
  video,
  closeModal,
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
      video_link: video?.video_link,
      tag: video?.tag,
      start_time: video?.start_time,
      end_time: video?.end_time,
    },
  });

  const { mutate, isPending } = useVideoLinkMutation();

  // const webSocket = new WebSocket("ws://localhost:8000/links");

  // const { sendJsonMessage } = useWebSocket("ws://localhost:8000/links");

  const onSubmit = (data: Schema) => {
    // console.log("data", data);
    const dataToStore = {
      video_link: data.video_link,
      schedule: checked,
      tag: data.tag,
      start_time: data.start_time!,
      end_time: data.end_time!,
    };

    mutate(dataToStore);

    // sendJsonMessage(JSON.stringify(dataToStore));

    // Check if WebSocket is open before sending
    // if (webSocket.readyState === WebSocket.OPEN) {
    //   webSocket.send(JSON.stringify(dataToStore));
    //   console.log("WebSocket is open. Data sent:", JSON.stringify(dataToStore));
    // } else {
    //   console.error(
    //     "WebSocket is not open. Current state:",
    //     webSocket.readyState
    //   );
    // }

    reset({ video_link: "", tag: "", start_time: "", end_time: "" });
    setChecked(false);
    closeModal?.();
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
          <Input
            {...register("video_link")}
            error={errors.video_link?.message}
          />
        </div>
        <div className="grid md:grid-cols-[82px,calc(100%_-_82px)] ">
          <label htmlFor="tags-input">Tags</label>
          <Input {...register("tag")} error={errors.tag?.message} />
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
              <label htmlFor="date-picker">Start date</label>
              <Input
                type="date"
                innerClassName="!bg-[#F3F4F6]"
                min={minDateString}
                {...register("start_time")}
                error={errors.start_time?.message}
              />
            </div>
            <div className="flex flex-col gap-2">
              <label htmlFor="time-picker">End time</label>
              <Input
                type="date"
                innerClassName="!bg-[#F3F4F6]"
                {...register("end_time")}
                error={errors.end_time?.message}
              />
            </div>
          </div>
        </Expandable>
        <Button
          type="button"
          className="max-w-[126px] self-end"
          onClick={handleSubmit(onSubmit)}
          disabled={isPending}
        >
          Save changes
        </Button>
      </form>
    </div>
  );
};

export default LiveVideoUrlForm;
