import AnswerBox from "@/components/answer-box";
import Footer from "@/components/footer";
import Navbar from "@/components/navbar";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col">
      <Navbar gradientBg={false} />
      <div>Live is meant to be easy, bruh!</div>

      <Footer />
     <Navbar gradientBg = {false} />
      <div>
      <AnswerBox chatHistory={["Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vitae aliquam quam. Nulla facilisi. Integer ac dapibus libero, eu efficitur purus. Nam consectetur venenatis libero, in rutrum ex. Vestibulum nec est tortor"
      ,"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vitae aliquam quam. Nulla facilisi. Integer ac dapibus libero, eu efficitur purus. Nam consectetur venenatis libero, in rutrum ex. Vestibulum nec est tortor"
    ,"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vitae aliquam quam. Nulla facilisi. Integer ac dapibus libero, eu efficitur purus. Nam consectetur venenatis libero, in rutrum ex. Vestibulum nec est tortor"] } />
      </div>
      <Footer/>
    </main>
  );
}
