import "@testing-library/jest-dom/extend-expect";
import { render, screen } from "@testing-library/react";
import Home from "../pages/index";

describe("Home", () => {
  it("renders the demo videos section", () => {
    render(<Home />);
    const demoVideosSection = screen.getByText("Demo Videos");
    expect(demoVideosSection).toBeInTheDocument();
  });

  it("renders three video cards", () => {
    render(<Home />);
    const videoCards = screen.getAllByTestId("video-card");
    expect(videoCards).toHaveLength(3);
    expect(videoCards[0]).toHaveTextContent("Try this out");
  });
});
