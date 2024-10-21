import dayjs from "dayjs";

export const formatTime = (time: string) => {
  return new Date(`2000-01-01T${time}`).toLocaleTimeString("en-US", {
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
  });
};

export function formatDate(value: string, format = "YYYY-MM-DD") {
  const converted = dayjs(value);
  if (!value || !converted.isValid()) return "";
  return converted.format(format);
}
