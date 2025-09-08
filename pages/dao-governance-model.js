import Head from 'next/head'

export default function DaoGovernanceModel() {
  return (
    <div>
      <Head>
        <title>DAO Governance Model - OpenDAO University</title>
        <meta name="description" content="The DAO governance model of OpenDAO University" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main>
        <h1>
          DAO Governance Model
        </h1>

        <h2>Tokenized Voting</h2>
        <ul>
          <li>Curriculum updates</li>
          <li>Credential issuance</li>
          <li>Contributor recognition</li>
        </ul>

        <h2>Roles & Reputation</h2>
        <ul>
          <li>Learner, Mentor, Curator, Synthesizer</li>
          <li>Reputation scores based on remix, review, and contribution</li>
        </ul>

        <h2>Treasury & Sustainability</h2>
        <ul>
          <li>Micro-grants for module creation</li>
          <li>NFT royalties for remixable content</li>
          <li>Transparent treasury dashboard</li>
        </ul>
      </main>
    </div>
  )
}
