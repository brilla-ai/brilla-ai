"use client";
import { DotsVerticalIcon } from "@radix-ui/react-icons";
import { ActionDropdown } from "./ui/action-dropdown-menu";
import { Modal } from "./ui/modal";
import React from "react";
import { DialogClose } from "./ui/dialog";
import { Button } from "./ui/button";
import LiveVideoUrlForm from "./live-video-url-form";

const LiveVideoLinks = () => {
  const links = [
    {
      id: 1,
      link: "https://youtube.com/brillaai/watch?v=1214",
      status: "Live",
      schedule_date: null,
      schedule_time: null,
      tags: "Quarter Finals",
    },
    {
      id: 2,
      link: "https://youtube.com/brillaai/watch?v=1234",
      status: "Scheduled",
      schedule_date: "2024-10-11",
      schedule_time: "13:15",
      tags: "Semi Finals",
    },
    {
      id: 3,
      link: "https://youtube.com/brillaai/watch?v=1256",
      status: "Scheduled",
      schedule_date: "2024-10-12",
      schedule_time: "13:15",
      tags: "Finals",
    },
  ];
  return (
    <>
      <div className="border border-[#ADB5BD] rounded py-4 px-7 max-w-[604px] w-full h-max">
        <div className="grid lg:grid-cols-2">
          <p className="text-lg text-[#0F172A] font-semibold">
            Live Video Links
          </p>
          <p className="text-lg text-[#0F172A] font-semibold">Status</p>
        </div>
        <div className="grid gap-8 mt-8">
          {links.map((video) => {
            return (
              <div key={video.id} className="grid lg:grid-cols-2">
                <p>{video.tags}</p>
                <div className="flex justify-between">
                  <p>{video.status}</p>
                  <ActionCell video={video} />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </>
  );
};

export default LiveVideoLinks;

const ActionCell = ({ video }: { video: any }) => {
  const [isOpen, setIsOpen] = React.useState(false);
  const [isStopLiveModalOpen, setIsStopLiveModalOpen] = React.useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = React.useState(false);
  const sharedAction = [
    {
      action: "Delete",
      onClickFn: () => setIsOpen(true),
    },
  ];
  const liveActions = [
    {
      action: "Stop",
      onClickFn: () => setIsStopLiveModalOpen(true),
    },
    ...sharedAction,
  ];

  const scheduledActions = [
    {
      action: "Edit",
      onClickFn: () => setIsEditModalOpen(true),
    },
    ...sharedAction,
  ];

  const actions = video.status === "Live" ? liveActions : scheduledActions;
  return (
    <>
      <ActionDropdown actions={actions}>
        <DotsVerticalIcon />
      </ActionDropdown>
      <Modal
        isOpen={isOpen}
        setIsOpen={setIsOpen}
        title="Delete Live Video Url"
        description="Are you sure you want to delete this live video url?"
      >
        <div className="bg-[#FAFAFA] p-4 flex gap-4 items-center justify-center rounded-b-lg">
          <DialogClose asChild>
            <Button className="max-w-[126px] self-end" variant={"outline"}>
              Cancel
            </Button>
          </DialogClose>
          <Button className="max-w-[126px] self-end bg-red-600">Proceed</Button>
        </div>
      </Modal>
      <Modal
        isOpen={isStopLiveModalOpen}
        setIsOpen={setIsStopLiveModalOpen}
        title="Stop Live Video"
        description="Are you sure you want to stop this live video?"
      >
        <div className="bg-[#FAFAFA] p-4 flex gap-4 items-center justify-center rounded-b-lg">
          <DialogClose asChild>
            <Button className="max-w-[126px] self-end" variant={"outline"}>
              Cancel
            </Button>
          </DialogClose>
          <Button className="max-w-[126px] self-end">Proceed</Button>
        </div>
      </Modal>
      <Modal isOpen={isEditModalOpen} setIsOpen={setIsEditModalOpen}>
        <div className="bg-white p-4 flex gap-4 items-center justify-center rounded-b-lg">
          <LiveVideoUrlForm />
        </div>
      </Modal>
    </>
  );
};
