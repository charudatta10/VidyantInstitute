import Head from 'next/head'

export default function Home() {
  return (
    <div>
      <Head>
        <title>OpenDAO University</title>
        <meta name="description" content="A decentralized, AI-powered learning ecosystem" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main>
        <h1>
          Welcome to OpenDAO University
        </h1>

        <p>
          The future of education is here.
        </p>

        <a href="/academic-structure">View Academic Structure</a>
        <br />
        <a href="/adaptive-learning-engine">View Adaptive Learning Engine</a>
        <br />
        <a href="/credentialing-system">View Credentialing System</a>
        <br />
        <a href="/dao-governance-model">View DAO Governance Model</a>
        <br />
        <a href="/implementation-roadmap">View Implementation Roadmap</a>
      </main>
    </div>
  )
}
