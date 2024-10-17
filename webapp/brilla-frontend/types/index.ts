export type User = {
  id: string;
  email: string;
  is_active: boolean;
  role: string;
  first_name: string;
  last_name: string;
};

export type Video = {
  id?: number;
  video_link: string;
  schedule: boolean;
  tag: string;
  start_time: string;
  end_time: string;
};