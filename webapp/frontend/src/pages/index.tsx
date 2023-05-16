import Layout from "@/components/layout/Layout";

export default function Home() {
  return (
    <Layout>
      <main className="flex min-h-screen flex-col items-center justify-between p-24">
        <div className="mx-auto max-w-2xl lg:mx-0">
          <h2 className="text-4xl font-bold tracking-tight sm:text-6xl">
            NSMQ AI Challenge
          </h2>
          <p className={"mt-6 text-lg leading-8 "}>
            {
              "Can an AI win Ghana's National Science and Maths Quiz?. This is the question posed by the NSMQ AI Grand Challenge which is an AI Grand Challenge for Education using Ghana's National Science and Maths Quiz competition (NSMQ) as a case study."
            }
            {
              "The goal of nsmqai is build an AI to compete live in the NSMQ competition and win — performing better than the best contestants in all rounds and stages of the competition."
            }
          </p>
        </div>
      </main>
    </Layout>
  );
}
