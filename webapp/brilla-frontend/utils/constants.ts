export const ENV_VARS = {
  WS_BASE_URL: process.env.NEXT_PUBLIC_WS_BASE_URL,
  API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL,
};

export const STATUS_CLASSES = {
  live: "!bg-green-600 text-[#edede9]",
  ended: "!bg-red-600 text-[#edede9]",
  upcoming: "!bg-yellow-600 text-[#edede9]",
};
